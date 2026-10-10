"""Behavioral checks for the standalone saved-evidence calculator."""

import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "recompute_scores.py"
SPEC = importlib.util.spec_from_file_location("recompute_scores", SCRIPT)
calculator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(calculator)


def row(record_id, evaluation, category="category"):
    return {"record_id": record_id, "benchmark": "sample", "category": category,
            "status": "success", "source_ref": {"question_id": record_id},
            "question": "What happened?", "reference_answer": "gold",
            "answer": "saved response", "evaluation": evaluation}


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "config").mkdir()
        (self.root / "data").mkdir()

    def write(self, rows, expected_score=None, expected_questions=None,
              data_file="data/sample.jsonl", panel_id="sample"):
        if expected_questions is None:
            expected_questions = len(rows)
        manifest = {"schema_version": 1, "panels": [{"id": panel_id, "label": "Sample",
            "expected_questions": expected_questions, "data_file": data_file,
            "expected_score": expected_score}]}
        (self.root / "config" / "suite.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.root / "data" / "sample.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")

    def write_multi(self, panels, aggregation):
        manifest_panels = []
        for panel_id, family, scores in panels:
            manifest_panels.append({"id": panel_id, "label": panel_id,
                "benchmark_family": family, "expected_questions": len(scores),
                "expected_score": sum(scores) / len(scores),
                "data_file": f"data/{panel_id}.jsonl"})
            rows = []
            for index, score in enumerate(scores):
                evidence = row(str(index), {"type": "binary_judge",
                    "judgments": [bool(score)], "saved_score": score})
                evidence["benchmark"] = panel_id
                rows.append(evidence)
            (self.root / "data" / f"{panel_id}.jsonl").write_text(
                "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        (self.root / "config" / "suite.json").write_text(json.dumps({
            "schema_version": 1, "panels": manifest_panels, "aggregation": aggregation
        }), encoding="utf-8")

    def test_binary_count_category_means_and_manifest_check(self):
        rows = [row("one", {"type": "binary_judge", "judgments": [True, False], "saved_score": .5}, "A"),
                row("two", {"type": "multiple_choice_saved", "judgments": [True], "saved_score": 1}, "B")]
        self.write(rows, expected_score=.75)
        panel = calculator.recompute(self.root, check=True)["panels"][0]
        self.assertEqual((panel["count"], panel["score"]), (2, .75))
        self.assertEqual((panel["binary_numerator"], panel["binary_denominator"]), (2, 3))
        self.assertEqual(panel["categories"]["A"], {"count": 1, "score": .5})

    def test_denominator_duplicate_missing_and_nonbool_fail(self):
        good = row("one", {"type": "binary_judge", "judgments": [True], "saved_score": 1})
        self.write([good], expected_questions=2)
        with self.assertRaisesRegex(calculator.EvidenceError, "expected 2 questions"):
            calculator.recompute(self.root)
        self.write([good, good], expected_questions=2)
        with self.assertRaisesRegex(calculator.EvidenceError, "duplicate"):
            calculator.recompute(self.root)
        bad = row("two", {"type": "binary_judge", "judgments": [1], "saved_score": 1})
        self.write([bad])
        with self.assertRaisesRegex(calculator.EvidenceError, "boolean"):
            calculator.recompute(self.root)
        bad["evaluation"]["judgments"] = []
        self.write([bad])
        with self.assertRaisesRegex(calculator.EvidenceError, "nonempty"):
            calculator.recompute(self.root)

    def test_rubric_uses_equal_item_weights_despite_different_run_counts(self):
        evaluation = {"type": "rubric_mean", "items": [
            {"item_index": 0, "scores": [1], "saved_score": 1},
            {"item_index": 1, "scores": [0, .5, 1], "saved_score": .5}],
            "saved_score": .75}
        public_row = row("one", evaluation)
        del public_row["question"]
        del public_row["reference_answer"]
        self.write([public_row], expected_score=.75)
        self.assertEqual(calculator.recompute(self.root, check=True)["panels"][0]["score"], .75)
        evaluation["items"][0]["saved_score"] = .5
        self.write([public_row])
        with self.assertRaisesRegex(calculator.EvidenceError, "saved_score"):
            calculator.recompute(self.root)

    def test_ordering_reversed_ties_missing_and_zero(self):
        # Gold order is [0,1,2]; all-ties tau-b is 0, so its normalized score is .5.
        positions = [[1, 2, 3], [3, 2, 1], [1, 1, 1], [1, -1, -1], [-1, -1, -1]]
        scores = [1, 0, .5, 1 / 6, 0]
        evaluation = {"type": "ordering_tau_b", "rubric": ["event_1", "event_2", "event_3"],
                      "positions": positions, "scores": scores,
                      "saved_score": sum(scores) / len(scores)}
        self.write([row("one", evaluation)], expected_score=evaluation["saved_score"])
        actual = calculator.recompute(self.root, check=True)["panels"][0]
        self.assertTrue(math.isclose(actual["score"], evaluation["saved_score"], abs_tol=1e-10))
        evaluation["scores"][2] = 1
        self.write([row("one", evaluation)])
        with self.assertRaisesRegex(calculator.EvidenceError, "scores\\[2\\]"):
            calculator.recompute(self.root)

    def test_tampered_row_and_manifest_score(self):
        evidence = row("one", {"type": "binary_judge", "judgments": [True], "saved_score": 0})
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "saved"):
            calculator.recompute(self.root)
        evidence["evaluation"]["saved_score"] = 1
        self.write([evidence], expected_score=0)
        self.assertEqual(calculator.recompute(self.root)["panels"][0]["score"], 1)
        with self.assertRaisesRegex(calculator.EvidenceError, "expected_score"):
            calculator.recompute(self.root, check=True)

    def test_manifest_path_escape_and_invalid_evidence(self):
        evidence = row("one", {"type": "binary_judge", "judgments": [True], "saved_score": 1})
        self.write([evidence], data_file="../outside.jsonl")
        with self.assertRaisesRegex(calculator.EvidenceError, "escapes package"):
            calculator.recompute(self.root)
        self.write([evidence])
        evidence["benchmark"] = "other"
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "benchmark"):
            calculator.recompute(self.root)
        evidence["benchmark"] = "sample"
        evidence["evaluation"]["saved_score"] = float("nan")
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "finite"):
            calculator.recompute(self.root)

    def test_optional_text_and_reasons_still_validate_when_present(self):
        evidence = row("one", {"type": "rubric_mean", "items": [
            {"item_index": 0, "scores": [1], "saved_score": 1}], "saved_score": 1})
        evidence.pop("question")
        evidence.pop("reference_answer")
        self.write([evidence], expected_score=1)
        self.assertEqual(calculator.recompute(self.root, check=True)["panels"][0]["score"], 1)
        evidence["question"] = ""
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "question"):
            calculator.recompute(self.root)
        evidence.pop("question")
        evidence["reference_answer"] = 7
        self.write([evidence])
        self.assertEqual(calculator.recompute(self.root)["panels"][0]["score"], 1)
        evidence["reference_answer"] = True
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "reference_answer"):
            calculator.recompute(self.root)
        evidence.pop("reference_answer")
        evidence["evaluation"]["items"][0]["reasons"] = []
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "reasons"):
            calculator.recompute(self.root)
        evidence["evaluation"]["items"][0].pop("reasons")
        evidence["evaluation"]["items"].append({"item_index": 0, "scores": [1], "saved_score": 1})
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "duplicate"):
            calculator.recompute(self.root)

    def test_missing_source_ref_and_empty_answer_fail(self):
        evidence = row("one", {"type": "binary_judge", "judgments": [True], "saved_score": 1})
        evidence.pop("source_ref")
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "source_ref"):
            calculator.recompute(self.root)
        evidence["source_ref"] = {"question_id": "one"}
        evidence["answer"] = ""
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "answer"):
            calculator.recompute(self.root)

    def test_licensed_withheld_answer_keeps_saved_score(self):
        for panel_id, license_name in (("locomo", "CC-BY-NC-4.0"),
                                       ("halumem", "CC-BY-NC-ND-4.0")):
            with self.subTest(panel=panel_id):
                evidence = row("one", {"type": "binary_judge",
                                       "judgments": [True, False], "saved_score": .5})
                evidence["benchmark"] = panel_id
                self.write([evidence], expected_score=.5, panel_id=panel_id)
                original = calculator.recompute(self.root, check=True)
                evidence.pop("answer")
                evidence["answer_disclosure"] = {
                    "status": "withheld", "reason": "dataset_license_scope",
                    "source_license": license_name,
                    "preserved_original_outside_package": True}
                self.write([evidence], expected_score=.5, panel_id=panel_id)
                withheld = calculator.recompute(self.root, check=True)
                self.assertEqual(withheld["overall"], original["overall"])
                self.assertEqual(withheld["panels"], original["panels"])

    def test_withheld_answer_requires_exact_panel_and_metadata(self):
        evidence = row("one", {"type": "binary_judge",
                               "judgments": [True], "saved_score": 1})
        evidence.pop("answer")
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "not allowed"):
            calculator.recompute(self.root)
        disclosure = {"status": "withheld", "reason": "dataset_license_scope",
                      "source_license": "CC-BY-NC-4.0",
                      "preserved_original_outside_package": True}
        evidence["answer_disclosure"] = disclosure
        self.write([evidence])
        with self.assertRaisesRegex(calculator.EvidenceError, "not allowed"):
            calculator.recompute(self.root)
        evidence.pop("answer_disclosure")
        evidence["benchmark"] = "locomo"
        self.write([evidence], panel_id="locomo")
        with self.assertRaisesRegex(calculator.EvidenceError, "answer_disclosure"):
            calculator.recompute(self.root)
        evidence["answer_disclosure"] = disclosure
        self.write([evidence], panel_id="locomo")
        self.assertEqual(calculator.recompute(self.root)["panels"][0]["score"], 1)
        for field, bad_value in (("status", "removed"), ("reason", "other"),
                                 ("source_license", "CC-BY-NC-ND-4.0"),
                                 ("preserved_original_outside_package", 1)):
            with self.subTest(field=field):
                bad = disclosure.copy()
                bad[field] = bad_value
                evidence["answer_disclosure"] = bad
                self.write([evidence], panel_id="locomo")
                with self.assertRaisesRegex(calculator.EvidenceError, "invalid withheld"):
                    calculator.recompute(self.root)
        evidence["answer_disclosure"] = {**disclosure, "extra": "not allowed"}
        self.write([evidence], panel_id="locomo")
        with self.assertRaisesRegex(calculator.EvidenceError, "exact withheld"):
            calculator.recompute(self.root)
        evidence["answer_disclosure"] = disclosure
        evidence["answer"] = "retained body"
        self.write([evidence], panel_id="locomo")
        with self.assertRaisesRegex(calculator.EvidenceError, "conflicts"):
            calculator.recompute(self.root)

    def test_composite_uses_question_counts_and_groups_beam_once(self):
        panels = [("locomo", "LoCoMo", [1, 1, 1, 1]),
                  ("beam100k", "BEAM", [0, 0]),
                  ("beam10m", "BEAM", [1])]
        self.write_multi(panels, {"method": "question_count_weighted",
                                  "expected_questions": 7, "expected_score": 5 / 7})
        result = calculator.recompute(self.root, check=True)
        self.assertEqual(result["overall"]["count"], 7)
        self.assertAlmostEqual(result["overall"]["score"], 5 / 7)
        self.assertNotAlmostEqual(result["overall"]["score"], (1 + 0 + 1) / 3)
        self.assertAlmostEqual(sum(w["weighted_contribution"]
                                   for w in result["overall"]["weights"]), 5 / 7)
        beam = next(f for f in result["benchmark_families"] if f["family"] == "BEAM")
        self.assertEqual(beam["panel_ids"], ["beam100k", "beam10m"])
        self.assertEqual(beam["count"], 3)
        self.assertAlmostEqual(beam["score"], 1 / 3)

    def test_aggregate_expectations_and_incomplete_panel_fail(self):
        panels = [("a", "A", [1]), ("b", "B", [0, 0])]
        aggregation = {"method": "question_count_weighted",
                       "expected_questions": 3, "expected_score": 1 / 3}
        self.write_multi(panels, aggregation)
        manifest_path = self.root / "config" / "suite.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["aggregation"]["expected_questions"] = 2
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(calculator.EvidenceError, "aggregation.expected_questions"):
            calculator.recompute(self.root, check=True)
        manifest["aggregation"]["expected_questions"] = 3
        manifest["aggregation"]["expected_score"] = .5
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(calculator.EvidenceError, "aggregation.expected_score"):
            calculator.recompute(self.root, check=True)
        manifest["aggregation"]["expected_score"] = 1 / 3
        manifest["aggregation"]["method"] = "panel_macro_average"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(calculator.EvidenceError, "aggregation.method"):
            calculator.recompute(self.root, check=True)
        manifest["aggregation"]["method"] = "question_count_weighted"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        (self.root / "data" / "b.jsonl").write_text("", encoding="utf-8")
        with self.assertRaisesRegex(calculator.EvidenceError, "expected 2 questions"):
            calculator.recompute(self.root)


if __name__ == "__main__":
    unittest.main()
