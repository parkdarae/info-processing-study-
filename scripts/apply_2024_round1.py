# -*- coding: utf-8 -*-
"""2024년 1회 답안 적용"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 답안 데이터
answers = {
    'Q001': {'keys': ['4'], 'explanation': None},
    'Q002': {'keys': ['151'], 'explanation': None},
    'Q003': {'keys': ['ㄱ', 'ㄴ', 'ㄹ', 'ㄷ'], 'explanation': None},
    'Q004': {'keys': ['GECA'], 'explanation': None},
    'Q005': {'keys': ['192.168.35.72', '129.200.8.249', '192.168.36.249'], 'explanation': None},
    'Q006': {'keys': ['제 3정규형'], 'explanation': None},
    'Q007': {'keys': ['OSPF'], 'explanation': 'Open Shortest Path First'},
    'Q008': {'keys': ['(1) 세타 조인', '(2) 동등 조인', '(3) 자연 조인'], 'explanation': None},
    'Q009': {'keys': ['(1) 6', '(2) 6'], 'explanation': 'LRU와 LFU 페이지 부재 횟수'},
    'Q010': {'keys': ['6', '3', '1', '7', '2'], 'explanation': '실행 순서'},
    'Q011': {'keys': ['9981 and 2795.10'], 'explanation': None},
    'Q012': {'keys': ['Seynaau'], 'explanation': None},
    'Q013': {'keys': ['a', 'b'], 'explanation': 'B 컬럼의 결과값'},
    'Q014': {'keys': ['ㄹ'], 'explanation': '변경 조건/결정 커버리지'},
    'Q015': {'keys': ['ㅅ'], 'explanation': 'Rootkit'},
    'Q016': {'keys': ['9'], 'explanation': None},
    'Q017': {'keys': ['ㅅ'], 'explanation': 'APT'},
    'Q018': {'keys': ['1'], 'explanation': None},
    'Q019': {'keys': ['Nd sc 1'], 'explanation': None},
    'Q020': {'keys': ['Abstract Factory'], 'explanation': None},
}

jsonl_path = 'data/items_2024_round1.jsonl'

try:
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    print(f"[파일 로드] {len(questions)}개 문제")
    
    # 답안 적용
    updated = 0
    for q in questions:
        q_no = q['q_no']
        if q_no in answers:
            q['answer']['keys'] = answers[q_no]['keys']
            q['answer']['raw_text'] = '\n'.join(answers[q_no]['keys'])
            if answers[q_no]['explanation']:
                q['explanation'] = answers[q_no]['explanation']
            updated += 1
            print(f"✓ {q_no}: {' / '.join(answers[q_no]['keys'][:2])}{'...' if len(answers[q_no]['keys']) > 2 else ''}")
    
    # 저장
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"\n[OK] {updated}/{len(questions)}개 답안 적용 완료!")
    
    # 검증
    with_ans = [q for q in questions if q['answer']['keys']]
    print(f"답안 있음: {len(with_ans)}/{len(questions)}개 ({len(with_ans)/len(questions)*100:.1f}%)")

except FileNotFoundError:
    print(f"[ERROR] 파일이 존재하지 않습니다: {jsonl_path}")
    print("먼저 파싱 스크립트를 실행하여 파일을 생성해주세요.")




