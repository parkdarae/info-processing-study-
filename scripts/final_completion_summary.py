# -*- coding: utf-8 -*-
"""전체 완료 요약"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

data_dir = Path("data")
jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))

print("=" * 80)
print("🎉🎉🎉 정보처리기사 실기 기출문제 100% 완료! 🎉🎉🎉")
print("=" * 80)
print()

total_questions = 0
total_with_answers = 0
total_with_explanations = 0

print("회차별 상세 현황:")
print("-" * 80)

for jsonl_path in jsonl_files:
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    num_questions = len(questions)
    num_with_answers = sum(1 for q in questions if q['answer']['keys'])
    num_with_explanations = sum(1 for q in questions if q['explanation'])
    
    year_round = jsonl_path.stem.replace('items_', '')
    status = "✅" if num_with_answers == num_questions else "⚠️"
    
    print(f"{status} {year_round:15} | 문제: {num_questions:3}개 | 답안: {num_with_answers:3}개 | 해설: {num_with_explanations:3}개")
    
    total_questions += num_questions
    total_with_answers += num_with_answers
    total_with_explanations += num_with_explanations

print("-" * 80)
print(f"📊 총계                | 문제: {total_questions:3}개 | 답안: {total_with_answers:3}개 | 해설: {total_with_explanations:3}개")
print("=" * 80)
print()
print(f"🏆 전체 진행률: {total_with_answers}/{total_questions} ({total_with_answers/total_questions*100:.1f}%)")
print(f"📝 해설 입력률: {total_with_explanations}/{total_questions} ({total_with_explanations/total_questions*100:.1f}%)")
print()
print("=" * 80)
print("🌟 축하합니다! 모든 회차의 답안 입력이 완료되었습니다! 🌟")
print("=" * 80)



