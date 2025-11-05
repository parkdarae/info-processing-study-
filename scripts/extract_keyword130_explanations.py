# -*- coding: utf-8 -*-
"""
핵심 키워드 130 문제의 해설 추출 스크립트
PDF 원본에서 텍스트를 추출하여 items.jsonl의 explanation 필드에 매칭
"""
import json
from pathlib import Path
import re
import sys
import io
import shutil

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber가 설치되지 않았습니다.")
    print("다음 명령어로 설치해주세요: pip install pdfplumber")
    sys.exit(1)

def load_jsonl(filepath: Path):
    """JSONL 파일 로드"""
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    questions.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: JSON decode error in line {line_num}: {e}")
                    continue
    return questions

def save_jsonl(filepath: Path, questions: list):
    """JSONL 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for question in questions:
            f.write(json.dumps(question, ensure_ascii=False) + '\n')

def extract_pdf_text(pdf_path: Path):
    """PDF에서 전체 텍스트 추출"""
    print(f"PDF 파일 열기: {pdf_path}")
    
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        print(f"총 {len(pdf.pages)} 페이지")
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text += f"\n[PAGE {page_num}]\n{text}\n"
                print(f"  페이지 {page_num} 추출 완료 ({len(text)} 문자)")
    
    return all_text

def parse_questions_from_pdf(pdf_text: str):
    """
    PDF 텍스트에서 문제별로 분리
    문제 번호 패턴: "1. ", "2. ", ... "130. "
    각 문제는 다음 문제 번호까지의 모든 텍스트를 포함
    """
    # 문제 번호 패턴 찾기 (줄 시작에서 숫자. 형식)
    pattern = r'^(\d+)\.\s+'
    
    questions_dict = {}
    lines = pdf_text.split('\n')
    
    current_q_num = None
    current_content = []
    
    for line in lines:
        # 문제 번호 패턴 매칭
        match = re.match(pattern, line)
        if match:
            # 이전 문제 저장
            if current_q_num is not None:
                questions_dict[current_q_num] = '\n'.join(current_content).strip()
            
            # 새 문제 시작
            current_q_num = int(match.group(1))
            current_content = [line]
        elif current_q_num is not None:
            current_content.append(line)
    
    # 마지막 문제 저장
    if current_q_num is not None:
        questions_dict[current_q_num] = '\n'.join(current_content).strip()
    
    print(f"PDF에서 {len(questions_dict)}개 문제 추출")
    return questions_dict

def extract_explanation_from_content(content: str, question_text: str):
    """
    문제 전체 내용에서 해설 부분만 추출
    전략: 문제 텍스트 이후의 내용을 해설로 간주
    """
    # 문제 텍스트를 기준으로 분리 시도
    # 실제 구현은 PDF 구조에 따라 조정 필요
    
    # 간단한 전략: "해설:", "정답:", "답:" 등의 키워드로 해설 시작 감지
    explanation_markers = [
        r'\n\s*(?:해설|설명|풀이)\s*[:：]\s*',
        r'\n\s*(?:정답|답)\s*[:：]\s*',
        r'\n\s*\[?(?:해설|설명|풀이)\]?\s*\n'
    ]
    
    for marker in explanation_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            explanation = content[match.end():].strip()
            if explanation:
                return explanation
    
    # 해설 마커를 찾지 못한 경우, 문제 텍스트 이후 모든 내용을 해설로 간주
    # 문제 텍스트의 첫 몇 줄을 찾아서 그 이후를 해설로 추출
    question_lines = question_text.strip().split('\n')[:3]  # 첫 3줄
    
    for q_line in question_lines:
        q_line_clean = re.sub(r'^\d+\.\s+', '', q_line.strip())
        if len(q_line_clean) > 10:  # 충분히 긴 줄만 사용
            pos = content.find(q_line_clean)
            if pos != -1:
                # 문제 텍스트 이후 내용 추출
                remaining = content[pos + len(q_line_clean):].strip()
                # "답:", "정답:" 등을 찾아서 그 이후를 해설로
                for marker in [r'(?:정답|답)\s*[:：]\s*', r'(?:해설|설명)\s*[:：]\s*']:
                    match = re.search(marker, remaining, re.IGNORECASE)
                    if match:
                        return remaining[match.end():].strip()
                
                # 마커를 못 찾으면 전체 remaining을 반환
                if len(remaining) > 50:
                    return remaining
    
    # 마지막 폴백: 전체 내용 반환
    return content

def extract_keyword130_explanations(project_root: Path):
    """
    PDF에서 해설을 추출하여 items.jsonl에 업데이트
    """
    pdf_path = project_root / "정보처리기사실기_01_키워드찾기130문제.pdf"
    items_file = project_root / "items.jsonl"
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    if not items_file.exists():
        print(f"Error: items.jsonl not found at {items_file}")
        return
    
    # 백업 생성
    backup_file = items_file.with_suffix('.jsonl.backup_explanations')
    shutil.copy(items_file, backup_file)
    print(f"Backup created: {backup_file}")
    
    # PDF 텍스트 추출
    print("\n" + "=" * 80)
    print("PDF에서 텍스트 추출 중...")
    print("=" * 80)
    pdf_text = extract_pdf_text(pdf_path)
    
    # 문제별로 분리
    print("\n" + "=" * 80)
    print("문제별로 분리 중...")
    print("=" * 80)
    pdf_questions = parse_questions_from_pdf(pdf_text)
    
    # items.jsonl 로드
    questions = load_jsonl(items_file)
    print(f"\nLoaded {len(questions)} questions from items.jsonl")
    
    # 각 문제에 해설 매칭
    print("\n" + "=" * 80)
    print("해설 추출 및 매칭 중...")
    print("=" * 80)
    
    updated_count = 0
    skipped_count = 0
    
    for question in questions:
        q_no = question.get('q_no', '')
        match = re.match(r'Q(\d+)', q_no)
        if not match:
            continue
        
        q_num = int(match.group(1))
        
        if q_num not in pdf_questions:
            print(f"  Warning: {q_no} not found in PDF")
            skipped_count += 1
            continue
        
        pdf_content = pdf_questions[q_num]
        question_text = question.get('question_text', '')
        
        # 해설 추출
        explanation = extract_explanation_from_content(pdf_content, question_text)
        
        if explanation and len(explanation) > 30:
            question['explanation'] = explanation
            updated_count += 1
            print(f"  {q_no}: 해설 추가 ({len(explanation)} 문자)")
        else:
            print(f"  {q_no}: 해설 추출 실패 (내용이 너무 짧거나 없음)")
            skipped_count += 1
    
    # 업데이트된 items.jsonl 저장
    save_jsonl(items_file, questions)
    
    print("\n" + "=" * 80)
    print(f"해설 추출 완료")
    print("=" * 80)
    print(f"총 {len(questions)}개 문제 중:")
    print(f"  - 해설 추가: {updated_count}개")
    print(f"  - 추출 실패/스킵: {skipped_count}개")
    print(f"백업 파일: {backup_file}")
    print("=" * 80)
    print("\nNote: 추출 실패한 문제는 수동으로 PDF를 확인하여 입력해야 합니다.")

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    extract_keyword130_explanations(project_root)

