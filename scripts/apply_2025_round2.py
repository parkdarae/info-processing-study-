# -*- coding: utf-8 -*-
"""2025년 2회 답안 적용 - 마지막 회차!"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 답안 데이터
answers = {
    'Q001': {'keys': ['인덱스'], 'explanation': '색인(Index) 접근 방법'},
    'Q002': {'keys': ['ㄷ'], 'explanation': 'Attribute'},
    'Q003': {'keys': ['SSH'], 'explanation': 'Secure Shell'},
    'Q004': {'keys': ['(1) SJF', '(2) SRT'], 'explanation': 'Shortest Job First, Shortest Remaining Time'},
    'Q005': {'keys': ['BB'], 'explanation': None},
    'Q006': {'keys': ['① 128', '② 62'], 'explanation': '네트워크 주소와 호스트 수'},
    'Q007': {'keys': ['Proxy'], 'explanation': 'Proxy 패턴'},
    'Q008': {'keys': ['AJAX'], 'explanation': 'Asynchronous JavaScript and XML'},
    'Q009': {'keys': ['19'], 'explanation': None},
    'Q010': {'keys': ['5P'], 'explanation': None},
    'Q011': {'keys': ['1234561', '124567'], 'explanation': '분기 커버리지'},
    'Q012': {'keys': ['2 그리고 3'], 'explanation': None},
    'Q013': {'keys': ['11.75'], 'explanation': '라운드로빈 평균 대기시간'},
    'Q014': {'keys': ['5 그리고 6'], 'explanation': None},
    'Q015': {'keys': ['1a3b3'], 'explanation': None},
    'Q016': {'keys': ['3 1 2'], 'explanation': None},
    'Q017': {'keys': ['2'], 'explanation': None},
    'Q018': {'keys': ['TSEB'], 'explanation': None},
    'Q019': {'keys': ['SYN Flooding'], 'explanation': None},
    'Q020': {'keys': ['TTL', '부장', '대리', '과장', '차장'], 'explanation': '프로젝션 연산'},
}

jsonl_path = 'data/items_2025_round2.jsonl'

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



