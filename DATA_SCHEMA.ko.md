[English](DATA_SCHEMA.md) | 한국어

# 공개 데이터 구조

모든 경로는 패키지 루트 기준 상대 경로다. `config/suite.json`은 `schema_version: 1`, 여섯 `panels`와 질문 수 가중 `aggregation`을 포함한다. 각 패널은 `id`, `label`, `benchmark_family`, `expected_questions`, `expected_score`, `data_file`을 갖는다. 패널 ID는 `locomo`, `lme`, `beam100k`, `beam10m`, `personamem`, `halumem`이다. `data_file`은 패키지 안의 UTF-8 JSONL 파일을 가리키며, 한 줄이 채점 대상 질문 한 건이다. 패널별 원문 필드 공개 정책은 `config/data-disclosure.json`에도 기록한다.

각 공개 행의 필수 필드는 다음과 같다.

| 필드 | 뜻 |
| --- | --- |
| `record_id` | 패널 안에서 유일한 공개 레코드 ID |
| `benchmark` | `suite.json`의 패널 ID와 일치 |
| `category` | 원본 평가에서 사용한 범주. LoCoMo는 숫자를 문자열로 표기하며 다른 패널은 보존된 범주 문자열 사용 |
| `status` | 공개한 최종 행에서는 `success` |
| `source_url` | 공식 공개 원본의 파일 또는 데이터셋 페이지 주소 |
| `source_ref` | 비어 있지 않은 객체. 보존된 입력에서의 위치 식별자; 외부 원본의 영구 버전 ID는 아님 |
| `answer` 또는 `answer_disclosure` | 아래 공개 정책에 따라 둘 중 하나만 포함 |
| `evaluation` | 아래 표의 채점 형태와 저장 수치 |

`lme`, `beam100k`, `beam10m`, `personamem`의 총 6,100행에는 비어 있지 않은 저장 답변 문자열 `answer`가 있다. `locomo`, `halumem`의 총 5,007행에는 `answer`가 없고 `answer_disclosure`가 있다. 해당 객체는 정확히 `status: "withheld"`, `reason: "dataset_license_scope"`, `source_license`, `preserved_original_outside_package: true`의 네 필드를 가진다. `source_license`는 LoCoMo에서 `CC-BY-NC-4.0`, HaluMem에서 `CC-BY-NC-ND-4.0`이다. 원래 답변은 비공개 원본에 보존했고, 공개 행은 원문 표현 재배포 가능성을 피하기 위한 제외 사실을 표시한다. 저장 판정·점수·문항 위치는 그대로 남아 산술 재계산이 가능하지만 답변 본문 검토는 불가능하다. 계산기는 무표시 누락, 다른 패널의 답변 누락, 잘못된 메타데이터와 답변·제외 표시의 동시 존재를 거부한다.

`lme`, `beam100k`, `beam10m`은 모든 행에, `personamem`은 5,000행 중 4,895행에 원본 질문 문자열 `question`과 원본 정답값 `reference_answer`를 포함한다. 공개한 정답은 문자열 또는 정수일 수 있으므로 타입을 임의로 문자열화하지 않는다. 공개된 PersonaMem 행의 `choices`는 보존된 `all_options` 원문 **문자열**이고 정답 선택지 문자는 `reference_answer`다. 나머지 PersonaMem 105행은 이 세 필드를 모두 생략하고 아래 `source_disclosure`를 포함한다. 모든 PersonaMem 행의 `answer_representation: "saved_normalized_choice"`는 `answer`가 보존된 정규화 선택 결과임을 뜻한다. 전체 원시 모델 응답을 담았다는 표시가 아니다.

PersonaMem의 제한 공개 행에는 `source_disclosure: {"mode":"source_link_only","reason":"sensitive_source_text","omitted_fields":["question","reference_answer","choices"]}`가 있다. 원본 벤치마크 문구에서 제공자 키·비공개 경로처럼 보이는 패턴이 발견되어 해당 세 필드를 함께 제외한 것이다. 이 표시는 실제 자격 증명이나 실제 비공개 경로를 확인했다는 주장이 아니다. 저장 답변, 정오 점수, `source_url`, `source_ref.csv_row_index0`은 계속 제공한다. `config/suite.json`의 `question_reference_coverage`는 패널별 `full`, `partial`, `source_link_only` 중 하나이며 질문·정답 쌍의 공개 건수와 함께 읽는다.

