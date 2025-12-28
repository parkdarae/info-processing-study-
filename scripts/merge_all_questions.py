#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 기출문제를 하나의 JSONL 파일로 통합
- 카테고리별 필터링을 위해 사용
- 각 문제는 원본 doc_id를 유지하여 추적 가능
"""

import json
import sys
from pathlib import Path

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 80)
    print("전체 문제 통합 시작")
    print("=" * 80)
    
    ROUNDS = [
        (2021, 1), (2022, 1), (2022, 2), (2022, 3),
        (2023, 1), (2023, 2), (2023, 3),
        (2024, 1), (2024, 2), (2024, 3),
        (2025, 1), (2025, 2)
    ]
    
    all_questions = []
    
    for year, round_num in ROUNDS:
        doc_id = f"{year}_round{round_num}"
        jsonl_path = Path(f"data/items_{doc_id}.jsonl")
        
        if not jsonl_path.exists():
            print(f"[건너뜀] {doc_id}: 파일 없음")
            continue
        
        print(f"[처리중] {doc_id}")
        
        # JSONL 읽기
        count = 0
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    q = json.loads(line)
                    all_questions.append(q)
                    count += 1
        
        print(f"  ✅ {count}개 문제 추가")
    
    # 통합 파일 저장
    output_path = Path("data/items_all.jsonl")
    with open(output_path, 'w', encoding='utf-8') as f:
        for q in all_questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print("\n" + "=" * 80)
    print(f"통합 완료: {len(all_questions)}개 문제")
    print(f"파일 위치: {output_path}")
    print("=" * 80)
    
    # 카테고리별 통계
    category_stats = {}
    for q in all_questions:
        cat = q.get("primary_category", "기타")
        category_stats[cat] = category_stats.get(cat, 0) + 1
    
    print("\n카테고리별 문제 수:")
    for cat, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(all_questions) * 100) if len(all_questions) > 0 else 0
        print(f"  {cat:15s}: {count:3d}개 ({percentage:5.1f}%)")

if __name__ == "__main__":
    main()




