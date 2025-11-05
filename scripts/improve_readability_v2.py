# -*- coding: utf-8 -*-
"""문제 텍스트 가독성 대폭 개선"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def improve_readability_v2(text):
    """텍스트 가독성 대폭 개선"""
    if not text:
        return text
    
    original = text
    
    # 1. [보기] 패턴 개선 - 앞뒤로 충분한 줄바꿈
    text = re.sub(r'([^\n])\s*\[보기\]', r'\1\n\n[보기]', text)
    text = re.sub(r'\[보기\]\s*([^\n\[])', r'[보기]\n\n\1', text)
    
    # 2. "보기" (괄호 없이) 패턴 개선
    text = re.sub(r'([가-힣])\s*보기\s*([ㄱㄴㄷ])', r'\1\n\n보기\n\n\2', text)
    
    # 3. 선택지 ㄱ. ㄴ. ㄷ. 패턴 줄바꿈
    text = re.sub(r'([^\n])\s*ㄱ\.', r'\1\n\nㄱ.', text)
    text = re.sub(r'([^\n])\s*ㄴ\.', r'\1\n\nㄴ.', text)
    text = re.sub(r'([^\n])\s*ㄷ\.', r'\1\n\nㄷ.', text)
    text = re.sub(r'([^\n])\s*ㄹ\.', r'\1\n\nㄹ.', text)
    text = re.sub(r'([^\n])\s*ㅁ\.', r'\1\n\nㅁ.', text)
    text = re.sub(r'([^\n])\s*ㅂ\.', r'\1\n\nㅂ.', text)
    text = re.sub(r'([^\n])\s*ㅅ\.', r'\1\n\nㅅ.', text)
    text = re.sub(r'([^\n])\s*ㅇ\.', r'\1\n\nㅇ.', text)
    
    # 4. "다음은", "아래는", "다음 설명" 등 뒤에 줄바꿈
    text = re.sub(r'(다음은[^\.]{1,50}이다)\s*\.', r'\1.\n', text)
    text = re.sub(r'(다음은[^\.]{1,50}입니다)\s*\.', r'\1.\n', text)
    text = re.sub(r'(아래는[^\.]{1,50}이다)\s*\.', r'\1.\n', text)
    text = re.sub(r'(아래의[^\.]{1,50}이다)\s*\.', r'\1.\n', text)
    text = re.sub(r'(다음 [^\.]{1,50}이다)\s*\.', r'\1.\n', text)
    text = re.sub(r'(아래 [^\.]{1,50}이다)\s*\.', r'\1.\n', text)
    
    # 5. 질문 시작 전 줄바꿈
    text = re.sub(r'([^\n])\s*\([ ]*①[ ]*\)', r'\1\n\n(①)', text)
    text = re.sub(r'([^\n])\s*\([ ]*1[ ]*\)', r'\1\n\n(1)', text)
    text = re.sub(r'([^\n])\s*①', r'\1\n\n①', text)
    text = re.sub(r'([^\n])\s*\([ ]*ㄱ[ ]*\)', r'\1\n\n(ㄱ)', text)
    
    # 6. "작성하시오", "쓰시오" 뒤에 줄바꿈
    text = re.sub(r'(작성하시오)\.([^\n])', r'\1.\n\n\2', text)
    text = re.sub(r'(쓰시오)\.([^\n])', r'\1.\n\n\2', text)
    text = re.sub(r'(골라[^\n]{0,20}작성하시오)\.', r'\1.\n', text)
    
    # 7. 표 데이터나 구조화된 데이터 앞에 줄바꿈
    text = re.sub(r'([가-힣])\n([가-힣]{2,10}\t)', r'\1\n\n\2', text)
    text = re.sub(r'([가-힣])\n([A-Z][0-9]+\t)', r'\1\n\n\2', text)
    
    # 8. 문제 번호 패턴 (1., 2., 3.) 앞에 줄바꿈
    text = re.sub(r'([^\n])\s*1\.\s+([^\d])', r'\1\n\n1. \2', text)
    text = re.sub(r'([^\n])\s*2\.\s+([^\d])', r'\1\n\n2. \2', text)
    text = re.sub(r'([^\n])\s*3\.\s+([^\d])', r'\1\n\n3. \2', text)
    text = re.sub(r'([^\n])\s*4\.\s+([^\d])', r'\1\n\n4. \2', text)
    
    # 9. 연속된 빈 줄 3개 이상을 2개로 축소
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 10. 마지막 공백 정리
    text = text.strip()
    
    return text

def process_all_files():
    """모든 JSONL 파일 처리"""
    data_dir = Path("data")
    jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))
    
    total_files = len(jsonl_files)
    total_improved = 0
    
    print(f"총 {total_files}개 파일 가독성 재개선 시작...\n")
    
    for jsonl_path in jsonl_files:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            questions = [json.loads(line) for line in f if line.strip()]
        
        improved_count = 0
        for q in questions:
            original = q['question_text']
            improved = improve_readability_v2(original)
            
            if original != improved:
                q['question_text'] = improved
                improved_count += 1
        
        # 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        if improved_count > 0:
            print(f"✓ {jsonl_path.name}: {improved_count}개 문제 재개선")
            total_improved += improved_count
        else:
            print(f"  {jsonl_path.name}: 변경 없음")
    
    print(f"\n[OK] 총 {total_improved}개 문제의 가독성이 추가 개선되었습니다!")

if __name__ == "__main__":
    process_all_files()



