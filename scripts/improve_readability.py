# -*- coding: utf-8 -*-
"""문제 텍스트 가독성 개선"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def improve_readability(text):
    """텍스트 가독성 개선"""
    if not text:
        return text
    
    # [보기] 앞뒤에 줄바꿈 추가 (이미 줄바꿈이 있으면 중복 방지)
    text = re.sub(r'([^\n])\[보기\]', r'\1\n\n[보기]', text)
    text = re.sub(r'\[보기\]([^\n])', r'[보기]\n\n\1', text)
    
    # 보기 (괄호 없이) 앞뒤에 줄바꿈 추가
    text = re.sub(r'([^\n])\n보기\n', r'\1\n\n보기\n\n', text)
    
    # "다음 설명", "다음 내용", "다음 표" 등 뒤에 줄바꿈 추가
    text = re.sub(r'(다음 [^\n]{0,30}이다\.)', r'\1\n', text)
    text = re.sub(r'(다음 [^\n]{0,30}입니다\.)', r'\1\n', text)
    
    # "아래 내용", "아래 표" 등 뒤에 줄바꿈 추가
    text = re.sub(r'(아래 [^\n]{0,30}이다\.)', r'\1\n', text)
    text = re.sub(r'(아래 [^\n]{0,30}입니다\.)', r'\1\n', text)
    
    # 표 데이터 앞에 줄바꿈 추가 (탭이나 여러 공백이 연속되는 경우)
    text = re.sub(r'([가-힣])\t', r'\1\n\n', text)
    
    # "다음을 참고하여", "다음을 보고" 등 뒤에 줄바꿈
    text = re.sub(r'(참고하여|보고|확인하여)([^\n])', r'\1\n\n\2', text)
    
    # 괄호로 시작하는 질문 앞에 줄바꿈 추가
    text = re.sub(r'([^\n])\n\([ ]*①', r'\1\n\n(①', text)
    text = re.sub(r'([^\n])\n\([ ]*1\)', r'\1\n\n(1)', text)
    
    # 연속된 빈 줄 3개 이상을 2개로 축소
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def process_all_files():
    """모든 JSONL 파일 처리"""
    data_dir = Path("data")
    jsonl_files = sorted(list(data_dir.glob("items_*.jsonl")))
    
    total_files = len(jsonl_files)
    total_improved = 0
    
    print(f"총 {total_files}개 파일 처리 시작...\n")
    
    for jsonl_path in jsonl_files:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            questions = [json.loads(line) for line in f if line.strip()]
        
        improved_count = 0
        for q in questions:
            original = q['question_text']
            improved = improve_readability(original)
            
            if original != improved:
                q['question_text'] = improved
                improved_count += 1
        
        # 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        if improved_count > 0:
            print(f"✓ {jsonl_path.name}: {improved_count}개 문제 개선")
            total_improved += improved_count
        else:
            print(f"  {jsonl_path.name}: 변경 없음")
    
    print(f"\n[OK] 총 {total_improved}개 문제의 가독성이 개선되었습니다!")

if __name__ == "__main__":
    process_all_files()




