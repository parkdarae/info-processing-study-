# -*- coding: utf-8 -*-
"""[보기] 수동 추가 (특정 문제들)"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 수동으로 수정할 문제들
fixes = [
    {
        'file': 'items_2025_round1.jsonl',
        'q_no': 'Q008',
        'insert_before': 'ㄱ. domain',
        'insert_text': '\n[보기]\n\n'
    },
    {
        'file': 'items_2024_round3.jsonl',
        'q_no': 'Q013',
        'insert_before': 'ㄱ. 조건',
        'insert_text': '\n[보기]\n\n'
    },
]

print("특정 문제들에 [보기] 수동 추가...\n")

for fix in fixes:
    file_path = Path("data") / fix['file']
    
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    q = next((q for q in questions if q['q_no'] == fix['q_no']), None)
    
    if q:
        original = q['question_text']
        
        if fix['insert_before'] in original and '[보기]' not in original:
            # insert_before 바로 앞에 insert_text 삽입
            updated = original.replace(
                fix['insert_before'],
                fix['insert_text'] + fix['insert_before']
            )
            
            q['question_text'] = updated
            
            print(f"✓ {fix['file']} - {fix['q_no']}")
            print(f"  변경 전 길이: {len(original)}")
            print(f"  변경 후 길이: {len(updated)}")
            
            # 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                for question in questions:
                    f.write(json.dumps(question, ensure_ascii=False) + '\n')
        else:
            if '[보기]' in original:
                print(f"  {fix['file']} - {fix['q_no']}: 이미 [보기] 있음")
            else:
                print(f"⚠️  {fix['file']} - {fix['q_no']}: insert_before 문자열 못 찾음")
    else:
        print(f"❌ {fix['file']} - {fix['q_no']}: 문제 없음")

print(f"\n[OK] 수동 수정 완료!")



