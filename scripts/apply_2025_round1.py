# -*- coding: utf-8 -*-
"""2025년 1회 답안 적용"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 답안 데이터
answers = {
    'Q001': {'keys': ['세션 하이재킹'], 'explanation': 'Session Hijacking'},
    'Q002': {'keys': ['ㄱ. 도메인', 'ㄴ. 개체', 'ㄷ. 참조'], 'explanation': '제약조건'},
    'Q003': {'keys': ['CRC'], 'explanation': 'Cyclic Redundancy Check'},
    'Q004': {'keys': ['ㄹ'], 'explanation': '스캐어 웨어 (Scareware)'},
    'Q005': {'keys': ['출력1출력5'], 'explanation': None},
    'Q006': {'keys': ['(1) ARP', '(2) RARP'], 'explanation': None},
    'Q007': {'keys': ['이순신', '1000'], 'explanation': 'SQL JOIN 결과'},
    'Q008': {'keys': ['(1) ㄷ', '(2) ㅁ', '(3) ㅅ', '(4) ㄱ'], 'explanation': 'degree, cardinality, foreign, domain'},
    'Q009': {'keys': ['ㄱ,ㄴ,ㄷ,ㄹ,ㅁ'], 'explanation': '서브넷 브로드캐스팅'},
    'Q010': {'keys': ['4', 'BACDE'], 'explanation': None},
    'Q011': {'keys': ['13'], 'explanation': None},
    'Q012': {'keys': ['(1) ㅁ', '(2) ㄴ', '(3) ㄹ'], 'explanation': '내용 결합도, 스탬프 결합도, 공통 결합도'},
    'Q013': {'keys': ['54'], 'explanation': None},
    'Q014': {'keys': ['Adapter'], 'explanation': 'Adapter 패턴'},
    'Q015': {'keys': ['(1) int a = 0', '(2) a < m || b[a] < x', '(3) b[a] < 0', '(4) b[a] = -b[a];', '(5) a++;', '(6) return 1;', '(7) ③ → ④ → ⑤ → ② → ⑥'], 'explanation': '문장 커버리지'},
    'Q016': {'keys': ['20'], 'explanation': None},
    'Q017': {'keys': ['13'], 'explanation': None},
    'Q018': {'keys': ['35421'], 'explanation': None},
    'Q019': {'keys': ['908'], 'explanation': None},
    'Q020': {'keys': ['4'], 'explanation': None},
}

jsonl_path = 'data/items_2025_round1.jsonl'

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


