# -*- coding: utf-8 -*-
"""
핵심 키워드 130 문제 데이터 검증 스크립트
이미지 누락, 해설 누락, 정답 불일치, 파일 누락 등을 검증
"""
import json
from pathlib import Path
import re
import sys
import io
from datetime import datetime

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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

def validate_keyword130(project_root: Path):
    """
    items.jsonl 데이터 검증 및 리포트 생성
    """
    items_file = project_root / "items.jsonl"
    images_dir = project_root / "images"
    output_file = project_root / "data" / "keyword130_validation_report.json"
    
    if not items_file.exists():
        print(f"Error: items.jsonl not found at {items_file}")
        return
    
    print("=" * 80)
    print("핵심 키워드 130 문제 데이터 검증")
    print("=" * 80)
    
    questions = load_jsonl(items_file)
    print(f"\n총 {len(questions)}개 문제 검증 중...\n")
    
    all_issues = []
    
    # 검증 키워드
    image_keywords = ["아래", "다음", "그림", "표", "도표", "차트", "다이어그램", "코드"]
    
    for question in questions:
        q_no = question.get('q_no', 'N/A')
        question_text = question.get('question_text', '')
        explanation = question.get('explanation', '')
        image_refs = question.get('image_refs', [])
        answer_keys = question.get('answer', {}).get('keys', [])
        
        # 1. 이미지 누락 검증
        has_image_keyword = any(keyword in question_text for keyword in image_keywords)
        if has_image_keyword and not image_refs:
            all_issues.append({
                "priority": 1,
                "q_no": q_no,
                "issue_type": "image_missing",
                "description": "question_text에 이미지 관련 키워드가 있으나 image_refs가 비어있음",
                "current_state": {
                    "question_text_preview": question_text[:100] + "...",
                    "image_refs": image_refs
                },
                "fix_guide": "PDF 페이지를 확인하여 이미지가 필요한지 검토. 필요시 이미지 추출 및 추가"
            })
        
        # 2. 이미지 파일 누락 검증
        for img_ref in image_refs:
            img_path = project_root / img_ref
            if not img_path.exists():
                all_issues.append({
                    "priority": 2,
                    "q_no": q_no,
                    "issue_type": "image_file_missing",
                    "description": f"image_refs에 경로가 있지만 실제 파일이 없음: {img_ref}",
                    "current_state": {
                        "image_ref": img_ref,
                        "expected_path": str(img_path)
                    },
                    "fix_guide": "PDF에서 이미지 추출 또는 image_refs에서 해당 경로 제거"
                })
        
        # 3. 해설 누락 검증
        if not explanation or (isinstance(explanation, str) and len(explanation.strip()) < 30):
            all_issues.append({
                "priority": 3,
                "q_no": q_no,
                "issue_type": "explanation_missing_or_short",
                "description": "해설이 없거나 너무 짧음 (<30자)",
                "current_state": {
                    "explanation_length": len(explanation) if explanation else 0,
                    "explanation": explanation if explanation else None
                },
                "fix_guide": "PDF 원본을 참고하여 상세한 해설 작성"
            })
        
        # 4. 정답 누락 검증
        if not answer_keys:
            all_issues.append({
                "priority": 2,
                "q_no": q_no,
                "issue_type": "answer_missing",
                "description": "answer.keys가 비어있음",
                "current_state": {
                    "answer_keys": answer_keys
                },
                "fix_guide": "PDF 원본을 참고하여 정답 입력"
            })
    
    # 우선순위별로 정렬
    all_issues.sort(key=lambda x: (x['priority'], x['q_no']))
    
    # 통계 계산
    priority_1_count = sum(1 for issue in all_issues if issue['priority'] == 1)
    priority_2_count = sum(1 for issue in all_issues if issue['priority'] == 2)
    priority_3_count = sum(1 for issue in all_issues if issue['priority'] == 3)
    
    # 리포트 생성
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_questions": len(questions),
        "total_issues": len(all_issues),
        "summary": {
            "priority_1_image_missing": priority_1_count,
            "priority_2_file_or_answer_missing": priority_2_count,
            "priority_3_explanation_missing": priority_3_count
        },
        "issues": all_issues
    }
    
    # 리포트 저장
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    print("검증 완료")
    print("=" * 80)
    print(f"총 {len(questions)}개 문제 중 {len(all_issues)}개 이슈 발견")
    print(f"  - 우선순위 1 (이미지 누락): {priority_1_count}개")
    print(f"  - 우선순위 2 (파일 또는 정답 누락): {priority_2_count}개")
    print(f"  - 우선순위 3 (해설 누락): {priority_3_count}개")
    print(f"\n리포트 저장: {output_file}")
    print("=" * 80)
    
    # 상위 10개 이슈 출력
    if all_issues:
        print("\n[우선순위별 상위 이슈 미리보기]")
        for priority in [1, 2, 3]:
            priority_issues = [i for i in all_issues if i['priority'] == priority]
            if priority_issues:
                print(f"\n우선순위 {priority}: {len(priority_issues)}개")
                for issue in priority_issues[:5]:
                    print(f"  - {issue['q_no']}: {issue['description']}")
                if len(priority_issues) > 5:
                    print(f"  ... 외 {len(priority_issues) - 5}개")
    
    return report

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    validate_keyword130(project_root)

