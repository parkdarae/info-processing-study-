# -*- coding: utf-8 -*-
"""
수동 입력을 위한 CSV 템플릿 생성 스크립트
- 현재 파싱된 문제 구조에서 답안과 해설만 입력할 수 있는 CSV 생성
"""
import json
import csv
from pathlib import Path

def create_manual_input_csv():
    """각 회차별로 수동 입력용 CSV 생성"""
    data_dir = Path("data")
    manual_dir = Path("data/manual_input")
    manual_dir.mkdir(exist_ok=True)
    
    # 모든 JSONL 파일 처리
    jsonl_files = list(data_dir.glob("items_*.jsonl"))
    
    for jsonl_file in jsonl_files:
        questions = []
        
        # JSONL 읽기
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    q = json.loads(line)
                    questions.append(q)
        
        # CSV 생성
        csv_name = jsonl_file.stem.replace('items_', 'manual_') + '.csv'
        csv_path = manual_dir / csv_name
        
        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            
            # 헤더
            writer.writerow([
                '문제번호', 
                '문제내용(처음 100자)', 
                '답안1', 
                '답안2', 
                '답안3', 
                '해설'
            ])
            
            # 각 문제
            for q in questions:
                q_no = q['q_no']
                q_text = q['question_text'][:100].replace('\n', ' ')
                
                # 기존 답안 (있다면)
                existing_answers = q['answer'].get('keys', [])
                ans1 = existing_answers[0] if len(existing_answers) > 0 else ''
                ans2 = existing_answers[1] if len(existing_answers) > 1 else ''
                ans3 = existing_answers[2] if len(existing_answers) > 2 else ''
                
                explanation = q.get('explanation', '') or ''
                
                writer.writerow([
                    q_no,
                    q_text,
                    ans1,
                    ans2,
                    ans3,
                    explanation
                ])
        
        print(f"[OK] 생성: {csv_path} ({len(questions)}개 문제)")
    
    print(f"\n총 {len(jsonl_files)}개 파일에 대한 CSV 생성 완료!")
    print(f"위치: {manual_dir.absolute()}")
    print("\n다음 단계:")
    print("1. Excel에서 CSV 파일 열기")
    print("2. 답안1, 답안2, 답안3, 해설 열에 데이터 입력")
    print("3. CSV 저장")
    print("4. apply_manual_input.py 실행하여 JSONL 업데이트")

if __name__ == "__main__":
    create_manual_input_csv()

