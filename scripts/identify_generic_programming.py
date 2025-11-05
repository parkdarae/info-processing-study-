import json
import re
import csv

# 범용적/추상적 패턴 정의
GENERIC_PATTERNS = [
    r'코드 실행 결과 분석 문제입니다',
    r'문제의 이미지를 참고하여',
    r'일반적인 코드 실행 분석 방법',
    r'변수 선언 및 초기화 상태 확인',
    r'반복문/조건문 실행 순서 추적',
    r'변수 값 변화 추적',
    r'출력문 위치와 순서 확인',
    r'정확한 출력값을 작성합니다',
    r'에 대한 이해를 묻는 문제입니다',
    r'\[답\].*\*\*["\']?\d+["\']?\*\*입니다\.$',  # 정답만 있는 경우
]

def has_generic_pattern(explanation):
    """범용적 패턴이 있는지 확인"""
    if not explanation:
        return True, "해설 없음"
    
    for pattern in GENERIC_PATTERNS:
        if re.search(pattern, explanation):
            return True, f"패턴 발견: {pattern[:30]}"
    
    return False, ""

def calculate_priority(explanation, has_pattern, pattern_reason):
    """우선순위 점수 계산 (높음=3, 중간=2, 낮음=1)"""
    if not explanation or len(explanation) < 100:
        return 3, "해설 매우 짧음 또는 없음"
    
    if has_pattern and len(explanation) < 300:
        return 3, f"범용적 패턴 + 짧은 해설 ({pattern_reason})"
    
    if has_pattern:
        return 2, f"범용적 패턴 발견 ({pattern_reason})"
    
    # 구체적인 실행 추적 요소 확인
    has_table = '|' in explanation and '---' in explanation
    has_steps = re.search(r'(i=\d+|반복 \d+회|단계 \d+)', explanation)
    has_detailed = '→' in explanation or '실행:' in explanation
    
    if not (has_table or has_steps or has_detailed):
        return 2, "단계별 실행 추적 부족"
    
    if len(explanation) < 500:
        return 1, "비교적 짧은 해설"
    
    return 0, "양호한 해설"

def analyze_programming_questions():
    """프로그래밍 문제 분석"""
    
    # 데이터 로드
    with open('data/items_all.jsonl', 'r', encoding='utf-8') as f:
        items = [json.loads(line) for line in f if line.strip()]
    
    # 프로그래밍 카테고리 필터
    programming = [item for item in items if item.get('primary_category') == '프로그래밍']
    
    print(f"Total programming questions: {len(programming)}")
    
    # 분석 결과
    results = []
    
    for item in programming:
        doc_id = item.get('doc_id', 'unknown')
        q_no = item.get('q_no', 'unknown')
        explanation = item.get('explanation', '')
        
        # 회차 정보 추출
        if 'round' in doc_id:
            parts = doc_id.split('_')
            year = parts[0] if len(parts) > 0 else ''
            round_num = parts[1].replace('round', '회') if len(parts) > 1 else ''
            exam_info = f"{year}년 {round_num}"
        else:
            exam_info = doc_id
        
        # 주제 추출 (태그 또는 문제 텍스트에서)
        tags = item.get('tags', [])
        subject = ', '.join(tags) if tags else '일반'
        
        # 범용적 패턴 체크
        has_pattern, pattern_reason = has_generic_pattern(explanation)
        
        # 우선순위 계산
        priority_score, priority_reason = calculate_priority(
            explanation, has_pattern, pattern_reason
        )
        
        if priority_score > 0:  # 개선 필요한 경우만
            priority_text = {3: '높음', 2: '중간', 1: '낮음'}.get(priority_score, '없음')
            
            results.append({
                'priority_score': priority_score,
                'priority': priority_text,
                'doc_id': doc_id,
                'exam_info': exam_info,
                'q_no': q_no,
                'subject': subject,
                'explanation_length': len(explanation),
                'reason': priority_reason,
                'question_preview': item.get('question_text', '')[:100].replace('\n', ' ')
            })
    
    # 우선순위 순으로 정렬
    results.sort(key=lambda x: (-x['priority_score'], x['explanation_length']))
    
    return results

def save_to_csv(results):
    """CSV 파일로 저장"""
    filepath = 'scripts/programming_manual_review_list.csv'
    
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            '우선순위', '문제ID', '회차', '문제번호', '주제', 
            '현재해설길이', '개선사유', '문제미리보기'
        ])
        
        for result in results:
            writer.writerow([
                result['priority'],
                result['doc_id'],
                result['exam_info'],
                result['q_no'],
                result['subject'],
                result['explanation_length'],
                result['reason'],
                result['question_preview']
            ])
    
    print(f"\nCSV 파일 저장 완료: {filepath}")
    return filepath

def print_summary(results):
    """요약 출력"""
    high = sum(1 for r in results if r['priority_score'] == 3)
    medium = sum(1 for r in results if r['priority_score'] == 2)
    low = sum(1 for r in results if r['priority_score'] == 1)
    
    # 파일로 저장
    summary_file = 'scripts/programming_review_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("프로그래밍 문제 해설 개선 필요 목록\n")
        f.write("="*80 + "\n\n")
        f.write(f"총 개선 필요 문제: {len(results)}개\n")
        f.write(f"  - 높음 (긴급): {high}개\n")
        f.write(f"  - 중간 (권장): {medium}개\n")
        f.write(f"  - 낮음 (선택): {low}개\n\n")
        
        f.write("우선순위 높음 문제 (상위 20개):\n")
        f.write("-"*80 + "\n")
        for i, result in enumerate(results[:20], 1):
            f.write(f"{i:2d}. [{result['exam_info']}] {result['q_no']} - {result['subject']}\n")
            f.write(f"    해설길이: {result['explanation_length']}자 | 사유: {result['reason']}\n")
            f.write(f"    문제: {result['question_preview']}\n\n")
    
    print(f"\n요약 파일 저장 완료: {summary_file}")
    print(f"총 개선 필요: {len(results)}개 (높음: {high}, 중간: {medium}, 낮음: {low})")

if __name__ == '__main__':
    results = analyze_programming_questions()
    save_to_csv(results)
    print_summary(results)
    
    # JSON으로도 저장
    with open('scripts/programming_review_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nJSON 파일도 저장되었습니다: scripts/programming_review_analysis.json")

