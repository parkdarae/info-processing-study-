# -*- coding: utf-8 -*-
"""
기출문제 품질 자동 검증 스크립트
- 이미지 누락
- 정답 불일치
- 해설 품질
"""
import json
from pathlib import Path
import re
from datetime import datetime
import sys
import io

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# URL 매핑 임포트
from tistory_url_mapping import get_tistory_url

def load_jsonl(filepath):
    """JSONL 파일 로드"""
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    questions.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: JSON decode error in {filepath.name} line {line_num}: {e}")
                    continue
    return questions

def check_image_missing(item, filename):
    """우선순위 1: 이미지 누락 검사"""
    issues = []
    question_text = item.get('question_text', '').lower()
    
    # 이미지가 필요할 것으로 보이는 키워드
    image_keywords = ['아래', '다음 코드', '다음 그림', '다음은 코드', '다음은 java', '다음은 c언어',
                      '다음은 파이썬', '그림', '도표', '다이어그램', '아래 코드', '아래의 코드',
                      '아래 그림', '아래의 그림', '위 코드', '위의 코드']
    
    has_image_keyword = any(keyword in question_text for keyword in image_keywords)
    image_refs = item.get('image_refs', [])
    code_blocks = item.get('code_blocks', [])
    
    # 이미지 키워드가 있는데 image_refs와 code_blocks가 모두 비어있는 경우
    if has_image_keyword and not image_refs and not code_blocks:
        issues.append({
            "priority": 1,
            "issue_type": "image_missing",
            "file": filename,
            "doc_id": item.get('doc_id'),
            "q_no": item.get('q_no'),
            "tistory_url": get_tistory_url(item.get('doc_id')),
            "description": f"question_text에 이미지 관련 키워드가 있으나 image_refs와 code_blocks가 비어있음",
            "current_state": {
                "question_text": item.get('question_text', '')[:100] + "...",
                "image_refs": image_refs,
                "code_blocks_count": len(code_blocks)
            }
        })
    
    return issues

def check_answer_mismatch(item, filename):
    """우선순위 2: 정답 불일치 검사"""
    issues = []
    answer = item.get('answer', {})
    answer_keys = answer.get('keys', [])
    raw_text = answer.get('raw_text', '')
    explanation = item.get('explanation', '')
    
    # 정답이 없는 경우
    if not answer_keys or not raw_text:
        issues.append({
            "priority": 2,
            "issue_type": "answer_missing",
            "file": filename,
            "doc_id": item.get('doc_id'),
            "q_no": item.get('q_no'),
            "tistory_url": get_tistory_url(item.get('doc_id')),
            "description": "answer.keys 또는 answer.raw_text가 비어있음",
            "current_state": {
                "answer_keys": answer_keys,
                "raw_text": raw_text
            }
        })
    
    # "정답 없음"인 경우
    if "정답 없음" in raw_text:
        issues.append({
            "priority": 2,
            "issue_type": "answer_none",
            "file": filename,
            "doc_id": item.get('doc_id'),
            "q_no": item.get('q_no'),
            "tistory_url": get_tistory_url(item.get('doc_id')),
            "description": "answer.raw_text가 '정답 없음'으로 표시됨",
            "current_state": {
                "raw_text": raw_text
            }
        })
    
    return issues

def check_explanation_quality(item, filename):
    """우선순위 3: 해설 품질 검사"""
    issues = []
    explanation = item.get('explanation', '')
    
    # 해설이 너무 짧은 경우 (50자 미만)
    if len(explanation) < 50:
        issues.append({
            "priority": 3,
            "issue_type": "explanation_too_short",
            "file": filename,
            "doc_id": item.get('doc_id'),
            "q_no": item.get('q_no'),
            "tistory_url": get_tistory_url(item.get('doc_id')),
            "description": f"해설이 너무 짧음 ({len(explanation)}자)",
            "current_state": {
                "explanation": explanation,
                "length": len(explanation)
            }
        })
    
    return issues

