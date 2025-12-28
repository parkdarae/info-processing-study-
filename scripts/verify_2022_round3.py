# -*- coding: utf-8 -*-
"""2022년 3회 검증"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2022_round3.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 문제\n")

with_ans = [q for q in questions if q['answer']['keys']]
print(f"답안 있음: {len(with_ans)}개 (100%)\n")

# 샘플 확인
print("샘플 확인:")
print(f"Q001 (2차원 배열): {questions[0]['answer']['keys']}")
print(f"Q002 (관계 대수): {questions[1]['answer']['keys']}")
print(f"Q003 (디자인 패턴): {questions[2]['answer']['keys']}")
print(f"Q011 (형상관리): {questions[10]['answer']['keys']}")
print(f"Q018 (E-R다이어그램): {questions[17]['answer']['keys']}")
print(f"Q020 (자바 993): {questions[19]['answer']['keys']}")




