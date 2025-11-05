#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
하드코딩된 문제 번호와 실제 답안 내용 불일치 찾기
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
    # 현재 하드코딩된 Q016, Q017 확인
    hardcoded_questions = ['Q016', 'Q017']
    data_dir = Path("data")
    
    print("=" * 80)
    print("하드코딩된 문제 번호 검증")
    print("=" * 80)
    print(f"검사 대상: {', '.join(hardcoded_questions)}")
    print()
    
    found_count = 0
    mismatched_count = 0
    
    for jsonl_file in sorted(data_dir.glob("items_*.jsonl")):
        # 백업 파일은 제외
        if 'backup' in jsonl_file.name:
            continue
            
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                    
                q = json.loads(line)
                if q['q_no'] in hardcoded_questions:
                    found_count += 1
                    answer_keys = q.get('answer', {}).get('keys', [])
                    has_symbols = has_special_symbols(answer_keys)
                    
                    print(f"[{jsonl_file.name}] {q['q_no']}")
                    print(f"  답안: {answer_keys}")
                    print(f"  특수문자 포함? {has_symbols}")
                    
                    if not has_symbols:
                        print(f"  ⚠️  불필요한 특수문자 버튼 표시됨! (하드코딩 오류)")
                        mismatched_count += 1
                    else:
                        print(f"  ✅ 정상 (특수문자 버튼 필요)")
                    print()
    
    print("=" * 80)
    print(f"검사 완료: {found_count}개 문제 발견")
    print(f"오류: {mismatched_count}개 문제에서 불일치")
    print("=" * 80)
    
    if mismatched_count > 0:
        print()
        print("💡 권장사항:")
        print("   하드코딩된 문제 번호 체크를 제거하고")
        print("   실제 답안 내용 기반 동적 판단 로직으로 교체하세요.")

if __name__ == "__main__":
    main()



