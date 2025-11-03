#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범용적 해설 패턴을 찾아서 개선이 필요한 문제 목록 작성
"""

import json
import sys
import glob
from pathlib import Path

# 한글 출력을 위한 인코딩 설정
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 범용적 해설 패턴
GENERIC_PATTERNS = [
    "이 문제는.*핵심 개념을 이해하는 문제입니다",
    "문제 해석 과정:",
    "문제 해석:.*종합적으로 고려하면",
    "학습 포인트:",
    "해당 개념에 대한 개념을 설명합니다",
    "코드의 실행 과정을 단계별로 설명합니다",
    "이 코드는.*변수의 값 변화를 추적하는 문제입니다",
    "이.*코드 문제는.*변수의 값 변화와 연산 과정을 추적하는 문제입니다",
    "이.*코드 문제는 자료구조와 알고리즘을 다루는 문제입니다",
]

def load_jsonl(file_path):
    """JSONL 파일을 읽어서 리스트로 반환"""
    items = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items

def is_generic(explanation):
    """해설이 범용적인지 확인"""
    if not explanation:
        return True, "해설 없음"
    
    import re
    explanation_lower = explanation.lower()
    
    for pattern in GENERIC_PATTERNS:
        if re.search(pattern, explanation, re.IGNORECASE):
            return True, f"패턴 매칭: {pattern}"
    
    # 해설이 너무 짧거나 구체적이지 않은 경우
    if len(explanation) < 100:
        return True, "해설이 너무 짧음"
    
    # 구체적인 정보가 없는 경우 (예: 문제의 실제 내용을 언급하지 않음)
    if "문제에서 설명" not in explanation and "문제에서 언급" not in explanation:
        if "종합적으로 고려하면" in explanation or "일반적으로" in explanation:
            return True, "구체적 설명 부족"
    
    return False, ""

def main():
    jsonl_files = glob.glob('data/items_*.jsonl')
    jsonl_files = [f for f in jsonl_files if 'backup' not in f and 'all' not in f]
    
    generic_questions = []
    
    for file_path in sorted(jsonl_files):
        items = load_jsonl(file_path)
        file_name = Path(file_path).stem
        
        for item in items:
            q_no = item.get('q_no', '')
            explanation = item.get('explanation', '')
            is_gen, reason = is_generic(explanation)
            
            if is_gen:
                expl_preview = ''
                if explanation:
                    expl_preview = explanation[:100] + '...' if len(explanation) > 100 else explanation
                else:
                    expl_preview = '(해설 없음)'
                
                generic_questions.append({
                    'file': file_name,
                    'q_no': q_no,
                    'reason': reason,
                    'explanation_preview': expl_preview
                })
    
    # 결과 출력
    print(f"총 {len(generic_questions)}개의 범용적 해설 발견\n")
    print("=" * 80)
    
    # 파일별로 그룹화
    by_file = {}
    for q in generic_questions:
        file_name = q['file']
        if file_name not in by_file:
            by_file[file_name] = []
        by_file[file_name].append(q)
    
    for file_name in sorted(by_file.keys()):
        print(f"\n{file_name}: {len(by_file[file_name])}개")
        for q in by_file[file_name]:
            print(f"  - {q['q_no']}: {q['reason']}")
            print(f"    해설 미리보기: {q['explanation_preview']}")
    
    # CSV로 저장
    import csv
    csv_path = 'data/generic_explanations_list.csv'
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'q_no', 'reason', 'explanation_preview'])
        writer.writeheader()
        writer.writerows(generic_questions)
    
    print(f"\n\n결과를 CSV 파일로 저장: {csv_path}")
    print(f"총 {len(generic_questions)}개 문제가 개선이 필요합니다.")

if __name__ == '__main__':
    main()

