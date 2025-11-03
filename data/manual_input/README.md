# 수동 답안/해설 입력 가이드

## 📋 개요

Selenium 자동 파싱이 어려운 경우, 이 방식을 사용하여 답안과 해설을 수동으로 입력할 수 있습니다.

## 🎯 구성

### 1. CSV 파일 구조

각 회차별로 CSV 파일이 생성되어 있습니다:
- `manual_2021_round1.csv` - 2021년 1회 (22문제)
- `manual_2022_round2.csv` - 2022년 2회 (34문제)
- `manual_2022_round3.csv` - 2022년 3회 (20문제)
- `manual_2023_round2.csv` - 2023년 2회 (20문제)
- `manual_2024_round1.csv` - 2024년 1회 (23문제)
- `manual_2024_round2.csv` - 2024년 2회 (20문제)
- `manual_2024_round3.csv` - 2024년 3회 (19문제)
- `manual_2025_round1.csv` - 2025년 1회 (20문제)
- `manual_2025_round2.csv` - 2025년 2회 (20문제)

### 2. CSV 열 구성

| 열 이름 | 설명 | 예시 |
|--------|------|------|
| 문제번호 | Q001, Q002 등 | `Q002` |
| 문제내용(처음 100자) | 참고용, 수정 불필요 | `다음은 DB 설계 절차에...` |
| 답안1 | 첫 번째 답안 | `1. 물리적 설계` |
| 답안2 | 두 번째 답안 (선택) | `2. 개념적 설계` |
| 답안3 | 세 번째 답안 (선택) | `3. 논리적 설계` |
| 해설 | 문제 해설 (선택) | `DB설계 절차 : 요구사항 분석 > ...` |

## 📝 사용 방법

### Step 1: CSV 파일 열기

```
Excel이나 Google Sheets에서 CSV 파일 열기
예: data/manual_input/manual_2021_round1.csv
```

### Step 2: 답안 입력

**예시 - 2021년 1회 2번 문제:**

| 문제번호 | 문제내용(처음 100자) | 답안1 | 답안2 | 답안3 | 해설 |
|---------|-------------------|------|------|------|------|
| Q002 | 다음은 DB 설계 절차에... | 1. 물리적 설계 | 2. 개념적 설계 | 3. 논리적 설계 | DB설계 절차 : 요구사항 분석 > 개념적 설계 > 논리적 설계 > 물리적 설계 > 구현 |

**주의사항:**
- 답안이 1개인 경우: 답안1만 입력
- 답안이 2개인 경우: 답안1, 답안2 입력
- 답안이 3개 이상인 경우: 답안1, 답안2, 답안3 입력 (3개 이상은 답안1에 모두 입력)
- 해설이 없으면 비워두기

### Step 3: CSV 저장

```
UTF-8 BOM 인코딩으로 저장 (Excel 기본값 사용)
```

### Step 4: JSONL 업데이트

```bash
# 프로젝트 루트에서 실행
python scripts/apply_manual_input.py
```

## ✅ 검증

업데이트 후 `data/items_YYYY_roundN.jsonl` 파일을 확인하여 답안과 해설이 제대로 반영되었는지 확인하세요.

```python
# 검증 예시
import json

with open('data/items_2021_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]
    
    # Q002 확인
    q002 = [q for q in questions if q['q_no'] == 'Q002'][0]
    print(f"답안: {q002['answer']['keys']}")
    print(f"해설: {q002['explanation']}")
```

## 🔄 재실행

답안을 다시 입력하려면:
1. CSV 파일 수정
2. `python scripts/apply_manual_input.py` 재실행

기존 답안이 덮어씌워집니다.

## 📊 진행 상황 확인

```bash
# 답안 입력률 확인
python scripts/check_answer_rate.py
```

## 💡 팁

1. **원본 자료 참고**: https://chobopark.tistory.com/191 등 원본 페이지를 보면서 입력
2. **복사-붙여넣기**: 웹페이지에서 답안을 복사하여 CSV에 붙여넣기
3. **일괄 처리**: 같은 회차는 한 번에 입력하면 효율적
4. **검증**: 입력 후 반드시 index.html에서 실제로 테스트

## 🚀 자동화 옵션 (추후)

추후 웹 UI를 만들어 브라우저에서 직접 입력할 수 있도록 개선 가능:
- 문제를 보면서 답안 입력
- 실시간 미리보기
- 자동 저장


