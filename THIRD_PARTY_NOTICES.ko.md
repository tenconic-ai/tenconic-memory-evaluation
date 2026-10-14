[English](THIRD_PARTY_NOTICES.md) | 한국어

# 제3자 자료 및 라이선스 안내

이 공개 패키지의 평가 하네스와 프롬프트 출처는 [MemTensor의 OmniMemEval](https://github.com/MemTensor/OmniMemEval)이다. 그 저장소의 [Apache License 2.0](https://github.com/MemTensor/OmniMemEval/blob/main/LICENSE) 및 NOTICE를 `notices/OmniMemEval-Apache-2.0.txt`, `notices/OmniMemEval-NOTICE.txt`에 동봉한다. **변경 고지(2026-10-10):** 보존된 로컬 하네스에서 필요한 프롬프트 문자열을 선택해 JSON으로 변환하고 출처·범위 메타데이터를 추가했다. 당시 저장된 문자열은 유지했으며 원본 Python 파일 전체를 그대로 배포하는 것은 아니다. 공개 프롬프트 스냅샷의 범위와 변경 고지는 `config/prompt-templates.json`과 [METHODOLOGY.md](METHODOLOGY.ko.md)에 적었다.

평가 자료의 원본 위치와 표시 라이선스는 다음과 같다. 패널별 필드 공개 범위는 [SOURCE_ACCESS.md](SOURCE_ACCESS.ko.md)에 따로 적었다.

| 자료·저작자 출처 | 공식 데이터 위치 | 표시 라이선스 | 동봉된 원본 필드 |
| --- | --- | --- | --- |
| [LoCoMo / Adyasha Maharana 등, snap-research](https://github.com/snap-research/locomo) | [locomo10.json](https://github.com/snap-research/locomo/blob/main/data/locomo10.json) | [CC BY-NC 4.0](https://github.com/snap-research/locomo/blob/main/LICENSE.txt) | 질문·정답 원문 대신 링크와 위치 |
| [LongMemEval / Di Wu 등](https://github.com/xiaowu0162/LongMemEval) | [longmemeval-cleaned](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned) | [MIT](https://github.com/xiaowu0162/LongMemEval/blob/main/LICENSE), Copyright (c) 2024 Di Wu | 500문항 질문·정답 |
| BEAM / Mohammad Tavakoli, Alireza Salemi, Carrie Ye, Mohamed Abdalla, Hamed Zamani, J Ross Mitchell | [100K](https://huggingface.co/datasets/Mohammadta/BEAM), [10M](https://huggingface.co/datasets/Mohammadta/BEAM-10M) | 두 데이터셋 모두 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | 600문항 질문·정답·루브릭 문구 |
| [PersonaMem-v2 / Bowen Jiang 등](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2) | [PersonaMem-v2](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | 4,895문항 질문·정답·선택지; 105문항 링크·위치 |
| [HaluMem / Ding Chen 등, Memtensor Research Group](https://huggingface.co/datasets/IAAR-Shanghai/HaluMem) | [HaluMem-Medium.jsonl](https://huggingface.co/datasets/IAAR-Shanghai/HaluMem/blob/main/HaluMem-Medium.jsonl) | [CC BY-NC-ND 4.0](https://github.com/MemTensor/HaluMem/blob/main/LICENSE.txt) | 질문·정답 원문 대신 링크와 위치 |

LongMemEval의 MIT 라이선스 및 저작권 고지 전문은 `notices/LongMemEval-MIT.txt`에 동봉한다. PersonaMem-v2 데이터 페이지는 CC BY 4.0을 표시하므로 과거 다른 버전의 MIT 표기를 이 데이터에 적용하지 않는다. BEAM의 저장 판정 이유는 평가 결과이며 원본 루브릭과 구분된다.

[PersonaMem-v2 공식 데이터 카드](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2)는 데이터를 LLM으로 생성했고, 민감·개인 정보 형태의 값도 실제 정보 입력 없이 가명화·생성했다고 설명한다. 실제 정보와 우연히 일치할 가능성도 명시한다. 따라서 이 패키지에 남은 해당 벤치마크의 연락처 형태 문구를 실존 인물의 정보나 운영 자격 증명으로 해석하지 않는다. 이 설명은 PersonaMem-v2에 대한 원 제공자의 설명이며 다른 데이터셋 전체에 일반화하지 않는다.

[BEAM 공식 데이터 카드](https://huggingface.co/datasets/Mohammadta/BEAM)와 [원 논문의 2.2절·B.3.2절](https://arxiv.org/html/2510.27246v1)은 대화와 사용자 프로필·계획을 생성해 합성 상호작용을 구성하는 절차를 설명한다. 해당 벤치마크의 임대·상속 시나리오에 나타난 장소 문구는 이 생성 자료의 맥락으로 보존했다. BEAM 답변의 키·암호처럼 보이는 후보는 코드 예제의 자리표시자나 일반적인 로컬 DB 접속 예제였고, 이메일 형식 후보는 HTML 예제였다. 이 분류는 실사용 자격 증명 확인이나 모든 생성 값이 현실과 절대로 일치하지 않는다는 보증이 아니다. LongMemEval의 전화번호 형식 후보는 테마파크 상품의 사업자 연락처 안내 맥락이며, 개인의 비공개 연락처로 확인되지 않았다.

공식 저장소·데이터 카드가 제공한 주요 논문 저자 표기는 다음과 같다.

- **LoCoMo:** Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, Yuwei Fang. *Evaluating Very Long-Term Conversational Memory of LLM Agents* (2024). [논문](https://arxiv.org/abs/2402.17753), [공식 인용 정보](https://github.com/snap-research/locomo/blob/main/README.MD).
- **PersonaMem-v2:** Bowen Jiang, Yuan Yuan, Maohao Shen, Zhuoqun Hao, Zhangchen Xu, Zichen Chen, Ziyi Liu, Anvesh Rao Vijjini, Jiashu He, Hanchao Yu, Radha Poovendran, Gregory Wornell, Lyle Ungar, Dan Roth, Sihao Chen, Camillo Jose Taylor. *PersonaMem-v2: Towards Personalized Intelligence via Learning Implicit User Personas and Agentic Memory* (2025). [논문](https://arxiv.org/abs/2512.06688), [공식 인용 정보](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2).
- **HaluMem:** Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong, Zhiyu Li. *HaluMem: Evaluating Hallucinations in Memory Systems of Agents* (2025). [논문](https://arxiv.org/abs/2511.03506), [공식 인용 정보](https://huggingface.co/datasets/IAAR-Shanghai/HaluMem).

원본 벤치마크 전체를 복제하지 않고 허용 범위의 평가 필드를 선택·발췌해 JSONL로 재배열했다. 공개한 PersonaMem 4,895문항의 선택지는 당시 보존된 순서와 문자열 서식을 유지한다. 나머지 105문항은 원본 벤치마크 문구에 제공자 키·비공개 경로처럼 보이는 패턴이 있어 질문·정답·선택지를 생략하고 공식 원본 링크·CSV 행 위치만 남겼다. 이 105건의 필드 생략은 배포본의 선택·발췌 변경 사항이며 원 저자가 한 수정이 아니다. 실제 사용 가능한 자격 증명이나 실재하는 비공개 경로가 확인되었다는 뜻은 아니다. 모든 5,000문항의 GPT 답변·점수는 유지했다. LoCoMo와 HaluMem은 무조건 공개 금지라는 뜻이 아니다. 사업·제품 목적의 이번 공개에서는 NC 조건이 붙은 두 패널의 원본 질문·정답을 링크와 위치로 대체하고, 원문 표현을 반복할 가능성이 있는 저장 GPT 답변 본문도 두 패널 전체 5,007건에서 제외했다. 문항 ID·원문 위치·저장 판정값은 유지하며 원래 답변은 비공개 원본에 보존한다. `answer_disclosure`는 이 배포 범위를 명시한다. NC는 단순히 유료 판매 여부만의 문제가 아니며 ND가 원문 일부 인용을 언제나 금지한다는 단정도 하지 않는다. 이 제외 조치는 모든 개별 답변에 법적 제한이 있다는 판단이 아니며, 공개본은 제외된 답변의 내용 검토를 지원한다고 주장하지 않는다.

2026-10-10에 위 공식 출처의 라이선스를 확인했다. 포함된 BEAM 벤치마크 유래 자료와 그 발췌·재배열에는 CC BY-SA 4.0을 유지하며, 해당 자료를 수정해 공유할 때도 그 동일조건변경허락 조건을 따라야 한다. PersonaMem 유래 자료는 CC BY 4.0, LongMemEval 유래 자료는 동봉한 MIT 고지를 유지한다. 본 패키지의 선택·발췌와 JSONL 포맷 변경을 원 저자의 변경으로 표현하거나 원 저자가 Tenconic을 보증한다고 표시하지 않는다.

이 문서는 출처와 적용 범위를 표시한다. 패키지 전체나 제품 코드에 새 전역 라이선스를 부여하지 않는다.

**변경 고지 (2026-10-14):** [OmniMemEval 공개 재현 결과](https://github.com/MemTensor/OmniMemEval/blob/0b1ea8d28aa2d3e03ac4a6aee17b3006a131da7d/docs/user_memory/results.md)의 유형별·BEAM 규모별 표를 `config/public-reference-details.json`으로 전사하고, 점수를 0–1 척도로 변환했습니다. 양언어 리더보드에서 별도로 계산한 Tenconic 결과와 함께 재정렬했습니다. 타사의 원 백엔드 이름·배포 방식·반올림된 값은 보존합니다. 이 출처 표의 변환 자료에는 포함된 OmniMemEval Apache 2.0 라이선스와 NOTICE를 적용합니다. 별도 Published Reference/업체 자체 주장 표는 포함하지 않습니다.
