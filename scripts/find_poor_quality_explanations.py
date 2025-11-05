# -*- coding: utf-8 -*-
"""
해설 품질이 낮은 문제 찾기 스크립트
범용적이거나 실질적이지 않은 해설을 찾아 개선이 필요한 항목을 식별합니다.
"""
# -*- coding: utf-8 -*-
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

def load_jsonl(filepath: Path):
    """JSONL 파일 로드"""
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    return questions

def analyze_explanation_quality(explanation, question_text=""):
    """해설 품질 분석"""
    if not explanation:
        return {"score": 0, "issues": ["해설 없음"], "is_poor": True}
    
    explanation_str = str(explanation).strip()
    issues = []
    score = 100
    
    # 1. 너무 짧은 해설 (20자 미만)
    if len(explanation_str) < 20:
        issues.append("너무 짧음")
        score -= 50
    elif len(explanation_str) < 50:
        issues.append("다소 짧음")
        score -= 20
    
    # 2. 범용적인 문구 확인
    generic_phrases = [
        "이 문제는 변수의 값 변화를 추적하는 문제입니다",
        "이 문제는 데이터베이스 분야의 개념을 이해하는 문제입니다",
        "이 문제는.*이해하는 문제입니다",  # 정규식 패턴
        "문제에서 설명한 내용과 특징을 정확히 분석하면",
        "코드의 실제 내용에 따라 구체적인 해설을 작성해야 합니다",
        "답이",
        "최종 출력값",
        "모든 연산을 완료한 후",
        "코드 실행 단계:",
        "초기 상태 확인",
        "메서드 호출 분석",
        "반복문/조건문 추적",
        "연산 수행",
        "최종 출력 계산",
        "변수의 초기값부터 시작하여",
        "코드의 실제 내용에 따라",
        "코드의 실제 내용.*에 따라",
        "구체적인 해설을 작성해야 합니다",
        "문제 요구사항:",
        "분석:",
        "답:"
    ]
    
    # 정규식 패턴과 일반 문자열 패턴 분리
    regex_patterns = [p for p in generic_phrases if '.*' in p or p.startswith('^') or p.endswith('$')]
    string_patterns = [p for p in generic_phrases if p not in regex_patterns]
    
    # 일반 문자열 매칭
    generic_count = sum(1 for phrase in string_patterns if phrase in explanation_str)
    
    # 정규식 매칭
    for pattern in regex_patterns:
        if re.search(pattern.replace('.*', '.*'), explanation_str):
            generic_count += 1
    
    if generic_count >= 3:
        issues.append("범용적인 설명 문구 과다")
        score -= 30
    elif generic_count >= 2:
        issues.append("범용적인 설명 문구 다수")
        score -= 15
    elif generic_count >= 1:
        issues.append("범용적인 설명 문구 사용")
        score -= 10
    
    # 3. 문제와 연관성이 없는 해설
    if question_text:
        question_keywords = set(re.findall(r'[가-힣]+', question_text[:100]))
        explanation_keywords = set(re.findall(r'[가-힣]+', explanation_str))
        common_keywords = question_keywords & explanation_keywords
        
        if len(common_keywords) < 2 and len(question_keywords) > 5:
            issues.append("문제 내용과 연관성 부족")
            score -= 40
    
    # 4. 단순 나열이나 키워드만 있음
    if len(explanation_str.split('\n')) > 10 and len(explanation_str.split()) < 30:
        issues.append("과도하게 나열된 형식")
        score -= 20
    
    # 5. 구체적인 설명 부족 (예시, 계산 과정 등)
    has_detail = any(word in explanation_str for word in ['예:', '예시', '예를 들어', '계산', '과정', '단계', '실행'])
    if not has_detail and len(explanation_str) > 50:
        issues.append("구체적인 설명 부족")
        score -= 20
    
    is_poor = score < 60 or len(issues) >= 2
    
    return {
        "score": max(0, score),
        "issues": issues,
        "is_poor": is_poor,
        "length": len(explanation_str)
    }

