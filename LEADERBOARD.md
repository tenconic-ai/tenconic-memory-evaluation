[Home](README.md) | [Methodology](METHODOLOGY.md) | [Korean](LEADERBOARD.ko.md)

# Public comparison leaderboard

Tenconic scores were recalculated from saved question records. Comparison-system scores come from a rounded snapshot of publicly reproduced results.
Both overall scores combine different 0–1 metrics into composite scores. They are neither an official aggregate accuracy nor a ranking from a new run under identical conditions.
Question-count weighting: Σ(panel question count × panel score) / total included questions. Equal benchmark weighting: (LoCoMo + LongMemEval + BEAM + PersonaMem + HaluMem) / 5.
The BEAM score is (400 × BEAM 100K + 200 × BEAM 10M) / 600. Both methods require scores in all six panels for an overall rank.

Comparison source: [OmniMemEval public reproduced results](https://github.com/MemTensor/OmniMemEval/blob/main/docs/user_memory/results.md) (retrieved 2026-10-08T09:29:05Z; upstream_reproduced_snapshot)

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

## LoCoMo categories 1-4 (locomo; binary_judge; n=1540)

| Rank | System | Score (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | MemOS | 88.8300 | Published table's rounded scores |
| 2 | Tenconic | 87.8571 | Recalculated from saved question records |
| 3 | Cognee | 83.4800 | Published table's rounded scores |
| 4 | EverOS | 82.7500 | Published table's rounded scores |
| 5 | Hindsight | 81.9900 | Published table's rounded scores |
| 6 | Mem0 | 77.6800 | Published table's rounded scores |
| 7 | Letta | 77.1200 | Published table's rounded scores |
| 8 | MemMachine | 73.9000 | Published table's rounded scores |
| 9 | mem9 | 73.6400 | Published table's rounded scores |
| 10 | Supermemory | 73.5300 | Published table's rounded scores |
| 11 | MemoryLake | 72.4900 | Published table's rounded scores |
| 12 | Viking | 69.3300 | Published table's rounded scores |
| 13 | Zep / Graphiti | 63.8300 | Published table's rounded scores |
| 14 | Memori | 41.3400 | Published table's rounded scores |
| 15 | Backboard.io | 22.4000 | Published table's rounded scores |

## LongMemEval-S cleaned (lme; binary_judge; n=500)

| Rank | System | Score (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | MemOS | 89.2000 | Published table's rounded scores |
| 2 | Tenconic | 86.6000 | Recalculated from saved question records |
| 3 | EverOS | 80.4000 | Published table's rounded scores |
| 4 | Zep / Graphiti | 79.8000 | Published table's rounded scores |
| 5 | mem9 | 78.0000 | Published table's rounded scores |
| 6 | Letta | 77.6700 | Published table's rounded scores |
| 7 | Hindsight | 72.2000 | Published table's rounded scores |
| 8 | Supermemory | 66.0700 | Published table's rounded scores |
| 9 | MemMachine | 63.6000 | Published table's rounded scores |
| 10 | Viking | 61.0700 | Published table's rounded scores |
| 11 | Mem0 | 56.0000 | Published table's rounded scores |
| 12 | Cognee | 51.8000 | Published table's rounded scores |
| 13 | Memori | 20.8000 | Published table's rounded scores |

No score (unranked): MemoryLake, Backboard.io

## BEAM 100K (beam100k; beam_nugget_mean; n=400)

| Rank | System | Score (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | Viking | 70.7600 | Published table's rounded scores |
| 2 | Mem0 | 70.4100 | Published table's rounded scores |
| 3 | Hindsight | 70.2200 | Published table's rounded scores |
| 4 | Tenconic | 69.6769 | Recalculated from saved question records |
| 5 | Letta | 69.2200 | Published table's rounded scores |
| 6 | Zep / Graphiti | 68.7000 | Published table's rounded scores |
| 7 | MemOS | 66.8700 | Published table's rounded scores |
| 8 | Supermemory | 65.9800 | Published table's rounded scores |
| 9 | mem9 | 65.7500 | Published table's rounded scores |
| 10 | MemMachine | 64.8000 | Published table's rounded scores |
| 11 | Cognee | 59.3000 | Published table's rounded scores |
| 12 | EverOS | 58.6400 | Published table's rounded scores |

No score (unranked): Memori, MemoryLake, Backboard.io

## BEAM 10M (beam10m; beam_nugget_mean; n=200)

| Rank | System | Score (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | Hindsight | 59.7500 | Published table's rounded scores |
| 2 | Viking | 58.1400 | Published table's rounded scores |
| 3 | mem9 | 57.3000 | Published table's rounded scores |
| 4 | MemOS | 56.7500 | Published table's rounded scores |
| 5 | Zep / Graphiti | 56.1100 | Published table's rounded scores |
| 6 | Cognee | 56.0200 | Published table's rounded scores |
| 7 | Tenconic | 55.2172 | Recalculated from saved question records |
| 8 | Supermemory | 52.4900 | Published table's rounded scores |
| 9 | Letta | 52.3000 | Published table's rounded scores |
| 10 | MemMachine | 51.9000 | Published table's rounded scores |
| 11 | EverOS | 47.7300 | Published table's rounded scores |
| 12 | Mem0 | 43.3300 | Published table's rounded scores |

No score (unranked): Memori, MemoryLake, Backboard.io

## PersonaMem v2 text 32K (personamem; multiple_choice_saved; n=5000)

| Rank | System | Score (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | MemOS | 40.5800 | Published table's rounded scores |
| 2 | Supermemory | 39.6400 | Published table's rounded scores |
| 3 | Hindsight | 37.9800 | Published table's rounded scores |
| 4 | Tenconic | 36.8400 | Recalculated from saved question records |
| 5 | Mem0 | 36.7600 | Published table's rounded scores |
| 6 | EverOS | 35.9400 | Published table's rounded scores |
| 7 | Letta | 35.1200 | Published table's rounded scores |
| 8 | MemMachine | 34.1400 | Published table's rounded scores |
| 9 | Memori | 33.1600 | Published table's rounded scores |
| 10 | Zep / Graphiti | 32.3400 | Published table's rounded scores |
| 11 | Viking | 30.8000 | Published table's rounded scores |
| 12 | mem9 | 30.7600 | Published table's rounded scores |
| 13 | Cognee | 26.4600 | Published table's rounded scores |

No score (unranked): MemoryLake, Backboard.io

## HaluMem Medium (halumem; binary_judge; n=3467)

| Rank | System | Score (0–100) | Score source |
| ---: | --- | ---: | --- |
| 1 | EverOS | 88.6600 | Published table's rounded scores |
| 2 | Tenconic | 86.4148 | Recalculated from saved question records |
| 3 | Letta | 85.4300 | Published table's rounded scores |
| 4 | Hindsight | 83.9900 | Published table's rounded scores |
| 5 | Zep / Graphiti | 81.7100 | Published table's rounded scores |
| 6 | MemOS | 80.9100 | Published table's rounded scores |
| 7 | Viking | 77.3900 | Published table's rounded scores |
| 8 | Mem0 | 73.6400 | Published table's rounded scores |
| 9 | mem9 | 72.8000 | Published table's rounded scores |
| 10 | Cognee | 72.6000 | Published table's rounded scores |
| 11 | Supermemory | 52.6100 | Published table's rounded scores |
| 12 | Memori | 49.3800 | Published table's rounded scores |
| 13 | MemMachine | 47.0200 | Published table's rounded scores |

No score (unranked): MemoryLake, Backboard.io
