"""
PMP PDF 파싱 디버그 스크립트 - 첫 번째 문제만 상세 분석
"""

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요: pip install pdfplumber")
    exit(1)

import re
from pathlib import Path

def main():
    pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'
    
    with pdfplumber.open(pdf_path) as pdf:
        # 전체 텍스트 추출
        full_text = ""
        for page in pdf.pages[:10]:  # 처음 10페이지만
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # No. 1 문제 추출
        pattern = r'No\.\s*1\s+(.*?)(?=No\.\s*2|$)'
        match = re.search(pattern, full_text, re.DOTALL)
        
        if match:
            q1_text = match.group(1)
            print("=" * 80)
            print("문제 1 전체 텍스트:")
            print("=" * 80)
            print(q1_text)
            print("\n" + "=" * 80)
            
            # 선택지 추출 시도
            print("\n선택지 추출 시도:")
            print("=" * 80)
            
            patterns = [
                (r'([A-E])\.\s*([^\n]+)', 'A. B. C. 패턴'),
                (r'([A-E])[)]\s*([^\n]+)', 'A) B) C) 패턴'),
            ]
            
            for pattern, desc in patterns:
                choices = re.findall(pattern, q1_text)
                print(f"\n{desc}: {len(choices)}개 발견")
                for i, (letter, text) in enumerate(choices[:5], 1):
                    print(f"  {letter}. {text[:50]}...")

if __name__ == '__main__':
    main()

