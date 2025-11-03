# -*- coding: utf-8 -*-
"""답안 입력률 확인 스크립트"""
import json
from pathlib import Path

def check_answer_rate():
    """각 회차별 답안 입력률 확인"""
    data_dir = Path("data")
    jsonl_files = sorted(data_dir.glob("items_*.jsonl"))
    
    print("="*70)
    print(f"{'파일명':<30} | {'전체':<5} | {'답안':<5} | {'해설':<5} | {'입력률':<8}")
    print("="*70)
    
    total_questions = 0
    total_with_answers = 0
    total_with_explanations = 0
    
    for jsonl_file in jsonl_files:
        questions = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        with_answers = sum(1 for q in questions if q['answer'].get('keys'))
        with_explanations = sum(1 for q in questions if q.get('explanation'))
        
        rate = (with_answers / len(questions) * 100) if questions else 0
        
        print(f"{jsonl_file.name:<30} | {len(questions):>5} | {with_answers:>5} | {with_explanations:>5} | {rate:>6.1f}%")
        
        total_questions += len(questions)
        total_with_answers += with_answers
        total_with_explanations += with_explanations
    
    print("="*70)
    overall_rate = (total_with_answers / total_questions * 100) if total_questions else 0
    print(f"{'전체':<30} | {total_questions:>5} | {total_with_answers:>5} | {total_with_explanations:>5} | {overall_rate:>6.1f}%")
    print("="*70)
    
    # 답안이 없는 문제 리스트
    print("\n[답안이 없는 문제들]")
    for jsonl_file in jsonl_files:
        questions = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        no_answer = [q for q in questions if not q['answer'].get('keys')]
        if no_answer:
            print(f"\n{jsonl_file.name}: {len(no_answer)}개")
            for q in no_answer[:5]:  # 처음 5개만
                print(f"  - {q['q_no']}: {q['question_text'][:50]}...")

if __name__ == "__main__":
    check_answer_rate()


