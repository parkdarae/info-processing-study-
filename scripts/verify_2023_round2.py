# -*- coding: utf-8 -*-
"""2023년 2회 검증"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round2.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"총 {len(questions)}개 문제\n")

with_ans = [q for q in questions if q['answer']['keys']]
print(f"답안 있음: {len(with_ans)}개 (100%)\n")

# 샘플 확인
print("샘플 확인:")
print(f"Q001 (C언어 배열): {questions[0]['answer']['keys']}")
print(f"Q002 (Java 화폐): {questions[1]['answer']['keys']}")
print(f"Q008 (템퍼프루핑): {questions[7]['answer']['keys']}")
print(f"Q010 (DB설계): {questions[9]['answer']['keys']}")
print(f"Q015 (암호화): {questions[14]['answer']['keys']}")
print(f"Q020 (스텁/드라이버): {questions[19]['answer']['keys']}")



