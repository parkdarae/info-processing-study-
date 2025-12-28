# -*- coding: utf-8 -*-
"""2023년 3회 문제 및 답안 출력"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round3.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print("=" * 100)
print("2023년 3회 정보처리기사 실기 문제 및 답안")
print("=" * 100)
print(f"\n총 {len(questions)}개 항목\n")

for i, q in enumerate(questions, 1):
    print(f"[문제 {i}] {q['q_no']}")
    
    # 문제 텍스트 (너무 길면 150자로 제한)
    question_text = q['question_text']
    if len(question_text) > 200:
        question_text = question_text[:200] + "..."
    print(f"문제: {question_text}")
    
    # 답안
    if q['answer']['keys']:
        answer_text = ' / '.join(q['answer']['keys'])
        print(f"✅ 답안: {answer_text}")
    else:
        print(f"❌ 답안: (없음)")
    
    # 해설
    if q.get('explanation'):
        print(f"💡 해설: {q['explanation']}")
    
    print("-" * 100)
    print()




