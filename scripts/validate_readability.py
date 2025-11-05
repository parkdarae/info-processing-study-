#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
가독성 검증 스크립트
- 보기 형식이 일관되게 적용되었는지 확인
- 줄바꿈이 적절히 사용되었는지 확인
- 공백 정렬이 제대로 처리되었는지 확인
- 특수 문자가 올바르게 표시되는지 확인
"""

import json
import re

def check_choices_format(item):
    """보기 형식 검증"""
    text = item['question_text']
    issues = []
    
    # 보기가 있는지 확인
    if '<보기>' in text or '＜보기＞' in text or '보기' in text:
        # 비표준 보기 표기 확인
        if '＜보기＞' in text:
            issues.append('비표준 보기 표기 (＜보기＞)')
        
        # 보기 전후 빈 줄 확인
        if '<보기>' in text:
            # 보기 앞에 빈 줄이 있는지
            if not re.search(r'\n\n<보기>', text):
                if text.find('<보기>') > 0:  # 첫 줄이 아닌 경우만
                    issues.append('보기 앞에 빈 줄 없음')
    
    return issues

def check_line_breaks(item):
    """줄바꿈 검증"""
    text = item['question_text']
    issues = []
    
    # 연속된 4개 이상의 빈 줄
    if '\n\n\n\n' in text:
        count = text.count('\n\n\n\n')
        issues.append(f'과도한 빈 줄 {count}개')
    
    # 매우 긴 한 줄 (200자 이상)
    lines = text.split('\n')
    long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 200]
    if long_lines:
        issues.append(f'긴 줄 {len(long_lines)}개 (라인: {long_lines[:3]})')
    
    return issues

def check_spacing(item):
    """공백 정렬 검증"""
    text = item['question_text']
    issues = []
    
    # 10칸 이상의 연속 공백 (보기 정렬 등)
    long_spaces = re.findall(r' {10,}', text)
    if long_spaces:
        issues.append(f'10칸 이상 공백 {len(long_spaces)}개')
    
    # 탭 문자 사용
    if '\t' in text:
        issues.append('탭 문자 사용')
    
    return issues

def check_special_chars(item):
    """특수 문자 검증"""
    text = item['question_text']
    issues = []
    
    # 깨진 문자 패턴 확인
    broken_patterns = ['â€', 'â', 'Ã', '�']
    for pattern in broken_patterns:
        if pattern in text:
            issues.append(f'깨진 문자 가능성: {pattern}')
            break
    
    # 올바른 특수 기호 사용 확인
    has_correct_symbols = bool(re.search(r'[㉠-㉧①-⑳㈎-㈜]', text))
    
    # 잘못된 기호 패턴 (괄호 안 한글 숫자)
    wrong_symbols = re.findall(r'\([일이삼사오육칠팔구십]\)', text)
    if wrong_symbols:
        issues.append(f'잘못된 기호: {wrong_symbols[:3]}')
    
    return issues

def main():
    print("=" * 60)
    print("가독성 검증")
    print("=" * 60)
    
    # items.jsonl 읽기
    with open('items.jsonl', 'r', encoding='utf-8') as f:
        items = [json.loads(line) for line in f]
    
    print(f"\n전체 문제 수: {len(items)}")
    
    # 검증 실행
    print("\n검증 중...")
    
    all_issues = {}
    issue_counts = {
        'choices': 0,
        'linebreaks': 0,
        'spacing': 0,
        'special_chars': 0
    }
    
    for item in items:
        q_no = item['q_no']
        
        # 각 검증 항목 실행
        choices_issues = check_choices_format(item)
        linebreak_issues = check_line_breaks(item)
        spacing_issues = check_spacing(item)
        char_issues = check_special_chars(item)
        
        # 이슈가 있으면 기록
        if any([choices_issues, linebreak_issues, spacing_issues, char_issues]):
            all_issues[q_no] = {
                'choices': choices_issues,
                'linebreaks': linebreak_issues,
                'spacing': spacing_issues,
                'special_chars': char_issues
            }
            
            if choices_issues:
                issue_counts['choices'] += 1
            if linebreak_issues:
                issue_counts['linebreaks'] += 1
            if spacing_issues:
                issue_counts['spacing'] += 1
            if char_issues:
                issue_counts['special_chars'] += 1
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("검증 결과")
    print("=" * 60)
    
    print(f"\n이슈가 있는 문제: {len(all_issues)}개")
    print(f"\n카테고리별 이슈 수:")
    print(f"  - 보기 형식: {issue_counts['choices']}개")
    print(f"  - 줄바꿈: {issue_counts['linebreaks']}개")
    print(f"  - 공백 정렬: {issue_counts['spacing']}개")
    print(f"  - 특수 문자: {issue_counts['special_chars']}개")
    
    if all_issues:
        print(f"\n상세 이슈 (상위 10개):")
        for q_no in list(all_issues.keys())[:10]:
            print(f"\n{q_no}:")
            issue_data = all_issues[q_no]
            
            if issue_data['choices']:
                print(f"  [보기] {', '.join(issue_data['choices'])}")
            if issue_data['linebreaks']:
                print(f"  [줄바꿈] {', '.join(issue_data['linebreaks'])}")
            if issue_data['spacing']:
                print(f"  [공백] {', '.join(issue_data['spacing'])}")
            if issue_data['special_chars']:
                print(f"  [문자] {', '.join(issue_data['special_chars'])}")
    
    # 보기가 있는 문제 통계
    print(f"\n\n보기가 있는 문제 통계:")
    choices_problems = [i for i in items if '<보기>' in i['question_text'] or '보기' in i['question_text']]
    print(f"  - 총 {len(choices_problems)}개")
    
    # Q021 상세 확인
    print(f"\n\nQ021 상세 확인:")
    q021 = next((i for i in items if i['q_no'] == 'Q021'), None)
    if q021:
        text = q021['question_text']
        print(f"  - 텍스트 길이: {len(text)}")
        print(f"  - 줄 수: {len(text.split(chr(10)))}")
        print(f"  - '<보기>' 포함: {'예' if '<보기>' in text else '아니오'}")
        print(f"  - 긴 공백(5칸): {text.count('     ')}개")
        print(f"  - 긴 공백(10칸): {text.count('          ')}개")
        
        if q021['q_no'] in all_issues:
            print(f"  - 이슈:")
            for category, issues in all_issues[q021['q_no']].items():
                if issues:
                    print(f"    {category}: {issues}")
        else:
            print(f"  - 이슈: 없음")
    
    # 최종 판정
    print(f"\n\n" + "=" * 60)
    if len(all_issues) == 0:
        print("통과: 모든 문제가 가독성 기준을 만족합니다!")
    elif len(all_issues) <= 5:
        print(f"경고: {len(all_issues)}개 문제에 경미한 이슈가 있습니다.")
    else:
        print(f"주의: {len(all_issues)}개 문제에 이슈가 있습니다. 검토가 필요합니다.")
    print("=" * 60)

if __name__ == '__main__':
    main()

