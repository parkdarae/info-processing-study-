"""
2025년 1회 이미지를 JSONL에 추가
"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("[2025년 1회 이미지 추가]")
print("="*60)

# 이미지 폴더 확인
images_dir = Path("images/2025_round1")
if not images_dir.exists():
    print(f"[ERROR] 이미지 폴더가 없습니다: {images_dir}")
    sys.exit(1)

# 이미지 파일 목록
image_files = sorted(list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg")))
print(f"\n총 {len(image_files)}개 이미지 파일 발견\n")

# 문제 번호별로 그룹화
images_by_question = {}
for img_file in image_files:
    # 파일명에서 문제 번호 추출: Q001_1.png, Q005.png 등
    match = re.match(r'Q(\d+)', img_file.stem)
    if match:
        q_no = f"Q{match.group(1)}"
        if q_no not in images_by_question:
            images_by_question[q_no] = []
        # 상대 경로로 저장
        rel_path = f"images/2025_round1/{img_file.name}"
        images_by_question[q_no].append(rel_path)
        print(f"  {q_no}: {img_file.name}")

print(f"\n총 {len(images_by_question)}개 문제에 이미지 추가\n")

# JSONL 파일 읽기
jsonl_path = Path("data/items_2025_round1.jsonl")
questions = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            questions.append(json.loads(line))

# 이미지 추가
updated_count = 0
for q in questions:
    q_no = q['q_no']
    if q_no in images_by_question:
        # 기존 image_refs와 병합 (중복 제거)
        existing_images = set(q.get('image_refs', []))
        new_images = set(images_by_question[q_no])
        all_images = sorted(list(existing_images | new_images))
        
        q['image_refs'] = all_images
        updated_count += 1
        print(f"[추가] {q_no}: {len(all_images)}개 이미지")

# JSONL 저장
with open(jsonl_path, 'w', encoding='utf-8') as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"\n{'='*60}")
print(f"[완료] {updated_count}개 문제에 이미지 추가됨")
print(f"{'='*60}")
print(f"\n파일: {jsonl_path.absolute()}")




