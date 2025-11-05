# -*- coding: utf-8 -*-
"""2022년 2회 문제 구조 분석"""
import json

with open('data/items_2022_round2.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 항목\n")
print("문제번호 | 문제 내용 (처음 80자)")
print("=" * 100)

for i, q in enumerate(questions, 1):
    q_no = q['q_no']
    text = q['question_text'][:80].replace('\n', ' ')
    print(f"{i:2}. {q_no:4} | {text}")



