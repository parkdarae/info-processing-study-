# -*- coding: utf-8 -*-
"""2023년 1회 문제 구조 분석"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 항목\n")
print("문제번호 | 문제 내용 (처음 100자)")
print("=" * 120)

for i, q in enumerate(questions, 1):
    q_no = q['q_no']
    text = q['question_text'][:100].replace('\n', ' ')
    print(f"{i:2}. {q_no:4} | {text}")
