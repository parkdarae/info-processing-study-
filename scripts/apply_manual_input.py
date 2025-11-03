# -*- coding: utf-8 -*-
"""
수동 입력한 CSV를 JSONL에 적용하는 스크립트
"""
import json
import csv
from pathlib import Path

def apply_manual_input():
    """CSV 데이터를 JSONL에 적용"""
    manual_dir = Path("data/manual_input")
    data_dir = Path("data")
    
    if not manual_dir.exists():
        print("[ERROR] data/manual_input 폴더가 없습니다.")
        return
    
    csv_files = list(manual_dir.glob("manual_*.csv"))
    
    if not csv_files:
        print("[ERROR] CSV 파일이 없습니다.")
        return
    
    for csv_file in csv_files:
        # 대응하는 JSONL 파일명
        jsonl_name = csv_file.stem.replace('manual_', 'items_') + '.jsonl'
        jsonl_path = data_dir / jsonl_name
        
        if not jsonl_path.exists():
            print(f"[WARNING] {jsonl_name} 파일을 찾을 수 없습니다. 건너뜀.")
            continue
        
        # JSONL 읽기
        questions = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        # CSV 읽기
        manual_data = {}
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_no = row['문제번호']
                manual_data[q_no] = {
                    'ans1': row['답안1'].strip(),
                    'ans2': row['답안2'].strip(),
                    'ans3': row['답안3'].strip(),
                    'explanation': row['해설'].strip()
                }
        
        # 데이터 병합
        updated_count = 0
        for q in questions:
            q_no = q['q_no']
            if q_no in manual_data:
                data = manual_data[q_no]
                
                # 답안 업데이트
                answers = []
                if data['ans1']:
                    answers.append(data['ans1'])
                if data['ans2']:
                    answers.append(data['ans2'])
                if data['ans3']:
                    answers.append(data['ans3'])
                
                if answers:
                    q['answer']['keys'] = answers
                    q['answer']['raw_text'] = '\n'.join(answers)
                    q['meta']['confidence'] = 1.0
                    q['meta']['warnings'] = []
                    updated_count += 1
                
                # 해설 업데이트
                if data['explanation']:
                    q['explanation'] = data['explanation']
        
        # JSONL 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"[OK] 업데이트: {jsonl_name} ({updated_count}/{len(questions)}개 문제)")
    
    print(f"\n총 {len(csv_files)}개 CSV 파일 적용 완료!")

if __name__ == "__main__":
    apply_manual_input()