`source_ref`는 패널별로 위치가 다르다. LoCoMo는 `conversation_index0`, `sample_id`, `original_qa_index0`, `evaluated_qa_index0`, `json_pointer`; LongMemEval은 `row_index0`, `question_id`; PersonaMem은 `csv_row_index0`; HaluMem은 `user_uuid`, `session_index0`, `question_index0`, `json_pointer`; BEAM은 `conversation_id`, `question_index0`을 사용한다. `index0`은 0부터 세는 인덱스다. LoCoMo/HaluMem의 5,007행과 PersonaMem의 105행, 총 5,112행은 질문·정답 원문 대신 `source_url`과 이 위치를 제공한다. 업스트림 데이터셋이 바뀌면 위치가 달라질 수 있으므로 [SOURCE_ACCESS.md](SOURCE_ACCESS.ko.md)의 대조 절차를 따른다.

| `evaluation.type` | 공개 필드 | 재계산 |
| --- | --- | --- |
| `binary_judge` | `judgments: [boolean, …]`, `saved_score` | 참 개수 / 판정 개수. LoCoMo, LongMemEval, HaluMem의 저장된 모델 판정 |
| `multiple_choice_saved` | `judgments: [boolean, …]`, `saved_score` | 참 개수 / 결정 개수. PersonaMem의 저장된 객관식 정오 |
| `rubric_mean` | `items: [{item_index, rubric, scores: [0/0.5/1, …], reasons: [string, …], saved_score}, …]`, `saved_score` | 항목별 실행 평균, 이어 항목 평균. BEAM 루브릭 질문 |
| `ordering_tau_b` | `rubric: [원본 이벤트 문자열, …]`, `positions: [[integer, …], …]`, `scores: [number, …]`, `reasons: [string, …]`, `saved_score` | 각 실행의 순서 점수, 이어 실행 평균. `positions`의 각 배열 길이는 `rubric` 길이와 동일 |

`saved_score`는 모든 형태에서 0 이상 1 이하의 유한 수다. `ordering_tau_b`에서 위치 0 이하는 미발견 이벤트이며 양수는 저장된 발견 위치를 뜻한다. 각 `scores` 원소는 대응하는 `positions` 실행의 계산 점수다. BEAM `rubric`은 원본 평가 문구, `reasons`는 저장된 판정 이유다. `binary_judge` 행에는 판정 이유가 없다.

계산기는 항목 점수부터 질문 점수, 범주별 평균과 패널 평균까지 다시 구한다. `--check`는 `expected_score`와 `aggregation.method: "question_count_weighted"`의 전체 11,107문항 점수도 대조한다. 결과 JSON의 `overall.weights`는 패널 문항 비중과 전체점수 기여도, `benchmark_families`는 같은 벤치마크 패널을 묶은 참고값이다. BEAM 두 패널 600문항은 전체 합계에서 중복하지 않는다. `binary_numerator`/`binary_denominator`는 저장된 이진 판정 수를 집계하며, `score_std_population`은 순서 질문이 있는 패널의 **질문 점수 모집단 표준편차**다. 이는 신뢰구간이나 여러 독립 실행 사이의 오차가 아니다.

`config/public-reference-scores.json`의 다른 시스템 점수는 공개 원본의 반올림된 0–1 수치 또는 누락을 나타내는 `null`이다. `scripts/build_leaderboard.py`는 Tenconic의 문항 재계산값과 이 스냅샷을 함께 읽어 `results/leaderboard.json` 및 `LEADERBOARD.ko.md` 형식으로 만든다. 여섯 값이 있는 시스템만 전체 순위를 계산하고 누락값을 0으로 대체하지 않는다. 다른 시스템의 문항별 답변이나 계산 근거가 이 패키지에 있다는 뜻은 아니다. 답변의 수치적 재계산과 원본 질문에 대한 의미적 재채점은 서로 다른 작업이다.

이 배포본의 `results/leaderboard.json`은 기존 `overall_ranked`, `overall_excluded`, `weights`와 `comparison_matrix`의 `overall_score`·`overall_rank`를 **문항 수 가중** 의미로 유지한다. `panel_leaderboards`도 기존 여섯 패널의 순위다. 새 `benchmark_equal_weighted` 객체가 **5개 벤치마크 균등 가중** 결과를 제공한다. JSON의 모든 점수와 가중치는 0–1 척도이고 Markdown 표에서는 100을 곱한다.

