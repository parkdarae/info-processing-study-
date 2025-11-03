#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
해설이 필요한 문제 목록 추출
각 회차별로 해설이 없거나 부족한 문제를 CSV로 추출
"""

import json
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def classify_explanation(explanation):
    """해설을 완전/부족/없음으로 분류"""
    if explanation is None:
        return "없음", True
    
    explanation_str = str(explanation).strip()
    
    if not explanation_str or len(explanation_str) < 10:
        return "없음", True
    
    # 50자 이상이고 구체적인 설명이 있는 경우
    if len(explanation_str) >= 50:
        # 단순 키워드나 약자 나열이 아닌 경우 완전한 해설로 판단
        if any(word in explanation_str for word in ['은', '는', '이', '가', '을', '를', '한다', '합니다', '이다', '입니다', '에서', '의']):
            return "완전", False
    
    # 10~50자 사이이거나 단순 키워드/약자인 경우
    if len(explanation_str) < 50:
        # 단순 키워드나 약자인지 확인
        simple_keywords = ['Session Hijacking', '제약조건', 'SQL JOIN 결과', 'CRC', 'OSPF', 'Cyclic Redundancy Check', 'Adapter 패턴']
        if explanation_str in simple_keywords or len(explanation_str.split()) <= 3:
            return "부족", True
        elif len(explanation_str) >= 30:
            return "완전", False
        else:
            return "부족", True
    
    return "완전", False

def extract_from_file(jsonl_file, year, round_num):
    """단일 JSONL 파일에서 해설이 필요한 문제 추출"""
    items = []
    
    if not jsonl_file.exists():
        return items
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                q = json.loads(line)
                
                explanation = q.get('explanation')
                classification, needs_work = classify_explanation(explanation)
                
                # 해설이 필요한 문제만 추출
                if needs_work:
                    # 이미지 참조 추출
                    image_refs = q.get('image_refs', [])
                    image_str = ', '.join(image_refs) if image_refs else ''
                    
                    # 코드 블록 언어 추출
                    code_blocks = q.get('code_blocks', [])
                    code_languages = []
                    if code_blocks:
                        for cb in code_blocks:
                            lang = cb.get('language', 'unknown')
                            if lang not in code_languages:
                                code_languages.append(lang)
                    code_language = ', '.join(code_languages) if code_languages else ''
                    
                    # 답안 추출
                    answer = q.get('answer', {})
                    answer_keys = answer.get('keys', [])
                    answer_str = ', '.join(str(k) for k in answer_keys) if answer_keys else ''
                    
                    # 문제 텍스트 미리보기 (50자)
                    question_text = q.get('question_text', '')
                    preview = question_text[:50] + '...' if len(question_text) > 50 else question_text
                    
                    items.append({
                        'q_no': q.get('q_no', ''),
                        'question_preview': preview.replace('\n', ' ').replace(',', '，'),  # CSV 엔트리 방지
                        'answer': answer_str.replace('\n', ' ').replace(',', '，'),
                        'current_explanation': str(explanation) if explanation else '',
                        'needs_work': classification,
                        'image_refs': image_str,
                        'code_language': code_language,
                        'year': year,
                        'round': round_num
                    })
            except json.JSONDecodeError:
                continue
    
    return items

def main():
    """메인 추출 함수"""
    data_dir = Path("data")
    output_dir = Path("data/manual_input")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 분석 대상 회차
    target_rounds = [
        ('2025', '1'), ('2025', '2'),
        ('2024', '1'), ('2024', '2'), ('2024', '3'),
        ('2023', '1'), ('2023', '2'), ('2023', '3'),
        ('2022', '1'), ('2022', '2'), ('2022', '3')
    ]
    
    all_items = []
    
    print("=" * 80)
    print("해설이 필요한 문제 목록 추출")
    print("=" * 80)
    print()
    
    for year, round_num in target_rounds:
        filename = f"items_{year}_round{round_num}.jsonl"
        jsonl_file = data_dir / filename
        
        items = extract_from_file(jsonl_file, year, round_num)
        all_items.extend(items)
        
        # CSV 파일로 저장
        csv_filename = f"explanations_{year}_round{round_num}.csv"
        csv_filepath = output_dir / csv_filename
        
        if items:
            # year, round 필드 제거 (회차별 CSV에는 불필요)
            items_for_csv = []
            for item in items:
                item_copy = item.copy()
                item_copy.pop('year', None)
                item_copy.pop('round', None)
                items_for_csv.append(item_copy)
            
            with open(csv_filepath, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'q_no', 'question_preview', 'answer', 'current_explanation', 
                    'needs_work', 'image_refs', 'code_language'
                ])
                writer.writeheader()
                writer.writerows(items_for_csv)
            
            print(f"✅ {year}년 {round_num}회: {len(items)}개 문제 → {csv_filepath}")
        else:
            print(f"⚠️  {year}년 {round_num}회: 해설이 필요한 문제 없음")
    
    # 전체 통합 CSV
    all_csv_filepath = output_dir / "explanations_all.csv"
    if all_items:
        with open(all_csv_filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'year', 'round', 'q_no', 'question_preview', 'answer', 
                'current_explanation', 'needs_work', 'image_refs', 'code_language'
            ])
            writer.writeheader()
            writer.writerows(all_items)
        
        print()
        print(f"✅ 전체 통합: {len(all_items)}개 문제 → {all_csv_filepath}")
    
    print()
    print("=" * 80)
    print(f"총 {len(all_items)}개 문제의 해설 작성이 필요합니다.")
    print("=" * 80)
    
    # 통계 출력
    needs_work_count = sum(1 for item in all_items if item['needs_work'] == '없음')
    insufficient_count = sum(1 for item in all_items if item['needs_work'] == '부족')
    
    print()
    print(f"❌ 해설 없음: {needs_work_count}개")
    print(f"⚠️  부족한 해설: {insufficient_count}개")
    print(f"📝 총 작업 필요: {len(all_items)}개")

if __name__ == "__main__":
    main()

