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
