#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단어장 불일치 분석 스크립트
실제 문제에서 단일 단어로 사용된 경우만 확인하여 정확한 수정 목록 생성
"""

import json
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def load_data():
    """데이터 로드"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    vocab_file = project_root / 'data' / 'cissp_vocabulary.json'
    items_file = project_root / 'data' / 'items_cissp.jsonl'
    issues_file = project_root / 'data' / 'vocabulary_issues.json'
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)
    
    items = []
    with open(items_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    
    with open(issues_file, 'r', encoding='utf-8') as f:
        issues = json.load(f)
    
    return vocabulary, items, issues

def find_exact_word_matches(items):
    """선택지가 정확히 단일 단어인 경우만 찾기"""
    exact_matches = {}  # {word: [translations]}
    
    for item in items:
        if 'choices_en' in item and 'choices_ko' in item:
            choices_en = item['choices_en']
            choices_ko = item['choices_ko']
            
            if isinstance(choices_en, dict) and isinstance(choices_ko, dict):
                for key in choices_en.keys():
                    choice_en = choices_en.get(key, '').strip()
                    choice_ko = choices_ko.get(key, '').strip()
                    
                    # 선택지가 단일 단어이고 짧은 경우 (30자 이하, 공백 없음)
                    if choice_en and choice_ko and len(choice_en) <= 30:
                        # 공백, 하이픈, 괄호가 없는 순수 단어인지 확인
                        clean_en = choice_en.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
                        if clean_en.isalpha() or (clean_en.replace('.', '').replace('/', '').isalnum() and len(choice_en.split()) == 1):
                            word = choice_en.lower().strip()
                            if word not in exact_matches:
                                exact_matches[word] = []
                            if choice_ko not in exact_matches[word]:
                                exact_matches[word].append(choice_ko)
    
    return exact_matches

def analyze_issues():
    """불일치 분석"""
    vocabulary, items, issues = load_data()
    
    print("=" * 60)
    print("단어장 불일치 분석 및 수정 목록")
    print("=" * 60)
    
    # 정확한 단어 매칭 찾기
    print("\n1. 실제 문제에서 단일 단어로 사용된 경우 확인 중...")
    exact_matches = find_exact_word_matches(items)
    print(f"   {len(exact_matches)}개 단어의 정확한 번역 발견")
    
    # 불일치 목록 분석
    print("\n2. 불일치 목록 분석 중...")
    
    real_issues = []  # 실제 수정이 필요한 항목
    false_positives = []  # 잘못된 매칭 (무시 가능)
    
    for issue in issues:
        word = issue['word']
        vocab_meaning = issue['vocab']
        actual_trans = issue['actual']
        
        # 정확한 매칭에서 해당 단어 찾기
        if word.lower() in exact_matches:
            exact_trans = exact_matches[word.lower()]
            
            # 정확한 번역과 비교
            if vocab_meaning not in exact_trans:
                # 실제로 수정이 필요한 경우
                real_issues.append({
                    'word': word,
                    'current': vocab_meaning,
                    'should_be': exact_trans[0] if exact_trans else vocab_meaning,
                    'all_uses': exact_trans
                })
            else:
                # 단어장이 맞는 경우 (다른 의미로도 사용됨)
                false_positives.append({
                    'word': word,
                    'vocab': vocab_meaning,
                    'actual': actual_trans,
                    'note': '정확한 매칭에서는 일치함'
                })
        else:
            # 정확한 매칭에서 찾을 수 없는 경우
            # 대부분 잘못된 매칭일 가능성이 높음
            false_positives.append({
                'word': word,
                'vocab': vocab_meaning,
                'actual': actual_trans,
                'note': '단일 단어로 사용되지 않음 (잘못된 매칭 가능성)'
            })
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("📋 수정이 필요한 단어 목록")
    print("=" * 60)
    
    if real_issues:
        print(f"\n총 {len(real_issues)}개 단어 수정 필요:\n")
        for i, issue in enumerate(real_issues, 1):
            print(f"{i}. {issue['word']}")
            print(f"   현재: {issue['current']}")
            print(f"   수정: {issue['should_be']}")
            if len(issue['all_uses']) > 1:
                print(f"   (다른 사용: {', '.join(issue['all_uses'][1:])})")
            print()
    else:
        print("\n수정이 필요한 단어가 없습니다.")
    
    # 잘못된 매칭 목록 (참고용)
    if false_positives:
        print("\n" + "=" * 60)
        print("ℹ️  잘못된 매칭으로 판단된 항목 (무시 가능)")
        print("=" * 60)
        print(f"\n총 {len(false_positives)}개 항목\n")
        for i, fp in enumerate(false_positives[:10], 1):
            print(f"{i}. {fp['word']}")
            print(f"   단어장: {fp['vocab']}")
            print(f"   잘못 매칭된 번역: {fp['actual']}")
            print(f"   참고: {fp['note']}")
            print()
        if len(false_positives) > 10:
            print(f"... 외 {len(false_positives) - 10}개 더 있음")
    
    # 수정 스크립트 생성
    if real_issues:
        print("\n" + "=" * 60)
        print("💾 수정 스크립트 생성")
        print("=" * 60)
        
        fixes = []
        for issue in real_issues:
            fixes.append({
                'word': issue['word'],
                'old': issue['current'],
                'new': issue['should_be']
            })
        
        output_file = project_root / 'data' / 'vocabulary_fixes.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixes, f, ensure_ascii=False, indent=2)
        
        print(f"\n수정 목록이 {output_file}에 저장되었습니다.")
        print("\n수정할 단어 목록:")
        for fix in fixes:
            print(f"  - {fix['word']}: '{fix['old']}' → '{fix['new']}'")
    
    return real_issues

if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    analyze_issues()

