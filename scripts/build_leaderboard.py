#!/usr/bin/env python3
"""Build read-only public comparisons from saved evidence and a cited score snapshot."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from recompute_scores import EvidenceError, load_json, nonempty_text, object_at, recompute, require

BENCHMARKS = (
    ("locomo", "LoCoMo", ("locomo",)),
    ("lme", "LongMemEval", ("lme",)),
    ("beam", "BEAM", ("beam100k", "beam10m")),
    ("personamem", "PersonaMem", ("personamem",)),
    ("halumem", "HaluMem", ("halumem",)),
)


def ranked(rows: list[dict], key: str = "score") -> list[dict]:
    """Competition ranks: equal reported values share a rank and leave a gap."""
    ordered = sorted(rows, key=lambda row: (-row[key], row["system"].casefold()))
    for index, row in enumerate(ordered):
        row["rank"] = (ordered[index - 1]["rank"] if index and
                       row[key] == ordered[index - 1][key] else index + 1)
    return ordered


def build(root: Path) -> dict:
    calculated = recompute(root, check=True)
    panels = calculated["panels"]
    counts = {panel["id"]: panel["count"] for panel in panels}
    panel_ids = list(counts)
    total = calculated["overall"]["count"]
    expected_ids = {panel_id for _, _, group in BENCHMARKS for panel_id in group}
    require(set(panel_ids) == expected_ids and len(panel_ids) == len(expected_ids),
            "validated panels: expected the six fixed benchmark panels")
    benchmark_weights = []
    for benchmark_id, label, member_ids in BENCHMARKS:
        group_count = sum(counts[panel_id] for panel_id in member_ids)
        benchmark_weights.append({
            "id": benchmark_id, "label": label, "panel_ids": list(member_ids),
            "question_count": group_count, "weight": 1 / len(BENCHMARKS),
            "question_count_weight": group_count / total,
            "panel_weights": [{"id": panel_id, "count": counts[panel_id],
                               "weight_within_benchmark": counts[panel_id] / group_count,
                               "effective_weight": counts[panel_id] / group_count / len(BENCHMARKS)}
                              for panel_id in member_ids]})
    manifest = object_at(load_json(root / "config" / "suite.json"), "manifest")
    manifest_panels = manifest.get("panels")
    require(isinstance(manifest_panels, list) and len(manifest_panels) == len(panels),
            "manifest.panels: differs from validated panels")
    metrics = {}
    for index, panel in enumerate(manifest_panels):
        panel = object_at(panel, f"manifest.panels[{index}]")
        panel_id = panel_ids[index]
        require(panel.get("id") == panel_id, f"manifest.panels[{index}].id: differs from validated panel")
        metrics[panel_id] = nonempty_text(panel.get("metric"), f"manifest.panels[{index}].metric")
    snapshot = object_at(load_json(root / "config" / "public-reference-scores.json"), "reference")
    require(type(snapshot.get("schema_version")) is int and snapshot["schema_version"] == 1,
            "reference.schema_version: expected 1")
    source = object_at(snapshot.get("source"), "reference.source")
    for field in ("url", "retrieved_at_utc", "original_score_precision",
                  "answer_model", "judge_model", "note"):
        nonempty_text(source.get(field), f"reference.source.{field}")
    require(source.get("kind") == "upstream_reproduced_snapshot",
            "reference.source.kind: expected upstream_reproduced_snapshot")
    require(source.get("score_scale") == "0-1", "reference.source.score_scale: expected 0-1")
    external = snapshot.get("rows")
    require(isinstance(external, list) and len(external) == 14,
            "reference.rows: expected 14 published system rows")
    systems = [{"system": "Tenconic", "origin": "saved_question_records",
                "scores": {panel["id"]: panel["score"] for panel in panels}}]
    seen = {"tenconic"}
    for index, raw in enumerate(external):
        where = f"reference.rows[{index}]"
        item = object_at(raw, where)
        name = nonempty_text(item.get("system"), f"{where}.system")
        require(name.casefold() not in seen, f"{where}.system: duplicate or Tenconic collision {name}")
        seen.add(name.casefold())
        raw_scores = object_at(item.get("scores"), f"{where}.scores")
        require(set(raw_scores) == set(panel_ids),
                f"{where}.scores: expected exactly {', '.join(panel_ids)}")
        scores = {}
        for panel_id in panel_ids:
            value = raw_scores[panel_id]
            require(value is None or (isinstance(value, (int, float)) and
                    not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 1),
                    f"{where}.scores.{panel_id}: expected finite 0-1 score or null")
            scores[panel_id] = None if value is None else float(value)
        systems.append({"system": name, "origin": "published_rounded_scores", "scores": scores})

    overall_complete = []
    overall_excluded = []
    matrix = []
    for system in systems:
        scores = system["scores"]
        missing = [panel_id for panel_id in panel_ids if scores[panel_id] is None]
        covered = sum(counts[panel_id] for panel_id in panel_ids if panel_id not in missing)
        common = {"system": system["system"], "origin": system["origin"],
                  "scores": scores.copy(), "missing_panels": missing,
                  "covered_questions": covered, "coverage_fraction": covered / total}
        if missing:
            overall_excluded.append(common.copy())
            matrix.append({**common, "overall_score": None, "overall_rank": None})
        else:
            value = math.fsum(counts[panel_id] * scores[panel_id] for panel_id in panel_ids) / total
            overall_complete.append({**common, "score": value})
            matrix.append({**common, "overall_score": value, "overall_rank": None})
    overall_complete = ranked(overall_complete)
    rank_by_name = {item["system"]: item["rank"] for item in overall_complete}
    for item in matrix:
        item["overall_rank"] = rank_by_name.get(item["system"])
    matrix.sort(key=lambda item: (item["overall_rank"] is None,
                                  item["overall_rank"] or 0))

    equal_complete = []
    for item in overall_complete:
        benchmark_scores = {}
        for benchmark in benchmark_weights:
            group_count = benchmark["question_count"]
            benchmark_scores[benchmark["id"]] = math.fsum(
                counts[panel_id] * item["scores"][panel_id]
                for panel_id in benchmark["panel_ids"]) / group_count
        equal_score = math.fsum(benchmark_scores.values()) / len(BENCHMARKS)
        equal_complete.append({"system": item["system"], "origin": item["origin"],
                               "benchmark_scores": benchmark_scores, "score": equal_score,
                               "question_weighted_score": item["score"],
                               "question_weighted_rank": item["rank"],
                               "score_change": equal_score - item["score"]})
    equal_complete = ranked(equal_complete)
    for item in equal_complete:
        item["rank_change"] = item["question_weighted_rank"] - item["rank"]

    panel_tables = []
    for panel in panels:
        panel_id = panel["id"]
        observed = [{"system": system["system"], "origin": system["origin"],
                     "score": system["scores"][panel_id]}
                    for system in systems if system["scores"][panel_id] is not None]
        absent = [system["system"] for system in systems if system["scores"][panel_id] is None]
        panel_tables.append({"id": panel_id, "label": panel["label"],
                             "metric": metrics[panel_id],
                             "count": panel["count"], "ranked": ranked(observed),
                             "unranked_missing": absent})
    return {"source": source, "weights": calculated["overall"]["weights"],
            "total_questions": total, "overall_ranked": overall_complete,
            "overall_excluded": overall_excluded, "comparison_matrix": matrix,
            "panel_leaderboards": panel_tables,
            "benchmark_equal_weighted": {
                "method": "benchmark_equal_weighted", "benchmark_count": len(BENCHMARKS),
                "within_benchmark_aggregation": "question_count_weighted",
                "missing_policy": "all_panels_required", "weights": benchmark_weights,
                "ranked": equal_complete, "excluded": [item.copy() for item in overall_excluded]}}


def markdown(result: dict) -> str:
    def pct(value: float | None) -> str:
        return "—" if value is None else f"{value * 100:.4f}"

    def origin(value: str) -> str:
        return {"saved_question_records": "문항별 저장 기록 재계산",
                "published_rounded_scores": "공개 표의 반올림 점수"}[value]

    short_labels = {"locomo": "LoCoMo", "lme": "LME", "beam100k": "BEAM100K",
                    "beam10m": "BEAM10M", "personamem": "PersonaMem", "halumem": "HaluMem"}

    lines = ["# 공개 비교 리더보드", "",
             "Tenconic 점수는 저장된 문항 기록에서 재계산했습니다. 비교 시스템 점수는 공개된 재현 결과의 반올림된 스냅샷입니다.",
             "두 종합점수는 서로 다른 0–1 지표를 합친 복합점수입니다. 공식 통합 정확도나 동일 조건에서 새로 실행한 순위가 아닙니다.",
             "문항 수 가중식: Σ(패널 문항 수 × 패널 점수) / 전체 포함 문항 수. 벤치마크 균등 가중식: (LoCoMo + LongMemEval + BEAM + PersonaMem + HaluMem) / 5.",
             "BEAM 점수는 (400 × BEAM 100K + 200 × BEAM 10M) / 600으로 계산합니다. 두 방법 모두 6개 패널 점수가 모두 있어야 전체 순위에 포함합니다.", "",
             f"비교 출처: [OmniMemEval 공개 재현 결과]({result['source']['url']}) (조회 {result['source']['retrieved_at_utc']}; {result['source']['kind']})", "",
             f"비교 점수 표기 정밀도: {result['source']['original_score_precision']}. 답변 모델: {result['source']['answer_model']}; 판정 모델: {result['source']['judge_model']}.",
             result["source"]["note"], "",
             "## 문항 수 가중치", "", "| 벤치마크 | 문항 수 | 가중치 |", "| --- | ---: | ---: |"]
    for entry in result["weights"]:
        lines.append(f"| {entry['label']} | {entry['count']} | {pct(entry['weight'])}% |")
    lines += [f"| 합계 | {result['total_questions']} | 100.0000% |", "",
              "## 벤치마크별 두 방식의 가중치", "",
              "| 벤치마크 | 포함 문항 수 | 문항 수 가중치 | 벤치마크 균등 가중치 | 내부 패널 비율 |",
              "| --- | ---: | ---: | ---: | --- |"]
    for entry in result["benchmark_equal_weighted"]["weights"]:
        within = ", ".join(f"{short_labels[panel['id']]} {pct(panel['weight_within_benchmark'])}%"
                           for panel in entry["panel_weights"])
        lines.append(f"| {entry['label']} | {entry['question_count']} | {pct(entry['question_count_weight'])}% | {pct(entry['weight'])}% | {within} |")
    lines += ["", "## 문항 수 가중 전체 순위: 6개 패널 모두 점수가 있는 시스템", "",
              "| 순위 | 시스템 | 문항 수 가중 복합점수 (0–100) | 점수 출처 |", "| ---: | --- | ---: | --- |"]
    for item in result["overall_ranked"]:
        lines.append(f"| {item['rank']} | {item['system']} | {pct(item['score'])} | {origin(item['origin'])} |")
    lines += ["", "## 벤치마크 균등 가중 전체 순위", "",
              "순위 변화는 문항 수 가중 순위에서 벤치마크 균등 가중 순위로 바뀐 자리 수입니다. 양수는 상승입니다.", "",
              "| 균등 가중 순위 | 시스템 | 균등 가중 점수 (0–100) | 문항 수 가중 순위 | 문항 수 가중 점수 (0–100) | 순위 변화 | 점수 변화 (0–100) |",
              "| ---: | --- | ---: | ---: | ---: | ---: | ---: |"]
    for item in result["benchmark_equal_weighted"]["ranked"]:
        lines.append(f"| {item['rank']} | {item['system']} | {pct(item['score'])} | "
                     f"{item['question_weighted_rank']} | {pct(item['question_weighted_score'])} | "
                     f"{item['rank_change']:+d} | {item['score_change'] * 100:+.4f} |")
    lines += ["", "일부 패널 점수가 없는 시스템은 전체 순위에서 제외합니다. 빠진 점수를 0으로 대입하거나 남은 패널에 가중치를 다시 나누지 않습니다.",
              "", "| 전체 순위 제외 시스템 | 점수 있는 패널 | 포함 문항 수 | 포함 비율 | 빠진 패널 |",
              "| --- | ---: | ---: | ---: | --- |"]
    for item in result["overall_excluded"]:
        missing = ", ".join(short_labels[panel_id] for panel_id in item["missing_panels"])
        lines.append(f"| {item['system']} | {len(result['weights']) - len(item['missing_panels'])}/{len(result['weights'])} | {item['covered_questions']} | {pct(item['coverage_fraction'])}% | {missing} |")
    lines += ["", "## 6개 패널 비교표 (전체 점수·순위는 문항 수 가중)", ""]
    panel_ids = [entry["id"] for entry in result["weights"]]
    lines.append("| 시스템 | " + " | ".join(short_labels[panel_id] for panel_id in panel_ids) + " | 문항 수 가중 점수 | 문항 수 가중 순위 | 빠진 패널 |")
    lines.append("| --- | " + " | ".join("---:" for _ in panel_ids) + " | ---: | ---: | --- |")
    for item in result["comparison_matrix"]:
        cells = [pct(item["scores"][panel_id]) for panel_id in panel_ids]
        lines.append("| " + item["system"] + " | " + " | ".join(cells) + " | " +
                     pct(item["overall_score"]) + " | " +
                     (str(item["overall_rank"]) if item["overall_rank"] is not None else "—") +
                     " | " + (", ".join(short_labels[panel_id] for panel_id in item["missing_panels"]) or "—") + " |")
    tenconic = next(item for item in result["overall_ranked"] if item["system"] == "Tenconic")
    lines += ["", f"Tenconic의 문항 수 가중 종합점수 {pct(tenconic['score'])}은 반올림 전 문항 점수로 계산하므로, 과거 표에서 패널별 표시값을 다시 가중한 63.1407과 소폭 다릅니다. 공개 비교 시스템의 표시값은 원 출처의 반올림 정밀도를 유지합니다.", ""]
    for table in result["panel_leaderboards"]:
        lines += [f"## {table['label']} ({table['id']}; {table['metric']}; n={table['count']})", "",
                  "| 순위 | 시스템 | 점수 (0–100) | 점수 출처 |", "| ---: | --- | ---: | --- |"]
        for item in table["ranked"]:
            lines.append(f"| {item['rank']} | {item['system']} | {pct(item['score'])} | {origin(item['origin'])} |")
        if table["unranked_missing"]:
            lines += ["", "점수 없음 (순위 제외): " + ", ".join(table["unranked_missing"])]
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="write full-precision JSON to stdout")
    output.add_argument("--markdown", action="store_true", help="write Korean Markdown to stdout")
    args = parser.parse_args(argv)
    try:
        result = build(args.root.resolve())
    except EvidenceError as exc:
        print(f"invalid package: {exc}", file=sys.stderr)
        return 1
    print(markdown(result) if args.markdown else json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
