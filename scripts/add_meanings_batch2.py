#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도 101-200번째 단어에 한글 의미 추가"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 101-200번째 단어의 한글 의미 (CISSP 맥락에 맞게)
meanings_batch2 = {
    "large": "큰, 대규모의",
    "requires": "요구한다",
    "purpose": "목적",
    "allows": "허용한다",
    "list": "목록, 나열하다",
    "factor": "요인, 요소",
    "because": "왜냐하면",
    "os": "OS (운영체제)",
    "chief": "수석의, 주요한",
    "principle": "원칙",
    "tools": "도구들",
    "markup": "마크업",
    "manager": "관리자",
    "event": "이벤트, 사건",
    "reporting": "보고",
    "accounts": "계정들",
    "assurance": "보증, 확신",
    "personnel": "인원, 직원",
    "across": "가로질러, 전반에",
    "ensuring": "보장하는",
    "require": "요구하다",
    "main": "주요한",
    "associated": "연관된",
    "like": "같은, 좋아하다",
    "full": "전체의, 완전한",
    "two": "두 개",
    "threats": "위협들",
    "duties": "의무들",
    "available": "사용 가능한",
    "automated": "자동화된",
    "performance": "성능, 수행",
    "center": "센터, 중심",
    "records": "기록들",
    "value": "값, 가치",
    "properly": "적절하게",
    "employees": "직원들",
    "department": "부서",
    "production": "생산, 운영",
    "actions": "행동들, 조치들",
    "performed": "수행된",
    "port": "포트",
    "high": "높은",
    "objectives": "목표들",
    "drive": "드라이브, 구동하다",
    "same": "같은",
    "rbac": "RBAC (역할 기반 접근 제어)",
    "roles": "역할들",
    "legal": "법적인",
    "criteria": "기준들",
    "passwords": "비밀번호들",
    "input": "입력",
    "objective": "목표",
    "patches": "패치들",
    "include": "포함하다",
    "identified": "식별된",
    "hard": "하드웨어, 어려운",
    "location": "위치",
    "place": "장소, 배치하다",
    "about": "약, 관련하여",
    "financial": "재정적인",
    "networks": "네트워크들",
    "acquisition": "획득",
    "results": "결과들",
    "cross": "교차, 가로지르다",
    "activities": "활동들",
    "mechanism": "메커니즘, 기제",
    "protocols": "프로토콜들",
    "reports": "보고서들",
    "due": "예정된, 만기된",
    "both": "둘 다",
    "functional": "기능적인",
    "customer": "고객",
    "architecture": "아키텍처",
    "transfer": "전송, 이전",
    "independent": "독립적인",
    "rules": "규칙들",
    "corporate": "기업의",
    "monitor": "모니터, 감시하다",
    "practices": "관행들, 실습",
    "individual": "개인의, 개별의",
    "developer": "개발자",
    "conduct": "수행하다, 행동",
    "make": "만들다",
    "federated": "연합된",
    "function": "함수, 기능",
    "encrypted": "암호화된",
    "effectiveness": "효과성",
    "mitigate": "완화하다",
    "help": "도움, 도와주다",
    "assertion": "단언, 주장",
    "target": "대상, 목표",
    "upon": "위에, 의하여",
    "communications": "통신",
    "transmission": "전송",
    "denial": "거부, 부인",
    "reason": "이유",
    "inventory": "재고, 목록",
    "industry": "산업",
    "components": "구성 요소들",
    "algorithm": "알고리즘"
}

def add_meanings():
    """의미 추가"""
    # 문제 단어 사전 로드
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미 추가
    added_count = 0
    for word, meaning in meanings_batch2.items():
        if word in vocab:
            if not vocab[word].get('meaning') or vocab[word].get('meaning', '').strip() == '':
                vocab[word]['meaning'] = meaning
                added_count += 1
                print(f"[OK] {word}: {meaning}")
            else:
                print(f"[SKIP] {word}: 이미 의미가 있음 ({vocab[word].get('meaning')})")
        else:
            print(f"[NOT FOUND] {word}: 사전에 없음")
    
    # 저장
    with open('data/cissp_problem_vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
    
    print(f"\n총 {added_count}개 단어에 의미가 추가되었습니다.")

if __name__ == '__main__':
    add_meanings()

