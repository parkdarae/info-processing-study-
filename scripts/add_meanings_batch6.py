#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도 301-400번째 단어에 한글 의미 추가"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 301-400번째 단어의 한글 의미
meanings_batch6 = {
    "stakeholders": "이해관계자들",
    "table": "테이블, 표",
    "copy": "복사하다",
    "iam": "IAM (신원 및 접근 관리)",
    "connected": "연결된",
    "gain": "획득하다",
    "tool": "도구",
    "basis": "기초",
    "delivery": "전달",
    "manage": "관리하다",
    "plans": "계획들",
    "useful": "유용한",
    "increased": "증가한",
    "interconnection": "상호 연결",
    "ports": "포트들",
    "detected": "탐지된",
    "consultant": "컨설턴트",
    "commercial": "상업적인",
    "exchange": "교환",
    "methodology": "방법론",
    "read": "읽다",
    "statement": "문장, 진술",
    "evaluating": "평가하는",
    "until": "까지",
    "features": "기능들",
    "securely": "안전하게",
    "working": "작동하는",
    "combination": "조합",
    "operation": "작업",
    "providers": "제공자들",
    "controller": "컨트롤러",
    "deployed": "배포된",
    "major": "주요한",
    "https": "HTTPS (보안 HTTP)",
    "command": "명령",
    "ics": "ICS (산업 제어 시스템)",
    "state": "상태",
    "follow": "따르다",
    "real": "실제의",
    "centralized": "중앙화된",
    "containing": "포함하는",
    "areas": "영역들",
    "establishing": "설립하는",
    "throughout": "전반에 걸쳐",
    "logical": "논리적인",
    "comply": "준수하다",
    "initial": "초기의",
    "obtain": "얻다",
    "text": "텍스트",
    "handshake": "핸드셰이크",
    "requests": "요청들",
    "lifecycle": "생명주기",
    "advantage": "장점",
    "regular": "정기적인",
    "tolerance": "허용 오차",
    "computing": "컴퓨팅",
    "overall": "전체적인",
    "minimize": "최소화하다",
    "pass": "통과하다",
    "rate": "비율",
    "cio": "CIO (최고 정보 책임자)",
    "tunneling": "터널링",
    "deploying": "배포하는",
    "managed": "관리되는",
    "rather": "오히려",
    "consider": "고려하다",
    "arp": "ARP (주소 해석 프로토콜)",
    "hashing": "해싱",
    "feature": "기능",
    "small": "작은",
    "minimum": "최소",
    "libraries": "라이브러리들",
    "com": "COM (구성 요소 객체 모델)",
    "situation": "상황",
    "entity": "엔티티",
    "supports": "지원한다",
    "voip": "VoIP (음성 인터넷 프로토콜)",
    "login": "로그인",
    "analyst": "분석가",
    "higher": "더 높은",
    "principals": "주체들",
    "characteristic": "특성",
    "sources": "소스들",
    "dedicated": "전용의",
    "last": "마지막",
    "radio": "라디오",
    "credential": "자격 증명",
    "contains": "포함한다",
    "controlled": "제어된",
    "models": "모델들",
    "conducted": "수행된",
    "assign": "할당하다",
    "sensitivity": "민감도",
    "outside": "외부",
    "long": "긴",
    "correct": "올바른",
    "digest": "다이제스트",
    "protects": "보호한다",
    "disable": "비활성화하다",
    "years": "년들"
}

def add_meanings():
    """의미 추가"""
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    added_count = 0
    for word, meaning in meanings_batch6.items():
        if word in vocab:
            if not vocab[word].get('meaning') or vocab[word].get('meaning', '').strip() == '':
                vocab[word]['meaning'] = meaning
                added_count += 1
                if added_count <= 20:
                    print(f"[OK] {word}: {meaning}")
    
    with open('data/cissp_problem_vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
    
    print(f"\n총 {added_count}개 단어에 의미가 추가되었습니다.")

if __name__ == '__main__':
    add_meanings()

