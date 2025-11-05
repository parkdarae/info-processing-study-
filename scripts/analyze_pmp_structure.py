#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import pdfplumber
import re
import json
from pathlib import Path

def analyze_pmp_pdf_structure():
    """PMP PDF 파일 구조 분석"""
    
    pdf_path = r"C:\Users\darae\Desktop\info_ver4\PMP-2025.07.30.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return None
    
    print(f"📄 PMP PDF 분석 시작: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📋 총 페이지 수: {len(pdf.pages)}")
            
            # 첫 10페이지 분석하여 구조 파악
            sample_text = ""
            for i, page in enumerate(pdf.pages[:10]):
                text = page.extract_text()
                if text:
                    sample_text += f"\n=== 페이지 {i+1} ===\n{text}\n"
            
            print("📝 샘플 텍스트 (첫 10페이지):")
            print(sample_text[:2000] + "..." if len(sample_text) > 2000 else sample_text)
            
            # 문제 패턴 분석
            question_patterns = [
                r'\d+\.\s+',  # 1. 2. 3. 형태
                r'Question\s+\d+',  # Question 1 형태
                r'\d+\)',  # 1) 2) 3) 형태
            ]
            
            choice_patterns = [
                r'[A-D]\)',  # A) B) C) D)
                r'[①②③④]',  # 원형 숫자
                r'\([A-D]\)',  # (A) (B) (C) (D)
            ]
            
            answer_patterns = [
                r'Answer:\s*[A-D]',  # Answer: A
                r'정답:\s*[①②③④A-D]',  # 정답: ①
                r'Correct\s*Answer:\s*[A-D]',  # Correct Answer: A
            ]
            
            explanation_patterns = [
                r'Explanation:',  # Explanation:
                r'해설:',  # 해설:
                r'풀이:',  # 풀이:
                r'Reference:',  # Reference:
            ]
            
            # 패턴 매칭 테스트
            print("\n🔍 패턴 분석 결과:")
            for pattern_name, patterns in [
                ("문제 번호", question_patterns),
                ("선택지", choice_patterns), 
                ("정답", answer_patterns),
                ("해설", explanation_patterns)
            ]:
                found_patterns = []
                for pattern in patterns:
                    matches = re.findall(pattern, sample_text, re.IGNORECASE | re.MULTILINE)
                    if matches:
                        found_patterns.append(f"{pattern}: {len(matches)}개")
                
                print(f"  {pattern_name}: {found_patterns if found_patterns else '없음'}")
            
            # 이미지 감지 (간단한 휴리스틱)
            image_indicators = [
                'figure', 'diagram', 'chart', 'graph', 'table',
                '그림', '도표', '차트', '표', '다이어그램'
            ]
            
            image_count = 0
            for indicator in image_indicators:
                matches = len(re.findall(indicator, sample_text, re.IGNORECASE))
                image_count += matches
            
            print(f"\n📊 이미지 관련 키워드: {image_count}개")
            
            return {
                'total_pages': len(pdf.pages),
                'sample_text': sample_text,
                'patterns_found': True,
                'has_images': image_count > 0
            }
            
    except Exception as e:
        print(f"❌ PDF 분석 중 오류: {e}")
        return None

if __name__ == "__main__":
    result = analyze_pmp_pdf_structure()
    if result:
        print("\n✅ PMP PDF 구조 분석 완료")
    else:
        print("\n❌ PMP PDF 구조 분석 실패")
