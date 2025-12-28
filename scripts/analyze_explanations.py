#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기출문제 해설 현황 분석
각 회차별 문제의 해설 상태를 분석하여 완전/부족/없음으로 분류
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# 해설 분류 기준
def classify_explanation(explanation):
    """해설을 완전/부족/없음으로 분류"""
    if explanation is None:
        return "없음"
    
    explanation_str = str(explanation).strip()
    
    if not explanation_str or len(explanation_str) < 10:
        return "없음"
    
    # 50자 이상이고 구체적인 설명이 있는 경우
    if len(explanation_str) >= 50:
        # 단순 키워드나 약자 나열이 아닌 경우 완전한 해설로 판단
        # 구체적인 설명이 있는지 확인 (동사, 조사 등이 포함)
        if any(word in explanation_str for word in ['은', '는', '이', '가', '을', '를', '한다', '합니다', '이다', '입니다', '에서', '의']):
            return "완전"
    
    # 10~50자 사이이거나 단순 키워드/약자인 경우
    if len(explanation_str) < 50:
        # 단순 키워드나 약자인지 확인
        simple_keywords = ['Session Hijacking', '제약조건', 'SQL JOIN 결과', 'CRC', 'OSPF', 'Cyclic Redundancy Check', 'Adapter 패턴']
        if explanation_str in simple_keywords or len(explanation_str.split()) <= 3:
            return "부족"
        elif len(explanation_str) >= 30:
            return "완전"
        else:
            return "부족"
    
    return "완전"

def analyze_file(jsonl_file):
    """단일 JSONL 파일 분석"""
    stats = {
        'total': 0,
        '완전': 0,
        '부족': 0,
        '없음': 0,
        '부족_문제': [],
        '없음_문제': []
    }
    
    if not jsonl_file.exists():
        return stats
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                q = json.loads(line)
                stats['total'] += 1
                
                explanation = q.get('explanation')
                classification = classify_explanation(explanation)
                stats[classification] += 1
                
                # 부족하거나 없는 문제 정보 저장
                if classification == '부족':
                    stats['부족_문제'].append({
                        'q_no': q.get('q_no'),
                        'explanation': explanation,
                        'preview': q.get('question_text', '')[:50] + '...'
                    })
                elif classification == '없음':
                    stats['없음_문제'].append({
                        'q_no': q.get('q_no'),
                        'preview': q.get('question_text', '')[:50] + '...'
                    })
            except json.JSONDecodeError:
                continue
    
    return stats

def main():
    """메인 분석 함수"""
    data_dir = Path("data")
    
    # 분석 대상 회차
    target_rounds = [
        ('2025', '1'), ('2025', '2'),
        ('2024', '1'), ('2024', '2'), ('2024', '3'),
        ('2023', '1'), ('2023', '2'), ('2023', '3'),
        ('2022', '1'), ('2022', '2'), ('2022', '3')
    ]
    
    total_stats = {
        'total': 0,
        '완전': 0,
        '부족': 0,
        '없음': 0
    }
    
    print("=" * 80)
    print("기출문제 해설 현황 분석")
    print("=" * 80)
    print()
    
    results = {}
    
    for year, round_num in target_rounds:
        filename = f"items_{year}_round{round_num}.jsonl"
        jsonl_file = data_dir / filename
        
        stats = analyze_file(jsonl_file)
        results[f"{year}_round{round_num}"] = stats
        
        # 전체 통계 집계
        total_stats['total'] += stats['total']
        total_stats['완전'] += stats['완전']
        total_stats['부족'] += stats['부족']
        total_stats['없음'] += stats['없음']
        
        # 개별 회차 출력
        print(f"{year}년 {round_num}회: 총 {stats['total']}문제")
        print(f"  ✅ 완전한 해설: {stats['완전']}개 ({stats['완전']/stats['total']*100:.1f}%)")
        print(f"  ⚠️  부족한 해설: {stats['부족']}개 ({stats['부족']/stats['total']*100:.1f}%)")
        print(f"  ❌ 해설 없음: {stats['없음']}개 ({stats['없음']/stats['total']*100:.1f}%)")
        
        # 부족한 해설 목록 (최대 5개만 표시)
        if stats['부족_문제']:
            print(f"\n  ⚠️  부족한 해설 예시:")
            for item in stats['부족_문제'][:5]:
                print(f"    - {item['q_no']}: {item['explanation']}")
        
        print()
    
    # 전체 통계
    print("=" * 80)
    print("전체 통계")
    print("=" * 80)
    print(f"총 문제 수: {total_stats['total']}개")
    print(f"✅ 완전한 해설: {total_stats['완전']}개 ({total_stats['완전']/total_stats['total']*100:.1f}%)")
    print(f"⚠️  부족한 해설: {total_stats['부족']}개 ({total_stats['부족']/total_stats['total']*100:.1f}%)")
    print(f"❌ 해설 없음: {total_stats['없음']}개 ({total_stats['없음']/total_stats['total']*100:.1f}%)")
    print()
    print(f"📝 해설 작업 필요: {total_stats['부족'] + total_stats['없음']}개")
    print("=" * 80)
    
    # 결과를 파일로 저장 (필요시)
    output_file = Path("data/manual_input/explanation_analysis.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("기출문제 해설 현황 분석 결과\n")
        f.write("=" * 80 + "\n\n")
        
        for year, round_num in target_rounds:
            key = f"{year}_round{round_num}"
            stats = results[key]
            f.write(f"{year}년 {round_num}회: 총 {stats['total']}문제\n")
            f.write(f"  완전한 해설: {stats['완전']}개\n")
            f.write(f"  부족한 해설: {stats['부족']}개\n")
            f.write(f"  해설 없음: {stats['없음']}개\n\n")
            
            if stats['부족_문제']:
                f.write(f"  부족한 해설 목록:\n")
                for item in stats['부족_문제']:
                    f.write(f"    - {item['q_no']}: {item['explanation']}\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("전체 통계\n")
        f.write("=" * 80 + "\n")
        f.write(f"총 문제 수: {total_stats['total']}개\n")
        f.write(f"완전한 해설: {total_stats['완전']}개\n")
        f.write(f"부족한 해설: {total_stats['부족']}개\n")
        f.write(f"해설 없음: {total_stats['없음']}개\n")
        f.write(f"해설 작업 필요: {total_stats['부족'] + total_stats['없음']}개\n")
    
    print(f"\n✅ 분석 결과가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    main()




