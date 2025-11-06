"""
수정된 PMP 데이터 검증
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from pathlib import Path

jsonl_path = Path(__file__).parent.parent / 'data' / 'items_pmp_fixed.jsonl'

questions = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        questions.append(json.loads(line))

print(f"총 {len(questions)}개 문제 검증\n")
print("="*80)

# 처음 5개 문제 상세 확인
for i, q in enumerate(questions[:5], 1):
    print(f"\n[문제 {q['q_no']}]")
    print(f"문제: {q['question'][:120]}...")
    print(f"선택지 개수: {len(q['options'])}개")
    print(f"정답: {q['answer']}")
    print(f"해설: {q['explanation'][:120]}...")
    print(f"물음표로 끝남: {q['question'].rstrip().endswith(('?', '가', '는가', '인가', '까'))}")

# 통계
print("\n" + "="*80)
print("\n전체 통계:")
ends_with_question = sum(1 for q in questions if q['question'].rstrip().endswith(('?', '가', '는가', '인가', '까')))
has_4_choices = sum(1 for q in questions if len(q['options']) == 4)
has_explanation = sum(1 for q in questions if len(q['explanation']) > 20)

print(f"  물음표로 끝나는 문제: {ends_with_question}개 ({ends_with_question/len(questions)*100:.1f}%)")
print(f"  선택지 4개인 문제: {has_4_choices}개 ({has_4_choices/len(questions)*100:.1f}%)")
print(f"  해설 있는 문제: {has_explanation}개 ({has_explanation/len(questions)*100:.1f}%)")

