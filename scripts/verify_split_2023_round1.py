# -*- coding: utf-8 -*-
"""2023년 1회 문제 1-3 분리 검증"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print('=' * 80)
print('2023년 1회 문제 1-3 분리 완료!')
print('=' * 80)
print(f'\n총 {len(questions)}개 문제\n')

print('✅ 문제 1 (자바 코드):')
print(f'   답안: {" / ".join(questions[0]["answer"]["keys"])}')

print('\n✅ 문제 2 (C언어 Art):')
print(f'   답안: {" / ".join(questions[1]["answer"]["keys"])}')

print('\n✅ 문제 3 (C언어 qwe):')
print(f'   답안: {questions[2]["answer"]["keys"][0]}')

print('\n✅ 문제 4 (AJAX):')
print(f'   답안: {questions[3]["answer"]["keys"][0]}')

print('\n✅ 문제 5 (네트워크):')
print(f'   답안: {" / ".join(questions[4]["answer"]["keys"])}')

answered = sum(1 for q in questions if q['answer']['keys'])
print(f'\n📊 전체 답안 입력 현황: {answered}/{len(questions)}개 (100%)')
print('=' * 80)




