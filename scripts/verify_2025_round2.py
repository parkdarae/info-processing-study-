# -*- coding: utf-8 -*-
"""2025년 2회 검증 - 마지막 회차!"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2025_round2.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print("=" * 80)
print("2025년 2회 정보처리기사 실기 답안 검증 - 마지막 회차!")
print("=" * 80)
print(f"\n총 {len(questions)}개 문제\n")

# 샘플 확인
samples = [
    ('Q001', '인덱스'),
    ('Q003', 'SSH'),
    ('Q007', 'Proxy 패턴'),
    ('Q011', '분기 커버리지'),
    ('Q019', 'SYN Flooding'),
    ('Q020', '프로젝션 연산')
]

for q_no, desc in samples:
    q = next((q for q in questions if q['q_no'] == q_no), None)
    if q:
        print(f"✅ {q_no} ({desc}):")
        print(f"   답안: {' / '.join(q['answer']['keys'][:2])}{'...' if len(q['answer']['keys']) > 2 else ''}")
        if q['explanation']:
            print(f"   해설: {q['explanation']}")

with_ans = [q for q in questions if q['answer']['keys']]
with_exp = [q for q in questions if q['explanation']]

print(f"\n📊 통계:")
print(f"  - 답안 있음: {len(with_ans)}/{len(questions)}개 ({len(with_ans)/len(questions)*100:.1f}%)")
print(f"  - 해설 있음: {len(with_exp)}/{len(questions)}개")
print("=" * 80)




