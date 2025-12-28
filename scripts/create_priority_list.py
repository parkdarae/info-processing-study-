# -*- coding: utf-8 -*-
"""
우선순위별 수정 대상 리스트 생성
validation_issues.json을 읽어 fix_priority_list.json 생성
"""
import json
from pathlib import Path
import sys
import io

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def create_priority_list():
    """우선순위별 수정 대상 리스트 생성"""
    data_dir = Path(__file__).parent.parent / "data"
    input_path = data_dir / "validation_issues.json"
    
    if not input_path.exists():
        print(f"Error: {input_path} 파일을 찾을 수 없습니다.")
        print("먼저 validate_question_quality.py를 실행하세요.")
        return
    
    # validation_issues.json 로드
    with open(input_path, 'r', encoding='utf-8') as f:
        validation_data = json.load(f)
    
    issues = validation_data.get('issues', [])
    
    # 우선순위별 분류
    priority_1_images = []
    priority_2_answers = []
    priority_3_explanations = []
    
    for issue in issues:
        priority = issue.get('priority')
        issue_type = issue.get('issue_type')
        
        item = {
            "file": issue.get('file'),
            "doc_id": issue.get('doc_id'),
            "q_no": issue.get('q_no'),
            "tistory_url": issue.get('tistory_url'),
            "issue_type": issue_type,
            "description": issue.get('description'),
            "current_state": issue.get('current_state')
        }
        
        if priority == 1:
            item["fix_guide"] = "Tistory 원본 확인 → 이미지 다운로드 → image_refs 추가"
            priority_1_images.append(item)
        elif priority == 2:
            if issue_type == "answer_missing":
                item["fix_guide"] = "Tistory 원본 확인 → 정답 입력 → answer.keys 및 answer.raw_text 수정"
            elif issue_type == "answer_none":
                item["fix_guide"] = "Tistory 원본 확인 → 정답 확인 후 수정"
            elif issue_type == "choices_missing":
                item["fix_guide"] = "Tistory 원본 확인 → 보기 추출 → choices 배열 추가"
            else:
                item["fix_guide"] = "Tistory 원본 확인 → 정답 매칭 확인"
            priority_2_answers.append(item)
        elif priority == 3:
            if issue_type == "poor_quality_explanation":
                score = issue['current_state'].get('quality_score', 0)
                item["quality_score"] = score
                item["fix_guide"] = "Tistory 원본 및 이미지/코드 확인 → 구체적이고 상세한 해설 작성"
            elif issue_type == "explanation_too_short":
                item["fix_guide"] = "Tistory 원본 확인 → 상세한 해설 추가"
            elif issue_type == "question_too_short":
                item["fix_guide"] = "Tistory 원본 확인 → 전체 문제 텍스트 확인"
            else:
                item["fix_guide"] = "해설 품질 개선 필요"
            priority_3_explanations.append(item)
    
    # 우선순위 3은 품질 점수 낮은 순으로 정렬
    priority_3_explanations.sort(key=lambda x: x.get('quality_score', 100))
    
    # 랭크 추가
    for i, item in enumerate(priority_1_images, 1):
        item['rank'] = i
    for i, item in enumerate(priority_2_answers, 1):
        item['rank'] = i
    for i, item in enumerate(priority_3_explanations, 1):
        item['rank'] = i
    
    # 결과 생성
    result = {
        "generated_at": validation_data.get('generated_at'),
        "summary": {
            "total_priority_1": len(priority_1_images),
            "total_priority_2": len(priority_2_answers),
            "total_priority_3": len(priority_3_explanations),
            "total": len(priority_1_images) + len(priority_2_answers) + len(priority_3_explanations)
        },
        "priority_1_images": priority_1_images,
        "priority_2_answers": priority_2_answers,
        "priority_3_explanations": priority_3_explanations
    }
    
    # 파일 저장
    output_path = data_dir / "fix_priority_list.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("=" * 80)
    print("우선순위별 수정 대상 리스트 생성 완료")
    print("=" * 80)
    print(f"우선순위 1 (이미지 누락): {len(priority_1_images)}개")
    print(f"우선순위 2 (정답 불일치): {len(priority_2_answers)}개")
    print(f"우선순위 3 (해설 품질): {len(priority_3_explanations)}개")
    print(f"총 {result['summary']['total']}개")
    print(f"\n결과 저장: {output_path}")
    print("=" * 80)
    
    # 상위 10개 미리보기
    print("\n[우선순위 1 - 이미지 누락 상위 10개]")
    for item in priority_1_images[:10]:
        print(f"  {item['rank']:2d}. {item['file']:<25s} {item['q_no']:<6s} - {item['description']}")
    
    print("\n[우선순위 2 - 정답 불일치 전체]")
    for item in priority_2_answers:
        print(f"  {item['rank']:2d}. {item['file']:<25s} {item['q_no']:<6s} - {item['description']}")
    
    print("\n[우선순위 3 - 해설 품질 상위 10개]")
    for item in priority_3_explanations[:10]:
        score = item.get('quality_score', 'N/A')
        print(f"  {item['rank']:2d}. {item['file']:<25s} {item['q_no']:<6s} (점수: {score}) - {item['description'][:50]}")
    
    return result

if __name__ == "__main__":
    create_priority_list()


