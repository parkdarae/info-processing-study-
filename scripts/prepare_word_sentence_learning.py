#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
자주 나오는 단어와 문장 학습 데이터 준비 스크립트
"""

import json
import sys
import re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

def load_json_file(filepath):
    """JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    """JSON 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_frequent_words():
    """빈도 40 이상인 단어들 추출 (1000개 미만)"""
    problem_vocab = load_json_file('data/cissp_problem_vocabulary.json')
    
    # 빈도 40 이상인 단어들 필터링
    frequent_words = []
    for word, data in problem_vocab.items():
        frequency = data.get('frequency', 0)
        if frequency >= 40:
            frequent_words.append({
                'word': word,
                'meaning': data.get('meaning', ''),
                'pos': data.get('pos', 'unknown'),
                'frequency': frequency,
                'example': data.get('example', '')
            })
    
    # 빈도순으로 정렬 (높은 순)
    frequent_words.sort(key=lambda x: x['frequency'], reverse=True)
    
    # 1000개 미만으로 제한
    frequent_words = frequent_words[:1000]
    
    print(f"[OK] 빈도 40 이상인 단어 {len(frequent_words)}개 추출 완료")
    print(f"[INFO] 최고 빈도: {frequent_words[0]['word']} ({frequent_words[0]['frequency']})")
    print(f"[INFO] 최저 빈도: {frequent_words[-1]['word']} ({frequent_words[-1]['frequency']})")
    
    # JSON 파일로 저장
    save_json_file('data/cissp_frequent_words.json', frequent_words)
    
    return frequent_words

def extract_common_sentences():
    """자주 나오는 문장 패턴 추출 (200개 미만)"""
    # items_cissp.jsonl에서 문장 추출
    sentences = []
    sentence_patterns = []
    
    try:
        with open('data/items_cissp.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        item = json.loads(line)
                        # 문제 본문에서 문장 추출
                        if item.get('question_en'):
                            question = item['question_en']
                            question_ko = item.get('question_ko', '')
                            
                            # 문장 단위로 분리
                            question_sentences = re.split(r'[.!?]\s+', question)
                            question_ko_sentences = re.split(r'[.!?]\s+', question_ko) if question_ko else []
                            
                            for i, sent in enumerate(question_sentences):
                                if sent.strip() and len(sent.strip()) > 10:
                                    sentences.append({
                                        'sentence_en': sent.strip(),
                                        'sentence_ko': question_ko_sentences[i].strip() if i < len(question_ko_sentences) else '',
                                        'source': f"문제 {item.get('q_no', '')}"
                                    })
                        
                        # 선택지에서도 문장 추출
                        choices_en = item.get('choices_en', {})
                        choices_ko = item.get('choices_ko', {})
                        
                        for key, choice in choices_en.items():
                            if choice and len(choice.strip()) > 10:
                                sentences.append({
                                    'sentence_en': choice.strip(),
                                    'sentence_ko': choices_ko.get(key, '').strip() if choices_ko else '',
                                    'source': f"문제 {item.get('q_no', '')} 선택지 {key}"
                                })
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        print("[WARNING] items_cissp.jsonl 파일을 찾을 수 없습니다.")
        return []
    
    # 문장 패턴 분석 (자주 나오는 시작 패턴)
    pattern_counter = Counter()
    common_sentences = []
    
    for sent_data in sentences:
        sentence = sent_data['sentence_en']
        # 문장 시작 부분 추출 (첫 5-10단어)
        words = sentence.split()[:8]
        if len(words) >= 3:
            pattern = ' '.join(words).lower()
            pattern_counter[pattern] += 1
    
    # 빈도가 높은 패턴들 선택
    top_patterns = pattern_counter.most_common(200)
    
    # 각 패턴에 해당하는 대표 문장 찾기
    for pattern, count in top_patterns:
        # 해당 패턴을 포함하는 문장 찾기
        for sent_data in sentences:
            sentence_lower = sent_data['sentence_en'].lower()
            pattern_words = pattern.split()
            if all(word in sentence_lower for word in pattern_words[:3]):
                # 중복 제거
                if not any(cs['sentence_en'].lower() == sent_data['sentence_en'].lower() 
                          for cs in common_sentences):
                    common_sentences.append({
                        'sentence_en': sent_data['sentence_en'],
                        'sentence_ko': sent_data['sentence_ko'],
                        'pattern': pattern,
                        'frequency': count,
                        'source': sent_data['source']
                    })
                    break
        
        if len(common_sentences) >= 200:
            break
    
    # 빈도순으로 정렬
    common_sentences.sort(key=lambda x: x['frequency'], reverse=True)
    
    print(f"[OK] 자주 나오는 문장 {len(common_sentences)}개 추출 완료")
    if common_sentences:
        print(f"[INFO] 최고 빈도 패턴: {common_sentences[0]['pattern']} ({common_sentences[0]['frequency']})")
    
    # JSON 파일로 저장
    save_json_file('data/cissp_common_sentences.json', common_sentences)
    
    return common_sentences

def main():
    """메인 함수"""
    print("=" * 60)
    print("CISSP 단어 및 문장 학습 데이터 준비")
    print("=" * 60)
    
    # 빈도 높은 단어 추출
    print("\n[1단계] 빈도 40 이상인 단어 추출 중...")
    frequent_words = extract_frequent_words()
    
    # 자주 나오는 문장 추출
    print("\n[2단계] 자주 나오는 문장 패턴 추출 중...")
    common_sentences = extract_common_sentences()
    
    print("\n" + "=" * 60)
    print("완료!")
    print(f"- 단어 학습 데이터: {len(frequent_words)}개")
    print(f"- 문장 학습 데이터: {len(common_sentences)}개")
    print("=" * 60)

if __name__ == '__main__':
    main()

