#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
특수문자 로직 검증 - 최종 확인
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 특수문자 패턴
SPECIAL_SYMBOLS = ['∪', '―', '×', 'π', '▷◁', '∩', '÷', 'Δ']

def has_special_symbols(answer_keys):
    """답안에 특수문자가 포함되어 있는지 확인"""
    if not answer_keys:
        return False
    
    for key in answer_keys:
        for symbol in SPECIAL_SYMBOLS:
            if symbol in str(key):
                return True
    return False

def verify_all_questions():
    """모든 문제의 특수문자 로직 검증"""
    data_dir = Path("data")
    total = 0
    symbol_needed = 0
    symbol_questions = []
    
    for jsonl_file in sorted(data_dir.glob("items_*.jsonl")):
        # 백업 파일 제외
        if 'backup' in jsonl_file.name:
            continue
            
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                q = json.loads(line)
                total += 1
                
                answer_keys = q.get('answer', {}).get('keys', [])
                has_symbols = has_special_symbols(answer_keys)
                
                if has_symbols:
                    symbol_needed += 1
                    symbol_questions.append({
                        'file': jsonl_file.name,
                        'q_no': q['q_no'],
                        'answer': answer_keys
                    })
    
    print("=" * 80)
    print("특수문자 버튼 로직 검증 결과")
    print("=" * 80)
    print()
    print(f"📊 총 문제 수: {total}개")
    print(f"✅ 특수문자 버튼 필요: {symbol_needed}개 ({symbol_needed/total*100:.1f}%)")
    print(f"📝 일반 입력: {total - symbol_needed}개 ({(total - symbol_needed)/total*100:.1f}%)")
    print()
    
    if symbol_needed > 0:
        print("=" * 80)
        print("특수문자 버튼이 표시될 문제:")
        print("=" * 80)
        for item in symbol_questions:
            print(f"[{item['file']}] {item['q_no']}")
            print(f"  답안: {item['answer']}")
        print()
    
    print("=" * 80)
    print("✅ 검증 완료!")
    print("=" * 80)
    print()
    print("💡 동작 예상:")
    print(f"  • {symbol_needed}개 문제: 특수문자 버튼 표시 + readonly 입력창")
    print(f"  • {total - symbol_needed}개 문제: 일반 텍스트 입력창")
    print()

if __name__ == "__main__":
    verify_all_questions()



