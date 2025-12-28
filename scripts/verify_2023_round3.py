# -*- coding: utf-8 -*-
"""2023년 3회 검증"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round3.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 항목\n")

with_ans = [q for q in questions if q['answer']['keys']]
without_ans = [q for q in questions if not q['answer']['keys']]

print(f"답안 있음: {len(with_ans)}개")
print(f"답안 없음: {len(without_ans)}개\n")

if without_ans:
    print("답안 없는 문제:")
    for q in without_ans:
        text = q['question_text'][:60].replace('\n', ' ')
        print(f"  - {q['q_no']}: {text}...")

# 샘플 확인
print("\n샘플 확인:")
print(f"Q001 (Java): {questions[0]['answer']['keys']}")
print(f"Q003 (chmod): {questions[2]['answer']['keys']}")
print(f"Q010 (포인터): {questions[9]['answer']['keys']}")
print(f"Q017 (클라우드): {questions[16]['answer']['keys']}")
print(f"Q020 (참조무결성): {questions[19]['answer']['keys']}")




