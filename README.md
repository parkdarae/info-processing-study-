# 📚 정보처리기사 실기 학습 시스템 v2.0

keyword130.pdf에서 130개 문제를 추출하여 실전과 동일한 학습 환경을 제공합니다.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

## 🎯 주요 기능

### 1. PDF 추출 시스템
- **문항 추출**: 문제 본문, 선택지, 정답, 해설
- **표 추출**: 표 구조 및 캡션 보존
- **이미지 매칭**: 이미지 파일과 문항 자동 연결
- **검증 시스템**: 100% 정확도 검증

### 2. 학습 모드 (5가지)
- **순차 풀기**: 문제 순서대로 학습
- **랜덤 풀기**: 무작위 순서로 학습
- **범위 설정**: 지정한 범위만 학습
- **오답만 풀기**: 틀린 문제만 반복 학습
- **체크한 문제**: 북마크한 문제만 학습

### 3. 스마트 정답 시스템
- **다양한 입력 형식 지원**: 
  - 숫자: 1/2/3, ①/②/③
  - 한글: ㄱ/ㄴ/ㄷ, ㉠/㉡/㉢ (자음 입력 가능)
  - 영문: a/b/c, A/B/C
- **대소문자 무시**: Agile = agile = AGILE
- **띄어쓰기 무시**: 애자일 = 애 자 일
- **특수문자 무시**: 1-2-3 = 123, 1,2,3 = 123
- **동의어 인식**: 애자일 = Agile
- **복수 정답 지원**: 각 답안마다 별도 입력창 제공
- **키워드 매칭**: 50% 이상 키워드 일치 시 정답 인정

### 4. Admin 페이지
- **추출 리포트**: 품질 점검 결과 시각화
- **문항/표 검수**: PDF 원문과 추출 텍스트 대조
- **검증 결과**: 자동 검증 상세 결과

## 📋 설치 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일에 API 키 입력:
```env
OPENAI_API_KEY=your_openai_api_key_here
# 또는
CURSOR_API_KEY=your_cursor_api_key_here
```

## 🚀 사용 방법

### 빠른 시작 (학습만 하는 경우)
이미 추출된 데이터가 포함되어 있으므로 바로 학습할 수 있습니다!

```bash
# Windows
server.bat

# 또는 Python 서버
python -m http.server 8080
```

브라우저에서 `http://localhost:8080/index.html` 접속

### PDF 재추출 (선택사항)
```bash
python extract.py
```

이 명령어는 다음 파일들을 생성합니다:
- `items.jsonl`: 문항 데이터 (130개 문제)
- `tables.jsonl`: 표 데이터
- `report.json`: 검증 리포트

### Admin 페이지
브라우저에서 `admin.html` 파일을 엽니다.

## 📁 파일 구조

```
info_ver2/
├── keyword130.pdf          # 원본 PDF 파일
├── images/                 # 이미지 파일
│   ├── 14.png
│   ├── 40.png
│   └── ...
├── extract.py              # PDF 추출 스크립트
├── requirements.txt        # Python 의존성
├── .env                    # 환경 변수 (생성 필요)
├── items.jsonl            # 추출된 문항 데이터 (생성됨)
├── tables.jsonl           # 추출된 표 데이터 (생성됨)
├── report.json            # 검증 리포트 (생성됨)
├── index.html             # 학습 시스템 프론트엔드
├── admin.html             # Admin 관리 페이지
└── README.md              # 프로젝트 문서
```

## 🎨 기술 스택

- **Backend**: Python 3.8+, PyPDF2, pdfplumber, OpenAI API
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js
- **Icons**: Font Awesome 6
- **Fonts**: Noto Sans KR
- **Storage**: LocalStorage

## 📊 스키마

### 문항 스키마
```json
{
  "doc_id": "keyword130",
  "page_range": [12, 13],
  "q_no": "Q047",
  "question_text": "원문 그대로",
  "choices": [
    {"key": "1", "raw_key": "ㄱ", "text": "원문"}
  ],
  "answer": {"keys": ["2"], "raw_text": "정답 ②"},
  "explanation": null,
  "table_refs": ["table_3_2"]],
  "image_refs": ["47-표1번.png"],
  "meta": {
    "layout": "two-column",
    "confidence": 1.0
  }
}
```

### 표 스키마
```json
{
  "table_id": "table_3_2",
  "doc_id": "keyword130",
  "page": 61,
  "caption": "원문",
  "header": ["컬럼1", "컬럼2"],
  "rows": [["셀1", "셀2"]],
  "span": [{"r": 0, "c": 0, "rowspan": 1, "colspan": 1}]
}
```

## ✅ 검증 기준

- **실패 = 0**: 금지 패턴, 무결성 검사 통과
- **경고 = 0**: 불확실한 항목 없음
- **100% 정확**: 원문 바이트 등가 보존

## 🔄 재현성

같은 버전으로 재실행 시 동일 결과:
- 온도 0.0
- top_p 0.1
- JSON 모드
- 스키마 고정

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 🤝 기여

버그 리포트나 개선 사항은 이슈로 등록해주세요.

