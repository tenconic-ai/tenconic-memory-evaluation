# Tenconic Memory Evaluation

**English** | [한국어](README.ko.md)

Public evaluation evidence for Tenconic's user-memory system: **11,107 scored questions across five benchmark families**, saved answer records where disclosed, and standalone Python tools to reproduce the published score calculations.

This repository is maintained by [Tenconic](https://github.com/tenconic-ai). It contains evaluation data, documentation, and calculation scripts. The Tenconic product implementation, runtime, model weights, and internal retrieval contexts are not distributed here.

[Results and leaderboards](LEADERBOARD.md) · [Methodology](METHODOLOGY.md) · [Download a release](https://github.com/tenconic-ai/tenconic-memory-evaluation/releases/latest) · [Dataset licenses](THIRD_PARTY_NOTICES.md)

## Overall leaderboards

Both tables compare **12 systems with all six panel scores**, on a **0–100 scale**. Peer values come from the October 8, 2026 [OmniMemEval Reproduced Results snapshot](https://github.com/MemTensor/OmniMemEval/blob/main/docs/user_memory/results.md); Tenconic values are recalculated from this repository's question records. These mixed-metric composites are descriptive comparisons, not official unified accuracy or a newly controlled head-to-head evaluation.

### Question-count weighted

Each panel is weighted by its number of evaluated questions: `sum(panel_score × panel_questions) / 11,107`.

| Rank | System | Composite score / 100 |
| ---: | --- | ---: |
| 1 | MemOS | 63.2854 |
| **2** | **Tenconic** | **63.1416** |
| 3 | EverOS | 61.9178 |
| 4 | Hindsight | 61.5374 |
| 5 | Letta | 60.1003 |
| 6 | Mem0 | 56.1418 |
| 7 | Zep / Graphiti | 55.9907 |
| 8 | Viking | 53.9791 |
| 9 | mem9 | 53.6926 |
| 10 | Cognee | 51.6240 |
| 11 | Supermemory | 50.7572 |
| 12 | MemMachine | 46.4234 |

### Five-benchmark equal weighted

LoCoMo, LongMemEval, BEAM, PersonaMem, and HaluMem each receive **20%**. BEAM is first pooled as `(400 × BEAM_100K + 200 × BEAM_10M) / 600`; the five benchmark scores are then averaged.

| Rank | System | Composite score / 100 |
| ---: | --- | ---: |
| 1 | MemOS | 72.6033 |
| **2** | **Tenconic** | **72.5138** |
| 3 | Hindsight | 68.5780 |
| 4 | EverOS | 68.5507 |
| 5 | Letta | 67.7840 |
| 6 | Zep / Graphiti | 64.4367 |
| 7 | mem9 | 63.6267 |
| 8 | Mem0 | 61.0927 |
| 9 | Viking | 61.0287 |
| 10 | Supermemory | 58.6667 |
| 11 | Cognee | 58.5093 |
| 12 | MemMachine | 55.8320 |

Overall scores are displayed to four decimal places. Score changes in the full leaderboards are calculated before display rounding, so they can differ in the last digit from subtracting the displayed scores.

**Excluded from both overall rankings:** Memori, MemoryLake, and Backboard.io have incomplete panel coverage. Missing scores are not filled with zero or reweighted away. Peer values retain their original published rounding. See the [full leaderboards](LEADERBOARD.md) for panel rankings, exact weights, coverage, and rank changes.

## Tenconic panel results

These are saved results from completed GPT-based evaluations started on October 6–8, 2026. The answer model was `gpt-4.1-mini-2025-04-14`; model-judged panels used `gpt-4o-mini-2024-07-18`. PersonaMem used multiple-choice correctness without a judge model.

| Evaluation panel | Questions | Metric | Tenconic result |
| --- | ---: | --- | ---: |
| LoCoMo categories 1–4 | 1,540 | Model-judged accuracy | 87.8571% |
| LongMemEval-S cleaned | 500 | Model-judged accuracy | 86.6000% |
| BEAM 100K | 400 | Mean per-question nugget score | 0.696769 |
| BEAM 10M | 200 | Mean per-question nugget score | 0.552172 |
| PersonaMem v2 text 32K | 5,000 | Saved multiple-choice accuracy | 36.8400% |
| HaluMem Medium | 3,467 | Model-judged accuracy | 86.4148% |

## Reproduce the score calculations

Download and extract the [latest release](https://github.com/tenconic-ai/tenconic-memory-evaluation/releases/latest), or clone this repository. Run from the repository root with **Python 3.10 or later**:

```sh
python -B scripts/recompute_scores.py --check
python -B scripts/build_leaderboard.py --markdown
```

No additional packages, GPU, server, API key, or network connection are needed for these commands. Use `python3` if that is the Python command on your system. The commands replay saved numerical evidence; they do not generate answers, rerun retrieval, or semantically rejudge responses.

For machine-readable output and the focused tests:

```sh
python -B scripts/recompute_scores.py --check --json
python -B scripts/build_leaderboard.py --json
python -B -m unittest discover -s tests -p "test_*.py" -v
```

The calculator returns a nonzero exit code for invalid records or a mismatch with expected counts or scores. Expected outputs are in [recomputed-scores.json](results/recomputed-scores.json) and [leaderboard.json](results/leaderboard.json). Korean leaderboard output is available with `--markdown --language ko`.

## What is included

| Material | Public coverage |
| --- | --- |
| Scoring records and source locations | All 11,107 evaluated questions |
| Saved answers | 6,100: LongMemEval, BEAM, and PersonaMem |
| Original question/reference pairs | 5,995 |
| Question rows represented by official source links | 5,112 |
| Withheld answer bodies | 5,007: all LoCoMo and HaluMem rows |

LoCoMo and HaluMem question/reference text and saved answer bodies are excluded from this business-purpose distribution because of the datasets' noncommercial license scope and possible repetition of source expression. Their numerical judgments remain available for score replay. The excluded Tenconic answers cannot be inspected through this package or the upstream question links.

An additional 105 PersonaMem rows omit question/reference/options text because the benchmark source contains credential-shaped or private-path patterns. This does not establish that those strings are live credentials. All 5,000 PersonaMem answers and scores remain included; answers are saved normalized choices, not complete raw model responses. Original private records remain preserved. Details and attribution are in [Source access](SOURCE_ACCESS.md) and [Third-party notices](THIRD_PARTY_NOTICES.md).

## Documentation and files

| Start here | Contents |
| --- | --- |
| [Leaderboard](LEADERBOARD.md) | Two composite methods, weight comparison, coverage, and six panel rankings |
| [Methodology](METHODOLOGY.md) | Evaluation scope, models, settings, metric definitions, and limitations |
| [Data schema](DATA_SCHEMA.md) | JSONL fields, source references, and omission metadata |
| [Source access](SOURCE_ACCESS.md) | How to locate original benchmark questions |
| [Licensing](LICENSE.md) and [third-party notices](THIRD_PARTY_NOTICES.md) | Rights and attribution by material |
| [Evaluation settings](config/evaluation-settings.json) and [prompt templates](config/prompt-templates.json) | Preserved historical configuration and selected prompt strings |
| [Suite](config/suite.json), [data](data/), and [results](results/) | Included panels, question records, and calculated outputs |
| [Calculation scripts](scripts/) and [tests](tests/) | Standard-library Python tools and their checks |

## Scope and reuse

This release supports inspection of disclosed records and independent recalculation of saved scores. It does not reproduce the full Tenconic product or a fresh end-to-end benchmark run. LoCoMo category 5 and auxiliary metrics outside the six listed primary scores are out of scope. Complete final question coverage does not imply that the original execution had no interruptions or retries.

GitHub's **“Source code (zip/tar.gz)”** links are automatically generated archives of the files in this repository at the release tag. Here, “source code” means the included evaluation calculation scripts and accompanying repository files; it does not mean that Tenconic's product source has been released. The separately attached ZIP is the curated evaluation package.

There is no repository-wide open-source license grant. Third-party materials retain their stated licenses; see [LICENSE.md](LICENSE.md). To cite the evidence release, use [CITATION.cff](CITATION.cff). Report reproducibility issues or proposed corrections through [GitHub Issues](https://github.com/tenconic-ai/tenconic-memory-evaluation/issues), following the [contribution notes](CONTRIBUTING.md).
