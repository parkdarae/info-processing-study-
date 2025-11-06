# 🔧 PMP PDF 파싱 가이드

## 📋 개요
`PMP-2025.07.30.pdf` 파일에서 문제, 답안, 해설을 추출하여 `data/items_pmp.jsonl` 파일로 변환하는 가이드입니다.

---

## 방법 1: Python 스크립트 사용 (권장)

### 1단계: 필수 라이브러리 설치

```bash
pip install pdfplumber
```

### 2단계: 파싱 스크립트 실행

```bash
python scripts/extract_pmp_real.py
```

### 3단계: 결과 확인

- 파일 위치: `data/items_pmp.jsonl`
- 콘솔에서 추출된 문제 수와 라벨 분포 확인

---

## 방법 2: 브라우저 도구 사용 (Python 없을 때)

### 1단계: 추출 도구 열기

브라우저에서 다음 파일을 엽니다:

```
scripts/extract_pmp_text.html
```

### 2단계: PDF 텍스트 복사

1. `PMP-2025.07.30.pdf` 파일을 PDF 뷰어로 열기
2. **Ctrl + A** (전체 선택)
3. **Ctrl + C** (복사)

### 3단계: 파싱 실행

1. 웹 도구의 텍스트 영역에 **Ctrl + V** (붙여넣기)
2. **"문제 추출하기"** 버튼 클릭
3. 추출 결과 확인

### 4단계: 파일 다운로드 및 교체

1. **"JSONL 파일 다운로드"** 버튼 클릭
2. 다운로드된 `items_pmp_extracted.jsonl` 파일을 `data/items_pmp.jsonl`로 이름 변경 및 이동

---

## 📊 파싱 스크립트 기능

### ✅ 자동 추출 항목
- **문제 번호**: 1, 2, 3, ...
- **문제 본문**: 질문 텍스트
- **선택지**: A, B, C, D (4개)
- **정답**: A, B, C, D 중 하나
- **해설**: 정답 설명

### ✅ 자동 라벨링
#### 10개 지식영역 (Knowledge Areas)
- `project_integration` - 통합관리
- `project_scope` - 범위관리
- `project_schedule` - 일정관리
- `project_cost` - 원가관리
- `project_quality` - 품질관리
- `project_resource` - 자원관리
- `project_communication` - 의사소통관리
- `project_risk` - 위험관리
- `project_procurement` - 조달관리
- `project_stakeholder` - 이해관계자관리

#### 5개 프로세스 그룹 (Process Groups)
- `initiating` - 착수
- `planning` - 기획
- `executing` - 실행
- `monitoring` - 감시통제
- `closing` - 종료

### ✅ 이미지 감지 및 제외
다음 키워드가 포함된 문제는 자동으로 제외됩니다:
- figure, diagram, chart, graph, table
- 그림, 도표, 차트, 표, 다이어그램

---

## 📁 출력 형식 (JSONL)

각 문제는 다음 형식으로 저장됩니다:

```json
{
  "id": "PMP001",
  "q_no": "1",
  "question": "프로젝트 관리자가 프로젝트 헌장을 개발할 때...",
  "options": [
    "A. 프로젝트 예산",
    "B. 이해관계자 식별",
    "C. 비즈니스 케이스",
    "D. 프로젝트 일정"
  ],
  "answer": "C",
  "answer_text": "비즈니스 케이스",
  "explanation": "프로젝트 헌장 개발 시 비즈니스 케이스가...",
  "labels": ["project_integration", "initiating"],
  "difficulty": "medium",
  "source": "PMP-2025.07.30.pdf",
  "type": "multiple_choice"
}
```

---

## 🔍 파싱 후 검증

### 자동 검증 항목
- ✅ 문제 수가 적절한지 (50-200개 예상)
- ✅ 모든 문제에 4개 선택지가 있는지
- ✅ 모든 문제에 정답이 있는지
- ✅ 라벨이 적절히 분류되었는지

### 수동 검증 권장
1. 첫 3-5개 문제를 PDF 원본과 비교
2. 정답이 올바르게 추출되었는지 확인
3. 해설이 정확한지 확인
4. 이미지 문제가 제외되었는지 확인

---

## 🐛 문제 해결

### 문제가 추출되지 않을 때
1. PDF 형식 확인 (텍스트 기반인지, 스캔본인지)
2. 문제 번호 패턴 확인 (1. 2. 3. 형식인지)
3. `scripts/extract_pmp_real.py`의 정규표현식 패턴 수정

### 정답이 잘못 추출될 때
1. PDF에서 "정답:" 또는 "Answer:" 키워드 확인
2. 정답 패턴 수정 필요

### 라벨링이 부정확할 때
1. `KNOWLEDGE_AREAS`와 `PROCESS_GROUPS`의 키워드 확장
2. 문제 본문과 해설에서 더 많은 키워드 추출

---

## 📞 지원

파싱 중 문제가 발생하면:
1. 콘솔 출력 메시지 확인
2. 샘플 문제 3-5개를 직접 확인
3. 필요시 파싱 규칙 수정

---

## ✨ 완료 후

파싱이 완료되면:
1. `data/items_pmp.jsonl` 파일 확인
2. Git에 커밋 (사용자 직접 수행)
3. Vercel 배포
4. PMP 모듈에서 실제 데이터로 학습 테스트

---

**마지막 업데이트**: 2025-11-05

