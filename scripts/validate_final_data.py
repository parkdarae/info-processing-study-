"""
최종 PMP 데이터 검증
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from pathlib import Path

jsonl_path = Path(__file__).parent.parent / 'data' / 'items_pmp_final.jsonl'

questions = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        questions.append(json.loads(line))

print(f"총 {len(questions)}개 문제 검증\n")
print("="*80)

# 처음 10개 문제 상세 확인
suspicious = []
for i, q in enumerate(questions[:10], 1):
    print(f"\n[문제 {q['q_no']}]")
    print(f"문제: {q['question'][:100]}...")
    print(f"선택지: {len(q['options'])}개")
    print(f"정답: {q['answer']}")
    print(f"해설: {q['explanation'][:100]}...")
    
    # 의심 케이스 체크
    issues = []
    if '해설' in q['question'][:100]:
        issues.append("문제에 '해설' 포함")
    if not q['question'].endswith(('?', '가', '는가', '인가', '까')):
        issues.append("물음표 없음")
    if q['explanation'].startswith(('프로젝트', '애자일', '팀')) and '?' in q['explanation'][:50]:
        issues.append("해설이 질문처럼 시작")
    
    if issues:
        print(f"⚠️ 의심: {', '.join(issues)}")
        suspicious.append(q['q_no'])

print("\n" + "="*80)
print(f"\n의심 케이스: {len(suspicious)}개")

# 전체 통계
print("\n전체 통계:")
ends_with_question = sum(1 for q in questions if q['question'].rstrip().endswith(('?', '가', '는가', '인가', '까')))
has_4_choices = sum(1 for q in questions if len(q['options']) == 4)
has_explanation = sum(1 for q in questions if len(q['explanation']) > 20)
has_explanation_in_q = sum(1 for q in questions if '해설' in q['question'][:100])

print(f"  물음표로 끝나는 문제: {ends_with_question}개 ({ends_with_question/len(questions)*100:.1f}%)")
print(f"  선택지 4개인 문제: {has_4_choices}개 ({has_4_choices/len(questions)*100:.1f}%)")
print(f"  해설 있는 문제: {has_explanation}개 ({has_explanation/len(questions)*100:.1f}%)")
print(f"  문제에 '해설' 포함: {has_explanation_in_q}개")

if has_explanation_in_q == 0 and ends_with_question > len(questions) * 0.95:
    print("\n✅ 데이터 품질 양호!")
else:
    print("\n⚠️ 추가 검토 필요")

