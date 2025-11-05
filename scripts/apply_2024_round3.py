# -*- coding: utf-8 -*-
"""2024년 3회 답안 적용"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 답안 데이터
answers = {
    'Q001': {'keys': ['OOAAA'], 'explanation': None},
    'Q002': {'keys': ['3'], 'explanation': None},
    'Q003': {'keys': ['1'], 'explanation': None},
    'Q004': {'keys': ['12'], 'explanation': 'LRU 페이지 부재 횟수'},
    'Q005': {'keys': ['스머프'], 'explanation': 'Smurf 또는 Smurfing'},
    'Q006': {'keys': ['행위'], 'explanation': '행위 패턴'},
    'Q007': {'keys': ['20'], 'explanation': None},
    'Q008': {'keys': ['개체'], 'explanation': '개체 무결성'},
    'Q009': {'keys': ['43125'], 'explanation': 'URL 구조'},
    'Q010': {'keys': ['45'], 'explanation': None},
    'Q011': {'keys': ['52'], 'explanation': None},
    'Q012': {'keys': ['312'], 'explanation': None},
    'Q013': {'keys': ['1. 문장', '2. 분기', '3. 조건'], 'explanation': '테스트 커버리지'},
    'Q014': {'keys': ['(1) 연관', '(2) 일반화', '(3) 의존'], 'explanation': 'UML 클래스 관계'},
    'Q015': {'keys': ['(1) 외래키', '(2) 후보키', '(3) 대체키', '(4) 슈퍼키'], 'explanation': None},
    'Q016': {'keys': ['1'], 'explanation': None},
    'Q017': {'keys': ['VPN'], 'explanation': None},
    'Q018': {'keys': ['101'], 'explanation': None},
    'Q019': {'keys': ['B0'], 'explanation': None},
    'Q020': {'keys': ['ㄹ'], 'explanation': 'Ad-hoc Network'},
}

jsonl_path = 'data/items_2024_round3.jsonl'

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