def check_additional_issues(item, filename):
    """추가 검증"""
    issues = []
    question_text = item.get('question_text', '')
    choices = item.get('choices', [])
    
    # 문제 텍스트가 너무 짧은 경우
    if len(question_text) < 30:
        issues.append({
            "priority": 3,
            "issue_type": "question_too_short",
            "file": filename,
            "doc_id": item.get('doc_id'),
            "q_no": item.get('q_no'),
            "tistory_url": get_tistory_url(item.get('doc_id')),
            "description": f"question_text가 비정상적으로 짧음 ({len(question_text)}자)",
            "current_state": {
                "question_text": question_text,
                "length": len(question_text)
            }
        })
    
    # 객관식인데 choices가 비어있는 경우 (①②③④ 패턴이 있는 경우)
    if re.search(r'[①②③④]', question_text) and not choices:
        issues.append({
            "priority": 2,
            "issue_type": "choices_missing",
            "file": filename,
            "doc_id": item.get('doc_id'),
            "q_no": item.get('q_no'),
            "tistory_url": get_tistory_url(item.get('doc_id')),
            "description": "객관식 문제로 보이나 choices 배열이 비어있음",
            "current_state": {
                "question_text": question_text[:100] + "...",
                "choices": choices
            }
        })
    
    return issues

def load_poor_quality_report():
    """기존 품질 리포트 로드"""
    report_path = Path(__file__).parent.parent / "data" / "poor_quality_explanations_all.json"
    if report_path.exists():
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def validate_all_questions():
    """전체 문제 검증"""
    data_dir = Path(__file__).parent.parent / "data"
    jsonl_files = sorted([f for f in data_dir.glob('items_*.jsonl') 
                          if 'backup' not in f.name and 'all' not in f.name])
    
    all_issues = []
    summary = {
        "priority_1_image": 0,
        "priority_2_answer": 0,
        "priority_3_explanation": 0,
        "total_issues": 0
    }
    
    # 기존 품질 리포트 로드
    poor_quality_report = load_poor_quality_report()
    poor_quality_items = {}
    if poor_quality_report:
        for item in poor_quality_report.get('items', []):
            key = f"{item['file']}_{item['q_no']}"
            poor_quality_items[key] = item
    
    print("=" * 80)
    print("기출문제 품질 자동 검증")
    print("=" * 80)
    
    for jsonl_file in jsonl_files:
        print(f"\n검증 중: {jsonl_file.name}")
        questions = load_jsonl(jsonl_file)
        
        for item in questions:
            # 각 검증 수행
            issues = []
            issues.extend(check_image_missing(item, jsonl_file.name))
            issues.extend(check_answer_mismatch(item, jsonl_file.name))
            issues.extend(check_explanation_quality(item, jsonl_file.name))
            issues.extend(check_additional_issues(item, jsonl_file.name))
            
            # 기존 품질 리포트에서 품질 점수 추가
            key = f"{jsonl_file.name}_{item.get('q_no')}"
            if key in poor_quality_items:
                poor_item = poor_quality_items[key]
                issues.append({
                    "priority": 3,
                    "issue_type": "poor_quality_explanation",
                    "file": jsonl_file.name,
                    "doc_id": item.get('doc_id'),
                    "q_no": item.get('q_no'),
                    "tistory_url": get_tistory_url(item.get('doc_id')),
                    "description": f"해설 품질 점수: {poor_item['quality']['score']}점",
                    "current_state": {
                        "quality_score": poor_item['quality']['score'],
                        "issues": poor_item['quality']['issues'],
                        "explanation_preview": poor_item['explanation_preview']
                    }
                })
            
            # 우선순위별 카운트
            for issue in issues:
                if issue['priority'] == 1:
                    summary['priority_1_image'] += 1
                elif issue['priority'] == 2:
                    summary['priority_2_answer'] += 1
                elif issue['priority'] == 3:
                    summary['priority_3_explanation'] += 1
            
            all_issues.extend(issues)
    
    summary['total_issues'] = len(all_issues)
    
    # 결과 저장
    result = {
        "generated_at": datetime.now().isoformat(),
        "summary": summary,
        "issues": all_issues
    }
    
    output_path = data_dir / "validation_issues.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    print("검증 완료")
    print("=" * 80)
    print(f"총 이슈: {summary['total_issues']}개")
    print(f"  - 우선순위 1 (이미지 누락): {summary['priority_1_image']}개")
    print(f"  - 우선순위 2 (정답 불일치): {summary['priority_2_answer']}개")
    print(f"  - 우선순위 3 (해설 품질): {summary['priority_3_explanation']}개")
    print(f"\n결과 저장: {output_path}")
    print("=" * 80)
    
    return result

if __name__ == "__main__":
    validate_all_questions()

