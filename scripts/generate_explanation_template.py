#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
해설 작성용 마크다운 템플릿 생성
각 회차별로 해설 작성을 위한 템플릿 파일 생성
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def classify_explanation(explanation):
    """해설을 완전/부족/없음으로 분류"""
    if explanation is None:
        return "없음", True
    
    explanation_str = str(explanation).strip()
    
    if not explanation_str or len(explanation_str) < 10:
        return "없음", True
    
    # 50자 이상이고 구체적인 설명이 있는 경우
    if len(explanation_str) >= 50:
        if any(word in explanation_str for word in ['은', '는', '이', '가', '을', '를', '한다', '합니다', '이다', '입니다', '에서', '의']):
            return "완전", False
    
    # 10~50자 사이이거나 단순 키워드/약자인 경우
    if len(explanation_str) < 50:
        simple_keywords = ['Session Hijacking', '제약조건', 'SQL JOIN 결과', 'CRC', 'OSPF', 'Cyclic Redundancy Check', 'Adapter 패턴']
        if explanation_str in simple_keywords or len(explanation_str.split()) <= 3:
            return "부족", True
        elif len(explanation_str) >= 30:
            return "완전", False
        else:
            return "부족", True
    
    return "완전", False

def get_code_block_content(code_blocks):
    """코드 블록 내용 반환"""
    if not code_blocks:
        return None
    
    # 첫 번째 코드 블록 사용
    cb = code_blocks[0]
    language = cb.get('language', 'unknown')
    code = cb.get('code', '')
    
    return {
        'language': language,
        'code': code,
        'line_numbers': cb.get('line_numbers', [])
    }

def generate_template(jsonl_file, year, round_num, output_dir):
    """단일 회차 템플릿 생성"""
    items = []
    
    if not jsonl_file.exists():
        return None
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                q = json.loads(line)
                
                explanation = q.get('explanation')
                classification, needs_work = classify_explanation(explanation)
                
                # 해설이 필요한 문제만 포함
                if needs_work:
                    # 이미지 참조
                    image_refs = q.get('image_refs', [])
                    images_str = ', '.join(image_refs) if image_refs else '없음'
                    
                    # 코드 블록
                    code_blocks = q.get('code_blocks', [])
                    code_info = get_code_block_content(code_blocks)
                    code_language = code_info['language'] if code_info else '없음'
                    
                    # 답안
                    answer = q.get('answer', {})
                    answer_keys = answer.get('keys', [])
                    answer_str = '\n'.join(str(k) for k in answer_keys) if answer_keys else ''
                    
                    items.append({
                        'q_no': q.get('q_no', ''),
                        'question_text': q.get('question_text', ''),
                        'answer': answer_str,
                        'current_explanation': str(explanation) if explanation else '',
                        'classification': classification,
                        'images': images_str,
                        'code_info': code_info,
                        'code_language': code_language,
                        'table_refs': q.get('table_refs', [])
                    })
            except json.JSONDecodeError:
                continue
    
    if not items:
        return None
    
    # 마크다운 템플릿 생성
    template_content = f"""# {year}년 {round_num}회 해설 작성

총 {len(items)}개 문제의 해설 작성이 필요합니다.

---

"""
    
    for item in items:
        q_no = item['q_no']
        question_text = item['question_text']
        answer = item['answer']
        current_explanation = item['current_explanation']
        classification = item['classification']
        images = item['images']
        code_info = item['code_info']
        table_refs = item['table_refs']
        
        template_content += f"""## {q_no}

**문제**:
```
{question_text}
```

**답안**:
```
{answer}
```

**현재 해설**: {current_explanation if current_explanation else '없음'}

**상태**: {'⚠️ 부족' if classification == '부족' else '❌ 없음'} ({classification})

**이미지**: {images}

"""
        
        # 코드 블록이 있으면 표시
        if code_info:
            template_content += f"""**코드 언어**: {code_info['language']}

**코드**:
```{code_info['language']}
{code_info['code']}
```

"""
        
        # 테이블 참조가 있으면 표시
        if table_refs:
            template_content += f"""**테이블**: {', '.join(str(t.get('id', '')) for t in table_refs)}

"""
        
        template_content += """**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

"""
    
    # 파일 저장
    template_filename = f"explanations_template_{year}_round{round_num}.md"
    template_filepath = output_dir / template_filename
    
    with open(template_filepath, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    return template_filepath

def main():
    """메인 함수"""
    data_dir = Path("data")
    output_dir = Path("data/manual_input")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 분석 대상 회차
    target_rounds = [
        ('2025', '1'), ('2025', '2'),
        ('2024', '1'), ('2024', '2'), ('2024', '3'),
        ('2023', '1'), ('2023', '2'), ('2023', '3'),
        ('2022', '1'), ('2022', '2'), ('2022', '3')
    ]
    
    print("=" * 80)
    print("해설 작성용 마크다운 템플릿 생성")
    print("=" * 80)
    print()
    
    generated_files = []
    
    for year, round_num in target_rounds:
        filename = f"items_{year}_round{round_num}.jsonl"
        jsonl_file = data_dir / filename
        
        template_path = generate_template(jsonl_file, year, round_num, output_dir)
        
        if template_path:
            generated_files.append(template_path)
            print(f"✅ {year}년 {round_num}회 템플릿 생성: {template_path}")
        else:
            print(f"⚠️  {year}년 {round_num}회: 해설이 필요한 문제 없음")
    
    print()
    print("=" * 80)
    print(f"총 {len(generated_files)}개 템플릿 파일 생성 완료")
    print("=" * 80)
    print()
    print("💡 사용 방법:")
    print("   1. 각 템플릿 파일을 열어 해설을 작성하세요")
    print("   2. 작성 완료 후 CSV 형식으로 변환하거나")
    print("   3. 직접 apply_explanations.py 스크립트를 사용하여 적용하세요")

if __name__ == "__main__":
    main()


