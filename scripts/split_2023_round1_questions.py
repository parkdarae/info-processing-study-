# -*- coding: utf-8 -*-
"""2023년 1회 문제 1-3 분리"""
import json
from pathlib import Path

# JSONL 파일 읽기
jsonl_path = Path("data/items_2023_round1.jsonl")
with open(jsonl_path, 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

# 새로운 문제 리스트 생성
new_questions = []

# 첫 번째 항목(Q001)을 3개로 분리
q001 = questions[0].copy()

# 문제 1: 자바 코드
q1 = q001.copy()
q1['q_no'] = 'Q001'
q1['question_text'] = '아래 자바 코드에서 출력되는 값을 작성하시오.'
q1['answer']['keys'] = ['10', '11', '10', '20']
q1['answer']['raw_text'] = '10\n11\n10\n20'
q1['meta']['confidence'] = 1.0
q1['meta']['warnings'] = []
new_questions.append(q1)

# 문제 2: C언어 Art
q2 = q001.copy()
q2['q_no'] = 'Q002'
q2['question_text'] = '다음 C언어의 출력값을 작성하시오.'
q2['answer']['keys'] = ['Art', 'A', 'A', 'Art', 'Art']
q2['answer']['raw_text'] = 'Art\nA\nA\nArt\nArt'
q2['meta']['confidence'] = 1.0
q2['meta']['warnings'] = []
new_questions.append(q2)

# 문제 3: C언어 qwe
q3 = q001.copy()
q3['q_no'] = 'Q003'
q3['question_text'] = '다음 C언어의 출력값을 작성하시오.'
q3['answer']['keys'] = ['qwe']
q3['answer']['raw_text'] = 'qwe'
q3['meta']['confidence'] = 1.0
q3['meta']['warnings'] = []
new_questions.append(q3)

# 나머지 문제들 추가 (Q004~Q020)
for q in questions[1:]:
    new_questions.append(q)

# JSONL 파일 저장
with open(jsonl_path, 'w', encoding='utf-8') as f:
    for q in new_questions:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"[OK] 문제 분리 완료!")
print(f"  - 기존: {len(questions)}개 항목")
print(f"  - 신규: {len(new_questions)}개 항목")
print(f"  - Q001: 자바 코드 (10, 11, 10, 20)")
print(f"  - Q002: C언어 Art")
print(f"  - Q003: C언어 qwe")
print(f"  - Q004~Q020: 기존 유지")



