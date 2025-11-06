#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PMP 복수 답안 문제 분석 스크립트
문제 텍스트에서 복수 선택 패턴을 찾고, explanation에서 실제 정답을 추출합니다.
"""

import json
import re
from pathlib import Path

def analyze_multiple_answers():
    """복수 답안 문제 분석"""
    
    jsonl_file = Path('data/items_pmp.jsonl')
    
    if not jsonl_file.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {jsonl_file}")
        return
    
    multiple_choice_problems = []
    
    print("=" * 80)
    print("PMP 복수 답안 문제 분석")
    print("=" * 80)
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                item = json.loads(line.strip())
                
                # 복수 선택 패턴 찾기
                question = item.get('question', '')
                match = re.search(r'\((\d+)\s*개\s*선택\)', question)
                
                if match:
                    required_count = int(match.group(1))
                    current_answer = item.get('answer', '')
                    explanation = item.get('explanation', '')
                    
                    # explanation에서 정답 추출
                    # 패턴: ", B, C" 또는 ", C, D" 또는 "① ② ③"
                    extracted_answers = []
                    
                    # 패턴 1: ", B, C" 형식
                    pattern1 = re.findall(r',\s*([A-F])', explanation[:100])
                    if pattern1:
                        extracted_answers = [current_answer] + pattern1
                    
                    # 패턴 2: 설명 첫 줄에서 "B, C, D" 형식
                    if not extracted_answers:
                        first_line = explanation.split('\n')[0] if explanation else ''
                        pattern2 = re.findall(r'\b([A-F])\b', first_line)
                        if len(pattern2) >= required_count:
                            extracted_answers = pattern2[:required_count]
                    
                    problem_info = {
                        'id': item.get('id'),
                        'q_no': item.get('q_no'),
                        'required_count': required_count,
                        'current_answer': current_answer,
                        'current_answer_type': type(current_answer).__name__,
                        'extracted_answers': extracted_answers,
                        'explanation_preview': explanation[:200] if explanation else ''
                    }
                    
                    multiple_choice_problems.append(problem_info)
                    
            except json.JSONDecodeError as e:
                print(f"[경고] 라인 {line_num} JSON 파싱 오류: {e}")
                continue
    
    # 결과 출력
    print(f"\n[분석] 발견된 복수 답안 문제: {len(multiple_choice_problems)}개\n")
    
    for idx, prob in enumerate(multiple_choice_problems, 1):
        print(f"{idx}. {prob['id']} (Q{prob['q_no']})")
        print(f"   요구 개수: {prob['required_count']}개")
        print(f"   현재 답안: {prob['current_answer']} (타입: {prob['current_answer_type']})")
        print(f"   추출 답안: {prob['extracted_answers']}")
        print(f"   해설 미리보기: {prob['explanation_preview'][:100]}...")
        print()
    
    # 보고서 저장
    report_file = Path('scripts/pmp_multiple_answers_report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(multiple_choice_problems, f, ensure_ascii=False, indent=2)
    
    print(f"[완료] 분석 결과가 저장되었습니다: {report_file}")
    print(f"\n통계:")
    print(f"  - 전체 복수 답안 문제: {len(multiple_choice_problems)}개")
    
    # 답안 타입별 통계
    str_count = sum(1 for p in multiple_choice_problems if p['current_answer_type'] == 'str')
    list_count = sum(1 for p in multiple_choice_problems if p['current_answer_type'] == 'list')
    
    print(f"  - 문자열 타입 답안: {str_count}개 (수정 필요)")
    print(f"  - 배열 타입 답안: {list_count}개 (이미 수정됨)")
    
    return multiple_choice_problems

if __name__ == '__main__':
    analyze_multiple_answers()

