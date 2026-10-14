**English** | [한국어](DATA_SCHEMA.ko.md)

# Public data schema

All paths are relative to the package root. `config/suite.json` contains `schema_version: 1`, six `panels`, and question-count-weighted `aggregation`. Each panel has `id`, `label`, `benchmark_family`, `expected_questions`, `expected_score`, and `data_file`. Panel IDs are `locomo`, `lme`, `beam100k`, `beam10m`, `personamem`, and `halumem`. `data_file` points to a UTF-8 JSONL file in this package; each line is one scored question. `config/data-disclosure.json` also records each panel's source-field policy.

Every published row requires:

| Field | Meaning |
| --- | --- |
| `record_id` | Public record ID unique within its panel |
| `benchmark` | Matches a panel ID in `suite.json` |
| `category` | Original evaluation category; LoCoMo numbers are strings, while other panels retain their category strings |
| `status` | `success` for published final rows |
| `source_url` | Official public source file or dataset page URL |
| `source_ref` | Nonempty location identifier from preserved input; not a permanent upstream revision ID |
| `answer` or `answer_disclosure` | Exactly one, according to the disclosure policy below |
| `evaluation` | Saved numeric result in one of the forms below |

All 6,100 `lme`, `beam100k`, `beam10m`, and `personamem` rows have a nonempty saved `answer` string. All 5,007 `locomo` and `halumem` rows omit `answer` and instead carry `answer_disclosure`, with exactly these four fields: `status: "withheld"`, `reason: "dataset_license_scope"`, `source_license`, and `preserved_original_outside_package: true`. `source_license` is `CC-BY-NC-4.0` for LoCoMo and `CC-BY-NC-ND-4.0` for HaluMem. Original answers remain in the private source records. These markers explain their exclusion here to avoid redistributing possible source wording. Saved judgments, scores, and question locations remain for arithmetic recomputation, but answer-text review is impossible for those rows. The calculator rejects unmarked absence, missing answers in other panels, malformed metadata, or simultaneous answer and disclosure marker.

Every `lme`, `beam100k`, and `beam10m` row, and 4,895 of the 5,000 `personamem` rows, include original `question` and `reference_answer`. A published reference can be a string or integer; its type is not arbitrarily coerced to string. PersonaMem `choices` is the preserved original **string** from `all_options`; `reference_answer` is the correct option letter. The other 105 PersonaMem rows omit all three fields and include `source_disclosure` below. Every PersonaMem row has `answer_representation: "saved_normalized_choice"`, indicating that `answer` is the preserved normalized selection, not necessarily the full raw model response.

The restricted PersonaMem rows carry `source_disclosure: {"mode":"source_link_only","reason":"sensitive_source_text","omitted_fields":["question","reference_answer","choices"]}`. Provider-key-like and private-path-like patterns were found in original benchmark wording, so all three fields were omitted together. This does not claim that any real credential or private path was verified. The saved answer, correctness score, `source_url`, and `source_ref.csv_row_index0` remain. `config/suite.json` uses `question_reference_coverage` values `full`, `partial`, or `source_link_only`; read them with published question/reference pair counts.

`source_ref` differs by panel. LoCoMo uses `conversation_index0`, `sample_id`, `original_qa_index0`, `evaluated_qa_index0`, `json_pointer`; LongMemEval uses `row_index0`, `question_id`; PersonaMem uses `csv_row_index0`; HaluMem uses `user_uuid`, `session_index0`, `question_index0`, `json_pointer`; BEAM uses `conversation_id`, `question_index0`. `index0` denotes a zero-based index. The 5,007 LoCoMo/HaluMem rows and 105 PersonaMem rows, 5,112 total, provide source URL and location in place of source question/reference text. Upstream changes can shift those positions; follow [SOURCE_ACCESS.md](SOURCE_ACCESS.md) to cross-check.

| `evaluation.type` | Published fields | Recomputation |
| --- | --- | --- |
| `binary_judge` | `judgments: [boolean, …]`, `saved_score` | True count / judgment count; saved model judgments for LoCoMo, LongMemEval, HaluMem |
| `multiple_choice_saved` | `judgments: [boolean, …]`, `saved_score` | True count / decision count; saved PersonaMem choice correctness |
| `rubric_mean` | `items: [{item_index, rubric, scores: [0/0.5/1, …], reasons: [string, …], saved_score}, …]`, `saved_score` | Mean per item across runs, then mean across items; BEAM rubric question |
| `ordering_tau_b` | `rubric: [original event string, …]`, `positions: [[integer, …], …]`, `scores: [number, …]`, `reasons: [string, …]`, `saved_score` | Ordering score for each run, then run mean; each `positions` array has the same length as `rubric` |

