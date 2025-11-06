"""
PMP 데이터 품질 점검 스크립트
- 가독성 (띄어쓰기, 문장 구조)
- 정합성 (문제-선택지-정답 일치)
- 완성도 (필수 필드 존재)
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import re
from pathlib import Path
from collections import defaultdict

jsonl_path = Path(__file__).parent.parent / 'data' / 'items_pmp.jsonl'

questions = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        questions.append(json.loads(line))

print(f"총 {len(questions)}개 문제 점검 시작\n")
print("="*80)

# 점검 결과 저장
issues = defaultdict(list)
stats = {
    'total': len(questions),
    'valid': 0,
    'has_explanation': 0,
    'good_readability': 0
}

for i, q in enumerate(questions, 1):
    q_no = q['q_no']
    issue_list = []
    
    # 1. 필수 필드 점검
    if not q.get('question') or len(q['question']) < 10:
        issue_list.append("문제 본문이 너무 짧음")
    
    if not q.get('options') or len(q['options']) != 4:
        issue_list.append(f"선택지 개수 오류: {len(q.get('options', []))}개")
    
    if not q.get('answer') or q['answer'] not in ['A', 'B', 'C', 'D']:
        issue_list.append(f"정답 형식 오류: {q.get('answer')}")
    
    # 2. 정답-선택지 정합성
    if q.get('answer') and q.get('options'):
        answer_idx = ord(q['answer']) - ord('A')
        if answer_idx < len(q['options']):
            option_text = q['options'][answer_idx]
            # 선택지에서 "A. " 제거 후 비교
            option_content = re.sub(r'^[A-D]\.\s*', '', option_text)
            if q.get('answer_text') and q['answer_text'] not in option_content:
                if len(q['answer_text']) > 10:  # 너무 짧은 텍스트는 제외
                    issue_list.append("정답 텍스트가 선택지와 불일치")
    
    # 3. 가독성 점검
    question_text = q.get('question', '')
    
    # 연속 공백
    if '  ' in question_text:
        issue_list.append("연속 공백 존재")
    
    # 문장 끝 공백
    if question_text.endswith(' '):
        issue_list.append("문장 끝 불필요한 공백")
    
    # 너무 긴 문장 (500자 이상)
    if len(question_text) > 500:
        issue_list.append(f"문제 본문이 너무 김 ({len(question_text)}자)")
    
    # 불완전한 문장 (끝이 중간에 잘림)
    if question_text and not question_text[-1] in '.?!가':
        if '...' not in question_text[-10:]:
            issue_list.append("문장이 불완전하게 끝남")
    
    # 4. 해설 점검
    explanation = q.get('explanation', '')
    if explanation and explanation != '해설이 없습니다.':
        stats['has_explanation'] += 1
        
        # 해설이 너무 짧음
        if len(explanation) < 20:
            issue_list.append("해설이 너무 짧음")
    else:
        issue_list.append("해설 없음")
    
    # 5. 선택지 점검
    for j, option in enumerate(q.get('options', [])):
        expected_letter = chr(ord('A') + j)
        if not option.startswith(f'{expected_letter}.'):
            issue_list.append(f"선택지 {j+1} 형식 오류")
        
        # 선택지 텍스트 추출
        option_text = re.sub(r'^[A-D]\.\s*', '', option)
        if len(option_text) < 3:
            issue_list.append(f"선택지 {expected_letter}가 너무 짧음")
    
    # 6. 라벨 점검
    if not q.get('labels') or len(q['labels']) == 0:
        issue_list.append("라벨 없음")
    
    # 통계 업데이트
    if not issue_list:
        stats['valid'] += 1
    
    if len(question_text) < 300 and '  ' not in question_text:
        stats['good_readability'] += 1
    
    # 문제 있는 경우만 기록
    if issue_list:
        issues[q_no] = issue_list

# 결과 출력
print("\n[통계]")
print(f"  총 문제 수: {stats['total']}개")
print(f"  완벽한 문제: {stats['valid']}개 ({stats['valid']/stats['total']*100:.1f}%)")
print(f"  해설 있음: {stats['has_explanation']}개 ({stats['has_explanation']/stats['total']*100:.1f}%)")
print(f"  가독성 양호: {stats['good_readability']}개 ({stats['good_readability']/stats['total']*100:.1f}%)")
print(f"  문제 있음: {len(issues)}개 ({len(issues)/stats['total']*100:.1f}%)")

# 문제 유형별 통계
issue_types = defaultdict(int)
for q_no, issue_list in issues.items():
    for issue in issue_list:
        # 이슈 유형 분류
        if "연속 공백" in issue:
            issue_types["연속 공백"] += 1
        elif "불완전" in issue:
            issue_types["불완전한 문장"] += 1
        elif "해설" in issue:
            issue_types["해설 문제"] += 1
        elif "선택지" in issue:
            issue_types["선택지 문제"] += 1
        elif "정답" in issue:
            issue_types["정답 문제"] += 1
        elif "라벨" in issue:
            issue_types["라벨 문제"] += 1
        else:
            issue_types["기타"] += 1

print("\n[문제 유형별 통계]")
for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {issue_type}: {count}개")

# 심각한 문제 (정답 불일치, 선택지 부족 등)
critical_issues = {}
for q_no, issue_list in issues.items():
    critical = [issue for issue in issue_list if any(keyword in issue for keyword in ['정답', '선택지 개수', '필수'])]
    if critical:
        critical_issues[q_no] = critical

if critical_issues:
    print(f"\n[심각한 문제] {len(critical_issues)}개")
    for q_no, issue_list in list(critical_issues.items())[:10]:
        print(f"  문제 {q_no}: {', '.join(issue_list)}")
    if len(critical_issues) > 10:
        print(f"  ... 외 {len(critical_issues)-10}개")

# 가독성 개선 필요 (연속 공백, 불완전한 문장)
readability_issues = {}
for q_no, issue_list in issues.items():
    readability = [issue for issue in issue_list if any(keyword in issue for keyword in ['공백', '불완전', '너무 김'])]
    if readability:
        readability_issues[q_no] = readability

if readability_issues:
    print(f"\n[가독성 개선 필요] {len(readability_issues)}개")
    for q_no, issue_list in list(readability_issues.items())[:10]:
        print(f"  문제 {q_no}: {', '.join(issue_list)}")
    if len(readability_issues) > 10:
        print(f"  ... 외 {len(readability_issues)-10}개")

# 개선 제안
print("\n[개선 제안]")
if issue_types.get("연속 공백", 0) > 0:
    print(f"  1. 연속 공백 제거 필요 ({issue_types['연속 공백']}개)")
if issue_types.get("불완전한 문장", 0) > 0:
    print(f"  2. 불완전한 문장 수정 필요 ({issue_types['불완전한 문장']}개)")
if issue_types.get("해설 문제", 0) > 0:
    print(f"  3. 해설 보완 필요 ({issue_types['해설 문제']}개)")

# 상세 리포트 저장
report_path = Path(__file__).parent.parent / 'pmp_quality_report.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("PMP 데이터 품질 점검 리포트\n")
    f.write("="*80 + "\n\n")
    f.write(f"총 문제 수: {stats['total']}개\n")
    f.write(f"문제 있는 항목: {len(issues)}개\n\n")
    
    for q_no, issue_list in sorted(issues.items(), key=lambda x: int(x[0])):
        f.write(f"\n문제 {q_no}:\n")
        for issue in issue_list:
            f.write(f"  - {issue}\n")

print(f"\n상세 리포트 저장: {report_path}")

