"""
PDF 형식 디버깅 스크립트 - 실제 문제 형식 확인
"""

import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요: pip install pdfplumber")
    exit(1)

import re
from pathlib import Path

def extract_sample_questions(pdf_path, num_samples=5):
    """PDF에서 샘플 문제 추출하여 형식 확인"""
    
    with pdfplumber.open(pdf_path) as pdf:
        # 첫 50 페이지에서 텍스트 추출
        full_text = ""
        for page in pdf.pages[:50]:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    # 문제 번호 패턴으로 분리
    pattern = r'No\.\s*(\d+)\s+(.*?)(?=No\.\s*\d+|$)'
    matches = list(re.finditer(pattern, full_text, re.MULTILINE | re.DOTALL))
    
    print(f"발견된 문제 수: {len(matches)}개\n")
    print("=" * 80)
    
    # 처음 5개 문제의 원본 텍스트 출력
    for i, match in enumerate(matches[:num_samples], 1):
        q_no = match.group(1)
        q_text = match.group(2).strip()[:1000]  # 첫 1000자만
        
        print(f"\n[문제 {q_no}] 원본 텍스트:")
        print("-" * 80)
        print(q_text)
        print("-" * 80)
        
        # 선택지 패턴 확인
        choice_patterns = [
            (r'([A-E])\.\s*([^\n]+)', 'A. B. C. 형식'),
            (r'([A-E])[)]\s*([^\n]+)', 'A) B) C) 형식'),
            (r'([①②③④⑤])\s*([^\n]+)', '① ② ③ 형식'),
            (r'([1-5])[)]\s*([^\n]+)', '1) 2) 3) 형식'),
        ]
        
        for pattern, desc in choice_patterns:
            choices = re.findall(pattern, q_text)
            if choices:
                print(f"\n✓ 선택지 패턴 발견: {desc}")
                print(f"  발견된 선택지 수: {len(choices)}개")
                for choice in choices[:4]:
                    print(f"  - {choice[0]}: {choice[1][:50]}...")
                break
        else:
            print("\n✗ 선택지 패턴을 찾을 수 없습니다!")
        
        # 정답 패턴 확인
        answer_patterns = [
            r'정답[\s:：]+([A-D, ]+)',
            r'(?:정답|Answer)[\s:：]+([A-D①②③④1-4])',
        ]
        
        for ap in answer_patterns:
            answer_match = re.search(ap, q_text, re.IGNORECASE)
            if answer_match:
                print(f"\n✓ 정답 발견: {answer_match.group(1)}")
                break
        else:
            print("\n✗ 정답을 찾을 수 없습니다!")

def main():
    pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'
    
    if not pdf_path.exists():
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print(f"PDF 파일 분석 중: {pdf_path.name}\n")
    extract_sample_questions(pdf_path, num_samples=10)

if __name__ == '__main__':
    main()

