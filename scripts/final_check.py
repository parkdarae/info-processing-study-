# -*- coding: utf-8 -*-
"""전체 진행률 확인"""
import json
import sys
from pathlib import Path

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

data_dir = Path("data")
jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))

total = 0
completed = 0

print("\n" + "="*70)
print(f"{'회차':<20} | {'문제수':>6} | {'완료':>6} | {'진행률':>8}")
print("="*70)

for jsonl_path in jsonl_files:
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    num = len(questions)
    done = sum(1 for q in questions if q['answer']['keys'])
    rate = (done / num * 100) if num > 0 else 0
    
    status = "OK" if rate >= 85 else "--" if rate == 0 else "~"
    name = jsonl_path.stem.replace('items_', '')
    
    print(f"{status} {name:<17} | {num:>6} | {done:>6} | {rate:>7.1f}%")
    
    total += num
    completed += done

print("="*70)
rate_total = (completed / total * 100) if total > 0 else 0
print(f"{'>> 전체':<20} | {total:>6} | {completed:>6} | {rate_total:>7.1f}%")
print("="*70)

print(f"\n진행 상황:")
print(f"  - 완료: {completed}/{total} 문제")
print(f"  - 남은 문제: {total - completed}개")
print(f"  - 전체 진행률: {rate_total:.1f}%")
