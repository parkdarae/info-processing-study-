# -*- coding: utf-8 -*-
"""2023년 3회 최종 확인"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round3.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print("=" * 80)
print("2023년 3회 최종 검증")
print("=" * 80)
print()

print("수정된 답안 확인:")
print(f"문제 6 (UNION): {questions[5]['answer']['keys']}")
print(f"문제 10 (포인터): {questions[9]['answer']['keys']}")
print(f"문제 19 (관계대수): {questions[18]['answer']['keys']}")
print(f"항목 21 (select): {questions[20]['answer']['keys']}")
print(f"항목 22 (division): {questions[21]['answer']['keys']}")
print(f"항목 23 (참조무결성): {questions[22]['answer']['keys']}")
print()

with_ans = [q for q in questions if q['answer']['keys']]
without_ans = [q for q in questions if not q['answer']['keys']]

print(f"총 {len(questions)}개 항목")
print(f"답안 있음: {len(with_ans)}개")
print(f"답안 없음: {len(without_ans)}개")
print()

if without_ans:
    print("답안 없는 항목:")
    for q in without_ans:
        print(f"  - {q['q_no']}: {q['question_text'][:50]}...")