| `benchmark_equal_weighted` 필드 | 뜻 |
| --- | --- |
| `method` | `benchmark_equal_weighted` |
| `benchmark_count` | 5 |
| `within_benchmark_aggregation` | `question_count_weighted`: BEAM 내부는 400:200 |
| `missing_policy` | `all_panels_required`: 두 BEAM 범위를 포함한 모든 6개 패널 필요 |
| `weights` | 벤치마크별 `id`, `label`, `panel_ids`, `question_count`, 균등 `weight`, 기존 `question_count_weight` |
| `weights[].panel_weights` | 패널별 `id`, `count`, 벤치마크 내부 비중 `weight_within_benchmark`, 전체 균등 점수의 비중 `effective_weight` |
| `ranked` | 균등 가중 점수 내림차순 시스템 목록 |
| `excluded` | 누락 패널로 두 종합 순위에서 제외된 시스템과 누락·포함 범위 정보 |

`ranked`의 각 행은 `system`, `origin`, 다섯 `benchmark_scores`, 균등 `score`·`rank`, 기존 `question_weighted_score`·`question_weighted_rank`, `rank_change`, `score_change`를 갖는다. `rank_change`는 기존 순위에서 균등 순위를 뺀 값이며 양수는 상승이다. `score_change`는 균등 점수에서 기존 점수를 뺀 0–1 척도 차이다. 같은 계산 점수는 공동 순위를 사용하고 다음 순위를 건너뛴다. 표에 보이는 반올림 값만 같을 때는 공동 순위로 간주하지 않는다.

## 벤치마크 세부 비교

`config/public-reference-details.json`은 고정된 OmniMemEval 공개 재현 결과에서 옮긴 유형별·BEAM 규모별 값입니다. `source`는 출처 URL·스냅샷 날짜·원래 정밀도·0–1 척도·공개 범위를 기록합니다. 6개 `panels`에는 유형 정의(`id`, 영문·국문 `label`)와 타사 `rows`가 있습니다.

| 필드 | 의미 |
| --- | --- |
| `system` | 기존 종합 비교와 연결하는 공통 시스템 이름 |
| `source_system` | `Zep`과 `graphiti-zep` 등을 구별한 원 벤치마크 표의 이름 |
| `deployment` | 출처에 표시된 메모리 백엔드 배포 방식 |
| `score` | 원 표의 패널 종합점수; 기존 `public-reference-scores.json`과 일치하는지 검사 |
| `categories` | 유형 ID별 점수; 타사 BEAM 행은 원 출처에 능력별 값이 없어 모두 `null` |
| `score_std` | BEAM의 출처상 분산 표기(0–1 척도); 다른 패널의 입력에서는 생략 |
| `context_tokens` | 출처의 평균 답변 컨텍스트 토큰; JSON 출처 정보로 보존하고 점수표에는 표시하지 않음 |

생성기는 `results/leaderboard.json`에 `benchmark_details`를 추가합니다. `source`와 6개 `panels` 아래에 유형 정의·문항 수·정렬된 `rows`가 있습니다. Tenconic의 유형별 문항 수·평균은 공개 기록에서 재계산하며 가중평균이 기존 패널 점수와 맞아야 합니다. Tenconic의 `score_std`는 BEAM 문항 점수의 모집단 표준편차이고 다른 패널은 `null`입니다. 공개 문항 스키마에는 토큰 수가 없으므로 Tenconic의 `context_tokens`도 `null`입니다. 타사도 BEAM 외 생성 결과의 `score_std`는 `null`입니다. 각 행에는 `rank`·`origin`이 추가되며 기존 `panel_leaderboards`와 두 종합 순위의 필드·값은 유지합니다.

타사 행은 LoCoMo 14개, LongMemEval·PersonaMem·HaluMem 각각 12개, BEAM 각 규모 11개입니다. 기존 종합 스냅샷에서 해당 패널 점수가 있는 모든 타사를 포함해야 하며 누락을 0으로 채우지 않습니다. 패키지 리비전 7부터 상세 스냅샷은 필수입니다. 영문·국문 리더보드는 같은 결합 결과로 생성합니다. 유형별 평균은 0–100 척도의 소수점 두 자리로 표시하고 JSON은 계산 정밀도를 보존합니다.
