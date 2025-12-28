# CISSP PDF 파싱 가이드

## 1. 사전 준비

### 1.1 OCR 텍스트 추출
`CISSP V21.65.pdf` 파일에서 텍스트를 추출하여 `cissp_raw.txt` 파일로 저장합니다.

**권장 OCR 도구:**
- Adobe Acrobat Pro (텍스트 인식 기능)
- ABBYY FineReader
- Google Document AI
- Microsoft Office Lens

### 1.2 이미지 추출
PDF에 포함된 이미지/다이어그램을 `images/cissp/` 폴더에 저장합니다.

**파일 명명 규칙:**
- `Q{문제번호}.png` (예: Q001.png, Q102.png)
- 이미지가 여러 개인 경우: `Q{문제번호}-{순번}.png` (예: Q102-1.png, Q102-2.png)

## 2. PDF 파싱 프로세스

### 2.1 배치 파싱 (50문제씩)
1. OCR 텍스트를 Cursor에게 제공
2. 50문제씩 37회 반복 파싱
3. 각 배치 결과를 `data/items_cissp.jsonl`에 추가

### 2.2 파싱 요청 템플릿
```
다음 텍스트에서 문제 1~50을 파싱해주세요.

[OCR 텍스트 붙여넣기]

출력 형식:
- JSONL 형식 (한 줄에 하나의 JSON 객체)
- 원문 100% 유지 (수정/요약 금지)
```

### 2.3 출력 JSON 포맷
```json
{
  "id": "CISSP001",
  "q_no": "1",
  "question_en": "Which of the following...",
  "question_ko": "",
  "choices_en": {"A": "...", "B": "...", "C": "...", "D": "..."},
  "choices_ko": {"A": "", "B": "", "C": "", "D": ""},
  "answer": ["C"],
  "images": [],
  "type": "multiple_choice",
  "source": "CISSP V21.65.pdf"
}
```

## 3. 필드 설명

| 필드 | 설명 | 예시 |
|------|------|------|
| id | 고유 ID | "CISSP001" |
| q_no | 문제 번호 | "1" |
| question_en | 영어 문제 | "Which of the following..." |
| question_ko | 한국어 문제 (추후 추가) | "" |
| choices_en | 영어 선택지 | {"A": "...", "B": "..."} |
| choices_ko | 한국어 선택지 (추후 추가) | {} |
| answer | 정답 (배열) | ["C"] 또는 ["A", "B"] |
| images | 이미지 파일명 | ["Q001.png"] |
| type | 문제 유형 | "multiple_choice" |
| source | 출처 | "CISSP V21.65.pdf" |

## 4. 파싱 규칙

### 4.1 텍스트 처리
- 줄바꿈으로 잘린 단어는 재결합
- 괄호/특수문자 원문 유지
- 대소문자 원문 유지

### 4.2 선택지 처리
- A., B., C., D. 또는 A), B), C), D) 형식 인식
- 선택지 텍스트 원문 유지

### 4.3 정답 처리
- 단일 정답: `["C"]`
- 복수 정답: `["A", "C"]`
- 대소문자 구분 없이 처리

### 4.4 금지 사항
- ❌ LLM 추론/요약/보정
- ❌ 원문 수정
- ❌ 해설 생성 (원본에 없는 경우)

## 5. 검증 체크리스트

- [ ] 총 문제 수 확인 (1850개)
- [ ] 모든 문제에 정답 존재
- [ ] 선택지 개수 확인 (4~5개)
- [ ] 이미지 파일 매칭 확인
- [ ] 특수문자 깨짐 없음

## 6. 파일 구조

```
info_ver5/
├── data/
│   ├── items_cissp.jsonl      # CISSP 문제 데이터
│   └── cissp_vocabulary.json  # 단어 사전
├── images/
│   └── cissp/                 # CISSP 이미지
│       ├── Q001.png
│       └── ...
├── js/
│   └── cissp-module.js        # CISSP 모듈
├── css/
│   └── cissp-module.css       # CISSP 스타일
└── CISSP V21.65.pdf           # 원본 PDF
```

## 7. 배치 파싱 일정

| 배치 | 문제 범위 | 상태 |
|------|-----------|------|
| 1 | Q1~Q50 | 대기 |
| 2 | Q51~Q100 | 대기 |
| 3 | Q101~Q150 | 대기 |
| ... | ... | ... |
| 37 | Q1801~Q1850 | 대기 |

## 8. 한국어 번역 추가 (선택사항)

파싱 완료 후, 다음 단계로 한국어 번역을 추가할 수 있습니다:

1. `question_en` → `question_ko` 번역
2. `choices_en` → `choices_ko` 번역
3. 전문 용어는 원어 병기

---

**시작하려면:**
1. PDF에서 OCR 텍스트 추출
2. 추출된 텍스트를 Cursor에게 제공
3. "Q1~Q50 파싱해주세요" 요청


