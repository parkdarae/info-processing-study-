# -*- coding: utf-8 -*-
"""2023년 1회 문제 및 답안 출력"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print("=" * 100)
print("2023년 1회 정보처리기사 실기 문제 및 답안")
print("=" * 100)
print()

for i, q in enumerate(questions, 1):
    # 실제 문제 번호 매핑
    if i == 1:
        actual_no = "1~3"
    else:
        actual_no = str(i + 2)
    
    print(f"[문제 {actual_no}]")
    print(f"{q['question_text'][:150]}...")
    print()
    print(f"답안: {', '.join(q['answer']['keys']) if q['answer']['keys'] else '(답안 없음)'}")
    print()
    print("-" * 100)
    print()


