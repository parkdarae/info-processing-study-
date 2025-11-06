"""
PMP PDF 구조 확인 스크립트
"""

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요: pip install pdfplumber")
    exit(1)

from pathlib import Path

def main():
    pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'
    
    if not pdf_path.exists():
        print(f"[오류] PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print(f"[확인] PDF 구조 분석 시작: {pdf_path.name}\n")
    
    with pdfplumber.open(pdf_path) as pdf:
        # 첫 5페이지의 텍스트 샘플 추출
        for i in range(min(5, len(pdf.pages))):
            page = pdf.pages[i]
            text = page.extract_text()
            
            print(f"=" * 80)
            print(f"페이지 {i+1} 샘플 (처음 1000자)")
            print("=" * 80)
            print(text[:1000] if text else "[빈 페이지]")
            print("\n")

if __name__ == '__main__':
    main()

