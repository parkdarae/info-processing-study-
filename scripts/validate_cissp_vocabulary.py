#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CISSP 단어장 검증 스크립트
items_cissp.jsonl의 실제 번역과 cissp_vocabulary.json의 번역을 비교하여
불일치하거나 문제가 있는 번역을 찾습니다.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_word(word):
    """단어 정규화 (소문자, 특수문자 제거)"""
    return word.lower().strip().replace(' ', '').replace('-', '').replace('_', '')

def extract_words_from_text(text):
    """텍스트에서 영어 단어 추출"""
    if not text:
        return []
    
    # 소문자 변환 및 특수문자 처리
    text = re.sub(r'[^\w\s-]', ' ', text.lower())
    text = re.sub(r'-', ' ', text)
    
    # 단어 추출 (알파벳만, 최소 2글자)
    words = re.findall(r'\b[a-z]{2,}\b', text)
    return words

def load_vocabulary(vocab_file):
    """단어장 로드"""
    if not Path(vocab_file).exists():
        print(f"경고: {vocab_file} 파일을 찾을 수 없습니다.")
        return {}
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_items(items_file):
    """문제 데이터 로드"""
    items = []
    with open(items_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items

def find_word_in_choices(word, choices_en, choices_ko):
    """선택지에서 단어를 찾고 해당 한국어 번역 반환"""
    word_lower = word.lower()
    
    for key in choices_en.keys():
        choice_en = choices_en.get(key, '')
        choice_ko = choices_ko.get(key, '')
        
        # 선택지 텍스트에서 단어 찾기
        if word_lower in choice_en.lower():
            return choice_ko
    
    return None

def validate_vocabulary():
    """단어장 검증"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    vocab_file = project_root / 'data' / 'cissp_vocabulary.json'
    items_file = project_root / 'data' / 'items_cissp.jsonl'
    
    print("=" * 60)
    print("CISSP 단어장 검증 시작")
    print("=" * 60)
    
    # 단어장 로드
    print(f"\n1. 단어장 로드 중: {vocab_file}")
    vocabulary = load_vocabulary(vocab_file)
    print(f"   총 {len(vocabulary)}개 단어 로드됨")
    
    # 문제 데이터 로드
    print(f"\n2. 문제 데이터 로드 중: {items_file}")
    items = load_items(items_file)
    print(f"   총 {len(items)}개 문제 로드됨")
    
    # 문제에서 실제 사용된 단어-번역 매핑 수집
    print(f"\n3. 문제에서 실제 사용된 번역 수집 중...")
    actual_translations = defaultdict(set)  # {word: {translation1, translation2, ...}}
    
    for item in items:
        # question_en과 question_ko 비교
        if 'question_en' in item and 'question_ko' in item:
            question_words = extract_words_from_text(item['question_en'])
            # 전체 질문에 대한 번역은 단어별로 매핑하기 어려우므로 스킵
        
        # choices_en과 choices_ko 비교
        if 'choices_en' in item and 'choices_ko' in item:
            choices_en = item['choices_en']
            choices_ko = item['choices_ko']
            
            if isinstance(choices_en, dict) and isinstance(choices_ko, dict):
                for key in choices_en.keys():
                    choice_en = choices_en.get(key, '').strip()
                    choice_ko = choices_ko.get(key, '').strip()
                    
                    if choice_en and choice_ko:
                        # 선택지 전체가 단어인 경우만 매칭 (예: "Privacy", "Availability", "Confidentiality")
                        # 선택지가 짧고(30자 이하) 단어처럼 보이는 경우
                        choice_en_normalized = normalize_word(choice_en)
                        
                        # 선택지가 단일 단어이거나 매우 짧은 경우
                        if len(choice_en) <= 30 and not ' ' in choice_en.strip():
                            # 단일 단어로 처리
                            word = choice_en.strip().lower()
                            actual_translations[word].add(choice_ko)
                        elif len(choice_en) <= 50:
                            # 짧은 선택지에서 주요 단어 추출 시도
                            # 하지만 정확한 매칭만 (선택지 전체가 단어인 경우)
                            words_in_choice = extract_words_from_text(choice_en)
                            for word in words_in_choice:
                                # 선택지가 단일 단어인 경우만
                                if normalize_word(choice_en) == normalize_word(word) and len(choice_en.split()) == 1:
                                    actual_translations[word].add(choice_ko)
    
    print(f"   {len(actual_translations)}개 단어의 실제 번역 수집됨")
    
    # 검증 시작
    print(f"\n4. 단어장 검증 중...")
    print("=" * 60)
    
    issues = []
    exact_matches = []
    partial_matches = []
    no_matches = []
    
    for word, vocab_data in vocabulary.items():
        vocab_meaning = vocab_data.get('meaning', '').strip()
        
        if not vocab_meaning:
            issues.append({
                'word': word,
                'type': 'empty_meaning',
                'message': '의미가 비어있습니다.'
            })
            continue
        
        # 실제 사용된 번역 확인
        actual_trans = actual_translations.get(word.lower())
        
        if not actual_trans:
            # 실제 문제에서 사용되지 않은 단어
            no_matches.append(word)
            continue
        
        # 실제 번역과 단어장 번역 비교
        actual_trans_list = list(actual_trans)
        
        # 정확히 일치하는지 확인
        exact_match = False
        partial_match = False
        
        for trans in actual_trans_list:
            # 정확히 일치
            if vocab_meaning == trans:
                exact_match = True
                break
            # 부분 일치 (단어장에 여러 의미가 있을 수 있음)
            elif trans in vocab_meaning or vocab_meaning in trans:
                partial_match = True
        
        if exact_match:
            exact_matches.append({
                'word': word,
                'vocab': vocab_meaning,
                'actual': actual_trans_list
            })
        elif partial_match:
            partial_matches.append({
                'word': word,
                'vocab': vocab_meaning,
                'actual': actual_trans_list
            })
        else:
            # 불일치
            issues.append({
                'word': word,
                'type': 'mismatch',
                'vocab': vocab_meaning,
                'actual': actual_trans_list,
                'message': f'단어장: "{vocab_meaning}" vs 실제: {actual_trans_list}'
            })
    
    # 결과 출력
    print(f"\n📊 검증 결과")
    print("=" * 60)
    print(f"✅ 정확히 일치: {len(exact_matches)}개")
    print(f"⚠️  부분 일치: {len(partial_matches)}개")
    print(f"❌ 불일치: {len(issues)}개")
    print(f"ℹ️  실제 사용 안 됨: {len(no_matches)}개")
    
    # 불일치 상세 출력
    if issues:
        print(f"\n❌ 불일치하는 단어 ({len(issues)}개):")
        print("-" * 60)
        for issue in issues[:20]:  # 최대 20개만 표시
            print(f"  • {issue['word']}")
            print(f"    단어장: {issue['vocab']}")
            print(f"    실제: {', '.join(issue['actual'])}")
            print()
        
        if len(issues) > 20:
            print(f"  ... 외 {len(issues) - 20}개 더 있음")
    
    # 부분 일치 상세 출력
    if partial_matches:
        print(f"\n⚠️  부분 일치하는 단어 ({len(partial_matches)}개, 최대 10개 표시):")
        print("-" * 60)
        for match in partial_matches[:10]:
            print(f"  • {match['word']}")
            print(f"    단어장: {match['vocab']}")
            print(f"    실제: {', '.join(match['actual'])}")
            print()
    
    # 의미가 비어있는 단어
    empty_meanings = [i for i in issues if i['type'] == 'empty_meaning']
    if empty_meanings:
        print(f"\n⚠️  의미가 비어있는 단어 ({len(empty_meanings)}개):")
        print("-" * 60)
        for issue in empty_meanings[:10]:
            print(f"  • {issue['word']}")
    
    # 실제 사용되지 않은 단어
    if no_matches:
        print(f"\nℹ️  실제 문제에서 사용되지 않은 단어 ({len(no_matches)}개, 최대 20개 표시):")
        print("-" * 60)
        for word in sorted(no_matches)[:20]:
            print(f"  • {word}")
        if len(no_matches) > 20:
            print(f"  ... 외 {len(no_matches) - 20}개 더 있음")
    
    # 요약
    print("\n" + "=" * 60)
    print("📋 요약")
    print("=" * 60)
    print(f"총 단어 수: {len(vocabulary)}")
    print(f"실제 사용된 단어: {len(actual_translations)}")
    print(f"정확히 일치: {len(exact_matches)} ({len(exact_matches)/len(actual_translations)*100:.1f}%)")
    print(f"부분 일치: {len(partial_matches)} ({len(partial_matches)/len(actual_translations)*100:.1f}%)")
    print(f"불일치: {len(issues)} ({len(issues)/len(actual_translations)*100:.1f}%)")
    
    # 불일치 목록을 파일로 저장
    if issues:
        output_file = project_root / 'data' / 'vocabulary_issues.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        print(f"\n💾 불일치 목록이 {output_file}에 저장되었습니다.")
    
    print("\n✅ 검증 완료!")

if __name__ == '__main__':
    validate_vocabulary()

