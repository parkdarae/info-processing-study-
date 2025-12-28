#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""단어 빈도 분석 및 의미 추가 우선순위 정하기"""

import json
import sys

def analyze_frequency():
    """빈도별로 단어 분석"""
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미가 없는 단어만 필터링
    missing = [(word, data) for word, data in vocab.items() 
               if not data.get('meaning') or data.get('meaning', '').strip() == '']
    
    # 빈도순으로 정렬 (높은 순서)
    missing_sorted = sorted(missing, key=lambda x: x[1].get('frequency', 0), reverse=True)
    
    print("=" * 80)
    print(f"의미가 없는 단어 총 {len(missing_sorted)}개")
    print("=" * 80)
    
    # 빈도 구간별 통계
    freq_ranges = {
        '1000 이상': 0,
        '500-999': 0,
        '100-499': 0,
        '50-99': 0,
        '10-49': 0,
        '1-9': 0
    }
    
    for word, data in missing_sorted:
        freq = data.get('frequency', 0)
        if freq >= 1000:
            freq_ranges['1000 이상'] += 1
        elif freq >= 500:
            freq_ranges['500-999'] += 1
        elif freq >= 100:
            freq_ranges['100-499'] += 1
        elif freq >= 50:
            freq_ranges['50-99'] += 1
        elif freq >= 10:
            freq_ranges['10-49'] += 1
        else:
            freq_ranges['1-9'] += 1
    
    print("\n빈도 구간별 단어 수:")
    for range_name, count in freq_ranges.items():
        print(f"  {range_name}: {count}개")
    
    # 상위 100개 단어 출력
    print("\n" + "=" * 80)
    print("빈도 상위 100개 단어 (의미 추가 우선순위)")
    print("=" * 80)
    for i, (word, data) in enumerate(missing_sorted[:100], 1):
        freq = data.get('frequency', 0)
        pos = data.get('pos', 'unknown')
        print(f"{i:3d}. {word:20s} (빈도: {freq:4d}, 품사: {pos})")
    
    # JSON 파일로 저장 (의미 추가용)
    priority_words = [word for word, _ in missing_sorted[:100]]
    with open('data/priority_words_100.json', 'w', encoding='utf-8') as f:
        json.dump(priority_words, f, ensure_ascii=False, indent=2)
    
    print(f"\n우선순위 100개 단어 목록이 'data/priority_words_100.json'에 저장되었습니다.")
    
    return missing_sorted

if __name__ == '__main__':
    analyze_frequency()

