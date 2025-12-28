#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CISSP PDF 텍스트 추출 스크립트
pdfplumber를 사용하여 PDF에서 텍스트를 추출합니다.
"""

import pdfplumber
import os
import re
import sys

# 콘솔 출력 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

def extract_text_from_pdf(pdf_path, output_path):
    """PDF에서 텍스트를 추출하여 파일로 저장"""
    
    if not os.path.exists(pdf_path):
        print(f"[ERROR] PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return False
    
    print(f"[INFO] PDF 파일 열기: {pdf_path}")
    
    all_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"[INFO] 총 {total_pages} 페이지")
            
            for i, page in enumerate(pdf.pages):
                if (i + 1) % 50 == 0 or i == 0:
                    print(f"  페이지 {i+1}/{total_pages} 처리 중...")
                text = page.extract_text()
                if text:
                    all_text.append(f"=== PAGE {i+1} ===\n{text}\n")
            
            print(f"[OK] 텍스트 추출 완료")
    
    except Exception as e:
        print(f"[ERROR] PDF 처리 중 오류: {e}")
        return False
    
    # 텍스트 파일로 저장
    full_text = "\n".join(all_text)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        # 통계 출력
        lines = full_text.split('\n')
        chars = len(full_text)
        
        print(f"[OK] 저장 완료: {output_path}")
        print(f"   - 총 {len(lines):,} 줄")
        print(f"   - 총 {chars:,} 문자")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 파일 저장 중 오류: {e}")
        return False


def analyze_questions(text_path):
    """추출된 텍스트에서 문제 패턴 분석"""
    
    if not os.path.exists(text_path):
        print(f"[ERROR] 텍스트 파일을 찾을 수 없습니다: {text_path}")
        return
    
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 문제 번호 패턴 찾기
    patterns = [
        (r'(?:^|\n)\s*(\d+)\.\s+', "숫자. 형식"),
        (r'(?:^|\n)\s*Q\.?\s*(\d+)', "Q숫자 형식"),
        (r'(?:^|\n)\s*Question\s+(\d+)', "Question 숫자"),
        (r'(?:^|\n)\s*#(\d+)', "#숫자 형식"),
    ]
    
    print("\n[ANALYSIS] 문제 패턴 분석:")
    
    for pattern, desc in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            numbers = [int(m) for m in matches if m.isdigit()]
            if numbers:
                print(f"   {desc}: {len(matches)}개 발견 (범위: {min(numbers)} ~ {max(numbers)})")
    
    # 선택지 패턴 찾기
    choice_patterns = [
        (r'[A-E]\.', "A. 형식"),
        (r'[A-E]\)', "A) 형식"),
        (r'\([A-E]\)', "(A) 형식"),
    ]
    
    print("\n[ANALYSIS] 선택지 패턴 분석:")
    for pattern, desc in choice_patterns:
        matches = re.findall(pattern, text)
        if matches:
            print(f"   {desc}: {len(matches)}개 발견")
    
    # 첫 10줄 샘플 출력
    print("\n[SAMPLE] 텍스트 샘플 (첫 30줄):")
    lines = text.split('\n')[:30]
    for line in lines:
        print(f"   {line[:100]}")


if __name__ == "__main__":
    # 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(base_dir, "CISSP V21.65.pdf")
    output_path = os.path.join(base_dir, "cissp_raw.txt")
    
    print("=" * 60)
    print("CISSP PDF Text Extractor")
    print("=" * 60)
    
    # 텍스트 추출
    success = extract_text_from_pdf(pdf_path, output_path)
    
    if success:
        # 문제 패턴 분석
        analyze_questions(output_path)
        
        print("\n" + "=" * 60)
        print("[DONE] 추출 완료!")
        print(f"[FILE] 출력 파일: {output_path}")
        print("=" * 60)
