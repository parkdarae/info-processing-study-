"""
누락된 문제 분석 스크립트
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요")
    exit(1)

import re
import json
from pathlib import Path

# 현재 추출된 문제 번호 확인
jsonl_path = Path(__file__).parent.parent / 'data' / 'items_pmp.jsonl'
extracted_q_nos = set()

with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        extracted_q_nos.add(int(data['q_no']))

print(f"추출된 문제 수: {len(extracted_q_nos)}개")
print(f"추출된 문제 번호 범위: {min(extracted_q_nos)} ~ {max(extracted_q_nos)}\n")

# PDF에서 전체 문제 번호 확인
pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# No. X 패턴으로 모든 문제 번호 찾기
all_q_nos = set()
for match in re.finditer(r'No\.\s*(\d+)', full_text):
    q_no = int(match.group(1))
    if 1 <= q_no <= 811:
        all_q_nos.add(q_no)

print(f"PDF 내 전체 문제 수: {len(all_q_nos)}개\n")

# 누락된 문제 찾기
missing_q_nos = sorted(all_q_nos - extracted_q_nos)

print(f"누락된 문제 수: {len(missing_q_nos)}개")
print(f"누락 비율: {len(missing_q_nos)/len(all_q_nos)*100:.1f}%\n")

# 누락된 문제 샘플 분석
print("누락된 문제 샘플 분석 (처음 10개):\n")

IMAGE_INDICATORS = ['figure', 'diagram', 'chart', 'graph', 'table', '그림', '도표', '차트', '표']

for i, q_no in enumerate(missing_q_nos[:10], 1):
    # 해당 문제 텍스트 추출
    pattern = rf'No\.\s*{q_no}\s+(.*?)(?=No\.\s*\d+|정답:|$)'
    match = re.search(pattern, full_text, re.DOTALL)
    
    if match:
        q_text = match.group(1)[:300]  # 처음 300자만
        
        # 이미지 키워드 확인
        has_image_keyword = any(ind in q_text.lower() for ind in IMAGE_INDICATORS)
        
        # 선택지 확인
        choices = re.findall(r'([A-E])\.\s+([^\n]+)', q_text)
        
        print(f"[{i}] 문제 {q_no}:")
        print(f"   이미지 키워드: {'있음' if has_image_keyword else '없음'}")
        print(f"   선택지 개수: {len(choices)}개")
        print(f"   텍스트 샘플: {q_text[:100]}...")
        print()

# 누락 패턴 분석
print("\n누락 패턴 분석:")
print(f"  연속된 누락 구간:")

consecutive_groups = []
current_group = [missing_q_nos[0]] if missing_q_nos else []

for i in range(1, len(missing_q_nos)):
    if missing_q_nos[i] == missing_q_nos[i-1] + 1:
        current_group.append(missing_q_nos[i])
    else:
        if len(current_group) >= 3:
            consecutive_groups.append(current_group)
        current_group = [missing_q_nos[i]]

if len(current_group) >= 3:
    consecutive_groups.append(current_group)

for group in consecutive_groups[:5]:
    print(f"    {group[0]} ~ {group[-1]} ({len(group)}개)")

# 이미지 키워드로 제외된 것 중 실제로는 텍스트 문제일 가능성
print(f"\n개선 제안:")
print(f"  1. 이미지 감지 로직을 더 정확하게 개선")
print(f"  2. 선택지가 있으면 텍스트 문제로 간주")
print(f"  3. 이미지 키워드가 해설에만 있는 경우 구분")

