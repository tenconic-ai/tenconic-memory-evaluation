"""Category snapshot contract and bilingual leaderboard rendering."""

import copy
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import benchmark_details  # noqa: E402
import build_leaderboard  # noqa: E402
from recompute_scores import EvidenceError, recompute  # noqa: E402


class DetailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calculated = recompute(ROOT, check=True)
        cls.reference = json.loads((ROOT / "config" / "public-reference-scores.json").read_text(
            encoding="utf-8"))
        cls.original = json.loads((ROOT / "config" / "public-reference-details.json").read_text(
            encoding="utf-8"))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        (self.root / "config" / "suite.json").write_text(
            json.dumps({"package_revision": 7}), encoding="utf-8")
        self.document = copy.deepcopy(self.original)
        self.save()

    def save(self):
        (self.root / "config" / "public-reference-details.json").write_text(
            json.dumps(self.document, ensure_ascii=False), encoding="utf-8")

    def details(self):
        self.save()
        return benchmark_details.build_details(self.root, self.calculated, self.reference)

    def test_category_counts_scores_and_locomo_mapping(self):
        details = self.details()
        expected_ids = [panel["id"] for panel in self.calculated["panels"]]
        self.assertEqual([panel["id"] for panel in details["panels"]], expected_ids)
        for detail, calculated in zip(details["panels"], self.calculated["panels"]):
            tenconic = next(row for row in detail["rows"] if row["system"] == "Tenconic")
            self.assertEqual(sum(category["count"] for category in detail["categories"]),
                             calculated["count"])
            weighted = math.fsum(category["count"] * tenconic["categories"][category["id"]]
                                 for category in detail["categories"]) / calculated["count"]
            self.assertAlmostEqual(weighted, calculated["score"])
            self.assertEqual(set(tenconic["categories"]), set(calculated["categories"]))
        locomo = details["panels"][0]
        self.assertEqual({category["id"]: category["label"]["en"]
                          for category in locomo["categories"]},
                         {"4": "Single-Hop", "1": "Multi-Hop", "2": "Temporal", "3": "Open-Domain"})

    def test_peer_overall_coverage_and_beam_dimensions(self):
        details = self.details()
        for detail in details["panels"]:
            expected = {row["system"] for row in self.reference["rows"]
                        if row["scores"][detail["id"]] is not None}
            actual = {row["system"] for row in detail["rows"] if row["system"] != "Tenconic"}
            self.assertEqual(actual, expected)
            for row in detail["rows"]:
                if detail["id"].startswith("beam"):
                    if row["system"] != "Tenconic":
                        self.assertIsNone(row["categories"])
                    self.assertIsNotNone(row["score_std"])
        self.document["panels"][0]["rows"][0]["score"] += .01
        with self.assertRaisesRegex(EvidenceError, "differs from reference overall"):
            self.details()
        self.document = copy.deepcopy(self.original)
        self.document["panels"][0]["rows"].pop()
        with self.assertRaisesRegex(EvidenceError, "missing or extra scored systems"):
            self.details()
        self.document = copy.deepcopy(self.original)
        self.document["panels"][2]["rows"][0]["categories"] = {"abstention": .8}
        with self.assertRaisesRegex(EvidenceError, "BEAM peer details unavailable"):
            self.details()

    def test_detail_file_required_for_revision_seven(self):
        (self.root / "config" / "public-reference-details.json").unlink()
        with self.assertRaisesRegex(EvidenceError, "required for package revision"):
            benchmark_details.build_details(self.root, self.calculated, self.reference)

    def test_bilingual_values_and_anchors(self):
        result = build_leaderboard.build(ROOT)
        english = build_leaderboard.markdown(result, "en")
        korean = build_leaderboard.markdown(result, "ko")
        self.assertIn('<a id="benchmark-details"></a>', english)
        self.assertIn('<a id="detail-locomo"></a>', korean)
        for panel in result["benchmark_details"]["panels"]:
            self.assertIn(f'<a id="detail-{panel["id"]}"></a>', english)
            tenconic = next(row for row in panel["rows"] if row["system"] == "Tenconic")
            token = f"{tenconic['score'] * 100:.2f}"
            self.assertIn(token, english)
            self.assertIn(token, korean)
        self.assertIn("**Tenconic**", english)
        self.assertIn("**Tenconic**", korean)
        self.assertIn("Peer BEAM ability scores were not published", english)
        self.assertIn("BEAM 능력별 점수는 공개 재현 결과에 없습니다", korean)


if __name__ == "__main__":
    unittest.main()
