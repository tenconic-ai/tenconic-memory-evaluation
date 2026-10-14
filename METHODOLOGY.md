**English** | [한국어](METHODOLOGY.ko.md)

# Evaluation methodology and interpretation

## Scope

This package publishes the saved scores and question locations for Tenconic's last completed GPT evaluation on the [OmniMemEval](https://github.com/MemTensor/OmniMemEval) path: six panels and 11,107 scored questions. It includes 6,100 saved answers from LongMemEval, BEAM, and PersonaMem. It omits 5,007 answers from LoCoMo and HaluMem because those answers could repeat source wording from datasets with noncommercial (NC) terms and this release serves a business purpose. All original answers remain preserved outside this package. `answer_disclosure` marks the omissions. The scores and full question count remain, but this package cannot support semantic review of the omitted answers. Published questions, references, and options came from the original benchmarks or saved evaluation records; they were not newly generated. See [Source access](SOURCE_ACCESS.md) and `config/data-disclosure.json` for panel disclosure.

| Panel ID | Evaluation scope | Questions | Saved mean score |
| --- | --- | ---: | ---: |
| `locomo` | [LoCoMo](https://github.com/snap-research/locomo), 10 conversations, categories 1–4; excludes 446 adversarial category 5 questions | 1,540 | 0.8785714285714286 |
| `lme` | [LongMemEval-S cleaned](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned) | 500 | 0.866 |
| `beam100k` | [BEAM 100K](https://huggingface.co/datasets/Mohammadta/BEAM), 20 conversations | 400 | 0.6967688155496329 |
| `beam10m` | [BEAM 10M](https://huggingface.co/datasets/Mohammadta/BEAM-10M), 10 conversations | 200 | 0.5521723765700567 |
| `personamem` | [PersonaMem-v2](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2), 32K scope | 5,000 | 0.3684 |
| `halumem` | [HaluMem Medium](https://huggingface.co/datasets/IAAR-Shanghai/HaluMem/blob/main/HaluMem-Medium.jsonl) | 3,467 | 0.8641476781078743 |

The selected retrieval configuration used Tenconic's local storage/retrieval path, combining lexical search over body text and captions with Qwen3-Embedding-0.6B Q8 dense search. Candidate fusion used reciprocal rank fusion constant 60. Qwen3-Reranker-0.6B Q8 reranked up to 96 anchors. Final context used up to 20 anchors and 24 exploration probes, with original source groups and adjacent units. The local full-input selection budget was 7,168 tokens estimated with `o200k_base`; the retrieved-context cap was 4,096 tokens. Local Ministral 3 8B was a storage/retrieval runtime dependency and generated neither answers nor judgments in this evaluation. See `config/evaluation-settings.json`. The retrieval engine implementation and original conversations are outside this package, so this release cannot regenerate retrieval results or independently audit retrieval fidelity.

Saved configuration names `gpt-4.1-mini-2025-04-14` as answer model and `gpt-4o-mini-2024-07-18` as judge. Preserved harness answer/judgment call code dated 2026-10-07 specifies `temperature=0`. This package has no per-question request captures; that code snapshot alone cannot establish every setting of every later request. `config/evaluation-settings.json` records the `temperature_evidence` boundary. The private original has one saved answer and corresponding scoring result per question. Omitting answers here does not change those original records or scores. No separate API `seed`, `max_tokens`, or `response_format` setting was recorded. Published `config/prompt-templates.json` converts selected prompt strings from the 2026-10-07 preserved OmniMemEval harness into JSON and includes a change notice. A matching prompt path in a later configuration does not prove every full request input matched that snapshot. The preserved evaluation path treats reference answers and dataset evidence as scoring inputs. Actual retrieval requests and full contexts are absent here, so question-level input separation cannot be independently rechecked. Earlier local trials informed configuration selection; these scores are not blind holdout performance.

## Computing saved scores

Published `locomo`, `lme`, and `halumem` rows contain saved binary judgments (`evaluation.judgments`). A question's score is true judgments divided by all judgments. `personamem` applies the same arithmetic to saved multiple-choice correctness (`is_correct`); it did not use the GPT judge. Published questions, references, and source links help inspect scoring context, but this calculation neither rejudges an answer nor independently validates its reference. Binary-judgment rows contain no raw judge reasons.

The shared LoCoMo/LongMemEval judging prompt takes a question, reference, and generated answer, and instructs the judge to accept a generous topical and semantic match. HaluMem has a separate prompt concerning key facts, latest state, and fabricated information. These model-judged scores differ from benchmark-native metrics such as LoCoMo token F1 and cannot be read as human-verified accuracy. Exact preserved text is in `config/prompt-templates.json`.

For BEAM rubric questions, each item's saved scores of 0, 0.5, or 1 are averaged over runs, then item means are averaged into a question score. Ordering questions compare published event order with saved event positions. Kendall tau-b with ties is calculated over pairs of found events and normalized as `max(0, (tau + 1) / 2) × found fraction`. No found events scores 0; one found event scores `0.5 × found fraction`; if all positions are tied and the tau-b denominator is zero, tau is set to 0. Original rubric/event wording and saved BEAM judgment reasons appear in question records. Multiple saved runs of a BEAM question are averaged; each panel is the arithmetic mean of question scores. Semantic validity of judgment reasons remains a separate issue.

The question-count-weighted **overall composite is 0.6314164042076046 (63.1416404 on a 0–100 display)**: `Σ(panel question count × panel mean) / 11,107`. The 600 BEAM 100K/10M questions each enter once. Because panel scoring methods differ, this is neither common accuracy nor an original single-benchmark metric. Panel weights/contributions and values grouping BEAM panels appear in `results/recomputed-scores.json`. This release calculates Tenconic scores from unrounded question-level values; rounding panel values before aggregation can change the final digits.

## Benchmark-equal and question-weighted aggregation

The release includes a ranking that gives each of five benchmarks 20%, alongside the existing question-count-weighted ranking. Let `S` be a panel score on a 0–1 scale. Tables multiply by 100.

```text
S_count = (1540*S_LoCoMo + 500*S_LongMemEval + 400*S_BEAM100K
           + 200*S_BEAM10M + 5000*S_PersonaMem + 3467*S_HaluMem) / 11107
S_BEAM = (400*S_BEAM100K + 200*S_BEAM10M) / 600
S_equal = (S_LoCoMo + S_LongMemEval + S_BEAM + S_PersonaMem + S_HaluMem) / 5
```

Within BEAM, the 100K and 10M panels retain a 400:200, or 2:1, question-count weighting. Equality applies **between five benchmarks**. Their effective weights are `(1/5)*(400/600)=2/15` for BEAM 100K and `(1/5)*(200/600)=1/15` for BEAM 10M. A plain mean of six panels or of the two BEAM scopes is different.

| Benchmark | Questions | Question-count weight | Benchmark-equal weight |
| --- | ---: | ---: | ---: |
| LoCoMo | 1,540 | 13.8651% | 20% |
| LongMemEval | 500 | 4.5017% | 20% |
| BEAM combined | 600 | 5.4020% | 20% |
| PersonaMem | 5,000 | 45.0167% | 20% |
| HaluMem | 3,467 | 31.2145% | 20% |
| Total | 11,107 | 100% | 100% |

Tenconic's combined BEAM score is 0.6485700025564408. Its benchmark-equal composite is **0.7251378218471487 (72.5138/100), rank 2**. Its original question-weighted score remains **63.1416/100, rank 2**. [Full leaderboards](LEADERBOARD.md) show both scores/ranks and changes for every system. `rank_change` is original question-weighted rank minus benchmark-equal rank, so a positive number indicates a rise. Different weights aggregate the same saved results.

Score change is the benchmark-equal score minus the question-count weighted score, calculated before display rounding and then shown on the 0–100 scale to four decimal places. Tenconic's change is **+9.3721**; subtracting the displayed scores, `72.5138 - 63.1416`, gives `+9.3722`. This last-digit difference is due to rounding, not a different calculation method or evaluation result.

Both overall rankings require all six panels. If either BEAM scope is missing, the system is excluded from both; weights are not redistributed over remaining scopes. Panel rankings still include systems with that panel's score. Sorting uses scores before display rounding. Exactly equal calculated scores share a rank and skip the next rank.

Recomputation needs only Python 3.10 or later and its standard library. From the package root:

```text
python -B scripts/recompute_scores.py --check
python -B scripts/recompute_scores.py --check --json
python -B scripts/build_leaderboard.py --json
python -B scripts/build_leaderboard.py --markdown
```

The first script checks UTF-8 JSONL row schema, panel IDs, counts, status, and duplicate IDs, and recomputes saved item, question, panel, and `config/suite.json` overall question-weighted scores. Its JSON output can be compared with `results/recomputed-scores.json`. The remaining commands combine the public comparison snapshot and calculate scores/ranks under both methods, producing the form of `results/leaderboard.json` and `LEADERBOARD.md`. This is an **offline arithmetic audit and display of saved numbers**. Public materials cannot regenerate GPT answers, call the judge again, or audit retrieval fidelity. LoCoMo/HaluMem answer bodies cannot be reviewed directly. PersonaMem's saved normalized choices may omit full raw model responses. We publish saved option order for 4,895 questions, but do not claim to prove the multiple-choice decision independently by reparsing raw responses.

All six panels filled their expected final question counts. Interrupted and retried in-progress work remains a separate historical fact; successful final rows do not erase it. This package excludes original conversations, internal retrieval contexts, full model inputs, product source, and raw run logs. These scores do not establish independent reproduction from full original datasets or operational reliability.

## Limits of the public comparison

Tenconic's comparison scores are recomputed from records here. The other 14 systems use a snapshot of then-rounded scores from [OmniMemEval's public Reproduced Results](https://github.com/MemTensor/OmniMemEval/blob/0b1ea8d28aa2d3e03ac4a6aee17b3006a131da7d/docs/user_memory/results.md), stored in `config/public-reference-scores.json`. **Published Reference** and **Reproduced Results** are different sources. Only 12 systems with all six panel scores enter overall rankings; three systems with missing values are excluded. Missing values are neither zero-filled nor used to redistribute weights. Panel comparisons include every system with a score on that panel.

Shared answer and judge model names do not establish same-time, same-deployment reruns for all systems. Entries grouped by name, including Zep and Graphiti, may mix deployment configurations. Earlier local trials influenced Tenconic's retrieval configuration, so the comparison does not establish blind holdout performance or superiority.

## Category comparisons

[Detailed leaderboard tables](LEADERBOARD.md#benchmark-details) calculate Tenconic's category means directly from the saved question scores. Category counts partition each panel; weighting those means by their counts recovers the panel mean. LoCoMo's stored IDs are `4 = Single-Hop`, `1 = Multi-Hop`, `2 = Temporal`, and `3 = Open-Domain`; category 5 remains excluded. PersonaMem has seven preference types in this evaluated set.

Peer category values in [public-reference-details.json](config/public-reference-details.json) come from the same October 8, 2026 [OmniMemEval Reproduced Results snapshot](https://github.com/MemTensor/OmniMemEval/blob/0b1ea8d28aa2d3e03ac4a6aee17b3006a131da7d/docs/user_memory/results.md) as the original aggregate comparison. Original backend names and deployment fields are retained: LoCoMo uses `Zep`, while the other tables use `graphiti-zep`; the summary retains the upstream `Zep / Graphiti` grouping. Peer overall scores are copied from the source rather than reconstructed from its rounded categories. Tenconic values are calculated before display rounding. Detailed score tables use two decimals on a 0–100 scale; the overall composite tables retain four.

BEAM peer comparisons show scale-level mean and source-reported dispersion. Tenconic's dispersion is the population standard deviation of saved question scores, not a confidence interval. Tenconic's 10 ability means are shown separately, with 40 questions per ability at 100K and 20 at 10M. The source publishes no peer ability values, so the package does not assign peer ability scores or ranks. The two scales use different question/conversation sets; their difference is not a controlled effect of history length. Event ordering retains its ordering metric, while other BEAM abilities use saved rubric-item scoring.

These category tables are an offline calculation and source-table transcription. No retrieval, answer generation, or semantic judging was rerun. Source-derived peer context-token values remain in the JSON snapshot for completeness; this score comparison does not infer equal token budgets or efficiency superiority.
