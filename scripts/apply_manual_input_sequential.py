# -*- coding: utf-8 -*-
"""CSV 데이터를 JSONL에 순차적으로 적용 (행 순서 매칭)"""
import json
import csv
from pathlib import Path

def apply_manual_input_sequential():
    """CSV 데이터를 JSONL에 순차적으로 적용 (문제번호 대신 행 순서 사용)"""
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
        print(f"\n[INFO] {csv_file.name} 처리 중...")
        
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
                questions.append(json.loads(line))
        
        # CSV 읽기 (순차적으로)
        csv_rows = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_rows.append(row)
        
        # 행 개수 확인
        if len(csv_rows) != len(questions):
            print(f"[WARNING] CSV 행 개수({len(csv_rows)})와 JSONL 문제 개수({len(questions)})가 다릅니다!")
            print(f"           최소값({min(len(csv_rows), len(questions))})개만 처리합니다.")
        
        # 순차적으로 매칭 및 업데이트
        updated_count = 0
        for i in range(min(len(csv_rows), len(questions))):
            row = csv_rows[i]
            q = questions[i]
            
            # 답안 처리
            ans_keys = []
            if row['답안1']:
                ans_keys.append(row['답안1'].strip())
            if row['답안2']:
                ans_keys.append(row['답안2'].strip())
            if row['답안3']:
                ans_keys.append(row['답안3'].strip())
            
            explanation_csv = row['해설'].strip() if row['해설'] else None
            
            # 업데이트
            if ans_keys:
                q['answer']['keys'] = ans_keys
                q['answer']['raw_text'] = '\n'.join(ans_keys)
                q['meta']['confidence'] = 1.0
                q['meta']['warnings'] = []
                updated_count += 1
            else:
                # 답안이 없으면 원래 상태 유지 (또는 경고)
                if not q['answer']['keys']:  # 기존에도 답안이 없었다면
                    q['meta']['confidence'] = 0.7
                    q['meta']['warnings'] = ["정답을 찾을 수 없음"]
            
            # 해설 업데이트
            if explanation_csv:
                q['explanation'] = explanation_csv
        
        # JSONL 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"[OK] 업데이트: {jsonl_name} ({updated_count}/{len(questions)}개 문제)")
    
    print(f"\n총 {len(csv_files)}개 CSV 파일 적용 완료!")

if __name__ == "__main__":
    apply_manual_input_sequential()




