"""
이미지 파일을 문제 번호에 정확하게 매칭
"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def map_images_for_round(year, round_num):
    """특정 회차의 이미지를 매칭"""
    print(f"\n{'='*60}")
    print(f"[{year}년 {round_num}회 이미지 매칭]")
    print(f"{'='*60}")
    
    doc_id = f"{year}_round{round_num}"
    images_dir = Path(f"images/{doc_id}")
    jsonl_path = Path(f"data/items_{doc_id}.jsonl")
    
    if not images_dir.exists():
        print(f"[SKIP] 이미지 폴더 없음: {images_dir}")
        return
    
    if not jsonl_path.exists():
        print(f"[SKIP] JSONL 파일 없음: {jsonl_path}")
        return
    
    # 이미지 파일 목록
    image_files = sorted(list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.jpeg")))
    print(f"\n이미지 파일 {len(image_files)}개:")
    
    # 문제 번호별로 그룹화
    images_by_question = {}
    for img_file in image_files:
        print(f"  - {img_file.name}")
        
        # 파일명에서 문제 번호 추출
        # Q001.png, Q001_1.png, Q001_code.png 등 지원
        match = re.match(r'[Qq]?0*(\d+)', img_file.stem)
        if match:
            q_num = int(match.group(1))
            q_no = f"Q{q_num:03d}"
            
            if q_no not in images_by_question:
                images_by_question[q_no] = []
            
            # 상대 경로
            rel_path = f"images/{doc_id}/{img_file.name}"
            images_by_question[q_no].append(rel_path)
    
    print(f"\n매칭된 문제: {len(images_by_question)}개")
    for q_no, imgs in sorted(images_by_question.items()):
        print(f"  {q_no}: {len(imgs)}개 이미지")
    
    # JSONL 읽기
    questions = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    
    # 이미지 추가/교체
    updated_count = 0
    for q in questions:
        q_no = q['q_no']
        if q_no in images_by_question:
            # 기존 image_refs를 새 이미지로 완전히 교체
            q['image_refs'] = images_by_question[q_no]
            updated_count += 1
            print(f"[업데이트] {q_no}: {images_by_question[q_no]}")
        else:
            # 이미지 없는 경우 빈 배열로
            if 'image_refs' not in q:
                q['image_refs'] = []
    
    # JSONL 저장
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"\n[완료] {updated_count}개 문제 업데이트")
    return updated_count

# 메인 실행
print("="*60)
print("[이미지 매칭 시작]")
print("="*60)

total_updated = 0

# 2025년 1회
total_updated += map_images_for_round(2025, 1)

# 2025년 2회
total_updated += map_images_for_round(2025, 2)

print(f"\n{'='*60}")
print(f"[전체 완료] 총 {total_updated}개 문제 업데이트")
print(f"{'='*60}")




