"""
PDF 원본 텍스트 추출 - 처음 5페이지
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요")
    exit(1)

from pathlib import Path

pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'

with pdfplumber.open(pdf_path) as pdf:
    for i in range(min(5, len(pdf.pages))):
        print(f"\n{'='*80}")
        print(f"페이지 {i+1}")
        print('='*80)
        text = pdf.pages[i].extract_text()
        print(text)

