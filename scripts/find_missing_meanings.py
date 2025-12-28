#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""의미가 없는 단어 찾기"""

import json
import sys

def find_missing_meanings(vocab_file):
    """의미가 없는 단어 찾기"""
    with open(vocab_file, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)
    
    missing = []
    for word, data in vocabulary.items():
        meaning = data.get('meaning', '')
        if not meaning or meaning.strip() == '' or meaning == 'unknown':
            missing.append(word)
    
    return missing, vocabulary

def main():
    # 주요 단어 사전 확인
    print("=" * 60)
    print("주요 단어 사전 (cissp_vocabulary.json) 확인")
    print("=" * 60)
    main_missing, main_vocab = find_missing_meanings('data/cissp_vocabulary.json')
    print(f"의미가 없는 단어: {len(main_missing)}개")
    if main_missing:
        print("\n의미가 없는 단어 목록:")
        for i, word in enumerate(main_missing[:50], 1):
            print(f"{i:3d}. {word}")
        if len(main_missing) > 50:
            print(f"... 외 {len(main_missing) - 50}개")
    
    # 문제 단어 사전 확인
    print("\n" + "=" * 60)
    print("문제 단어 사전 (cissp_problem_vocabulary.json) 확인")
    print("=" * 60)
    try:
        problem_missing, problem_vocab = find_missing_meanings('data/cissp_problem_vocabulary.json')
        print(f"의미가 없는 단어: {len(problem_missing)}개")
        if problem_missing:
            print("\n의미가 없는 단어 목록 (처음 50개):")
            for i, word in enumerate(problem_missing[:50], 1):
                print(f"{i:3d}. {word}")
            if len(problem_missing) > 50:
                print(f"... 외 {len(problem_missing) - 50}개")
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        problem_missing = []
    
    # 전체 요약
    print("\n" + "=" * 60)
    print("요약")
    print("=" * 60)
    print(f"주요 단어 사전: {len(main_missing)}개 단어에 의미 없음")
    print(f"문제 단어 사전: {len(problem_missing)}개 단어에 의미 없음")
    print(f"총 {len(main_missing) + len(problem_missing)}개 단어에 의미 추가 필요")

if __name__ == '__main__':
    main()

