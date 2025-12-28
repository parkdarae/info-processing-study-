#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
빈도 40 이상인 단어들을 cissp_vocabulary.json에 추가하는 스크립트
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def load_json_file(filepath):
    """JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    """JSON 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_frequency_40_words():
    """빈도 40 이상인 단어들 추가"""
    # 문제 단어 사전 로드
    problem_vocab = load_json_file('data/cissp_problem_vocabulary.json')
    
    # 기존 단어 사전 로드
    vocab = load_json_file('data/cissp_vocabulary.json')
    
    # 빈도 40 이상인 단어들 필터링 (이미 추가된 단어 제외)
    words_to_add = {}
    for word, data in problem_vocab.items():
        frequency = data.get('frequency', 0)
        if frequency >= 40 and word not in vocab:
            words_to_add[word] = {
                "meaning": data.get('meaning', ''),
                "pos": data.get('pos', 'unknown'),
                "example": ""  # 나중에 추가 가능
            }
    
    # 단어 사전에 추가
    vocab.update(words_to_add)
    
    # 저장
    save_json_file('data/cissp_vocabulary.json', vocab)
    
    print(f"[OK] {len(words_to_add)}개 단어가 추가되었습니다.")
    print(f"[INFO] 빈도 40 이상인 단어 중 {len(words_to_add)}개가 새로 추가되었습니다.")
    
    # 추가된 단어 목록 출력 (상위 20개)
    sorted_words = sorted(words_to_add.items(), key=lambda x: problem_vocab[x[0]].get('frequency', 0), reverse=True)
    print("\n[추가된 단어 목록 (상위 20개)]:")
    for word, data in sorted_words[:20]:
        freq = problem_vocab[word].get('frequency', 0)
        meaning = data.get('meaning', '의미 없음')
        print(f"  {word}: {meaning} (빈도: {freq})")

if __name__ == '__main__':
    add_frequency_40_words()

