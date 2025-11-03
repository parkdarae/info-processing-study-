#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
해설 적용 스크립트
CSV 파일에서 해설을 읽어 JSONL 파일에 적용
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def backup_file(filepath):
    """파일 백업"""
    if not filepath.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = filepath.parent / f"{filepath.stem}_backup_{timestamp}{filepath.suffix}"
    
    import shutil
    shutil.copy2(filepath, backup_path)
    return backup_path

def apply_explanations_from_csv(jsonl_file, csv_file):
    """CSV 파일의 해설을 JSONL 파일에 적용"""
    
    if not csv_file.exists():
        print(f"⚠️  CSV 파일이 없습니다: {csv_file}")
        return 0, []
    
    # CSV 읽기
    explanations = {}
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            q_no = row.get('q_no', '').strip()
            explanation = row.get('explanation', '').strip()
            if q_no and explanation:
                explanations[q_no] = explanation
    
    if not explanations:
        print(f"⚠️  CSV 파일에 해설 데이터가 없습니다: {csv_file}")
        return 0, []
    
    # 백업 생성
    backup_path = backup_file(jsonl_file)
    if backup_path:
        print(f"✅ 백업 생성: {backup_path}")
    
    # JSONL 읽기 및 업데이트
    updated_questions = []
    questions = []
    updated_count = 0
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                q = json.loads(line)
                q_no = q.get('q_no', '')
                
                # 해설이 있는 경우 업데이트
                if q_no in explanations:
                    old_explanation = q.get('explanation')
                    new_explanation = explanations[q_no]
                    
                    if old_explanation != new_explanation:
                        q['explanation'] = new_explanation
                        updated_count += 1
                        updated_questions.append({
                            'q_no': q_no,
                            'old': str(old_explanation) if old_explanation else '없음',
                            'new': new_explanation[:50] + '...' if len(new_explanation) > 50 else new_explanation
                        })
                
                questions.append(q)
            except json.JSONDecodeError:
                continue
    
    # 업데이트된 내용 저장
    if updated_count > 0:
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    return updated_count, updated_questions

def main():
    """메인 함수"""
    data_dir = Path("data")
    input_dir = Path("data/manual_input")
    
    # 분석 대상 회차
    target_rounds = [
        ('2025', '1'), ('2025', '2'),
        ('2024', '1'), ('2024', '2'), ('2024', '3'),
        ('2023', '1'), ('2023', '2'), ('2023', '3'),
        ('2022', '1'), ('2022', '2'), ('2022', '3')
    ]
    
    print("=" * 80)
    print("해설 적용 스크립트")
    print("=" * 80)
    print()
    print("💡 사용 방법:")
    print("   CSV 파일명: explanations_YYYY_roundX.csv")
    print("   형식: q_no,explanation")
    print()
    
    total_updated = 0
    total_files = 0
    
    for year, round_num in target_rounds:
        jsonl_filename = f"items_{year}_round{round_num}.jsonl"
        csv_filename = f"explanations_{year}_round{round_num}.csv"
        
        jsonl_file = data_dir / jsonl_filename
        csv_file = input_dir / csv_filename
        
        if not jsonl_file.exists():
            print(f"⚠️  JSONL 파일이 없습니다: {jsonl_file}")
            continue
        
        if not csv_file.exists():
            print(f"⚠️  CSV 파일이 없습니다 (건너뜀): {csv_file}")
            continue
        
        print(f"📝 {year}년 {round_num}회 처리 중...")
        updated_count, updated_questions = apply_explanations_from_csv(jsonl_file, csv_file)
        
        if updated_count > 0:
            total_updated += updated_count
            total_files += 1
            print(f"  ✅ {updated_count}개 문제 해설 업데이트 완료")
            
            # 업데이트된 문제 목록 출력 (최대 5개)
            if updated_questions:
                print(f"  📋 업데이트된 문제:")
                for item in updated_questions[:5]:
                    print(f"    - {item['q_no']}: {item['old']} → {item['new']}")
                if len(updated_questions) > 5:
                    print(f"    ... 외 {len(updated_questions) - 5}개")
        else:
            print(f"  ℹ️  업데이트된 문제 없음")
        
        print()
    
    print("=" * 80)
    print(f"총 {total_files}개 파일 처리 완료")
    print(f"총 {total_updated}개 문제의 해설이 업데이트되었습니다.")
    print("=" * 80)

if __name__ == "__main__":
    main()


