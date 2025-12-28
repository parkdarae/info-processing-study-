# -*- coding: utf-8 -*-
"""[보기] 없는 문제들에 [보기] 추가"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def needs_choices_marker(text):
    """[보기]가 필요한지 확인"""
    # 이미 [보기]가 있으면 필요없음
    if '[보기]' in text or '보기\n\n' in text:
        return False
    
    # ㄱ. ㄴ. ㄷ. 같은 선택지가 있는데 [보기]가 없으면 필요
    if re.search(r'\nㄱ\.', text) or re.search(r'\n①', text):
        # 하지만 답안 번호 (1), (2), (3) 같은 경우는 제외
        if not re.search(r'\([ ]*\d[ ]*\)', text):
            return True
    
    return False

def add_choices_marker(text):
    """선택지 앞에 [보기] 추가"""
    if not needs_choices_marker(text):
        return text
    
    # ㄱ. 앞에 [보기] 추가
    if re.search(r'\nㄱ\.', text):
        # 마지막 작성하시오 또는 문장 끝 찾기
        # "작성하시오.\n\nㄱ." -> "작성하시오.\n\n[보기]\n\nㄱ."
        text = re.sub(
            r'(작성하시오|쓰시오|골라)\s*\.\s*\n+(\s*ㄱ\.)',
            r'\1.\n\n[보기]\n\n\2',
            text,
            count=1
        )
        
        # 여전히 [보기]가 없으면 다른 패턴 시도
        if '[보기]' not in text:
            # 일반 문장 끝 + ㄱ.
            text = re.sub(
                r'([가-힣])\s*\.\s*\n+(\s*ㄱ\.)',
                r'\1.\n\n[보기]\n\n\2',
                text,
                count=1
            )
    
    return text

# 모든 JSONL 파일 처리
data_dir = Path("data")
jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))

total_fixed = 0

print(f"총 {len(jsonl_files)}개 파일에서 [보기] 누락 확인...\n")

for jsonl_path in jsonl_files:
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    fixed_count = 0
    fixed_questions = []
    
    for q in questions:
        original = q['question_text']
        fixed = add_choices_marker(original)
        
        if original != fixed:
            q['question_text'] = fixed
            fixed_count += 1
            fixed_questions.append(q['q_no'])
    
    if fixed_count > 0:
        # 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"✓ {jsonl_path.name}: {fixed_count}개 수정 ({', '.join(fixed_questions)})")
        total_fixed += fixed_count
    else:
        print(f"  {jsonl_path.name}: 변경 없음")

print(f"\n[OK] 총 {total_fixed}개 문제에 [보기] 추가!")




