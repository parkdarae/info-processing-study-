# -*- coding: utf-8 -*-
"""샘플 문제 가독성 확인"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 샘플로 몇 개 문제 확인
samples = [
    ('items_2025_round1.jsonl', 'Q004'),
    ('items_2025_round1.jsonl', 'Q008'),
    ('items_2024_round3.jsonl', 'Q013'),
]

print("=" * 80)
print("가독성 확인 - 샘플 문제")
print("=" * 80)

for filename, q_no in samples:
    file_path = Path("data") / filename
    
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    q = next((q for q in questions if q['q_no'] == q_no), None)
    if q:
        print(f"\n📝 {filename} - {q_no}")
        print("-" * 80)
        print(q['question_text'])
        print("-" * 80)
        
        # 줄바꿈 개수 확인
        newline_count = q['question_text'].count('\n')
        double_newline_count = q['question_text'].count('\n\n')
        print(f"줄바꿈 개수: {newline_count}, 이중 줄바꿈: {double_newline_count}")
        
        if '[보기]' in q['question_text']:
            print("✅ [보기] 포함됨")
        else:
            print("⚠️  [보기] 없음")

print("\n[OK] 가독성 확인 완료")


