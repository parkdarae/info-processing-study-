import json
import re

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
    
    # 2. 코드 패턴 체크 (더 포괄적)
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
        r'[a-zA-Z_]\w*\s*=\s*\d+;',  # 변수 선언
        r'i\+\+',  # 증감 연산자
        r'[a-zA-Z_]\w*\s*\[\s*\d+\s*\]',  # 배열 접근
        r'\}\s*\n\s*\}',  # 중첩된 중괄호
    ]
    
    for pattern in code_patterns:
        if re.search(pattern, question_text, re.IGNORECASE):
            return True
    
    # 3. 다중 줄 들여쓰기 (코드 블록)
    lines = question_text.split('\n')
    indented_count = 0
    for line in lines:
        if line.startswith('  ') or line.startswith('\t'):
            indented_count += 1
    
    if indented_count >= 3:  # 3줄 이상 들여쓰기
        return True
    
    return False

def is_generic_explanation(explanation):
    """범용적인 해설인지 확인"""
    if not explanation or len(explanation) < 50:
        return True
    
    # 범용적 패턴
    generic_phrases = [
        '코드 실행 결과 분석 문제',
        '문제입니다',
        '에 대한 이해를 묻는 문제',
        '대한 설명이다',
    ]
    
    for phrase in generic_phrases:
        if phrase in explanation[:200]:  # 앞부분만 체크
            return True
    
    return False

total_stats = {
    'total_questions': 0,
    'code_questions': 0,
    'generic_explanations': 0,
}

file_stats = []

for filepath in files:
    filename = filepath.split('/')[-1].replace('items_', '').replace('.jsonl', '')
    
    total = 0
    code_count = 0
    generic_count = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                total += 1
                
                explanation = item.get('explanation', '')
                
                if has_code(item):
                    code_count += 1
                    
                    if is_generic_explanation(explanation):
                        generic_count += 1
    
    file_stats.append({
        'file': filename,
        'total': total,
        'code': code_count,
        'generic': generic_count,
    })
    
    total_stats['total_questions'] += total
    total_stats['code_questions'] += code_count
    total_stats['generic_explanations'] += generic_count

# 파일로 저장
with open('scripts/programming_questions_analysis.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_stats': total_stats,
        'file_stats': file_stats,
    }, f, ensure_ascii=False, indent=2)

print("Analysis complete!")

