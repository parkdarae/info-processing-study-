"""
빠른 병합: 현재 완료된 코드 블록만 병합
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("[빠른 병합] 코드 블록 데이터 병합")
print("="*60)

data_dir = Path("data")
parsed_codes_dir = data_dir / "parsed_codes"

# 코드 블록 데이터 로드
codes_cache = {}
if parsed_codes_dir.exists():
    for json_file in parsed_codes_dir.glob("codes_*.json"):
        doc_id = json_file.stem.replace("codes_", "")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            codes_cache[doc_id] = {item['q_no']: item for item in data}
        print(f"[로드] {doc_id}: {len(data)}개 문제")

print(f"\n총 {len(codes_cache)}개 회차 로드 완료\n")

# JSONL 파일 업데이트
jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))
total_updated = 0

for jsonl_path in jsonl_files:
    doc_id = jsonl_path.stem.replace("items_", "")
    
    if doc_id not in codes_cache:
        continue
    
    print(f"[병합] {jsonl_path.name}")
    
    # 문제 로드
    questions = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    
    # 코드 블록 병합
    updated_count = 0
    for q in questions:
        q_no = q['q_no']
        if q_no in codes_cache[doc_id]:
            q['code_blocks'] = codes_cache[doc_id][q_no]['code_blocks']
            updated_count += 1
        else:
            # 기존에 없으면 빈 배열로 초기화
            if 'code_blocks' not in q:
                q['code_blocks'] = []
    
    # 저장
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"  ✓ {updated_count}개 문제에 코드 블록 추가")
    total_updated += updated_count

print(f"\n{'='*60}")
print(f"[완료] 총 {total_updated}개 문제에 코드 블록 병합 완료")
print(f"{'='*60}")


