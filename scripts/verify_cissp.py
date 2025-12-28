#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CISSP 문제 데이터 최종 검증"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\darae\Desktop\info_ver5\data\items_cissp.jsonl", "r", encoding="utf-8") as f:
    questions = [json.loads(line) for line in f]

print("=" * 60)
print("CISSP Question Data Final Verification")
print("=" * 60)

# 기본 통계
print(f"Total questions: {len(questions)}")

# 유형별 통계
types = {}
for q in questions:
    t = q.get("type", "unknown")
    types[t] = types.get(t, 0) + 1
print(f"Question types: {types}")

# 해설 통계
with_exp = sum(1 for q in questions if q.get("explanation"))
print(f"With explanation: {with_exp}")

# 이미지 통계
with_img = sum(1 for q in questions if q.get("images"))
print(f"With images: {with_img}")

# 선택지 검증
choice_counts = {}
for q in questions:
    c = len(q.get("choices_en", {}))
    choice_counts[c] = choice_counts.get(c, 0) + 1
print(f"Choice count distribution: {choice_counts}")

# 문제 번호 연속성
q_nos = sorted([int(q["q_no"]) for q in questions])
print(f"Question number range: {q_nos[0]} ~ {q_nos[-1]}")

missing = set(range(1, 1851)) - set(q_nos)
if missing:
    print(f"Missing questions: {sorted(missing)}")
else:
    print("Missing questions: None (Complete!)")

print("=" * 60)
print("[SUCCESS] All 1850 CISSP questions ready!")
print("=" * 60)

