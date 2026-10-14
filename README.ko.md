# Tenconic Memory Evaluation

[English](README.md) | **한국어**

텐코닉 사용자 메모리 시스템의 공개 평가 자료입니다. **5개 벤치마크 계열, 11,107문항**의 채점 기록, 공개 범위에 해당하는 저장 답변, 점수를 다시 계산하는 독립 Python 도구를 제공합니다.

[Tenconic](https://github.com/tenconic-ai)이 관리하는 저장소이며 평가 데이터·문서·계산 스크립트를 담습니다. 텐코닉 제품 구현, 런타임, 모델 가중치와 내부 검색 문맥은 배포하지 않습니다.

[결과·리더보드](LEADERBOARD.ko.md) · [평가 방법](METHODOLOGY.ko.md) · [릴리스 다운로드](https://github.com/tenconic-ai/tenconic-memory-evaluation/releases/latest) · [데이터 라이선스](THIRD_PARTY_NOTICES.ko.md)

## 종합 리더보드

두 표 모두 **6개 패널 점수를 갖춘 12개 시스템**을 **0–100 척도**로 비교합니다. 다른 시스템은 2026년 10월 8일 [OmniMemEval 공개 재현 결과 스냅샷](https://github.com/MemTensor/OmniMemEval/blob/0b1ea8d28aa2d3e03ac4a6aee17b3006a131da7d/docs/user_memory/results.md)을, Tenconic은 이 저장소의 문항별 재계산 결과를 사용합니다. 서로 다른 지표를 결합한 비교용 복합점수이며, 공식 통합 정확도나 동일 조건에서 새로 실행한 대결이 아닙니다.

### 문항 수 가중

각 패널에 평가 문항 수만큼의 비중을 줍니다. 계산식은 `Σ(패널 점수 × 패널 문항 수) / 11,107`입니다.

| 순위 | 시스템 | 종합점수 / 100 |
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

### 5개 벤치마크 균등 가중

LoCoMo·LongMemEval·BEAM·PersonaMem·HaluMem에 각각 **20%**를 줍니다. BEAM은 먼저 `(400 × BEAM 100K + 200 × BEAM 10M) / 600`으로 통합하고, 5개 벤치마크 점수를 평균합니다.

| 순위 | 시스템 | 종합점수 / 100 |
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

종합점수는 소수점 넷째 자리까지 표시합니다. 전체 리더보드의 점수 변화는 표시용 반올림 전에 계산하므로, 표에 표시된 점수끼리 뺀 값과 마지막 자릿수가 다를 수 있습니다.

**두 종합 순위에서 제외:** Memori·MemoryLake·Backboard.io는 패널 점수가 누락되어 있습니다. 누락 점수를 0으로 채우거나 남은 패널에 가중치를 다시 배분하지 않습니다. 다른 시스템의 점수는 원 출처의 반올림 정밀도를 유지합니다. 패널별 순위·정확한 가중치·포함 범위·순위 변동은 [전체 리더보드](LEADERBOARD.ko.md)에 있습니다.

## 벤치마크 세부 항목 비교

[전체 점수표](LEADERBOARD.ko.md#benchmark-details)는 Tenconic과 공개 결과가 있는 모든 비교 시스템의 **LoCoMo 4개·LongMemEval 6개·PersonaMem 7개·HaluMem 6개 유형별 점수**를 함께 제공합니다. 열에는 유형별 문항 수를 표시하고 기존 패널 종합점수 순으로 정렬합니다.

[LoCoMo](LEADERBOARD.ko.md#detail-locomo) · [LongMemEval](LEADERBOARD.ko.md#detail-lme) · [BEAM 100K](LEADERBOARD.ko.md#detail-beam100k) · [BEAM 10M](LEADERBOARD.ko.md#detail-beam10m) · [PersonaMem v2](LEADERBOARD.ko.md#detail-personamem) · [HaluMem](LEADERBOARD.ko.md#detail-halumem)

BEAM은 규모별 타사 비교와 **각 규모에서 Tenconic의 10개 능력 점수**를 제공합니다. 인용한 타사 공개 표에는 BEAM 능력별 점수가 없습니다. 기존 종합 순위와 동일한 10월 8일 스냅샷을 사용하며, 표 추가로 평가 결과가 바뀌지 않습니다. [상세 비교 JSON](config/public-reference-details.json)은 원 출처의 백엔드 이름과 배포 방식을 보존합니다.

## Tenconic 패널별 결과

2026년 10월 6~8일에 시작한 완료 GPT 평가의 저장 결과입니다. 답변 모델은 `gpt-4.1-mini-2025-04-14`, 모델 판정을 사용한 패널의 판정 모델은 `gpt-4o-mini-2024-07-18`입니다. PersonaMem은 판정 모델 없이 객관식 정오로 평가했습니다.

| 평가 범위 | 문항 수 | 지표 | Tenconic 결과 |
| --- | ---: | --- | ---: |
| LoCoMo 범주 1–4 | 1,540 | 모델 판정 정답률 | 87.8571% |
| LongMemEval-S cleaned | 500 | 모델 판정 정답률 | 86.6000% |
| BEAM 100K | 400 | 질문별 nugget score 평균 | 0.696769 |
| BEAM 10M | 200 | 질문별 nugget score 평균 | 0.552172 |
| PersonaMem v2 text 32K | 5,000 | 저장된 객관식 정답률 | 36.8400% |
| HaluMem Medium | 3,467 | 모델 판정 정답률 | 86.4148% |

## 점수 재계산

[최신 릴리스](https://github.com/tenconic-ai/tenconic-memory-evaluation/releases/latest)를 내려받아 풀거나 이 저장소를 복제합니다. **Python 3.10 이상**으로 저장소 루트에서 실행합니다.

```sh
python -B scripts/recompute_scores.py --check
python -B scripts/build_leaderboard.py --markdown --language ko
```

추가 패키지, GPU, 서버, API 키, 네트워크 연결이 필요하지 않습니다. 시스템 명령이 `python3`이면 바꾸어 사용합니다. 저장된 채점 수치를 다시 계산하며, 새 답변 생성·검색 재실행·답변의 의미적 재판정은 수행하지 않습니다.

JSON 출력과 계산기 테스트:

```sh
python -B scripts/recompute_scores.py --check --json
python -B scripts/build_leaderboard.py --json
python -B -m unittest discover -s tests -p "test_*.py" -v
```

잘못된 레코드나 기대 문항 수·점수와의 불일치가 있으면 계산기는 0이 아닌 종료 코드를 반환합니다. 기준 출력은 [recomputed-scores.json](results/recomputed-scores.json)과 [leaderboard.json](results/leaderboard.json)에 있습니다. 리더보드 출력의 기본 언어는 영어입니다.

## 공개 범위

| 자료 | 공개 범위 |
| --- | --- |
| 채점 기록·원문 위치 | 전체 11,107문항 |
| 저장 답변 | LongMemEval·BEAM·PersonaMem 6,100건 |
| 원본 질문·정답 쌍 | 5,995건 |
| 공식 원문 링크로 제공하는 질문 행 | 5,112건 |
| 제외된 답변 본문 | LoCoMo·HaluMem 전체 5,007건 |

LoCoMo·HaluMem은 비상업 라이선스의 적용 범위와 원문 표현의 반복 가능성을 고려하여, 이번 사업 목적 배포에서 질문·정답과 저장 답변 본문을 제외했습니다. 채점 수치는 재계산할 수 있습니다. 제외한 Tenconic 답변 본문은 이 패키지나 업스트림 질문 링크로 검토할 수 없습니다.

PersonaMem 105문항은 원본 벤치마크의 키·비공개 경로 형태 문구 때문에 질문·정답·선택지를 추가로 제외했습니다. 실제 사용 가능한 자격 증명으로 확인했다는 뜻은 아닙니다. PersonaMem 5,000문항의 답변·점수는 모두 수록하되, 답변은 전체 원시 응답이 아닌 당시 파서가 저장한 정규화 선택지입니다. 비공개 원본 기록은 보존합니다. [원문 접근 안내](SOURCE_ACCESS.ko.md)와 [제3자 자료 고지](THIRD_PARTY_NOTICES.ko.md)에 세부 범위와 출처를 적었습니다.

## 문서와 파일

| 안내 | 내용 |
| --- | --- |
| [리더보드](LEADERBOARD.ko.md) | 두 종합 가중 방식, 포함 범위, 6개 패널 순위와 세부 항목 비교표 |
| [평가 방법](METHODOLOGY.ko.md) | 평가 범위·모델·설정·지표 정의·한계 |
| [데이터 구조](DATA_SCHEMA.ko.md) | JSONL 필드, 원문 위치, 제외 메타데이터 |
| [원문 접근](SOURCE_ACCESS.ko.md) | 원본 벤치마크 문항을 찾는 방법 |
| [라이선스](LICENSE.md)·[제3자 자료 고지](THIRD_PARTY_NOTICES.ko.md) | 자료별 권리와 출처 |
| [실험 설정](config/evaluation-settings.json)·[프롬프트](config/prompt-templates.json) | 당시 보존된 설정과 선택된 프롬프트 문자열 |
| [평가 범위](config/suite.json)·[데이터](data/)·[결과](results/) | 포함 패널·문항 기록·계산 결과 |
| [계산 스크립트](scripts/)·[테스트](tests/) | Python 표준 라이브러리 기반 도구와 검사 |

## 해석과 이용 범위

공개한 답변 기록의 검토와 저장 점수의 독립적인 재계산을 지원합니다. 텐코닉 제품 전체나 새로운 종단 간 벤치마크 실행을 재현하지는 않습니다. LoCoMo 범주 5와 6개 주 지표 밖의 보조 지표는 포함하지 않습니다. 최종 문항 누락이 없다는 사실이 과거 실행 중 중단·재시도가 없었다는 뜻은 아닙니다.

GitHub의 **“Source code (zip/tar.gz)”**는 릴리스 태그 시점의 저장소 파일로 자동 생성한 압축본입니다. 여기서는 평가 계산 스크립트와 동봉 파일을 뜻하며, 텐코닉 제품 소스를 공개했다는 뜻이 아닙니다. 별도로 첨부한 ZIP은 정리된 평가 자료 패키지입니다.

저장소 전체에 새 오픈소스 라이선스를 부여하지 않습니다. 제3자 자료는 각 표시 라이선스를 따릅니다([LICENSE.md](LICENSE.md)). 인용 정보는 [CITATION.cff](CITATION.cff), 재현 문제·정정 제안은 [GitHub Issues](https://github.com/tenconic-ai/tenconic-memory-evaluation/issues)와 [기여 안내](CONTRIBUTING.md)를 이용합니다.
