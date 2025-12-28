#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도순으로 의미 없는 단어에 한글 의미 자동 추가 (배치 처리)"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 일반적인 영어 단어의 한글 의미 사전 (CISSP 맥락)
common_meanings = {
    "standards": "표준들",
    "phase": "단계",
    "language": "언어",
    "ip": "IP (인터넷 프로토콜)",
    "vendor": "벤더, 공급업체",
    "required": "필요한",
    "role": "역할",
    "number": "숫자",
    "prevent": "방지하다",
    "host": "호스트",
    "such": "그런",
    "implementation": "구현",
    "session": "세션",
    "personal": "개인의",
    "training": "교육, 훈련",
    "implementing": "구현하는",
    "sensitive": "민감한",
    "against": "대항하여",
    "remote": "원격의",
    "support": "지원하다",
    "set": "설정하다, 세트",
    "administrator": "관리자",
    "way": "방법",
    "private": "사적인, 비공개",
    "operating": "운영하는",
    "professional": "전문가",
    "transport": "전송",
    "implemented": "구현된",
    "client": "클라이언트",
    "organizations": "조직들",
    "likely": "가능성이 높은",
    "risks": "위험들",
    "project": "프로젝트",
    "computer": "컴퓨터",
    "external": "외부의",
    "mobile": "모바일",
    "non": "비-",
    "hardware": "하드웨어",
    "protected": "보호된",
    "infrastructure": "인프라",
    "end": "끝",
    "procedures": "절차들",
    "officer": "담당자",
    "changes": "변경사항들",
    "message": "메시지",
    "need": "필요하다",
    "cost": "비용",
    "assets": "자산들",
    "cycle": "주기",
    "logs": "로그들",
    "steps": "단계들",
    "provisioning": "프로비저닝",
    "specific": "특정한",
    "multiple": "다중의",
    "physical": "물리적인",
    "application": "애플리케이션",
    "control": "통제, 제어",
    "network": "네트워크",
    "specific": "특정한",
    "multiple": "다중의",
    "physical": "물리적인",
    "application": "애플리케이션",
    "control": "통제, 제어",
    "network": "네트워크"
}

def get_meaning_for_word(word):
    """단어에 대한 한글 의미 생성 (간단한 규칙 기반)"""
    # 이미 정의된 의미가 있으면 사용
    if word in common_meanings:
        return common_meanings[word]
    
    # 복수형 처리
    if word.endswith('s') and len(word) > 1:
        singular = word[:-1]
        if singular in common_meanings:
            return common_meanings[singular] + "들"
    
    # -ed, -ing, -ly 등 어미 제거 후 확인
    base_forms = [
        word.rstrip('ed'),
        word.rstrip('ing'),
        word.rstrip('ly'),
        word.rstrip('er'),
        word.rstrip('tion'),
        word.rstrip('sion')
    ]
    
    for base in base_forms:
        if base in common_meanings:
            return common_meanings[base]
    
    # 기본 번역 규칙 (간단한 경우만)
    # 대부분의 경우 수동으로 추가해야 함
    return None

def add_meanings_batch(start_idx=0, batch_size=100):
    """의미 없는 단어에 의미 추가 (배치 처리)"""
    # 문제 단어 사전 로드
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미가 없는 단어만 필터링
    missing = [(w, data) for w, data in vocab.items() 
               if not data.get('meaning') or data.get('meaning', '').strip() == '']
    missing.sort(key=lambda x: x[1].get('frequency', 0), reverse=True)
    
    # 배치 범위
    end_idx = min(start_idx + batch_size, len(missing))
    batch = missing[start_idx:end_idx]
    
    print(f"처리 범위: {start_idx+1}-{end_idx}번째 단어 ({len(batch)}개)")
    print("=" * 80)
    
    added_count = 0
    no_meaning_count = 0
    
    for word, data in batch:
        # 의미 가져오기
        meaning = get_meaning_for_word(word)
        
        if meaning:
            vocab[word]['meaning'] = meaning
            added_count += 1
            if added_count <= 20:  # 처음 20개만 출력
                print(f"[OK] {word}: {meaning}")
        else:
            no_meaning_count += 1
            if no_meaning_count <= 10:  # 처음 10개만 출력
                print(f"[SKIP] {word}: 의미 사전에 없음 (수동 추가 필요)")
    
    # 저장
    with open('data/cissp_problem_vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
    
    print(f"\n총 {added_count}개 단어에 의미가 추가되었습니다.")
    if no_meaning_count > 0:
        print(f"의미 사전에 없는 단어: {no_meaning_count}개 (수동 추가 필요)")
    
    return added_count, no_meaning_count

if __name__ == '__main__':
    # 301-400번째 배치
    print("배치 4: 301-400번째 단어")
    add_meanings_batch(300, 100)
    
    print("\n" + "=" * 80 + "\n")
    
    # 401-500번째 배치
    print("배치 5: 401-500번째 단어")
    add_meanings_batch(400, 100)

