#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지 매칭 검증 스크립트
- 각 JSONL 파일의 image_refs가 실제 파일과 일치하는지 확인
- 존재하지 않는 이미지 경로가 있는지 확인
"""

import json
import sys
from pathlib import Path

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

ROUNDS = [
    (2021, 1), (2022, 1), (2022, 2), (2022, 3),
    (2023, 1), (2023, 2), (2023, 3),
    (2024, 1), (2024, 2), (2024, 3),
    (2025, 1), (2025, 2)
]

def main():
    print("=" * 80)
    print("이미지 매칭 검증")
    print("=" * 80)
    
    total_questions = 0
    total_with_images = 0
    total_image_refs = 0
    total_missing = 0
    
    for year, round_num in ROUNDS:
        doc_id = f"{year}_round{round_num}"
        jsonl_path = Path(f"data/items_{doc_id}.jsonl")
        
        if not jsonl_path.exists():
            continue
        
        print(f"\n[{doc_id}]")
        
        # JSONL 파일 읽기
        questions = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        questions_with_images = 0
        image_count = 0
        missing_files = []
        
        for q in questions:
            total_questions += 1
            
            if q.get('image_refs') and len(q['image_refs']) > 0:
                questions_with_images += 1
                total_with_images += 1
                
                for img_path in q['image_refs']:
                    image_count += 1
                    total_image_refs += 1
                    
                    # 파일 존재 여부 확인
                    if not Path(img_path).exists():
                        missing_files.append((q['q_no'], img_path))
                        total_missing += 1
        
        print(f"  총 문제: {len(questions)}개")
        print(f"  이미지 있는 문제: {questions_with_images}개")
        print(f"  총 이미지 파일: {image_count}개")
        
        if missing_files:
            print(f"  ⚠️ 누락된 파일: {len(missing_files)}개")
            for q_no, img_path in missing_files[:3]:
                print(f"    - {q_no}: {img_path}")
            if len(missing_files) > 3:
                print(f"    ... 외 {len(missing_files) - 3}개")
        else:
            print(f"  ✅ 모든 이미지 파일 존재")
    
    print("\n" + "=" * 80)
    print("검증 결과 요약")
    print("=" * 80)
    print(f"총 문제 수: {total_questions}개")
    print(f"이미지 있는 문제: {total_with_images}개 ({total_with_images/total_questions*100:.1f}%)")
    print(f"총 이미지 참조: {total_image_refs}개")
    print(f"누락된 파일: {total_missing}개")
    
    if total_missing == 0:
        print("\n✅ 모든 이미지가 정상적으로 매칭되었습니다!")
    else:
        print(f"\n⚠️ {total_missing}개의 이미지 파일이 누락되었습니다.")

if __name__ == "__main__":
    main()


