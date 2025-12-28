# -*- coding: utf-8 -*-
"""2024년 2회 답안 적용"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 답안 데이터
answers = {
    'Q001': {'keys': ['NNN'], 'explanation': None},
    'Q002': {'keys': ['반정규화'], 'explanation': None},
    'Q003': {'keys': ['① VALUES', '② SELECT', '③ FROM', '④ SET'], 'explanation': None},
    'Q004': {'keys': ['① 5', '② 4'], 'explanation': 'Cardinality와 Degree'},
    'Q005': {'keys': ['IPSec'], 'explanation': None},
    'Q006': {'keys': ['ab3ca3'], 'explanation': None},
    'Q007': {'keys': ['AES'], 'explanation': None},
    'Q008': {'keys': ['① 가상회선', '② 데이터그램'], 'explanation': None},
    'Q009': {'keys': ['ㅂ'], 'explanation': '순차적(sequential)'},
    'Q010': {'keys': ['Iterator'], 'explanation': None},
    'Q011': {'keys': ['A → D → C → F'], 'explanation': 'RIP 최단 경로'},
    'Q012': {'keys': ['6.5'], 'explanation': 'SRT 스케줄링 평균 대기시간'},
    'Q013': {'keys': ['21'], 'explanation': None},
    'Q014': {'keys': ['25, 20'], 'explanation': None},
    'Q015': {'keys': ['10'], 'explanation': None},
    'Q016': {'keys': ['제어'], 'explanation': 'Control Coupling'},
    'Q017': {'keys': ['dcba'], 'explanation': None},
    'Q018': {'keys': ['-13'], 'explanation': None},
    'Q019': {'keys': ['20'], 'explanation': None},
    'Q020': {'keys': ['S'], 'explanation': None},
}

jsonl_path = 'data/items_2024_round2.jsonl'

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




