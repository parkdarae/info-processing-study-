#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 가독성 개선 스크립트
- 단어 중간 줄바꿈 제거
- 단락 구분 명확화
- 리스트 항목 정리
- [보기] 섹션 강조
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def improve_readability(text):
    """텍스트 가독성 개선"""
    if not text:
        return text
    
    # 1. 단어 중간 줄바꿈 제거 (한글/영문 1-3글자 사이)
    # 예: "다음은\nDB" → "다음은 DB"
    text = re.sub(r'([가-힣a-zA-Z]{1,3})\n([가-힣a-zA-Z]{1,3})', r'\1 \2', text)
    
    # 2. 연속 줄바꿈 정리 (3개 이상 → 2개)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 3. 괄호와 숫자 정리
    # "- (\n\n1. )" → "- (1.)"
    text = re.sub(r'-\s*\(\s*\n+\s*(\d+\.)', r'\n\n- (\1', text)
    text = re.sub(r'\(\s*\n+\s*(\d+\.)', r'(\1', text)
    
    # 4. 리스트 항목 앞에 줄바꿈 추가
    # "텍스트\n- 항목" → "텍스트\n\n- 항목"
    text = re.sub(r'([^\n])\n([-•]\s)', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\n(\d+\.\s)', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\n([ㄱ-ㅎ]\.\s)', r'\1\n\n\2', text)
    
    # 5. [보기] 섹션 강조
    # "텍스트\n[보기]" → "텍스트\n\n[보기]"
    text = re.sub(r'([^\n])\n(\[보기\])', r'\1\n\n\2', text)
    # "[보기]\n내용" → "[보기]\n\n내용" (단, [보기]\n: 는 제외)
    text = re.sub(r'(\[보기\])\n([^:\n])', r'\1\n\n\2', text)
    
    # 6. 문장 끝 후 줄바꿈 정리
    # "문장.\n다음문장" → "문장.\n다음문장" (유지)
    text = re.sub(r'([.?!])\s*\n\s*([가-힣A-Z])', r'\1\n\2', text)
    
    # 7. 추가: 숫자 뒤 공백 정리
    # "1.)" → "1.)" (유지하되 불필요한 공백 제거)
    text = re.sub(r'(\d+\.)\s+\)', r'\1)', text)
    
    return text.strip()

def process_jsonl_file(file_path):
    """JSONL 파일 처리"""
    print(f"\n처리 중: {file_path}")
    
    # 백업 생성
    backup_path = file_path.parent / f"{file_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    
    # 백업 저장
    with open(backup_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f"  백업 생성: {backup_path.name}")
    
    # 가독성 개선 적용
    improved_count = 0
    for q in questions:
        original = q.get('question_text', '')
        improved = improve_readability(original)
        
        if original != improved:
            q['question_text'] = improved
            improved_count += 1
    
    # 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"  개선된 문제 수: {improved_count}/{len(questions)}")
    return improved_count, len(questions)

def main():
    """메인 실행"""
    data_dir = Path("data")
    
    # 처리할 파일 목록
    jsonl_files = list(data_dir.glob("items_*.jsonl"))
    
    print("=" * 60)
    print("가독성 개선 스크립트 시작")
    print("=" * 60)
    print(f"처리할 파일 수: {len(jsonl_files)}")
    
    total_improved = 0
    total_questions = 0
    
    for file_path in sorted(jsonl_files):
        improved, total = process_jsonl_file(file_path)
        total_improved += improved
        total_questions += total
    
    print("\n" + "=" * 60)
    print("가독성 개선 완료")
    print("=" * 60)
    print(f"총 문제 수: {total_questions}")
    print(f"개선된 문제 수: {total_improved} ({total_improved/total_questions*100:.1f}%)")
    print("\n✅ 모든 파일이 성공적으로 처리되었습니다.")
    print("💾 백업 파일이 data/ 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    main()



