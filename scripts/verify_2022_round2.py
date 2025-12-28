# -*- coding: utf-8 -*-
"""2022년 2회 검증"""
import json

with open('data/items_2022_round2.jsonl', 'r', encoding='utf-8') as f:
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
print("\n\n샘플 확인:")
print(f"Q001 (관계해석): {questions[0]['answer']['keys']}")
print(f"Q001 (IDEA, 행3): {questions[2]['answer']['keys']}")
print(f"Q002 (SKIPJACK, 행4): {questions[3]['answer']['keys']}")
print(f"Q009 (IP주소): {questions[10]['answer']['keys']}")
print(f"Q001 (베타, 행13): {questions[12]['answer']['keys']}")
print(f"Q012 (TTL): {questions[15]['answer']['keys']}")




