"""
PMP 데이터 가독성 개선 스크립트
- 연속 공백 제거
- 문장 끝 정리
- 해설 문단 구분 개선
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import re
from pathlib import Path

jsonl_path = Path(__file__).parent.parent / 'data' / 'items_pmp.jsonl'

questions = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        questions.append(json.loads(line))

print(f"총 {len(questions)}개 문제 가독성 개선 시작\n")

improved_count = 0

for q in questions:
    original_question = q['question']
    original_explanation = q.get('explanation', '')
    
    # 1. 문제 본문 개선
    question = q['question']
    
    # 연속 공백 제거
    question = re.sub(r'\s+', ' ', question)
    
    # 문장 끝 공백 제거
    question = question.strip()
    
    # 괄호 앞뒤 공백 정리
    question = re.sub(r'\s*\(\s*', ' (', question)
    question = re.sub(r'\s*\)\s*', ') ', question)
    question = re.sub(r'\s+', ' ', question).strip()
    
    # 문장 부호 앞뒤 공백 정리
    question = re.sub(r'\s*([.,?!:;])\s*', r'\1 ', question)
    question = re.sub(r'\s+', ' ', question).strip()
    
    # 문장 끝 공백 제거
    if question.endswith(' '):
        question = question.rstrip()
    
    q['question'] = question
    
    # 2. 해설 개선
    if original_explanation and original_explanation != '해설이 없습니다.':
        explanation = original_explanation
        
        # 연속 공백 제거
        explanation = re.sub(r'\s+', ' ', explanation)
        
        # 문장 구분 개선 (마침표 뒤 줄바꿈)
        explanation = re.sub(r'([.!?])\s+([A-Z가-힣①②③④])', r'\1\n\n\2', explanation)
        
        # 번호 항목 앞에 줄바꿈
        explanation = re.sub(r'\s*([1-9])\)\s*', r'\n\n\1) ', explanation)
        explanation = re.sub(r'\s*([①②③④⑤⑥⑦⑧⑨⑩])\s*', r'\n\n\1 ', explanation)
        
        # 중복 줄바꿈 제거
        explanation = re.sub(r'\n{3,}', '\n\n', explanation)
        
        # 앞뒤 공백 제거
        explanation = explanation.strip()
        
        q['explanation'] = explanation
    
    # 3. 선택지 개선
    improved_options = []
    for option in q.get('options', []):
        # 선택지 텍스트 추출
        match = re.match(r'^([A-D])\.\s*(.*)$', option)
        if match:
            letter = match.group(1)
            text = match.group(2)
            
            # 공백 정리
            text = re.sub(r'\s+', ' ', text).strip()
            
            improved_options.append(f'{letter}. {text}')
        else:
            improved_options.append(option)
    
    q['options'] = improved_options
    
    # 변경 여부 확인
    if (q['question'] != original_question or 
        q.get('explanation') != original_explanation):
        improved_count += 1

# 저장
output_path = Path(__file__).parent.parent / 'data' / 'items_pmp_improved.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"[완료] {improved_count}개 문제 개선")
print(f"저장 위치: {output_path}")
print(f"\n개선 내용:")
print(f"  - 연속 공백 제거")
print(f"  - 문장 부호 앞뒤 공백 정리")
print(f"  - 해설 문단 구분 개선")
print(f"  - 선택지 공백 정리")
print(f"\n원본 파일을 교체하려면:")
print(f"  copy data\\items_pmp_improved.jsonl data\\items_pmp.jsonl")

