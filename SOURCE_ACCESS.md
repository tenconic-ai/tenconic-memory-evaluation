# 원본 질문 접근과 공개 범위

이 배포본의 모든 11,107행에는 `source_url`과 `source_ref`가 있다. [LongMemEval](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned) 500행, [BEAM 100K](https://huggingface.co/datasets/Mohammadta/BEAM) 400행, [BEAM 10M](https://huggingface.co/datasets/Mohammadta/BEAM-10M) 200행, [PersonaMem-v2](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2) 4,895행에는 원본 질문과 정답을 함께 넣었다. 공개 쌍은 합계 5,995행이다. BEAM에는 원본 루브릭·이벤트 문구와 저장 판정 이유가, 공개된 PersonaMem 4,895행에는 당시 보존된 선택지 문자열과 정답 문자가 포함된다.

[LoCoMo](https://github.com/snap-research/locomo/blob/main/data/locomo10.json) 1,540행과 [HaluMem Medium](https://huggingface.co/datasets/IAAR-Shanghai/HaluMem/blob/main/HaluMem-Medium.jsonl) 3,467행에는 질문·정답 원문과 GPT 답변 본문을 제외하고 저장 점수·공식 원본 링크·위치·`answer_disclosure`를 제공한다. 이 두 자료의 5,007행은 표시된 NC 조건과 답변에 원문 표현이 포함될 가능성을 고려해 사업·제품 목적의 배포 범위를 제한했다. 원래 답변은 비공개 원본에 보존했다. 공식 원문 링크에서는 벤치마크 질문을 찾을 수 있으나, 그 링크에 Tenconic의 생성 답변이 있는 것은 아니다. 따라서 두 패널은 저장 점수 재계산은 가능하고 답변 본문 검토는 불가능하다. PersonaMem 105행도 원본 문구에 제공자 키·비공개 경로처럼 보이는 패턴이 있어 질문·정답·선택지를 제외하고 링크·위치로 제공한다. 실제 자격 증명이나 실제 비공개 경로의 존재가 확인되었다는 뜻은 아니다. 따라서 링크·위치로 대체한 행은 총 5,112개다. 저장된 GPT 답변과 정오 점수는 PersonaMem 5,000행 모두 남아 있다. 원본 대화, 검색 문맥, 전체 모델 입력, 데이터셋 증거 내용은 어느 패널에도 동봉하지 않는다.

| 패널 | 공식 원본에서 해당 질문을 찾는 방법 |
| --- | --- |
| `locomo` | `source_url`의 `locomo10.json`에서 `source_ref.conversation_index0`번째 대화를 찾는다. `sample_id`로 대화 ID를 대조한 뒤 `original_qa_index0`번째 `qa`를 본다. `json_pointer`는 `/{conversation_index0}/qa/{original_qa_index0}` 형식이고 `evaluated_qa_index0`은 평가 행의 위치다. |
| `halumem` | `source_url`의 `HaluMem-Medium.jsonl`에서 원본 `uuid`가 공개 행의 `source_ref.user_uuid`와 같은 레코드를 찾는다. 그 레코드의 `sessions`에서 `session_index0`, 이어 `questions`에서 `question_index0`을 사용한다. `json_pointer`는 **해당 JSONL 레코드 내부**의 `/sessions/{session_index0}/questions/{question_index0}` 형식이다. |
| `lme` | `row_index0`과 `question_id`를 함께 써서 cleaned S 원본 행을 대조한다. 공개 행의 `question`과 `reference_answer`도 확인한다. |
| `beam100k`, `beam10m` | 서로 다른 `source_url`에서 `conversation_id`를 찾는다. `question_index0`은 평가 파서가 차원별 질문을 펼친 순서이므로 공개한 `category`와 `question` 문자열을 원본 질문과 함께 대조한다. 100K와 10M을 하나의 원본으로 혼동하지 않는다. |
| `personamem` | `csv_row_index0`으로 당시 text 32K CSV 행을 찾는다. 4,895행의 공개 `choices` 문자열은 저장된 `all_options` 순서와 서식을 보존하고, `reference_answer`는 정답 선택지 문자다. 제한 공개된 105행에는 `source_disclosure`가 있으며 같은 `source_url`과 CSV 행 위치로 원본을 찾는다. 공식 데이터셋 페이지에서 해당 text 32K 자료를 확인한다. |

인덱스는 0부터 시작한다. 이 식별자는 평가 시점의 저장 입력에 대한 주소이며 업스트림 저장소의 불변 리비전이나 원본 파일 무결성 증명이 아니다. 업스트림 자료가 업데이트되면 같은 인덱스에 다른 항목이 올 수 있다. UUID·문항 ID·샘플 ID와 공개 질문 문자열을 함께 대조하고, 맞지 않으면 동일 원본으로 간주하지 않는다. 원본의 다운로드·접근 조건과 라이선스는 각 제공처의 현재 안내를 확인한다. 출처·저작자·표시 라이선스는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)에 정리했다.