def find_poor_quality_explanations():
    """2025~2021 전체 회차 해설 품질 분석"""
    data_dir = Path("data")
    
    # 2025~2021 모든 회차 파일 찾기
    target_files = []
    for year in range(2021, 2026):
        for round_num in range(1, 4):
            filename = f"items_{year}_round{round_num}.jsonl"
            filepath = data_dir / filename
            if filepath.exists():
                target_files.append(filename)
    
    poor_quality = []
    
    for filename in sorted(target_files):
        filepath = data_dir / filename
        if not filepath.exists():
            continue
        
        questions = load_jsonl(filepath)
        
        for q in questions:
            explanation = q.get('explanation')
            question_text = q.get('question_text', '')
            
            quality = analyze_explanation_quality(explanation, question_text)
            
            if quality['is_poor']:
                poor_quality.append({
                    'file': filename,
                    'q_no': q.get('q_no'),
                    'doc_id': q.get('doc_id'),
                    'question_text': question_text[:200],  # 전체 텍스트 일부
                    'question_full': question_text,  # 전체 텍스트
                    'explanation_current': str(explanation) if explanation else None,
                    'explanation_preview': str(explanation)[:200] if explanation else None,
                    'image_refs': q.get('image_refs', []),
                    'code_blocks': q.get('code_blocks', []),
                    'table_refs': q.get('table_refs', []),
                    'answer': q.get('answer', {}),
                    'primary_category': q.get('primary_category'),
                    'quality': quality
                })
    
    return poor_quality

def main():
    print("=" * 80)
    print("해설 품질 분석: 범용적이거나 실질적이지 않은 해설 찾기")
    print("=" * 80)
    
    poor_quality = find_poor_quality_explanations()
    
    if not poor_quality:
        print("\n[결과] 품질이 낮은 해설을 찾지 못했습니다.")
        return
    
    print(f"\n[발견] 품질이 낮은 해설: {len(poor_quality)}개")
    print("=" * 80)
    
    # 파일별로 그룹화
    by_file = {}
    for item in poor_quality:
        filename = item['file']
        if filename not in by_file:
            by_file[filename] = []
        by_file[filename].append(item)
    
    for filename, items in by_file.items():
        print(f"\n[{filename}]")
        print("-" * 80)
        
        for item in items:
            print(f"\n{item['q_no']}:")
            print(f"  문제: {item['question_text']}...")
            if item.get('explanation_preview'):
                print(f"  해설: {item['explanation_preview']}...")
            else:
                print(f"  해설: (해설 없음)")
            print(f"  품질 점수: {item['quality']['score']}/100")
            print(f"  이슈: {', '.join(item['quality']['issues'])}")
            print(f"  길이: {item['quality']['length']}자")
    
    # 리포트 저장
    report = {
        "version": "2.0",
        "generated_at": datetime.now().isoformat(),
        "total": len(poor_quality),
        "stats": {
            "by_file": {},
            "by_issue_type": {}
        },
        "items": poor_quality
    }
    
    # 파일별 통계
    for item in poor_quality:
        filename = item['file']
        if filename not in report['stats']['by_file']:
            report['stats']['by_file'][filename] = 0
        report['stats']['by_file'][filename] += 1
        
        # 이슈 타입별 통계
        for issue in item['quality']['issues']:
            if issue not in report['stats']['by_issue_type']:
                report['stats']['by_issue_type'][issue] = 0
            report['stats']['by_issue_type'][issue] += 1
    
    report_path = Path("data/poor_quality_explanations_all.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장] 리포트: {report_path}")
    print(f"[통계] 파일별: {len(report['stats']['by_file'])}개 파일")
    print(f"[통계] 이슈 유형: {len(report['stats']['by_issue_type'])}개 유형")
    print("=" * 80)

if __name__ == "__main__":
    main()

