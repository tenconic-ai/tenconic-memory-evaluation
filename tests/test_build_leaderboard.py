"""Leaderboard joins saved evidence and a published score snapshot without partial ranks."""

import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("build_leaderboard", SCRIPTS / "build_leaderboard.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

PANEL_IDS = ("locomo", "lme", "beam100k", "beam10m", "personamem", "halumem")
COUNTS = (4, 2, 1, 1, 1, 1)


class LeaderboardTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "config").mkdir()
        self.calculated = {"panels": [{"id": panel_id, "label": panel_id,
                                       "count": count, "score": .5}
                                      for panel_id, count in zip(PANEL_IDS, COUNTS)],
                           "overall": {"count": 10, "weights": [
                               {"id": panel_id, "label": panel_id, "count": count,
                                "weight": count / 10, "score": .5,
                                "weighted_contribution": count / 20}
                               for panel_id, count in zip(PANEL_IDS, COUNTS)]}}
        self.rows = [{"system": f"System {index}",
                      "scores": {panel_id: 0.0 for panel_id in PANEL_IDS}}
                     for index in range(14)]
        self.snapshot = {"schema_version": 1, "source": {
            "url": "https://example.org/snapshot", "retrieved_at_utc": "2026-10-08T00:00:00Z",
            "kind": "upstream_reproduced_snapshot", "score_scale": "0-1",
            "original_score_precision": "two decimal places on 0-100 scale",
            "answer_model": "published answer model", "judge_model": "published judge model",
            "note": "Published rounded snapshot"}, "rows": self.rows}
        (self.root / "config" / "suite.json").write_text(json.dumps({
            "schema_version": 1, "panels": [{"id": panel_id, "metric": "binary_judge"}
                                              for panel_id in PANEL_IDS]
        }), encoding="utf-8")
        self.save()

    def save(self):
        (self.root / "config" / "public-reference-scores.json").write_text(
            json.dumps(self.snapshot), encoding="utf-8")

    def build(self):
        with patch.object(builder, "recompute", return_value=self.calculated) as recompute:
            result = builder.build(self.root)
            recompute.assert_called_once_with(self.root, check=True)
            return result

    def test_question_weighted_complete_rank_and_partial_exclusion(self):
        self.rows[0]["scores"] = {panel_id: 0.0 for panel_id in PANEL_IDS}
        self.rows[0]["scores"]["locomo"] = 1.0
        self.rows[1]["scores"] = {panel_id: .5 for panel_id in PANEL_IDS}
        self.rows[2]["scores"]["halumem"] = None
        self.save()
        result = self.build()
        by_name = {row["system"]: row for row in result["overall_ranked"]}
        self.assertAlmostEqual(by_name["System 0"]["score"], .4)
        self.assertEqual(by_name["System 0"]["rank"], 3)
        self.assertEqual(by_name["Tenconic"]["rank"], 1)
        self.assertEqual(by_name["System 1"]["rank"], 1)
        self.assertNotIn("System 2", by_name)
        equal = result["benchmark_equal_weighted"]
        self.assertEqual((equal["method"], equal["benchmark_count"],
                          equal["within_benchmark_aggregation"], equal["missing_policy"]),
                         ("benchmark_equal_weighted", 5, "question_count_weighted", "all_panels_required"))
        equal_by_name = {item["system"]: item for item in equal["ranked"]}
        self.assertEqual((equal_by_name["Tenconic"]["rank"],
                          equal_by_name["System 1"]["rank"]), (1, 1))
        self.assertNotIn("System 2", [item["system"] for item in equal["ranked"]])
        self.assertEqual(equal["excluded"][0]["missing_panels"], ["halumem"])
        excluded = result["overall_excluded"][0]
        self.assertEqual(excluded["missing_panels"], ["halumem"])
        self.assertEqual(excluded["covered_questions"], 9)
        self.assertEqual(excluded["coverage_fraction"], .9)
        self.assertIsNone(next(row for row in result["comparison_matrix"]
                               if row["system"] == "System 2")["overall_score"])
        panel = next(row for row in result["panel_leaderboards"]
                     if row["id"] == "halumem")
        self.assertEqual(panel["metric"], "binary_judge")
        self.assertIn("System 2", panel["unranked_missing"])
        self.assertNotIn("System 2", [row["system"] for row in panel["ranked"]])
        document = builder.markdown(result)
        self.assertIn("6개 패널", document)
        self.assertIn("63.1407", document)

    def test_beam_two_to_one_weighting_and_weight_sums(self):
        counts = (4, 2, 400, 200, 1, 1)
        total = sum(counts)
        for panel, count in zip(self.calculated["panels"], counts):
            panel["count"] = count
        self.calculated["overall"]["count"] = total
        self.calculated["overall"]["weights"] = [
            {"id": panel_id, "label": panel_id, "count": count,
             "weight": count / total, "score": .5,
             "weighted_contribution": count / total / 2}
            for panel_id, count in zip(PANEL_IDS, counts)]
        self.rows[0]["scores"]["beam100k"] = 1.0
        self.save()
        result = self.build()
        equal = result["benchmark_equal_weighted"]
        beam = next(item for item in equal["weights"] if item["id"] == "beam")
        row = next(item for item in equal["ranked"] if item["system"] == "System 0")
        self.assertEqual((beam["question_count"], beam["panel_ids"]),
                         (600, ["beam100k", "beam10m"]))
        self.assertAlmostEqual(row["benchmark_scores"]["beam"], 2 / 3)
        self.assertAlmostEqual(row["score"], 2 / 15)
        self.assertNotAlmostEqual(row["score"], 1 / 6)
        self.assertAlmostEqual(row["question_weighted_score"], 400 / total)
        self.assertAlmostEqual(sum(w["weight"] for w in equal["weights"]), 1)
        self.assertAlmostEqual(sum(p["effective_weight"] for w in equal["weights"]
                                   for p in w["panel_weights"]), 1)
        self.assertAlmostEqual(beam["panel_weights"][0]["effective_weight"], 2 / 15)
        self.assertAlmostEqual(beam["panel_weights"][1]["effective_weight"], 1 / 15)

    def test_rank_swap_ties_and_missing_beam_panel_excludes_both(self):
        self.rows[0]["scores"]["locomo"] = 1.0
        self.rows[1]["scores"] = {panel_id: .3 for panel_id in PANEL_IDS}
        self.rows[2]["scores"]["beam10m"] = None
        self.save()
        result = self.build()
        old = {item["system"]: item for item in result["overall_ranked"]}
        equal = {item["system"]: item for item in result["benchmark_equal_weighted"]["ranked"]}
        self.assertLess(old["System 0"]["rank"], old["System 1"]["rank"])
        self.assertGreater(equal["System 0"]["rank"], equal["System 1"]["rank"])
        self.assertEqual(equal["System 1"]["rank_change"], 1)
        self.assertEqual(equal["System 0"]["rank_change"], -1)
        self.assertEqual(equal["Tenconic"]["rank"], 1)
        self.assertNotIn("System 2", old)
        self.assertNotIn("System 2", equal)
        self.assertEqual(result["benchmark_equal_weighted"]["excluded"][0]["missing_panels"],
                         ["beam10m"])
        self.assertIn("400 × BEAM 100K + 200 × BEAM 10M", builder.markdown(result))

    def test_duplicate_bad_shape_and_invalid_scores_fail(self):
        self.rows[1]["system"] = "system 0"
        self.save()
        with self.assertRaisesRegex(builder.EvidenceError, "duplicate"):
            self.build()
        self.rows[1]["system"] = "Tenconic"
        self.save()
        with self.assertRaisesRegex(builder.EvidenceError, "collision"):
            self.build()
        self.rows[1]["system"] = "System 1"
        del self.rows[1]["scores"]["lme"]
        self.save()
        with self.assertRaisesRegex(builder.EvidenceError, "exactly"):
            self.build()
        self.rows[1]["scores"]["lme"] = float("nan")
        self.save()
        with self.assertRaisesRegex(builder.EvidenceError, "finite"):
            self.build()
        self.rows[1]["scores"]["lme"] = True
        self.save()
        with self.assertRaisesRegex(builder.EvidenceError, "finite"):
            self.build()
        self.rows[1]["scores"]["lme"] = 1.1
        self.save()
        with self.assertRaisesRegex(builder.EvidenceError, "finite"):
            self.build()


if __name__ == "__main__":
    unittest.main()
