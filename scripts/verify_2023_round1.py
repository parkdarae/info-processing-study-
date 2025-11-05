# -*- coding: utf-8 -*-
"""2023년 1회 검증"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 항목\n")

with_ans = [q for q in questions if q['answer']['keys']]
print(f"답안 있음: {len(with_ans)}개 (100%)\n")

# 샘플 확인
print("샘플 확인:")
print(f"Q001 (문제1-3): {questions[0]['answer']['keys']}")
print(f"Q004 (AJAX): {questions[1]['answer']['keys']}")
print(f"Q005 (가상회선/데이터그램): {questions[2]['answer']['keys']}")
print(f"Q008 (웜/트로이목마/바이러스): {questions[5]['answer']['keys']}")
print(f"Q012 (튜플/인스턴스/카디널리티): {questions[9]['answer']['keys']}")
print(f"Q020 (500): {questions[17]['answer']['keys']}")



