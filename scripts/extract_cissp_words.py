#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CISSP 문제에서 단어 추출 스크립트
1850개 문제의 question_en, choices_en, explanation에서 영어 단어를 추출하여
별도 사전 파일로 저장합니다.
"""

import json
import re
from collections import Counter
from pathlib import Path

# 불용어 목록 (제거할 단어)
STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their',
    'he', 'she', 'his', 'her', 'him', 'we', 'us', 'our', 'you', 'your',
    'i', 'me', 'my', 'mine', 'of', 'to', 'in', 'on', 'at', 'for', 'with',
    'by', 'from', 'as', 'or', 'and', 'but', 'if', 'when', 'where', 'how',
    'what', 'which', 'who', 'whom', 'whose', 'why', 'than', 'then', 'so',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below',
    'into', 'onto', 'through', 'during', 'before', 'after', 'while',
    'all', 'each', 'every', 'some', 'any', 'no', 'not', 'only', 'just',
    'more', 'most', 'less', 'least', 'many', 'much', 'few', 'little',
    'very', 'too', 'also', 'also', 'even', 'still', 'yet', 'already',
    'here', 'there', 'where', 'now', 'then', 'today', 'yesterday', 'tomorrow'
}

# 최소 단어 길이
MIN_WORD_LENGTH = 2

def extract_words_from_text(text):
    """텍스트에서 영어 단어 추출"""
    if not text:
        return []
    
    # 소문자 변환 및 특수문자 처리
    # 하이픈으로 연결된 단어는 분리 (예: "multi-factor" -> "multi", "factor")
    text = re.sub(r'[^\w\s-]', ' ', text.lower())
    text = re.sub(r'-', ' ', text)
    
    # 단어 추출 (알파벳만, 최소 길이 이상)
    words = re.findall(r'\b[a-z]{' + str(MIN_WORD_LENGTH) + r',}\b', text)
    
    # 불용어 제거
    words = [w for w in words if w not in STOP_WORDS and len(w) >= MIN_WORD_LENGTH]
    
    return words

def load_existing_vocabulary(vocab_file):
    """기존 단어 사전 로드"""
    if not Path(vocab_file).exists():
        return set()
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 기존 사전의 모든 단어 (소문자)를 집합으로 반환
    existing_words = set(word.lower() for word in vocab.keys())
    return existing_words

def extract_words_from_items(items_file, existing_vocab_file):
    """JSONL 파일에서 단어 추출"""
    print(f"기존 단어 사전 로드 중: {existing_vocab_file}")
    existing_words = load_existing_vocabulary(existing_vocab_file)
    print(f"기존 단어 {len(existing_words)}개 제외")
    
    print(f"문제 파일 읽기 중: {items_file}")
    word_counter = Counter()
    
    with open(items_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            
            try:
                item = json.loads(line)
                
                # question_en에서 단어 추출
                if 'question_en' in item:
                    words = extract_words_from_text(item['question_en'])
                    word_counter.update(words)
                
                # choices_en에서 단어 추출
                if 'choices_en' in item and isinstance(item['choices_en'], dict):
                    for choice_text in item['choices_en'].values():
                        words = extract_words_from_text(choice_text)
                        word_counter.update(words)
                
                # explanation에서 단어 추출
                if 'explanation' in item:
                    words = extract_words_from_text(item['explanation'])
                    word_counter.update(words)
                
                if line_num % 100 == 0:
                    print(f"진행 중... {line_num}개 문제 처리")
                    
            except json.JSONDecodeError as e:
                print(f"경고: {line_num}번째 줄 파싱 실패: {e}")
                continue
    
    print(f"\n총 {len(word_counter)}개의 고유 단어 추출됨")
    
    # 기존 사전에 없는 단어만 필터링
    new_words = {word: count for word, count in word_counter.items() 
                 if word.lower() not in existing_words}
    
    print(f"기존 사전 제외 후 {len(new_words)}개의 새 단어")
    
    return new_words

def create_vocabulary_dict(words_with_freq):
    """단어 빈도수를 사전 형식으로 변환"""
    vocab_dict = {}
    
    # 빈도수로 정렬 (높은 순)
    sorted_words = sorted(words_with_freq.items(), key=lambda x: x[1], reverse=True)
    
    for word, frequency in sorted_words:
        # 기본 정보만 포함 (의미는 나중에 수동 또는 자동 번역으로 추가 가능)
        vocab_dict[word] = {
            "meaning": "",  # 나중에 추가
            "pos": "unknown",  # 나중에 추가
            "frequency": frequency
        }
    
    return vocab_dict

def main():
    """메인 함수"""
    # 파일 경로
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    items_file = project_root / 'data' / 'items_cissp.jsonl'
    existing_vocab_file = project_root / 'data' / 'cissp_vocabulary.json'
    output_file = project_root / 'data' / 'cissp_problem_vocabulary.json'
    
    # 파일 존재 확인
    if not items_file.exists():
        print(f"오류: {items_file} 파일을 찾을 수 없습니다.")
        return
    
    # 단어 추출
    words_with_freq = extract_words_from_items(items_file, existing_vocab_file)
    
    if not words_with_freq:
        print("추출된 새 단어가 없습니다.")
        return
    
    # 사전 형식으로 변환
    vocab_dict = create_vocabulary_dict(words_with_freq)
    
    # JSON 파일로 저장
    print(f"\n단어 사전 저장 중: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vocab_dict, f, ensure_ascii=False, indent=2)
    
    print(f"완료! {len(vocab_dict)}개의 단어가 {output_file}에 저장되었습니다.")
    print(f"\n빈도수 상위 20개 단어:")
    for i, (word, data) in enumerate(list(vocab_dict.items())[:20], 1):
        print(f"{i:2d}. {word:20s} (빈도: {data['frequency']:4d})")

if __name__ == '__main__':
    main()

