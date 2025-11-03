#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
해설 품질 검증 스크립트
작성된 해설의 품질을 확인하고 점수를 제공
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def validate_explanation(explanation, question_text=""):
    """해설 품질 검증"""
    if not explanation:
        return {
            'has_explanation': False,
            'length': 0,
            'score': 0,
            'issues': ['해설이 없습니다']
        }
    
    explanation_str = str(explanation).strip()
    length = len(explanation_str)
    
    issues = []
    score = 100
    
    # 길이 체크
    if length < 30:
        issues.append(f"해설이 너무 짧습니다 ({length}자, 권장: 30자 이상)")
        score -= 30
    elif length < 50:
        issues.append(f"해설이 다소 짧습니다 ({length}자, 권장: 50자 이상)")
        score -= 10
    
    # 구체적인 설명이 있는지 체크
    explanation_words = ['은', '는', '이', '가', '을', '를', '한다', '합니다', '이다', '입니다', '에서', '의', '이다', '로서', '따라서', '때문에']
    has_explanation_words = any(word in explanation_str for word in explanation_words)
    
    if not has_explanation_words:
        issues.append("구체적인 설명 문장이 부족합니다 (단순 키워드나 약자만 있음)")
        score -= 20
    
    # 단순 키워드나 약자만 있는지 체크
    simple_keywords = ['Session Hijacking', '제약조건', 'SQL JOIN 결과', 'CRC', 'OSPF']
    if explanation_str in simple_keywords or len(explanation_str.split()) <= 3:
        issues.append("단순 키워드나 약자만 있습니다. 구체적인 설명을 추가하세요")
        score -= 40
    
    # 답의 이유 설명이 있는지 체크 (문제 텍스트에 키워드가 있으면)
    if question_text:
        question_lower = question_text.lower()
        explanation_lower = explanation_str.lower()
        
        # 문제에서 중요한 키워드 추출 (간단한 휴리스틱)
        if '왜' in question_text or '이유' in question_text or '설명' in question_text:
            if '따라서' not in explanation_str and '때문에' not in explanation_str and '이유' not in explanation_str:
                issues.append("답의 이유에 대한 설명이 부족합니다")
                score -= 10
    
    # 최소 점수 보장
    if score < 0:
        score = 0
    
    return {
        'has_explanation': True,
        'length': length,
        'score': score,
        'issues': issues
    }

def validate_file(jsonl_file):
    """단일 JSONL 파일 검증"""
    results = {
        'total': 0,
        'with_explanation': 0,
        'without_explanation': 0,
        'quality_scores': [],
        'issues': []
    }
    
    if not jsonl_file.exists():
        return results
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                q = json.loads(line)
                results['total'] += 1
                
                explanation = q.get('explanation')
                question_text = q.get('question_text', '')
                
                validation = validate_explanation(explanation, question_text)
                
                if validation['has_explanation']:
                    results['with_explanation'] += 1
                    results['quality_scores'].append(validation['score'])
                    
                    if validation['issues']:
                        results['issues'].append({
                            'q_no': q.get('q_no'),
                            'issues': validation['issues'],
                            'score': validation['score']
                        })
                else:
                    results['without_explanation'] += 1
                    results['issues'].append({
                        'q_no': q.get('q_no'),
                        'issues': validation['issues'],
                        'score': 0
                    })
            except json.JSONDecodeError:
                continue
    
    return results

def main():
    """메인 검증 함수"""
    data_dir = Path("data")
    
    # 분석 대상 회차
    target_rounds = [
        ('2025', '1'), ('2025', '2'),
        ('2024', '1'), ('2024', '2'), ('2024', '3'),
        ('2023', '1'), ('2023', '2'), ('2023', '3'),
        ('2022', '1'), ('2022', '2'), ('2022', '3')
    ]
    
    print("=" * 80)
    print("해설 품질 검증")
    print("=" * 80)
    print()
    
    all_scores = []
    all_results = {}
    
    for year, round_num in target_rounds:
        filename = f"items_{year}_round{round_num}.jsonl"
        jsonl_file = data_dir / filename
        
        results = validate_file(jsonl_file)
        all_results[f"{year}_round{round_num}"] = results
        
        if results['total'] == 0:
            continue
        
        # 평균 점수 계산
        avg_score = sum(results['quality_scores']) / len(results['quality_scores']) if results['quality_scores'] else 0
        all_scores.extend(results['quality_scores'])
        
        print(f"{year}년 {round_num}회:")
        print(f"  총 문제: {results['total']}개")
        print(f"  해설 있음: {results['with_explanation']}개 ({results['with_explanation']/results['total']*100:.1f}%)")
        print(f"  해설 없음: {results['without_explanation']}개 ({results['without_explanation']/results['total']*100:.1f}%)")
        
        if results['quality_scores']:
            print(f"  평균 품질 점수: {avg_score:.1f}/100")
        
        # 문제가 있는 해설 표시 (최대 3개)
        if results['issues']:
            problem_count = sum(1 for item in results['issues'] if item['score'] < 70)
            if problem_count > 0:
                print(f"  ⚠️  개선 필요: {problem_count}개")
                
                # 점수가 낮은 문제 표시
                low_score_issues = [item for item in results['issues'] if item['score'] < 70][:3]
                for item in low_score_issues:
                    print(f"    - {item['q_no']}: 점수 {item['score']}/100")
                    for issue in item['issues'][:2]:
                        print(f"      • {issue}")
        
        print()
    
    # 전체 통계
    if all_scores:
        overall_avg = sum(all_scores) / len(all_scores)
        print("=" * 80)
        print("전체 통계")
        print("=" * 80)
        print(f"평균 품질 점수: {overall_avg:.1f}/100")
        print(f"검증된 해설: {len(all_scores)}개")
        
        # 점수 분포
        excellent = sum(1 for s in all_scores if s >= 80)
        good = sum(1 for s in all_scores if 60 <= s < 80)
        poor = sum(1 for s in all_scores if s < 60)
        
        print()
        print(f"점수 분포:")
        print(f"  ✅ 우수 (80점 이상): {excellent}개 ({excellent/len(all_scores)*100:.1f}%)")
        print(f"  ⚠️  양호 (60-79점): {good}개 ({good/len(all_scores)*100:.1f}%)")
        print(f"  ❌ 개선 필요 (60점 미만): {poor}개 ({poor/len(all_scores)*100:.1f}%)")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()