In every form, `saved_score` is a finite number from 0 to 1. In `ordering_tau_b`, positions at or below zero mean event not found; positive numbers are saved found positions. Each `scores` element is calculated for its corresponding `positions` run. BEAM `rubric` holds original evaluation wording and `reasons` holds saved judgment reasons. `binary_judge` rows have no reasons.

The calculator recomputes item, question, category mean, and panel mean scores. `--check` compares `expected_score` and the `aggregation.method: "question_count_weighted"` overall score for 11,107 questions. Result JSON `overall.weights` records panel question shares and contributions; `benchmark_families` groups panels of the same benchmark as reference values. BEAM's 600 questions are not duplicated in the overall total. `binary_numerator`/`binary_denominator` count saved binary judgments. `score_std_population`, where present for a panel with ordering questions, is the **population standard deviation of question scores**, not a confidence interval or variation between independent runs.

Other-system scores in `config/public-reference-scores.json` are rounded public-source numbers on a 0–1 scale, or `null` for missing. `scripts/build_leaderboard.py` combines Tenconic's recomputed question scores with this snapshot to build the form of `results/leaderboard.json` and `LEADERBOARD.md`. Only systems with six values receive overall ranks; missing values are not zero-filled. This package does not contain other systems' question-level answers or calculations. Numeric recomputation of saved answers' scores and semantic rejudgment against source questions are different tasks.

The release keeps `overall_ranked`, `overall_excluded`, `weights`, and `comparison_matrix.overall_score`/`overall_rank` in `results/leaderboard.json` **question-count-weighted**. `panel_leaderboards` still covers six panel rankings. The new `benchmark_equal_weighted` object gives the result weighted equally across **five benchmarks**. JSON scores and weights use 0–1; Markdown tables multiply by 100.

| `benchmark_equal_weighted` field | Meaning |
| --- | --- |
| `method` | `benchmark_equal_weighted` |
| `benchmark_count` | 5 |
| `within_benchmark_aggregation` | `question_count_weighted`: 400:200 within BEAM |
| `missing_policy` | `all_panels_required`: all six panels, including both BEAM scopes |
| `weights` | Per-benchmark `id`, `label`, `panel_ids`, `question_count`, equal `weight`, original `question_count_weight` |
| `weights[].panel_weights` | Per-panel `id`, `count`, `weight_within_benchmark`, and overall `effective_weight` |
| `ranked` | Systems descending by benchmark-equal score |
| `excluded` | Systems absent from both overall rankings due to missing panels, with included/missing scope information |

Each `ranked` row has `system`, `origin`, five `benchmark_scores`, equal `score`/`rank`, original `question_weighted_score`/`question_weighted_rank`, `rank_change`, and `score_change`. `rank_change` is original rank minus equal-weighted rank; positive means a rise. `score_change` is equal score minus original score on the 0–1 scale. Exactly equal calculated scores share a rank and skip the next rank. Equal displayed rounded values alone do not establish a tie.

## Detailed benchmark comparisons

`config/public-reference-details.json` stores the category and BEAM scale values transcribed from the pinned OmniMemEval reproduced-results snapshot. Its `source` gives the dated source URL, original precision, 0–1 scale and scope. Each of the six `panels` supplies category definitions (`id`, English/Korean `label`) and peer `rows`:

| Field | Meaning |
| --- | --- |
| `system` | Canonical name used to join the existing overall comparison |
| `source_system` | Original per-benchmark label, including `Zep` versus `graphiti-zep` |
| `deployment` | Source-reported memory backend deployment |
| `score` | Published overall panel score, checked against `public-reference-scores.json` |
| `categories` | Category-ID to score mapping; `null` for every peer BEAM row because the source provides no ability breakdown |
| `score_std` | BEAM's source-reported dispersion on the same 0–1 scale; omitted for other source panels |
| `context_tokens` | Source-reported average answer-context tokens; retained as source metadata, not displayed in the score tables |

The builder adds `benchmark_details` to `results/leaderboard.json`: `source` and six `panels` with category definitions/counts and sorted `rows`. Tenconic category counts and means come from recalculated public records; their weighted mean must recover the panel score. Tenconic's `score_std` is its question-score population standard deviation for BEAM and `null` otherwise; its `context_tokens` is `null` because this public record schema does not supply token counts. Peer `score_std` is `null` outside BEAM in the generated output. Output rows also contain `rank` and `origin`; existing `panel_leaderboards` and both aggregate rankings retain their original fields and values.

The source snapshot has 14 LoCoMo peer rows, 12 each for LongMemEval/PersonaMem/HaluMem, and 11 per BEAM scale. Every scored peer in the existing overall snapshot must appear in its detail panel. Missing peers are not zero-filled. Package revision 7 requires the detail snapshot. `LEADERBOARD.md` and `LEADERBOARD.ko.md` are generated from this same joined output. Category means are displayed to two decimal places on a 0–100 scale; JSON retains the calculation precision.
