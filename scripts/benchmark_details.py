"""Validate published category snapshots and join them to saved Tenconic scores."""

from __future__ import annotations

import math
from pathlib import Path

from recompute_scores import load_json, nonempty_text, object_at, require


def score(value, where: str) -> float:
    require(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1,
            f"{where}: expected finite 0-1 score")
    return float(value)


def build_details(root: Path, calculated: dict, reference: dict) -> dict | None:
    manifest = object_at(load_json(root / "config" / "suite.json"), "manifest")
    revision = manifest.get("package_revision", 0)
    require(type(revision) is int and revision >= 0,
            "manifest.package_revision: expected nonnegative integer")
    path = root / "config" / "public-reference-details.json"
    require(path.exists() or revision < 7,
            "reference details: public-reference-details.json required for package revision >= 7")
    if not path.exists():
        return None

    document = object_at(load_json(path), "details")
    require(document.get("schema_version") == 1 and type(document.get("schema_version")) is int,
            "details.schema_version: expected 1")
    source = object_at(document.get("source"), "details.source")
    for field in ("url", "snapshot_date", "note"):
        nonempty_text(source.get(field), f"details.source.{field}")
    require(source.get("kind") == "upstream_reproduced_snapshot" and
            source.get("score_scale") == "0-1", "details.source: unsupported source kind or scale")

    panels = calculated["panels"]
    reference_rows = {row["system"]: row["scores"] for row in reference["rows"]}
    raw_panels = document.get("panels")
    require(isinstance(raw_panels, list) and len(raw_panels) == len(panels),
            "details.panels: expected six panels")
    output = []
    for index, (raw_panel, panel) in enumerate(zip(raw_panels, panels)):
        where = f"details.panels[{index}]"
        entry = object_at(raw_panel, where)
        panel_id = panel["id"]
        require(entry.get("id") == panel_id, f"{where}.id: expected {panel_id}")
        raw_categories = entry.get("categories")
        require(isinstance(raw_categories, list) and len(raw_categories) == len(panel["categories"]),
                f"{where}.categories: expected exact category coverage")
        definitions = []
        category_ids = set()
        for cat_index, raw_category in enumerate(raw_categories):
            cat_where = f"{where}.categories[{cat_index}]"
            definition = object_at(raw_category, cat_where)
            category_id = nonempty_text(definition.get("id"), f"{cat_where}.id")
            require(category_id not in category_ids, f"{cat_where}.id: duplicate category")
            category_ids.add(category_id)
            label = object_at(definition.get("label"), f"{cat_where}.label")
            definitions.append({"id": category_id,
                                "label": {language: nonempty_text(label.get(language),
                                                                  f"{cat_where}.label.{language}")
                                          for language in ("en", "ko")},
                                "count": panel["categories"][category_id]["count"]
                                if category_id in panel["categories"] else None})
        require(category_ids == set(panel["categories"]),
                f"{where}.categories: keys differ from recomputed records")
        tenconic_categories = {category["id"]: panel["categories"][category["id"]]["score"]
                               for category in definitions}
        count = sum(category["count"] for category in definitions)
        require(count == panel["count"], f"{where}.categories: counts do not partition panel")
        mean = math.fsum(category["count"] * tenconic_categories[category["id"]]
                         for category in definitions) / count
        require(math.isclose(mean, panel["score"], rel_tol=0, abs_tol=1e-12),
                f"{where}.categories: weighted mean differs from panel")
        beam = panel_id.startswith("beam")
        std = score(panel["score_std_population"], f"{where}.score_std_population") if beam else None
        peers = entry.get("rows")
        require(isinstance(peers, list), f"{where}.rows: expected list")
        expected_systems = {name for name, scores in reference_rows.items()
                            if scores[panel_id] is not None}
        peer_rows = []
        seen = set()
        for row_index, raw_row in enumerate(peers):
            row_where = f"{where}.rows[{row_index}]"
            row = object_at(raw_row, row_where)
            system = nonempty_text(row.get("system"), f"{row_where}.system")
            require(system in expected_systems and system not in seen,
                    f"{row_where}.system: unknown or duplicate canonical row")
            seen.add(system)
            source_system = nonempty_text(row.get("source_system"), f"{row_where}.source_system")
            deployment = row.get("deployment")
            require(deployment in ("cloud", "local/self-hosted"),
                    f"{row_where}.deployment: unsupported value")
            overall = score(row.get("score"), f"{row_where}.score")
            require(math.isclose(overall, reference_rows[system][panel_id], rel_tol=0,
                                 abs_tol=1e-10),
                    f"{row_where}.score: differs from reference overall")
            raw_values = row.get("categories")
            if beam:
                require(raw_values is None, f"{row_where}.categories: BEAM peer details unavailable")
                row_std = score(row.get("score_std"), f"{row_where}.score_std")
            else:
                values = object_at(raw_values, f"{row_where}.categories")
                require(set(values) == category_ids,
                        f"{row_where}.categories: expected exact category coverage")
                raw_values = {category["id"]: score(values[category["id"]],
                                                      f"{row_where}.categories.{category['id']}")
                              for category in definitions}
                require("score_std" not in row, f"{row_where}.score_std: only BEAM has std")
                row_std = None
            context = row.get("context_tokens")
            require(type(context) is int and context > 0,
                    f"{row_where}.context_tokens: expected positive integer")
            peer_rows.append({"system": system, "source_system": source_system,
                              "deployment": deployment, "score": overall,
                              "categories": raw_values, "score_std": row_std,
                              "context_tokens": context, "origin": "published_rounded_scores"})
        require(seen == expected_systems,
                f"{where}.rows: missing or extra scored systems {sorted(expected_systems - seen)}")
        tenconic = {"system": "Tenconic", "source_system": "Tenconic",
                    "deployment": "local/self-hosted", "score": panel["score"],
                    "categories": tenconic_categories, "score_std": std,
                    "context_tokens": None, "origin": "saved_question_records"}
        rows = sorted([tenconic, *peer_rows],
                      key=lambda row: (-row["score"], row["system"].casefold()))
        for row_index, row in enumerate(rows):
            row["rank"] = (rows[row_index - 1]["rank"] if row_index and
                           row["score"] == rows[row_index - 1]["score"] else row_index + 1)
        output.append({"id": panel_id, "label": panel["label"], "count": panel["count"],
                       "categories": definitions, "rows": rows})
    return {"source": source, "panels": output}
