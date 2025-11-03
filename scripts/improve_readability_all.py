# -*- coding: utf-8 -*-
"""
2021~2025년 전체 문제 가독성 개선 스크립트
문제 텍스트, 선택지, 해설의 가독성을 개선합니다.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

def normalize_text(text: str) -> str:
    """텍스트 가독성 개선"""
    if not text:
        return text
    
    # 불필요한 줄바꿈 제거 (단어 중간 줄바꿈)
    # 예: "DB\n설계" → "DB 설계"
    text = re.sub(r'([가-힣a-zA-Z0-9])\n([가-힣a-zA-Z0-9])', r'\1 \2', text)
    
    # 연속된 줄바꿈 정리 (3개 이상 → 2개)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 각 줄의 앞뒤 공백 제거
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)
    
    # 빈 줄 정리 (2개 연속 이상 → 2개로 통일)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # 불필요한 공백 정리 (2개 이상 공백 → 1개)
    text = re.sub(r' {2,}', ' ', text)
    
    # 특정 패턴 정리
    # "보완" → "보안" (오타 수정)
    text = re.sub(r'보완에\s*관련된', '보안에 관련된', text)
    text = re.sub(r'네트워크\s*보완', '네트워크 보안', text)
    
    # 중복 단어 제거 (예: "공격 공격" → "공격")
    text = re.sub(r'(\S+)\s+\1\b', r'\1', text)
    
    # "공격 공격" → "공격" (더 정확한 패턴)
    text = re.sub(r'공격\s+공격', '공격', text)
    
    # "괄호안에" → "괄호 안에" (띄어쓰기)
    text = re.sub(r'괄호안에', '괄호 안에', text)
    text = re.sub(r'괄호\(', '괄호 (', text)
    
    # "보기에" → "보기에서" (일관성)
    # text = re.sub(r'보기에', '보기에서', text)  # 너무 강력할 수 있음
    
    # 문장 끝 공백 제거
    text = text.strip()
    
    return text

def normalize_question_text(question_text: str) -> str:
    """문제 텍스트 가독성 개선"""
    if not question_text:
        return question_text
    
    # 기본 정규화
    text = normalize_text(question_text)
    
    # 문제 번호 제거 (이미 별도 필드에 있음)
    text = re.sub(r'^\d+\.\s*', '', text)
    
    # "다음은" 다음 줄바꿈 정리
    text = re.sub(r'다음은\s*\n', '다음은 ', text)
    
    # 보기 표시 정리
    text = re.sub(r'\[보기\]\s*\n\s*\n', '[보기]\n\n', text)
    
    # 번호 목록 정리
    # "- (1.)" 패턴 정리
    text = re.sub(r'-\s*\(\s*(\d+)\s*\.?\s*\)', r'- (\1)', text)
    
    return text

def normalize_choices(choices: list) -> list:
    """선택지 가독성 개선"""
    if not choices:
        return choices
    
    normalized = []
    for choice in choices:
        if not choice:
            continue
        
        # 기본 정규화
        normalized_choice = normalize_text(str(choice))
        
        # 선택지 번호 형식 통일
        # "①", "1.", "(1)" 등을 정리 (원본 형식 유지하되 공백 정리)
        normalized_choice = re.sub(r'(\S)\s*([①-④ㄱ-ㅎ])', r'\1 \2', normalized_choice)
        
        normalized.append(normalized_choice)
    
    return normalized

def normalize_explanation(explanation: str) -> str:
    """해설 가독성 개선"""
    if not explanation:
        return explanation
    
    # 기본 정규화
    text = normalize_text(explanation)
    
    # 마크다운 스타일 정리
    # "**텍스트**" 패턴 유지하되 앞뒤 공백 정리
    text = re.sub(r'\*\*([^\*]+)\*\*', r'**\1**', text)
    
    # 번호 목록 정리
    text = re.sub(r'(\d+)\.\s+', r'\1. ', text)
    
    return text

def improve_question_readability(q: Dict[str, Any]) -> Dict[str, Any]:
    """개별 문제 가독성 개선"""
    improved = q.copy()
    
    # 문제 텍스트 개선
    if 'question_text' in improved:
        improved['question_text'] = normalize_question_text(improved['question_text'])
    
    # 선택지 개선
    if 'choices' in improved and improved['choices']:
        improved['choices'] = normalize_choices(improved['choices'])
    
    # 해설 개선
    if 'explanation' in improved and improved['explanation']:
        improved['explanation'] = normalize_explanation(improved['explanation'])
    
    # 답안 텍스트 정리
    if 'answer' in improved:
        if 'raw_text' in improved['answer']:
            improved['answer']['raw_text'] = normalize_text(improved['answer']['raw_text'])
        
        if 'keys' in improved['answer']:
            improved['answer']['keys'] = [normalize_text(str(k)) for k in improved['answer']['keys']]
    
    # 메타데이터 업데이트
    if 'meta' not in improved:
        improved['meta'] = {}
    
    improved['meta']['readability_improved'] = datetime.now().isoformat()
    
    return improved

def improve_file_readability(filepath: Path) -> int:
    """파일 단위 가독성 개선"""
    print(f"[처리 중] {filepath.name}")
    
    # JSONL 읽기
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    
    # 각 문제 개선
    improved_questions = []
    for q in questions:
        improved_q = improve_question_readability(q)
        improved_questions.append(improved_q)
    
    # 백업 생성
    backup_dir = filepath.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"{filepath.stem}_before_readability_{timestamp}{filepath.suffix}"
    
    import shutil
    shutil.copy2(filepath, backup_path)
    
    # 개선된 데이터 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        for q in improved_questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"  [완료] {len(questions)}개 문제 개선")
    return len(questions)

def main():
    print("=" * 80)
    print("2021~2025년 전체 문제 가독성 개선")
    print("=" * 80)
    
    data_dir = Path("data")
    
    # 2021~2025년 모든 JSONL 파일 찾기
    target_files = []
    for year in range(2021, 2026):
        for round_num in range(1, 4):
            filename = f"items_{year}_round{round_num}.jsonl"
            filepath = data_dir / filename
            if filepath.exists():
                target_files.append(filepath)
    
    # items_all.jsonl도 포함
    all_file = data_dir / "items_all.jsonl"
    if all_file.exists():
        target_files.append(all_file)
    
    if not target_files:
        print("[오류] 처리할 파일이 없습니다.")
        return
    
    print(f"\n[발견] 총 {len(target_files)}개 파일")
    print("-" * 80)
    
    total_questions = 0
    for filepath in sorted(target_files):
        count = improve_file_readability(filepath)
        total_questions += count
    
    print("\n" + "=" * 80)
    print(f"[완료] 총 {len(target_files)}개 파일, {total_questions}개 문제 가독성 개선 완료")
    print("=" * 80)
    print("\n개선 항목:")
    print("  - 불필요한 줄바꿈 제거")
    print("  - 공백 정리")
    print("  - 오타 수정 (보완 → 보안)")
    print("  - 중복 단어 제거")
    print("  - 선택지 형식 통일")
    print("=" * 80)

if __name__ == "__main__":
    main()

