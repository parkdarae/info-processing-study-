"""
PMP 데이터 검사 - 문제와 해설 혼동 확인
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from pathlib import Path

jsonl_path = Path(__file__).parent.parent / 'data' / 'items_pmp.jsonl'

questions = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        questions.append(json.loads(line))

print(f"총 {len(questions)}개 문제 검사\n")
print("="*80)

# 문제와 해설이 혼동된 케이스 찾기
suspicious_cases = []

for i, q in enumerate(questions[:20], 1):  # 처음 20개만 상세 검사
    q_no = q['q_no']
    question = q['question']
    explanation = q.get('explanation', '')
    
    print(f"\n[문제 {q_no}]")
    print(f"문제 길이: {len(question)}자")
    print(f"문제 시작: {question[:80]}...")
    print(f"해설 길이: {len(explanation)}자")
    print(f"해설 시작: {explanation[:80]}...")
    
    # 의심 케이스 체크
    suspicious = False
    reasons = []
    
    # 1. 문제에 "해설" 키워드가 있는 경우
    if '해설' in question[:200]:
        suspicious = True
        reasons.append("문제에 '해설' 키워드 포함")
    
    # 2. 문제가 설명조로 시작하는 경우
    explanation_patterns = [
        '일 장소 근무에서',
        '프로젝트 관리자의 역할은',
        '이 문제는',
        '정답은',
        '따라서'
    ]
    if any(pattern in question[:100] for pattern in explanation_patterns):
        suspicious = True
        reasons.append("문제가 해설처럼 시작")
    
    # 3. 문제가 물음표로 끝나지 않는 경우
    if question and not question.rstrip().endswith(('?', '가', '는가', '인가')):
        suspicious = True
        reasons.append("문제가 물음표로 끝나지 않음")
    
    # 4. 해설이 질문으로 시작하는 경우
    if explanation and explanation[:50].count('?') > 0:
        suspicious = True
        reasons.append("해설이 질문 포함")
    
    if suspicious:
        suspicious_cases.append({
            'q_no': q_no,
            'reasons': reasons,
            'question_preview': question[:150],
            'explanation_preview': explanation[:150]
        })
        print(f"⚠️ 의심: {', '.join(reasons)}")

print("\n" + "="*80)
print(f"\n의심 케이스: {len(suspicious_cases)}개\n")

if suspicious_cases:
    print("상세 내역:\n")
    for case in suspicious_cases:
        print(f"문제 {case['q_no']}:")
        print(f"  이유: {', '.join(case['reasons'])}")
        print(f"  문제: {case['question_preview']}...")
        print(f"  해설: {case['explanation_preview']}...")
        print()

# 전체 데이터 통계
print("\n전체 통계:")
no_question_mark = sum(1 for q in questions if not q['question'].rstrip().endswith(('?', '가', '는가', '인가')))
has_explanation_in_question = sum(1 for q in questions if '해설' in q['question'][:200])

print(f"  물음표 없는 문제: {no_question_mark}개 ({no_question_mark/len(questions)*100:.1f}%)")
print(f"  문제에 '해설' 포함: {has_explanation_in_question}개")

