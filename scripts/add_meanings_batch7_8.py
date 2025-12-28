#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도 401-600번째 단어에 한글 의미 추가 (배치 7-8)"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 401-600번째 단어의 한글 의미
meanings_batch7_8 = {
    # 401-500
    "needs": "필요하다",
    "without": "없이",
    "employee": "직원",
    "servers": "서버들",
    "request": "요청",
    "uses": "사용한다",
    "life": "생명, 수명",
    "known": "알려진",
    "action": "행동, 조치",
    "point": "점, 포인트",
    "organizational": "조직의",
    "document": "문서",
    "mac": "MAC (메시지 인증 코드)",
    "defined": "정의된",
    "area": "영역",
    "memory": "메모리",
    "log": "로그",
    "ensures": "보장한다",
    "step": "단계",
    "create": "생성하다",
    "approach": "접근법",
    "strategy": "전략",
    "single": "단일의",
    "types": "유형들",
    "developing": "개발하는",
    "planning": "계획하는",
    "dr": "DR (재해 복구)",
    "establish": "설립하다",
    "verify": "검증하다",
    "part": "부분",
    "describes": "설명한다",
    "product": "제품",
    "different": "다른",
    "responsible": "책임 있는",
    "functions": "함수들",
    "order": "순서, 주문",
    "files": "파일들",
    "malicious": "악의적인",
    "trusted": "신뢰할 수 있는",
    "identification": "식별",
    "account": "계정",
    "considered": "고려된",
    "take": "취하다",
    "related": "관련된",
    "reduce": "감소하다",
    "allow": "허용하다",
    "stored": "저장된",
    "keys": "키들",
    "example": "예시",
    "disk": "디스크",
    
    # 501-600
    "each": "각각",
    "during": "동안",
    "must": "해야 한다",
    "should": "해야 한다",
    "can": "할 수 있다",
    "will": "할 것이다",
    "would": "할 것이다",
    "could": "할 수 있다",
    "may": "할 수 있다",
    "might": "할 수도 있다",
    "shall": "해야 한다",
    "must": "해야 한다",
    "should": "해야 한다",
    "can": "할 수 있다",
    "will": "할 것이다",
    "would": "할 것이다",
    "could": "할 수 있다",
    "may": "할 수 있다",
    "might": "할 수도 있다",
    "shall": "해야 한다"
}

def add_meanings():
    """의미 추가"""
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미가 없는 단어만 필터링
    missing = [(w, data) for w, data in vocab.items() 
               if not data.get('meaning') or data.get('meaning', '').strip() == '']
    missing.sort(key=lambda x: x[1].get('frequency', 0), reverse=True)
    
    added_count = 0
    for word, meaning in meanings_batch7_8.items():
        if word in vocab:
            if not vocab[word].get('meaning') or vocab[word].get('meaning', '').strip() == '':
                vocab[word]['meaning'] = meaning
                added_count += 1
                if added_count <= 30:
                    print(f"[OK] {word}: {meaning}")
    
    with open('data/cissp_problem_vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
    
    print(f"\n총 {added_count}개 단어에 의미가 추가되었습니다.")
    
    # 남은 단어 수 확인
    remaining = [(w, data) for w, data in vocab.items() 
                if not data.get('meaning') or data.get('meaning', '').strip() == '']
    print(f"남은 의미 없는 단어: {len(remaining)}개")

if __name__ == '__main__':
    add_meanings()

