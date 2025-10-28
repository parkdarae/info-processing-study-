# 📚 정보처리기사 실기 학습 시스템 v3.0

정보처리기사 실기 시험 대비 학습 시스템입니다. 핵심 키워드 130문제와 코드-제어문 14문제를 포함합니다.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

## 🎯 주요 기능

### 1. 모듈형 학습 시스템
- **핵심 키워드 130문제**: 정보처리기사 실기 핵심 개념
- **코드-제어문 14문제**: C, Java, Python 코드 분석 문제
- 햄버거 메뉴에서 문제집 선택 가능

### 2. 학습 모드 (5가지)
- **순차 풀기**: 문제 순서대로 학습
- **랜덤 풀기**: 무작위 순서로 학습
- **범위 설정**: 지정한 범위만 학습
- **오답만 풀기**: 틀린 문제만 반복 학습
- **체크한 문제**: 북마크한 문제만 학습

### 3. 코드 문제 특화 기능
- **정확한 들여쓰기**: PDF와 동일한 코드 구조 보존
- **원형 숫자 표시**: ❶❷❸... 번호로 코드 라인 표시
- **코드 박스 스타일**: 가독성 좋은 회색 배경
- **동영상 해설**: 문제별 YouTube 해설 링크 제공
- **이미지 표**: 변수 추적 표를 이미지로 제공

### 4. 스마트 정답 시스템
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

### 5. 학습 통계 및 관리
- **진도율 표시**: 현재 학습 진행 상황
- **정답률 추적**: 맞은 문제 / 전체 문제
- **오답 노트**: 틀린 문제 자동 저장
- **북마크 기능**: 중요한 문제 표시
- **폰트 크기 조절**: 4단계 (작게/보통/크게/아주 크게)

## 📋 설치 방법

### 방법 1: GitHub Pages (권장)
1. 이 저장소를 Fork합니다
2. Settings > Pages에서 배포 설정
3. `main` 브랜치 선택 후 저장
4. 생성된 URL로 접속

### 방법 2: 로컬 실행
```bash
# 저장소 클론
git clone https://github.com/YOUR_USERNAME/info_ver3.git
cd info_ver3

# 서버 실행 (Windows)
server.bat

# 또는 Python 서버
python -m http.server 8080
```

브라우저에서 `http://localhost:8080/index.html` 접속

## 🚀 사용 방법

### 빠른 시작
1. 브라우저에서 `index.html` 열기
2. 햄버거 메뉴(☰)에서 문제집 선택
   - 핵심 키워드 130문제
   - 코드-제어문 14문제
3. 학습 모드 선택 (순차/랜덤/범위/오답/체크)
4. 문제 풀기 시작!

### 코드 문제 학습 팁
- **해설 보기**: 상세한 코드 설명과 변수 추적 표 제공
- **동영상 설명**: YouTube 아이콘 클릭 시 동영상 해설 시청
- **코드 들여쓰기**: 원형 숫자(❶❷❸)를 참고하여 코드 흐름 파악

## 📁 파일 구조

```
info_ver3/
├── index.html                          # 메인 학습 시스템
├── items.jsonl                         # 핵심 키워드 130문제 데이터
├── tables.jsonl                        # 핵심 키워드 표 데이터
├── items_code_control.jsonl            # 코드-제어문 14문제 데이터
├── tables_code_control.jsonl           # 코드-제어문 표 데이터 (빈 파일)
├── images/                             # 핵심 키워드 이미지
│   ├── 14.png
│   ├── 40.png
│   └── ...
├── images2/                            # 코드-제어문 이미지
│   ├── 1.png                          # 문제 1 변수 추적 표
│   ├── 2-1.png, 2-2.png              # 문제 2 변수 추적 표
│   └── ...
├── README.md                           # 프로젝트 문서
├── requirements.txt                    # Python 의존성 (PDF 추출용)
└── server.bat                          # Windows 서버 실행 스크립트
```

## 🎨 기술 스택

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: LocalStorage (학습 진도, 오답, 북마크 저장)
- **Icons**: Font Awesome 6
- **Fonts**: Noto Sans KR
- **Backend** (선택): Python 3.8+ (PDF 추출 시에만 필요)

## 📊 데이터 스키마

### 핵심 키워드 문항 스키마
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
  "table_refs": ["table_3_2"],
  "image_refs": ["47-표1번.png"],
  "meta": {
    "layout": "two-column",
    "confidence": 1.0
  }
}
```

### 코드-제어문 문항 스키마
```json
{
  "doc_id": "code_control",
  "page_range": [1, 2],
  "q_no": "C001",
  "question_text": "코드 문제 (들여쓰기 보존)",
  "choices": [],
  "answer": {"keys": ["2"], "raw_text": "답 : 2"},
  "explanation": "<pre class=\"code-box\">코드 해설 (들여쓰기 보존)</pre>",
  "table_refs": [],
  "image_refs": [],
  "meta": {
    "layout": "single",
    "confidence": 1.0
  },
  "video_url": "https://youtu.be/..."
}
```

## 🎓 학습 데이터 출처

- **핵심 키워드 130문제**: keyword130.pdf (v1.0.0)
- **코드-제어문 14문제**: 정보처리기사실기_03_코드-제어문14문제.pdf

## ✨ v3.0 주요 업데이트

### 모듈형 구조
- 문제집 선택 기능 추가
- 각 모듈별 독립적인 데이터 파일
- 동적 범위 설정 (130문제 / 14문제)

### 코드 문제 최적화
- PDF와 100% 동일한 코드 들여쓰기
- 원형 숫자(❶❷❸) 표시
- 코드 박스 스타일 (회색 배경, 좌측 보라색 테두리)
- 해설 코드 폰트 크기 증가 (1.3em)
- 줄 간격 최적화 (2.0)

### 동영상 해설
- YouTube 해설 링크 통합
- 동영상이 있는 문제만 버튼 표시
- 새 탭에서 동영상 열기

### 이미지 통합
- 변수 추적 표를 이미지로 제공
- 텍스트 표 제거 및 이미지 대체
- 이미지 간격 최적화

## 🔧 개발자 가이드

### PDF 재추출 (선택사항)
```bash
# 의존성 설치
pip install -r requirements.txt

# 핵심 키워드 추출
python extract.py

# 코드-제어문 추출
python parse_code_control_manual.py
```

### 커스터마이징
- **폰트 크기**: `index.html`의 CSS 섹션에서 `.code-box` 스타일 수정
- **색상 테마**: CSS 변수 수정
- **문제 추가**: JSONL 파일에 새 문제 추가

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 🤝 기여

버그 리포트나 개선 사항은 이슈로 등록해주세요.

## 📞 문의

문제나 질문이 있으시면 GitHub Issues를 이용해주세요.

---

**Made with ❤️ for 정보처리기사 실기 수험생**
