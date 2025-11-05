#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단어 끊김 검증 스크립트
수정 후 남은 단어 끊김과 비정상적인 결합을 확인합니다.
"""

import json
import re

def count_word_breaks(text):
    """한글-줄바꿈-한글 패턴 개수 세기"""
    pattern = r'([가-힣]+)\n([가-힣]+)'
    matches = re.findall(pattern, text)
    return len(matches), matches

def detect_abnormal_joins(text):
    """비정상적인 단어 결합 감지"""
    abnormal = []
    
    # 의심스러운 패턴들
    suspicious_patterns = [
        r'[다요임]\s*[가-힣]{2,}',  # 문장 종결 후 바로 이어지는 단어
        r'[을를이가은는]\s*[을를이가은는]',  # 연속된 조사
    ]
    
    for pattern in suspicious_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            abnormal.append(match.group(0))
    
    return abnormal

def main():
    print("=" * 60)
    print("단어 끊김 검증")
    print("=" * 60)
    
    # items.jsonl 읽기
    with open('items.jsonl', 'r', encoding='utf-8') as f:
        items = [json.loads(line) for line in f]
    
    print(f"\n전체 문제 수: {len(items)}")
    
    # 검증
    print("\n검증 중...")
    
    total_breaks = 0
    problems_with_breaks = []
    all_abnormal = []
    
    for item in items:
        q_no = item['q_no']
        text = item['question_text']
        
        # 단어 끊김 확인
        break_count, breaks = count_word_breaks(text)
        if break_count > 0:
            total_breaks += break_count
            problems_with_breaks.append({
                'q_no': q_no,
                'count': break_count,
                'samples': breaks[:3]
            })
        
        # 비정상 결합 확인
        abnormal = detect_abnormal_joins(text)
        if abnormal:
            all_abnormal.extend([{
                'q_no': q_no,
                'pattern': a
            } for a in abnormal[:2]])
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("검증 결과")
    print("=" * 60)
    
    print(f"\n남은 단어 끊김:")
    print(f"  - 총 {total_breaks}개")
    print(f"  - {len(problems_with_breaks)}개 문제에서 발견")
    
    if problems_with_breaks:
        print(f"\n상세 (상위 10개):")
        for prob in problems_with_breaks[:10]:
            print(f"\n{prob['q_no']}: {prob['count']}개")
            for sample in prob['samples']:
                print(f"  - {sample[0]}\\n{sample[1]}")
    
    if all_abnormal:
        print(f"\n\n비정상 결합 의심:")
        print(f"  - 총 {len(all_abnormal)}개")
        for abn in all_abnormal[:10]:
            print(f"  - {abn['q_no']}: [{abn['pattern']}]")
    else:
        print(f"\n비정상 결합: 없음")
    
    # 샘플 문제 출력
    print(f"\n\n샘플 문제 (Q001, Q003, Q021):")
    for q_no in ['Q001', 'Q003', 'Q021']:
        item = next((i for i in items if i['q_no'] == q_no), None)
        if item:
            print(f"\n{q_no}:")
            text = item['question_text']
            # 첫 200자 출력
            lines = text[:200].split('\n')
            for i, line in enumerate(lines[:3], 1):
                print(f"  {i}: {line}")
            if len(text) > 200:
                print(f"  ... ({len(text)} chars total)")
    
    # 최종 판정
    print(f"\n\n" + "=" * 60)
    if total_breaks == 0:
        print("통과: 모든 단어 끊김이 수정되었습니다!")
    elif total_breaks <= 10:
        print(f"양호: {total_breaks}개의 단어 끊김이 남아있습니다. (대부분 의도적)")
    else:
        print(f"주의: {total_breaks}개의 단어 끊김이 남아있습니다. 추가 검토 필요")
    print("=" * 60)

if __name__ == '__main__':
    main()

