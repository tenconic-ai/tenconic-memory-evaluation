#!/usr/bin/env python3
"""Recompute scores from the saved, public evaluation evidence. No model calls."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

TOLERANCE = 1e-10
WITHHELD_ANSWER_LICENSES = {
    "locomo": "CC-BY-NC-4.0",
    "halumem": "CC-BY-NC-ND-4.0",
}


class EvidenceError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def object_at(value: object, where: str) -> dict:
    require(isinstance(value, dict), f"{where}: expected object")
    return value


def nonempty_text(value: object, where: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected nonempty text")
    return value


def array_at(value: object, where: str, *, nonempty: bool = True) -> list:
    require(isinstance(value, list) and (not nonempty or bool(value)), f"{where}: expected {'nonempty ' if nonempty else ''}array")
    return value


def number(value: object, where: str, *, unit: bool = True) -> float:
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{where}: expected number")
    result = float(value)
    require(math.isfinite(result), f"{where}: expected finite number")
    if unit:
        require(0 <= result <= 1, f"{where}: score outside [0, 1]")
    return result


def equal_score(actual: float, saved: object, where: str) -> None:
    expected = number(saved, where)
    require(math.isclose(actual, expected, rel_tol=0, abs_tol=TOLERANCE),
            f"{where}: saved {expected:.12g} differs from recomputed {actual:.12g}")


def score_binary(evaluation: dict, where: str) -> tuple[float, dict]:
    judgments = array_at(evaluation.get("judgments"), f"{where}.judgments")
    require(all(type(j) is bool for j in judgments), f"{where}.judgments: each judgment must be boolean")
    numerator = sum(judgments)
    value = numerator / len(judgments)
    equal_score(value, evaluation.get("saved_score"), f"{where}.saved_score")
    return value, {"numerator": numerator, "denominator": len(judgments)}


def score_rubric(evaluation: dict, where: str) -> tuple[float, dict]:
    items = array_at(evaluation.get("items"), f"{where}.items")
    item_scores = []
    seen_indices = set()
    for i, raw_item in enumerate(items):
        location = f"{where}.items[{i}]"
        item = object_at(raw_item, location)
        if "rubric" in item:
            nonempty_text(item["rubric"], f"{location}.rubric")
        if "item_index" in item or "rubric" not in item:
            item_index = item.get("item_index")
            require(type(item_index) is int and item_index >= 0,
                    f"{location}.item_index: expected nonnegative integer when rubric is omitted")
            require(item_index not in seen_indices, f"{location}.item_index: duplicate {item_index}")
            seen_indices.add(item_index)
        raw_scores = array_at(item.get("scores"), f"{location}.scores")
        scores = [number(s, f"{location}.scores[{j}]") for j, s in enumerate(raw_scores)]
        require(all(s in (0, 0.5, 1) for s in scores), f"{location}.scores: expected 0, 0.5 or 1")
        if "reasons" in item:
            reasons = array_at(item["reasons"], f"{location}.reasons")
            require(len(reasons) == len(scores) and all(isinstance(r, str) for r in reasons),
                    f"{location}.reasons: expected one reason per score")
        value = statistics.fmean(scores)
        equal_score(value, item.get("saved_score"), f"{location}.saved_score")
        item_scores.append(value)
    value = statistics.fmean(item_scores)
    equal_score(value, evaluation.get("saved_score"), f"{where}.saved_score")
    return value, {}


def ordering_score(positions: list[int]) -> float:
    """BEAM ordering score; gold order is the rubric index, ties use tau-b."""
    found = [(i, p) for i, p in enumerate(positions) if p > 0]
    coverage = len(found) / len(positions)
    if len(found) < 2:
        return 0.0 if not found else 0.5 * coverage
    concordant = discordant = ties_pred = 0
    for i in range(len(found)):
        for j in range(i + 1, len(found)):
            difference = found[i][1] - found[j][1]
            if difference == 0:
                ties_pred += 1
            elif difference < 0:
                concordant += 1
            else:
                discordant += 1
    pairs = len(found) * (len(found) - 1) // 2
    denominator = math.sqrt(pairs * (pairs - ties_pred))
    tau = 0.0 if denominator == 0 else (concordant - discordant) / denominator
    return max(0.0, (tau + 1) / 2) * coverage


def score_ordering(evaluation: dict, where: str) -> tuple[float, dict]:
    rubric = array_at(evaluation.get("rubric"), f"{where}.rubric")
    require(all(isinstance(r, str) and r.strip() for r in rubric), f"{where}.rubric: expected text items")
    positions = array_at(evaluation.get("positions"), f"{where}.positions")
    raw_scores = array_at(evaluation.get("scores"), f"{where}.scores")
    require(len(positions) == len(raw_scores), f"{where}: positions and scores must have equal lengths")
    if "reasons" in evaluation:
        reasons = array_at(evaluation["reasons"], f"{where}.reasons")
        require(len(reasons) == len(positions), f"{where}.reasons: expected one reason per run")
        require(all(isinstance(r, str) for r in reasons), f"{where}.reasons: expected text")
    run_scores = []
    for i, raw in enumerate(positions):
        run = array_at(raw, f"{where}.positions[{i}]")
        require(len(run) == len(rubric), f"{where}.positions[{i}]: length differs from rubric")
        require(all(type(p) is int for p in run), f"{where}.positions[{i}]: expected integer positions")
        value = ordering_score(run)
        equal_score(value, raw_scores[i], f"{where}.scores[{i}]")
        run_scores.append(value)
    value = statistics.fmean(run_scores)
    equal_score(value, evaluation.get("saved_score"), f"{where}.saved_score")
    return value, {}


def score_row(row: dict, where: str) -> tuple[float, dict]:
    evaluation = object_at(row.get("evaluation"), f"{where}.evaluation")
    kind = evaluation.get("type")
    if kind in ("binary_judge", "multiple_choice_saved"):
        return score_binary(evaluation, f"{where}.evaluation")
    if kind == "rubric_mean":
        return score_rubric(evaluation, f"{where}.evaluation")
    if kind == "ordering_tau_b":
        return score_ordering(evaluation, f"{where}.evaluation")
    raise EvidenceError(f"{where}.evaluation.type: unsupported type {kind!r}")


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"{path}: cannot read JSON: {exc}") from exc


def panel_path(root: Path, relative: object) -> Path:
    name = nonempty_text(relative, "data_file")
    path = Path(name)
    require(not path.is_absolute() and not path.drive, f"data_file: absolute path forbidden: {name}")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()), f"data_file: path escapes package: {name}")
    require(resolved.suffix == ".jsonl", f"data_file: expected .jsonl: {name}")
    return resolved


def recompute(root: Path, *, check: bool = False) -> dict:
    manifest = object_at(load_json(root / "config" / "suite.json"), "manifest")
    require(manifest.get("schema_version") == 1 and type(manifest.get("schema_version")) is int,
            "manifest.schema_version: expected 1")
    panels = array_at(manifest.get("panels"), "manifest.panels")
    results = []
    panel_ids = set()
    for index, raw_panel in enumerate(panels):
        where = f"manifest.panels[{index}]"
        panel = object_at(raw_panel, where)
        panel_id = nonempty_text(panel.get("id"), f"{where}.id")
        require(panel_id not in panel_ids, f"{where}.id: duplicate panel {panel_id}")
        panel_ids.add(panel_id)
        label = nonempty_text(panel.get("label"), f"{where}.label")
        expected = panel.get("expected_questions")
        require(type(expected) is int and expected > 0, f"{where}.expected_questions: expected positive integer")
        path = panel_path(root, panel.get("data_file"))
        scores = []
        categories: dict[str, list[float]] = defaultdict(list)
        seen_ids = set()
        binary_numerator = binary_denominator = 0
        has_ordering = False
        try:
            with path.open("r", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    location = f"{path}:{line_number}"
                    require(bool(line.strip()), f"{location}: blank line")
                    try:
                        row = object_at(json.loads(line), location)
                    except (json.JSONDecodeError, UnicodeError) as exc:
                        raise EvidenceError(f"{location}: invalid JSON: {exc}") from exc
                    record_id = nonempty_text(row.get("record_id"), f"{location}.record_id")
                    require(record_id not in seen_ids, f"{location}.record_id: duplicate {record_id}")
                    seen_ids.add(record_id)
                    require(row.get("benchmark") == panel_id, f"{location}.benchmark: expected {panel_id}")
                    require(row.get("status") == "success", f"{location}.status: expected success")
                    category = nonempty_text(row.get("category"), f"{location}.category")
                    require(bool(object_at(row.get("source_ref"), f"{location}.source_ref")),
                            f"{location}.source_ref: expected nonempty object")
                    if "question" in row:
                        nonempty_text(row["question"], f"{location}.question")
                    if "reference_answer" in row:
                        reference = row["reference_answer"]
                        require(isinstance(reference, str) or type(reference) is int,
                                f"{location}.reference_answer: expected text or integer")
                    if "answer" in row:
                        require("answer_disclosure" not in row,
                                f"{location}.answer_disclosure: conflicts with present answer")
                        nonempty_text(row["answer"], f"{location}.answer")
                    else:
                        require(panel_id in WITHHELD_ANSWER_LICENSES,
                                f"{location}.answer: missing answer is not allowed for {panel_id}")
                        disclosure = object_at(row.get("answer_disclosure"),
                                               f"{location}.answer_disclosure")
                        require(set(disclosure) == {"status", "reason", "source_license",
                                                   "preserved_original_outside_package"},
                                f"{location}.answer_disclosure: expected exact withheld metadata fields")
                        require(disclosure["status"] == "withheld" and
                                disclosure["reason"] == "dataset_license_scope" and
                                disclosure["source_license"] == WITHHELD_ANSWER_LICENSES[panel_id] and
                                disclosure["preserved_original_outside_package"] is True,
                                f"{location}.answer_disclosure: invalid withheld metadata or license")
                    value, extra = score_row(row, location)
                    scores.append(value)
                    categories[category].append(value)
                    binary_numerator += extra.get("numerator", 0)
                    binary_denominator += extra.get("denominator", 0)
                    has_ordering |= row["evaluation"]["type"] == "ordering_tau_b"
        except (OSError, UnicodeError) as exc:
            raise EvidenceError(f"{path}: cannot read data: {exc}") from exc
        require(len(scores) == expected, f"{path}: expected {expected} questions, found {len(scores)}")
        overall = statistics.fmean(scores)
        if check:
            equal_score(overall, panel.get("expected_score"), f"{where}.expected_score")
        result = {"id": panel_id, "label": label, "count": len(scores), "score": overall,
                  "categories": {k: {"count": len(v), "score": statistics.fmean(v)}
                                 for k, v in sorted(categories.items())}}
        if binary_denominator:
            result["binary_numerator"] = binary_numerator
            result["binary_denominator"] = binary_denominator
        if has_ordering:
            result["score_std_population"] = statistics.pstdev(scores)
        results.append(result)
    total = sum(panel["count"] for panel in results)
    weighted_sum = sum(panel["count"] * panel["score"] for panel in results)
    composite = weighted_sum / total
    weights = [{"id": panel["id"], "label": panel["label"],
                "count": panel["count"], "weight": panel["count"] / total,
                "score": panel["score"],
                "weighted_contribution": panel["count"] * panel["score"] / total}
               for panel in results]
    aggregation = manifest.get("aggregation")
    if check and aggregation is not None:
        aggregation = object_at(aggregation, "manifest.aggregation")
        require(aggregation.get("method") == "question_count_weighted",
                "manifest.aggregation.method: expected question_count_weighted")
        intended = aggregation.get("expected_questions")
        require(type(intended) is int and intended == total,
                f"manifest.aggregation.expected_questions: expected {total}")
        equal_score(composite, aggregation.get("expected_score"),
                    "manifest.aggregation.expected_score")

    families: dict[str, list[dict]] = defaultdict(list)
    for index, (raw_panel, result) in enumerate(zip(panels, results)):
        family = raw_panel.get("benchmark_family")
        if family is not None:
            families[nonempty_text(family, f"manifest.panels[{index}].benchmark_family")].append(result)
    family_results = []
    for family, members in families.items():
        count = sum(member["count"] for member in members)
        family_results.append({"family": family, "count": count,
                               "score": sum(member["count"] * member["score"]
                                            for member in members) / count,
                               "panel_ids": [member["id"] for member in members]})
    return {"schema_version": 1, "panels": results,
            "overall": {"metric": "question_count_weighted_composite", "count": total,
                        "score": composite, "weights": weights},
            "benchmark_families": family_results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="public package root (default: parent of scripts)")
    parser.add_argument("--check", action="store_true", help="also compare panel and aggregate scores with manifest expectations")
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    args = parser.parse_args(argv)
    try:
        result = recompute(args.root.resolve(), check=args.check)
    except EvidenceError as exc:
        print(f"invalid package: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        overall = result["overall"]
        print(f"Question-count weighted composite: {overall['score']:.6f} "
              f"(n={overall['count']} full included questions)")
        print("Weights: " + ", ".join(
            f"{entry['label']}={entry['weight']:.6f} (n={entry['count']})"
            for entry in overall["weights"]))
        print("Panel  Count  Score  Categories")
        for panel in result["panels"]:
            cats = ", ".join(f"{name}={value['score']:.6f} (n={value['count']})"
                             for name, value in panel["categories"].items())
            print(f"{panel['label']}  {panel['count']}  {panel['score']:.6f}  {cats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
