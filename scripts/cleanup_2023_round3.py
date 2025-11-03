# -*- coding: utf-8 -*-
"""2023년 3회 중복 항목 제거 및 최종 정리"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2023_round3.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"원본: {len(questions)}개 항목")

# 중복 Q002, Q003, Q004 제거 (Q019에 이미 포함됨)
# Q019가 전체 답안을 포함하고 있으므로, 소문제들은 삭제
cleaned = []
for q in questions:
    # Q019의 소문제들 (20번, 21번, 22번 줄)은 제외
    if q['q_no'] in ['Q002', 'Q003', 'Q004'] and ('project' in q['question_text'] or 
                                                     'select' in q['question_text'] or 
                                                     'division' in q['question_text']):
        print(f"중복 제거: {q['q_no']} - {q['question_text'][:30]}...")
        continue
    cleaned.append(q)

print(f"정리 후: {len(cleaned)}개 항목")

# Q_no 재정렬 (Q001~Q020)
for i, q in enumerate(cleaned):
    old_qno = q['q_no']
    q['q_no'] = f"Q{i+1:03d}"
    q['meta']['anchors'] = [f"{i+1}."]
    if old_qno != q['q_no']:
        print(f"번호 변경: {old_qno} → {q['q_no']}")

# 저장
with open('data/items_2023_round3.jsonl', 'w', encoding='utf-8') as f:
    for q in cleaned:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"\n[OK] 최종 정리 완료! 총 {len(cleaned)}개 문제")

# 최종 확인
with_ans = [q for q in cleaned if q['answer']['keys']]
print(f"\n답안 있음: {len(with_ans)}/{len(cleaned)}개 ({len(with_ans)/len(cleaned)*100:.1f}%)")


