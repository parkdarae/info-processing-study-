<!-- 66d99e11-3693-4cb7-8e11-45e064630375 c40f4582-4e1b-4b5f-96c4-a0abc695f124 -->
# 기출문제 파싱 스크립트 개선 및 재실행

## 현재 문제점 분석

`data/items_2021_round1.jsonl` 파일 분석 결과:

- Q002가 line 2, 3, 4, 10, 11, 12 등 여러 객체로 분리됨
- 다중 답안 문제(1, 2, 3)를 단일 답안으로만 파싱
- 해설이 `explanation: null`로 누락
- "더보기" 기반 정규식이 복잡한 구조를 처리하지 못함

## 개선 방향

### 1. HTML 구조 개선 (`scripts/crawl_tistory_final.py`)

**파싱 로직 전면 개편:**

- 기존: `더보기` 키워드 기반 정규식 (line 71)
- 개선: DOM 구조 기반 파싱으로 변경
  - `<p>`, `<div>`, `<span>` 태그 순회
  - 문제 번호(`1.`, `2.` 등) 인식
  - 색상 정보로 답안/해설 구분

**다중 답안 처리:**

- 답안 텍스트에서 `1.`, `2.`, `3.` 패턴 감지
- `answer.keys` 배열로 분리 저장
- 예: `["1. 물리적 설계", "2. 개념적 설계", "3. 논리적 설계"]`

**해설 추출:**

- 파란색(`color: blue` 또는 `color: #0000ff`) 텍스트 식별
- `explanation` 필드에 저장
- 예: "DB설계 절차 : 요구사항 분석 > 개념적 설계 > 논리적 설계 > 물리적 설계 > 구현"

**문제 통합:**

- 문제 번호 변경 전까지를 하나의 문제로 그룹화
- 보기, 표, 코드 블록을 `question_text`에 포함
- 하나의 문제 = 하나의 JSON 객체

### 2. 파싱 알고리즘

```python
def extract_questions_improved(self, html, year, round_num, url):
    soup = BeautifulSoup(html, 'html.parser')
    content = find_content_area(soup)
    
    questions = []
    current_q = None
    current_q_num = None
    
    for elem in content.descendants:
        # 문제 번호 감지 (1., 2., 3. 등)
        if is_question_number(elem):
            if current_q:
                questions.append(current_q)
            current_q = initialize_question()
            current_q_num = extract_number(elem)
        
        # 현재 문제 본문 수집
        elif current_q:
            # 초록색 = 답안
            if is_green_text(elem):
                parse_answer(current_q, elem)
            # 파란색 = 해설
            elif is_blue_text(elem):
                current_q['explanation'] = elem.get_text()
            # 일반 텍스트 = 문제
            else:
                current_q['question_text'] += elem.get_text()
    
    return questions
```

### 3. 실행 및 검증

**재파싱 실행:**

```bash
python scripts/crawl_tistory_final.py
```

**검증 항목:**

- 각 회차별 20~21개 문제가 정확히 추출되는지
- Q002의 답안이 3개 배열로 저장되는지
- 해설이 `explanation` 필드에 포함되는지
- 기존 `items.jsonl` 형식과 호환되는지

**출력 파일:**

- `data/items_2021_round1.jsonl` ~ `data/items_2025_round2.jsonl` (9개 파일)
- `data/report_*.json` (검증 리포트)

## 주요 수정 파일

- `scripts/crawl_tistory_final.py`: 파싱 로직 전면 개편
  - `extract_questions()` 메서드 재작성
  - 색상 기반 답안/해설 구분 함수 추가
  - 다중 답안 파싱 함수 추가

### To-dos

- [x] URL 샘플 페이지(https://chobopark.tistory.com/191)의 HTML 구조 분석 및 색상/태그 패턴 파악