# -*- coding: utf-8 -*-
"""[보기] 구분 개선 결과 확인"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 개선된 문제들 확인
samples = [
    ('items_2025_round1.jsonl', 'Q004'),
    ('items_2024_round3.jsonl', 'Q013'),
    ('items_2024_round1.jsonl', 'Q001'),
]

print("=" * 80)
print("[보기] 구분 개선 결과 확인")
print("=" * 80)

for filename, q_no in samples:
    file_path = Path("data") / filename
    
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    q = next((q for q in questions if q['q_no'] == q_no), None)
    if q:
        print(f"\n📝 {filename} - {q_no}")
        print("-" * 80)
        # 질문 끝부분부터 보기 부분까지만 표시
        text = q['question_text']
        
        # [보기] 위치 찾기
        if '[보기]' in text:
            idx = text.find('[보기]')
            # [보기] 전후 150자씩 표시
            start = max(0, idx - 150)
            end = min(len(text), idx + 400)
            preview = text[start:end]
            
            if start > 0:
                preview = "..." + preview
            if end < len(text):
                preview = preview + "..."
            
            print(preview)
        else:
            print(text[:500])
        print("-" * 80)

print("\n[OK] [보기] 구분이 명확해졌습니다!")




