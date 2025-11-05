# 정보처리기사 실기 학습 시스템 v3.0

## 📚 모듈형 학습 시스템

기존 정보처리기사 실기 학습 시스템 v2.0에 **코드-제어문14문제** 모듈이 추가되었습니다.

## 🎯 주요 기능

### 1. 모듈 시스템
- 햄버거 메뉴에서 두 개의 문제집을 선택할 수 있습니다
- 📚 **핵심 키워드130**: 기존 130개 문제
- 💻 **코드-제어문14문제**: 새로 추가된 14개 문제

### 2. 통합된 학습 모드 (각 모듈별로 사용 가능)
- 순차 풀기
- 랜덤 풀기
- 범위 설정
- 오답만 풀기
- 체크한 문제

## 📁 파일 구조

```
info_ver3/
├── index.html                     # 통합 학습 시스템 프론트엔드
├── extract.py                     # 키워드130 추출 스크립트
├── extract_code_control.py        # 코드-제어문14문제 추출 스크립트
├── items.jsonl                    # 키워드130 문제 데이터
├── items_code_control.jsonl       # 코드-제어문14문제 데이터
├── tables.jsonl                   # 키워드130 표 데이터
├── tables_code_control.jsonl      # 코드-제어문14문제 표 데이터
├── images/                        # 키워드130 이미지
├── images_code_control/           # 코드-제어문14문제 이미지 (미추출 상태)
├── requirements.txt
└── README.md
```

## 🚀 사용 방법

### 1. 더미 데이터로 테스트 (현재 상태)
```bash
# Windows
server.bat

# 또는 Python 서버
python -m http.server 8080
```
브라우저에서 http://localhost:8080/index.html 접속

### 2. 실제 PDF 추출 (코드-제어문14문제)
```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 또는 CURSOR_API_KEY 입력

# 추출 실행
python extract_code_control.py
```

## 🔄 모듈 전환 방법

1. 화면 우측 상단의 **햄버거 메뉴(☰)** 클릭
2. **문제집 선택** 섹션에서 원하는 모듈 클릭
   - 📚 핵심 키워드130
   - 💻 코드-제어문14문제
3. 선택한 모듈의 문제가 로드됩니다
4. 각 모듈은 독립적인 학습 통계를 관리합니다

## 📊 각 모듈의 특징

### 키워드130 (keyword130)
- 문제 번호: Q001 ~ Q130
- 범위: 1~130번
- 데이터 파일: items.jsonl, tables.jsonl

### 코드-제어문14문제 (code_control)
- 문제 번호: C001 ~ C014
- 범위: 1~14번
- 데이터 파일: items_code_control.jsonl, tables_code_control.jsonl

## 🔧 새로운 모듈 추가 방법

1. **추출 스크립트 생성**: extract_모듈명.py
2. **데이터 파일 생성**: 
   - items_모듈명.jsonl
   - tables_모듈명.jsonl
3. **index.html 수정**:
   - `moduleConfig` 객체에 새 모듈 추가
   - 햄버거 메뉴에 새 메뉴 아이템 추가

예시:
```javascript
const moduleConfig = {
    'keyword130': { ... },
    'code_control': { ... },
    'new_module': {  // 새 모듈 추가
        title: '새 모듈 제목',
        itemsFile: 'items_new_module.jsonl',
        tablesFile: 'tables_new_module.jsonl',
        maxRange: 50
    }
};
```

## 📝 라이선스
이 프로젝트는 교육 목적으로 제작되었습니다.


