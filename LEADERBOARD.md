[Home](README.md) | [Methodology](METHODOLOGY.md) | [Korean](LEADERBOARD.ko.md)

# Public comparison leaderboard

[Jump to detailed tables](#benchmark-details): [LoCoMo categories 1-4](#detail-locomo) · [LongMemEval-S cleaned](#detail-lme) · [BEAM 100K](#detail-beam100k) · [BEAM 10M](#detail-beam10m) · [PersonaMem v2 text 32K](#detail-personamem) · [HaluMem Medium](#detail-halumem)

Tenconic scores were recalculated from saved question records. Comparison-system scores come from a rounded snapshot of publicly reproduced results.
Both overall scores combine different 0–1 metrics into composite scores. They are neither an official aggregate accuracy nor a ranking from a new run under identical conditions.
Question-count weighting: Σ(panel question count × panel score) / total included questions. Equal benchmark weighting: (LoCoMo + LongMemEval + BEAM + PersonaMem + HaluMem) / 5.
The BEAM score is (400 × BEAM 100K + 200 × BEAM 10M) / 600. Both methods require scores in all six panels for an overall rank.

Comparison source: [OmniMemEval public reproduced results](https://github.com/MemTensor/OmniMemEval/blob/0b1ea8d28aa2d3e03ac4a6aee17b3006a131da7d/docs/user_memory/results.md) (retrieved 2026-10-08T09:29:05Z; upstream_reproduced_snapshot)

Comparison-score display precision: two decimal places on 0-100 scale. Answer model: gpt-4.1-mini-2025-04-14; judge model: gpt-4o-mini-2024-07-18.
Uses the 2026-10-08 snapshot of OmniMemEval Reproduced Results. Published Reference Results are excluded. External raw question records are not in this package. This is not a synchronized controlled rerun. Zep / Graphiti retains the upstream grouping across different deployment routes.

## Question-count weights

| Benchmark | Questions | Weight |
| --- | ---: | ---: |
| LoCoMo categories 1-4 | 1540 | 13.8651% |
| LongMemEval-S cleaned | 500 | 4.5017% |
| BEAM 100K | 400 | 3.6013% |
| BEAM 10M | 200 | 1.8007% |
| PersonaMem v2 text 32K | 5000 | 45.0167% |
| HaluMem Medium | 3467 | 31.2145% |
| Total | 11107 | 100.0000% |

## Benchmark weights under both methods

| Benchmark | Included questions | Question-count weight | Equal benchmark weight | Within-benchmark panel shares |
| --- | ---: | ---: | ---: | --- |
| LoCoMo | 1540 | 13.8651% | 20.0000% | LoCoMo 100.0000% |
| LongMemEval | 500 | 4.5017% | 20.0000% | LME 100.0000% |
| BEAM | 600 | 5.4020% | 20.0000% | BEAM100K 66.6667%, BEAM10M 33.3333% |
| PersonaMem | 5000 | 45.0167% | 20.0000% | PersonaMem 100.0000% |
| HaluMem | 3467 | 31.2145% | 20.0000% | HaluMem 100.0000% |

## Question-count weighted overall ranking: systems with all six panel scores

| Rank | System | Question-count weighted composite (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | MemOS | 63.2854 | Published table's rounded scores |
| 2 | Tenconic | 63.1416 | Recalculated from saved question records |
| 3 | EverOS | 61.9178 | Published table's rounded scores |
| 4 | Hindsight | 61.5374 | Published table's rounded scores |
| 5 | Letta | 60.1003 | Published table's rounded scores |
| 6 | Mem0 | 56.1418 | Published table's rounded scores |
| 7 | Zep / Graphiti | 55.9907 | Published table's rounded scores |
| 8 | Viking | 53.9791 | Published table's rounded scores |
| 9 | mem9 | 53.6926 | Published table's rounded scores |
| 10 | Cognee | 51.6240 | Published table's rounded scores |
| 11 | Supermemory | 50.7572 | Published table's rounded scores |
| 12 | MemMachine | 46.4234 | Published table's rounded scores |

## Equal benchmark weighted overall ranking

Rank change counts places gained from the question-count weighted rank to the equal benchmark weighted rank; a positive value means a rise.

Score change is the equal benchmark weighted score minus the question-count weighted score, calculated before display rounding. It may differ in the last digit from subtracting the displayed scores.

| Equal-weight rank | System | Equal-weight score (0–100) | Question-count rank | Question-count score (0–100) | Rank change | Score change (0–100) |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | MemOS | 72.6033 | 1 | 63.2854 | +0 | +9.3179 |
| 2 | Tenconic | 72.5138 | 2 | 63.1416 | +0 | +9.3721 |
| 3 | Hindsight | 68.5780 | 4 | 61.5374 | +1 | +7.0406 |
| 4 | EverOS | 68.5507 | 3 | 61.9178 | -1 | +6.6328 |
| 5 | Letta | 67.7840 | 5 | 60.1003 | +0 | +7.6837 |
| 6 | Zep / Graphiti | 64.4367 | 7 | 55.9907 | +1 | +8.4460 |
| 7 | mem9 | 63.6267 | 9 | 53.6926 | +2 | +9.9341 |
| 8 | Mem0 | 61.0927 | 6 | 56.1418 | -2 | +4.9509 |
| 9 | Viking | 61.0287 | 8 | 53.9791 | -1 | +7.0495 |
| 10 | Supermemory | 58.6667 | 11 | 50.7572 | +1 | +7.9095 |
| 11 | Cognee | 58.5093 | 10 | 51.6240 | -1 | +6.8854 |
| 12 | MemMachine | 55.8320 | 12 | 46.4234 | +0 | +9.4086 |

Systems missing any panel score are excluded from overall rankings. Missing scores are not set to zero, and the remaining panels are not reweighted.

| System excluded from overall rank | Scored panels | Covered questions | Coverage | Missing panels |
| --- | ---: | ---: | ---: | --- |
| Memori | 4/6 | 10507 | 94.5980% | BEAM100K, BEAM10M |
| MemoryLake | 1/6 | 1540 | 13.8651% | LME, BEAM100K, BEAM10M, PersonaMem, HaluMem |
| Backboard.io | 1/6 | 1540 | 13.8651% | LME, BEAM100K, BEAM10M, PersonaMem, HaluMem |

## Six-panel comparison (overall score and rank use question-count weighting)

| System | LoCoMo | LME | BEAM100K | BEAM10M | PersonaMem | HaluMem | Question-count score | Question-count rank | Missing panels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MemOS | 88.8300 | 89.2000 | 66.8700 | 56.7500 | 40.5800 | 80.9100 | 63.2854 | 1 | — |
| Tenconic | 87.8571 | 86.6000 | 69.6769 | 55.2172 | 36.8400 | 86.4148 | 63.1416 | 2 | — |
| EverOS | 82.7500 | 80.4000 | 58.6400 | 47.7300 | 35.9400 | 88.6600 | 61.9178 | 3 | — |
| Hindsight | 81.9900 | 72.2000 | 70.2200 | 59.7500 | 37.9800 | 83.9900 | 61.5374 | 4 | — |
| Letta | 77.1200 | 77.6700 | 69.2200 | 52.3000 | 35.1200 | 85.4300 | 60.1003 | 5 | — |
| Mem0 | 77.6800 | 56.0000 | 70.4100 | 43.3300 | 36.7600 | 73.6400 | 56.1418 | 6 | — |
| Zep / Graphiti | 63.8300 | 79.8000 | 68.7000 | 56.1100 | 32.3400 | 81.7100 | 55.9907 | 7 | — |
| Viking | 69.3300 | 61.0700 | 70.7600 | 58.1400 | 30.8000 | 77.3900 | 53.9791 | 8 | — |
| mem9 | 73.6400 | 78.0000 | 65.7500 | 57.3000 | 30.7600 | 72.8000 | 53.6926 | 9 | — |
| Cognee | 83.4800 | 51.8000 | 59.3000 | 56.0200 | 26.4600 | 72.6000 | 51.6240 | 10 | — |
| Supermemory | 73.5300 | 66.0700 | 65.9800 | 52.4900 | 39.6400 | 52.6100 | 50.7572 | 11 | — |
| MemMachine | 73.9000 | 63.6000 | 64.8000 | 51.9000 | 34.1400 | 47.0200 | 46.4234 | 12 | — |
| Memori | 41.3400 | 20.8000 | — | — | 33.1600 | 49.3800 | — | — | BEAM100K, BEAM10M |
| MemoryLake | 72.4900 | — | — | — | — | — | — | — | LME, BEAM100K, BEAM10M, PersonaMem, HaluMem |
| Backboard.io | 22.4000 | — | — | — | — | — | — | — | LME, BEAM100K, BEAM10M, PersonaMem, HaluMem |

Tenconic's question-count weighted overall score 63.1416 uses unrounded question-level scores. Rounding panel values before aggregation can change the final digits. Published comparison scores retain the source's rounding precision.

<a id="benchmark-details"></a>

## Detailed benchmark comparisons

Tenconic category scores and counts come from its saved question records. Peer category values are rounded upstream reproduced results from the dated snapshot, not a synchronized rerun. System names preserve the original Zep / graphiti-zep naming and deployment route. Detailed scores use 0–100 with two decimal places; ranks use the unrounded values. Deployment describes the memory backend, separately from external answer/judge APIs.

Category comparison snapshot: [OmniMemEval public reproduced results](https://github.com/MemTensor/OmniMemEval/blob/0b1ea8d28aa2d3e03ac4a6aee17b3006a131da7d/docs/user_memory/results.md) (2026-10-08; upstream_reproduced_snapshot; 0-1). Category scores, original backend names, deployment routes, context-token values and BEAM dispersion were transcribed from the same reproduced-results snapshot as public-reference-scores.json. Published Reference Results are excluded. No peer question-level records or BEAM ability scores are supplied by that table.

<a id="detail-locomo"></a>

## LoCoMo categories 1-4 (locomo; binary_judge; n=1540)

| Rank | System | Deployment | Single-Hop (n=841) | Multi-Hop (n=282) | Temporal (n=321) | Open-Domain (n=96) | Overall (0–100) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | MemOS | cloud | 92.51 | 88.65 | 85.05 | 69.79 | 88.83 |
| 2 | **Tenconic** | local/self-hosted | 94.65 | 77.66 | 84.42 | 69.79 | 87.86 |
| 3 | Cognee | cloud | 87.99 | 78.84 | 81.83 | 63.19 | 83.48 |
| 4 | EverOS | cloud | 86.80 | 77.78 | 84.11 | 57.29 | 82.75 |
| 5 | Hindsight | cloud | 88.98 | 78.84 | 73.52 | 58.33 | 81.99 |
| 6 | Mem0 | cloud | 81.09 | 76.12 | 77.15 | 54.17 | 77.68 |
| 7 | Letta | cloud | 87.99 | 76.24 | 53.48 | 63.54 | 77.12 |
| 8 | MemMachine | local/self-hosted | 83.47 | 53.19 | 71.96 | 57.29 | 73.90 |
| 9 | mem9 | cloud | 79.27 | 62.88 | 73.62 | 55.90 | 73.64 |
| 10 | Supermemory | cloud | 75.39 | 77.07 | 67.60 | 66.67 | 73.53 |
| 11 | MemoryLake | cloud | 70.87 | 75.30 | 79.75 | 54.17 | 72.49 |
| 12 | Viking | cloud | 78.04 | 73.29 | 48.81 | 50.00 | 69.33 |
| 13 | Zep | cloud | 65.36 | 68.79 | 55.56 | 63.54 | 63.83 |
| 14 | Memori | cloud | 47.32 | 44.09 | 22.53 | 43.75 | 41.34 |
| 15 | Backboard.io | cloud | 25.09 | 22.34 | 13.40 | 29.17 | 22.40 |

<a id="detail-lme"></a>

## LongMemEval-S cleaned (lme; binary_judge; n=500)

| Rank | System | Deployment | SS-User (n=70) | SS-Asst (n=56) | SS-Pref (n=30) | Temporal Reasoning (n=133) | Multi-Session (n=133) | Knowledge Update (n=78) | Overall (0–100) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | MemOS | cloud | 100.00 | 100.00 | 100.00 | 89.47 | 78.95 | 84.62 | 89.20 |
| 2 | **Tenconic** | local/self-hosted | 98.57 | 100.00 | 96.67 | 85.71 | 72.93 | 87.18 | 86.60 |
| 3 | EverOS | local/self-hosted | 91.43 | 89.29 | 96.67 | 81.95 | 66.17 | 79.49 | 80.40 |
| 4 | graphiti-zep | local/self-hosted | 94.29 | 100.00 | 86.67 | 74.44 | 67.67 | 79.49 | 79.80 |
| 5 | mem9 | cloud | 95.71 | 94.64 | 56.67 | 77.44 | 62.41 | 85.90 | 78.00 |
| 6 | Letta | cloud | 95.71 | 98.21 | 76.67 | 69.42 | 65.41 | 82.05 | 77.67 |
| 7 | Hindsight | local/self-hosted | 82.86 | 14.29 | 96.67 | 82.71 | 71.43 | 78.21 | 72.20 |
| 8 | Supermemory | cloud | 87.14 | 41.07 | 65.56 | 68.42 | 60.15 | 71.37 | 66.07 |
| 9 | MemMachine | local/self-hosted | 75.71 | 96.43 | 83.33 | 55.64 | 39.85 | 75.64 | 63.60 |
| 10 | Viking | cloud | 75.24 | 46.43 | 96.67 | 55.39 | 57.89 | 60.26 | 61.07 |
| 11 | Mem0 | cloud | 8.57 | 85.71 | 96.67 | 51.13 | 50.38 | 79.49 | 56.00 |
| 12 | Cognee | local/self-hosted | 67.14 | 60.71 | 83.33 | 47.37 | 37.59 | 51.28 | 51.80 |
| 13 | Memori | cloud | 84.14 | 1.79 | 23.33 | 3.76 | 18.80 | 6.41 | 20.80 |

No score (unranked): MemoryLake, Backboard.io

<a id="detail-beam100k"></a>

## BEAM 100K (beam100k; beam_nugget_mean; n=400)

| Rank | System | Deployment | Overall ± std (0–100) |
| ---: | --- | --- | ---: |
| 1 | Viking | cloud | 70.76 ± 35.23 |
| 2 | Mem0 | cloud | 70.41 ± 36.36 |
| 3 | Hindsight | local/self-hosted | 70.22 ± 36.44 |
| 4 | **Tenconic** | local/self-hosted | 69.68 ± 36.23 |
| 5 | Letta | cloud | 69.22 ± 36.76 |
| 6 | graphiti-zep | local/self-hosted | 68.70 ± 36.46 |
| 7 | MemOS | cloud | 66.87 ± 37.37 |
| 8 | Supermemory | cloud | 65.98 ± 37.10 |
| 9 | mem9 | cloud | 65.75 ± 38.92 |
| 10 | MemMachine | local/self-hosted | 64.80 ± 37.62 |
| 11 | Cognee | local/self-hosted | 59.30 ± 39.44 |
| 12 | EverOS | local/self-hosted | 58.64 ± 39.36 |

Peer BEAM ability scores were not published in the reproduced snapshot; only Tenconic ability scores are shown below. Peer dispersion is copied as reported; Tenconic uses the population standard deviation of saved question scores. These are not confidence intervals.

| Ability | Questions | Tenconic score (0–100) |
| --- | ---: | ---: |
| Abstention | 40 | 78.75 |
| Contradiction Resolution | 40 | 68.75 |
| Event Ordering | 40 | 28.74 |
| Information Extraction | 40 | 91.25 |
| Instruction Following | 40 | 88.12 |
| Knowledge Update | 40 | 65.00 |
| Multi-Session Reasoning | 40 | 62.74 |
| Preference Following | 40 | 88.75 |
| Summarization | 40 | 69.67 |
| Temporal Reasoning | 40 | 55.00 |

No score (unranked): Memori, MemoryLake, Backboard.io

<a id="detail-beam10m"></a>

## BEAM 10M (beam10m; beam_nugget_mean; n=200)

| Rank | System | Deployment | Overall ± std (0–100) |
| ---: | --- | --- | ---: |
| 1 | Hindsight | local/self-hosted | 59.75 ± 39.63 |
| 2 | Viking | cloud | 58.14 ± 39.57 |
| 3 | mem9 | cloud | 57.30 ± 39.03 |
| 4 | MemOS | cloud | 56.75 ± 39.17 |
| 5 | graphiti-zep | local/self-hosted | 56.11 ± 40.70 |
| 6 | Cognee | local/self-hosted | 56.02 ± 41.33 |
| 7 | **Tenconic** | local/self-hosted | 55.22 ± 40.52 |
| 8 | Supermemory | cloud | 52.49 ± 40.44 |
| 9 | Letta | cloud | 52.30 ± 41.06 |
| 10 | MemMachine | local/self-hosted | 51.90 ± 40.46 |
| 11 | EverOS | local/self-hosted | 47.73 ± 41.66 |
| 12 | Mem0 | cloud | 43.33 ± 41.99 |

Peer BEAM ability scores were not published in the reproduced snapshot; only Tenconic ability scores are shown below. Peer dispersion is copied as reported; Tenconic uses the population standard deviation of saved question scores. These are not confidence intervals.

| Ability | Questions | Tenconic score (0–100) |
| --- | ---: | ---: |
| Abstention | 20 | 75.00 |
| Contradiction Resolution | 20 | 69.38 |
| Event Ordering | 20 | 13.99 |
| Information Extraction | 20 | 58.75 |
| Instruction Following | 20 | 61.25 |
| Knowledge Update | 20 | 63.75 |
| Multi-Session Reasoning | 20 | 20.92 |
| Preference Following | 20 | 72.50 |
| Summarization | 20 | 75.39 |
| Temporal Reasoning | 20 | 41.25 |

No score (unranked): Memori, MemoryLake, Backboard.io

<a id="detail-personamem"></a>

## PersonaMem v2 text 32K (personamem; multiple_choice_saved; n=5000)

| Rank | System | Deployment | Anti-Stereotypical (n=855) | Ask-to-Forget (n=1048) | Health/Medical (n=568) | Neutral (n=858) | Sensitive (n=511) | Stereotypical (n=533) | Therapy (n=627) | Overall (0–100) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | MemOS | cloud | 33.80 | 57.82 | 32.57 | 35.66 | 36.59 | 39.40 | 39.23 | 40.58 |
| 2 | Supermemory | cloud | 42.34 | 31.97 | 42.96 | 42.42 | 30.72 | 49.72 | 40.67 | 39.64 |
| 3 | Hindsight | local/self-hosted | 33.57 | 40.65 | 36.62 | 38.11 | 36.01 | 42.78 | 38.12 | 37.98 |
| 4 | **Tenconic** | local/self-hosted | 28.77 | 50.57 | 31.16 | 33.33 | 33.07 | 34.52 | 39.87 | 36.84 |
| 5 | Mem0 | cloud | 41.40 | 24.33 | 38.38 | 39.28 | 30.72 | 45.78 | 43.54 | 36.76 |
| 6 | EverOS | cloud | 33.57 | 31.49 | 34.68 | 37.76 | 33.27 | 44.47 | 40.19 | 35.94 |
| 7 | Letta | cloud | 31.46 | 38.93 | 32.39 | 34.85 | 27.40 | 39.40 | 39.23 | 35.12 |
| 8 | MemMachine | local/self-hosted | 28.19 | 45.04 | 32.22 | 28.44 | 29.75 | 32.46 | 38.60 | 34.14 |
| 9 | Memori | cloud | 30.18 | 27.48 | 32.39 | 37.53 | 33.46 | 36.77 | 38.12 | 33.16 |
| 10 | graphiti-zep | local/self-hosted | 28.19 | 29.77 | 28.70 | 31.93 | 30.92 | 37.90 | 42.58 | 32.34 |
| 11 | Viking | cloud | 31.58 | 25.38 | 29.23 | 29.49 | 33.66 | 36.59 | 34.77 | 30.80 |
| 12 | mem9 | cloud | 32.28 | 22.90 | 32.57 | 34.50 | 25.05 | 38.27 | 33.33 | 30.76 |
| 13 | Cognee | local/self-hosted | 18.83 | 41.13 | 16.90 | 18.65 | 32.88 | 16.51 | 34.93 | 26.46 |

No score (unranked): MemoryLake, Backboard.io

<a id="detail-halumem"></a>

## HaluMem Medium (halumem; binary_judge; n=3467)

| Rank | System | Deployment | Basic Fact (n=746) | Boundary (n=828) | Conflict (n=769) | Generalization (n=746) | Multi-Hop (n=198) | Dynamic Update (n=180) | Overall (0–100) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | EverOS | local/self-hosted | 87.80 | 88.89 | 89.99 | 90.48 | 86.36 | 80.56 | 88.66 |
| 2 | **Tenconic** | local/self-hosted | 84.99 | 85.14 | 88.56 | 89.68 | 86.36 | 75.56 | 86.41 |
| 3 | Letta | cloud | 85.92 | 83.45 | 85.70 | 90.62 | 84.34 | 71.11 | 85.43 |
| 4 | Hindsight | local/self-hosted | 78.42 | 87.45 | 86.61 | 86.19 | 81.31 | 73.89 | 83.99 |
| 5 | graphiti-zep | local/self-hosted | 69.44 | 89.13 | 88.43 | 84.05 | 79.80 | 62.22 | 81.71 |
| 6 | MemOS | cloud | 69.03 | 91.30 | 86.48 | 83.51 | 74.24 | 55.00 | 80.91 |
| 7 | Viking | cloud | 57.91 | 92.51 | 80.49 | 84.72 | 74.75 | 47.78 | 77.39 |
| 8 | Mem0 | cloud | 56.30 | 91.91 | 74.77 | 78.42 | 68.69 | 42.22 | 73.64 |
| 9 | mem9 | cloud | 54.56 | 94.20 | 68.79 | 80.16 | 70.71 | 38.89 | 72.80 |
| 10 | Cognee | local/self-hosted | 52.41 | 92.51 | 74.64 | 78.28 | 69.70 | 35.56 | 72.60 |
| 11 | Supermemory | cloud | 25.20 | 97.46 | 44.86 | 49.87 | 41.92 | 16.11 | 52.61 |
| 12 | Memori | cloud | 20.91 | 93.24 | 41.35 | 53.35 | 24.24 | 11.11 | 49.38 |
| 13 | MemMachine | local/self-hosted | 20.38 | 97.42 | 34.72 | 45.31 | 26.77 | 11.11 | 47.02 |

No score (unranked): MemoryLake, Backboard.io
