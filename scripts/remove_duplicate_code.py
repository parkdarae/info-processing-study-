#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지가 있는 문제에서 중복된 코드 블록 제거 스크립트
"""

import json
import shutil
from pathlib import Path

def remove_duplicate_code_blocks(items_file):
    """이미지가 있으면 코드 블록 제거"""
    
    # 백업
    backup_file = items_file.parent / f"{items_file.stem}_backup_dedupe{items_file.suffix}"
    shutil.copy(items_file, backup_file)
    print(f"백업 생성: {backup_file}")
    
    # 파일 로드
    with open(items_file, 'r', encoding='utf-8') as f:
        items = [json.loads(line) for line in f if line.strip()]
    
    modified_count = 0
    
    for item in items:
        # image_refs가 있고 code_blocks도 있는 경우
        if item.get('image_refs') and len(item.get('image_refs', [])) > 0:
            if item.get('code_blocks') and len(item.get('code_blocks', [])) > 0:
                print(f"\n중복 발견: {item.get('q_no', item.get('doc_id'))}")
                print(f"  이미지: {len(item['image_refs'])}개")
                print(f"  코드블록: {len(item['code_blocks'])}개")
                
                # 코드 블록 제거
                item['code_blocks'] = []
                modified_count += 1
                print(f"  → 코드블록 제거됨")
    
    # 저장
    with open(items_file, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"\n총 {modified_count}개 문제 수정 완료")
    print(f"저장: {items_file}")
    
    return modified_count

def main():
    # 모든 기출문제 파일 처리
    data_dir = Path('data')
    
    # 기출문제 파일 목록
    exam_files = [
        'items_2021_round1.jsonl',
        'items_2022_round1.jsonl',
        'items_2022_round2.jsonl',
        'items_2022_round3.jsonl',
        'items_2023_round1.jsonl',
        'items_2023_round2.jsonl',
        'items_2023_round3.jsonl',
        'items_2024_round1.jsonl',
        'items_2024_round2.jsonl',
        'items_2024_round3.jsonl',
        'items_2025_round1.jsonl',
        'items_2025_round2.jsonl',
    ]
    
    total_modified = 0
    
    for filename in exam_files:
        filepath = data_dir / filename
        if filepath.exists():
            print(f"\n{'='*60}")
            print(f"처리 중: {filename}")
            print(f"{'='*60}")
            count = remove_duplicate_code_blocks(filepath)
            total_modified += count
        else:
            print(f"파일 없음: {filepath}")
    
    print(f"\n{'='*60}")
    print(f"전체 요약: 총 {total_modified}개 문제에서 중복 코드 블록 제거 완료")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

