#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
특수문자가 포함된 답안 찾기
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

def main():
    # 모든 JSONL 파일 검토
    data_dir = Path("data")
    results = []

    for jsonl_file in sorted(data_dir.glob("items_*.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                q = json.loads(line)
                answer_keys = q.get('answer', {}).get('keys', [])
                
                if has_special_symbols(answer_keys):
                    results.append({
                        'file': jsonl_file.name,
                        'q_no': q['q_no'],
                        'answer_keys': answer_keys,
                        'question_preview': q['question_text'][:60]
                    })

    # 결과 출력
    print("=" * 80)
    print(f"특수문자가 포함된 문제: {len(results)}개")
    print("=" * 80)
    print()
    
    for item in results:
        print(f"[{item['file']}] {item['q_no']}")
        print(f"  답안: {item['answer_keys']}")
        print(f"  문제: {item['question_preview']}...")
        print()
    
    if len(results) == 0:
        print("⚠️ 특수문자가 포함된 문제를 찾지 못했습니다.")
        print("   현재 정의된 특수문자: " + ", ".join(SPECIAL_SYMBOLS))

if __name__ == "__main__":
    main()



