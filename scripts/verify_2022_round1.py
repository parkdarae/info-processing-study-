# -*- coding: utf-8 -*-
"""2022년 1회 검증"""
import json

with open('data/items_2022_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 문제")
with_ans = [q for q in questions if q['answer']['keys']]
print(f"답안 있음: {len(with_ans)}개")
with_exp = [q for q in questions if q.get('explanation')]
print(f"해설 있음: {len(with_exp)}개")

# Q001, Q002 확인
q001 = [q for q in questions if q['q_no'] == 'Q001'][0]
print(f"\nQ001 (RAID 0)")
print(f"  답안: {q001['answer']['keys']}")

q002 = [q for q in questions if q['q_no'] == 'Q002'][0]
print(f"\nQ002 (redo/undo)")
print(f"  답안: {q002['answer']['keys']}")

q005 = [q for q in questions if q['q_no'] == 'Q005'][0]
print(f"\nQ005 (삭제 이상)")
print(f"  답안: {q005['answer']['keys']}")
print(f"  해설: {q005.get('explanation', '없음')}")

q020 = [q for q in questions if q['q_no'] == 'Q020'][0]
print(f"\nQ020 (테스트 단계)")
print(f"  답안: {q020['answer']['keys']}")




