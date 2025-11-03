# -*- coding: utf-8 -*-
"""[보기] 없는 선택지 가독성 개선"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def improve_choice_readability(text):
    """[보기] 없는 선택지 가독성 개선"""
    if not text:
        return text
    
    # 1. 문장 끝나고 바로 ㄱ. 으로 시작하는 경우 (보기 단어 없음)
    # "...이다. ㄱ.xxx" -> "...이다.\n\n[보기]\n\nㄱ.xxx"
    # "...입니다. ㄱ.xxx" -> "...입니다.\n\n[보기]\n\nㄱ.xxx"
    # "...있다. ㄱ.xxx" -> "...있다.\n\n[보기]\n\nㄱ.xxx"
    
    # 패턴: 문장 종결(다, 다., 요, 요.) 후 공백/줄바꿈 그리고 ㄱ. 이 오는 경우
    if re.search(r'[다요]\s*\.\s*ㄱ\.', text):
        # [보기]가 없고 바로 ㄱ.이 나오는 경우
        if '[보기]' not in text and '보기\n\n' not in text:
            # 문장 끝 후 ㄱ. 앞에 [보기] 삽입
            text = re.sub(
                r'([가-힣])\s*\.\s*\n*\s*(ㄱ\.)',
                r'\1.\n\n[보기]\n\n\2',
                text,
                count=1  # 첫 번째만
            )
    
    # 2. 질문 끝나고 바로 선택지가 나오는 경우
    # "작성하시오. ㄱ.xxx" -> "작성하시오.\n\n[보기]\n\nㄱ.xxx"
    # "쓰시오. ㄱ.xxx" -> "쓰시오.\n\n[보기]\n\nㄱ.xxx"
    if re.search(r'(작성하시오|쓰시오|골라)\s*\.\s*ㄱ\.', text):
        if '[보기]' not in text and '보기\n\n' not in text:
            text = re.sub(
                r'(작성하시오|쓰시오|골라)\s*\.\s*\n*\s*(ㄱ\.)',
                r'\1.\n\n[보기]\n\n\2',
                text,
                count=1
            )
    
    # 3. 영문 보기 (A. B. C.) 패턴
    if re.search(r'[다요]\s*\.\s*A\.', text, re.IGNORECASE):
        if '[보기]' not in text and '보기\n\n' not in text:
            text = re.sub(
                r'([가-힣])\s*\.\s*\n*\s*(A\.)',
                r'\1.\n\n[보기]\n\n\2',
                text,
                count=1,
                flags=re.IGNORECASE
            )
    
    # 4. 숫자 보기 (①, ②, ③) 패턴
    if re.search(r'[다요]\s*\.\s*①', text):
        if '[보기]' not in text and '보기\n\n' not in text:
            text = re.sub(
                r'([가-힣])\s*\.\s*\n*\s*(①)',
                r'\1.\n\n[보기]\n\n\2',
                text,
                count=1
            )
    
    # 5. [보기] 추가 후 선택지들 사이 줄바꿈 확인
    # ㄱ.xxx ㄴ.xxx -> ㄱ.xxx\n\nㄴ.xxx
    text = re.sub(r'(ㄱ\.[^\n]+)\s+(ㄴ\.)', r'\1\n\n\2', text)
    text = re.sub(r'(ㄴ\.[^\n]+)\s+(ㄷ\.)', r'\1\n\n\2', text)
    text = re.sub(r'(ㄷ\.[^\n]+)\s+(ㄹ\.)', r'\1\n\n\2', text)
    text = re.sub(r'(ㄹ\.[^\n]+)\s+(ㅁ\.)', r'\1\n\n\2', text)
    text = re.sub(r'(ㅁ\.[^\n]+)\s+(ㅂ\.)', r'\1\n\n\2', text)
    text = re.sub(r'(ㅂ\.[^\n]+)\s+(ㅅ\.)', r'\1\n\n\2', text)
    text = re.sub(r'(ㅅ\.[^\n]+)\s+(ㅇ\.)', r'\1\n\n\2', text)
    
    # 6. 연속된 빈 줄 3개 이상을 2개로 축소
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def process_all_files():
    """모든 JSONL 파일 처리"""
    data_dir = Path("data")
    jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))
    
    total_files = len(jsonl_files)
    total_improved = 0
    
    print(f"총 {total_files}개 파일 [보기] 없는 선택지 개선 시작...\n")
    
    for jsonl_path in jsonl_files:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            questions = [json.loads(line) for line in f if line.strip()]
        
        improved_count = 0
        improved_questions = []
        
        for q in questions:
            original = q['question_text']
            improved = improve_choice_readability(original)
            
            if original != improved:
                q['question_text'] = improved
                improved_count += 1
                improved_questions.append((q['q_no'], original[:80], improved[:80]))
        
        # 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        if improved_count > 0:
            print(f"✓ {jsonl_path.name}: {improved_count}개 문제 개선")
            for q_no, orig_preview, new_preview in improved_questions[:3]:  # 최대 3개만 미리보기
                print(f"  - {q_no}")
            total_improved += improved_count
        else:
            print(f"  {jsonl_path.name}: 변경 없음")
    
    print(f"\n[OK] 총 {total_improved}개 문제에 [보기] 구분이 추가되었습니다!")

if __name__ == "__main__":
    process_all_files()


