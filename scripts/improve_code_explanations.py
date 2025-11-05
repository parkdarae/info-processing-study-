import json
import re
import os
from datetime import datetime

files = [
    'data/items_2021_round1.jsonl',
    'data/items_2022_round1.jsonl',
    'data/items_2022_round2.jsonl',
    'data/items_2022_round3.jsonl',
    'data/items_2023_round1.jsonl',
    'data/items_2023_round2.jsonl',
    'data/items_2023_round3.jsonl',
    'data/items_2024_round1.jsonl',
    'data/items_2024_round2.jsonl',
    'data/items_2024_round3.jsonl',
    'data/items_2025_round1.jsonl',
    'data/items_2025_round2.jsonl',
]

def has_code(item):
    """문제에 코드가 포함되어 있는지 확인"""
    question_text = item.get('question_text', '')
    
    if not question_text:
        return False
    
    # 1. code_blocks 필드 확인
    if item.get('code_blocks') and len(item.get('code_blocks', [])) > 0:
        return True
    
    # 2. 코드 패턴 체크
    code_patterns = [
        r'public\s+class',
        r'public\s+static\s+void\s+main',
        r'def\s+\w+\s*\(',
        r'function\s+\w+',
        r'for\s*\([^)]*\)\s*\{',
        r'while\s*\([^)]*\)\s*\{',
        r'if\s*\([^)]*\)\s*\{',
        r'#include\s*<',
        r'int\s+main\s*\(',
        r'System\.out\.print',
        r'printf\s*\(',
        r'cout\s*<<',
        r'Console\.WriteLine',
        r'print\s*\(',
        r'[a-zA-Z_]\w*\s*=\s*\d+;',
        r'i\+\+',
        r'[a-zA-Z_]\w*\s*\[\s*\d+\s*\]',
        r'\}\s*\n\s*\}',
    ]
    
    for pattern in code_patterns:
        if re.search(pattern, question_text, re.IGNORECASE):
            return True
    
    # 3. 다중 줄 들여쓰기
    lines = question_text.split('\n')
    indented_count = 0
    for line in lines:
        if line.startswith('  ') or line.startswith('\t'):
            indented_count += 1
    
    if indented_count >= 3:
        return True
    
    return False

def is_generic_explanation(explanation):
    """범용적인 해설인지 확인 (개선 필요)"""
    if not explanation or len(explanation) < 50:
        return True
    
    # 좋은 해설의 특징
    good_patterns = [
        r'\[1단계\]|\[2단계\]|\[3단계\]',  # 단계별 분석
        r'i=\d+:',  # iteration 추적
        r'→',  # 화살표로 변화 추적
        r'실행 과정|단계별|추적',  # 명시적 추적
        r'\d+\.\s*\[',  # 번호와 대괄호 조합
    ]
    
    has_good_pattern = False
    for pattern in good_patterns:
        if re.search(pattern, explanation[:500]):  # 앞부분만 체크
            has_good_pattern = True
            break
    
    if has_good_pattern:
        return False  # 이미 좋은 해설
    
    # 범용적 패턴
    generic_phrases = [
        '코드 실행 결과 분석 문제입니다',
        '에 대한 이해를 묻는 문제입니다',
        '문제입니다.\n\n[코드 분석]',
    ]
    
    for phrase in generic_phrases:
        if phrase in explanation[:300]:
            return True
    
    # 해설이 너무 짧은 경우
    if len(explanation) < 200:
        return True
    
    return False

def identify_needs_improvement():
    """개선이 필요한 문제들 식별"""
    needs_improvement = []
    
    for filepath in files:
        filename = filepath.split('/')[-1].replace('items_', '').replace('.jsonl', '')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    item = json.loads(line)
                    
                    if has_code(item):
                        explanation = item.get('explanation', '')
                        
                        if is_generic_explanation(explanation):
                            needs_improvement.append({
                                'file': filepath,
                                'filename': filename,
                                'line_num': line_num,
                                'q_no': item.get('q_no', ''),
                                'question_text': item.get('question_text', '')[:200] + '...',
                                'explanation_length': len(explanation),
                                'code_blocks': len(item.get('code_blocks', [])),
                            })
    
    return needs_improvement

def save_improvement_list(needs_improvement):
    """개선 필요 목록 저장"""
    output = {
        'total': len(needs_improvement),
        'timestamp': datetime.now().isoformat(),
        'items': needs_improvement
    }
    
    with open('scripts/needs_improvement.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 파일별로 그룹화
    by_file = {}
    for item in needs_improvement:
        filename = item['filename']
        if filename not in by_file:
            by_file[filename] = []
        by_file[filename].append(item['q_no'])
    
    print(f"Total problems needing improvement: {len(needs_improvement)}")
    print("\nBy file:")
    for filename, q_nos in sorted(by_file.items()):
        print(f"  {filename}: {len(q_nos)} problems - {', '.join(q_nos)}")

if __name__ == '__main__':
    needs_improvement = identify_needs_improvement()
    save_improvement_list(needs_improvement)

