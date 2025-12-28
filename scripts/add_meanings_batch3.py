#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도 201-300번째 단어에 한글 의미 추가"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 201-300번째 단어의 한글 의미 (CISSP 맥락에 맞게)
meanings_batch3 = {
    "practice": "실습, 관행",
    "strong": "강한, 견고한",
    "install": "설치하다",
    "case": "케이스, 경우",
    "platform": "플랫폼",
    "regulatory": "규제의",
    "goal": "목표",
    "international": "국제적인",
    "object": "객체, 목적",
    "benefit": "이익, 혜택",
    "signature": "서명, 시그니처",
    "principles": "원칙들",
    "metrics": "지표들",
    "knowledge": "지식",
    "approved": "승인된",
    "question": "질문",
    "frequency": "빈도",
    "static": "정적인",
    "developed": "개발된",
    "form": "형식, 양식",
    "needed": "필요한",
    "query": "쿼리, 질의",
    "run": "실행하다",
    "levels": "수준들",
    "existing": "기존의",
    "techniques": "기법들",
    "endpoint": "엔드포인트",
    "tests": "테스트들",
    "developers": "개발자들",
    "domain": "도메인",
    "increase": "증가하다",
    "acceptable": "수용 가능한",
    "individuals": "개인들",
    "own": "자신의",
    "acceptance": "수용, 승인",
    "includes": "포함한다",
    "defense": "방어",
    "unique": "고유한",
    "regarding": "관련하여",
    "scope": "범위",
    "environments": "환경들",
    "osi": "OSI (개방형 시스템 상호 연결)",
    "execute": "실행하다",
    "including": "포함하여",
    "proper": "적절한",
    "routing": "라우팅",
    "certificates": "인증서들",
    "chain": "체인, 연쇄",
    "equipment": "장비",
    "name": "이름",
    "node": "노드",
    "authenticate": "인증하다",
    "connections": "연결들",
    "understand": "이해하다",
    "concern": "우려, 관심사",
    "measure": "측정하다, 조치",
    "goals": "목표들",
    "dynamic": "동적인",
    "documentation": "문서화",
    "check": "확인하다",
    "significant": "중요한",
    "dac": "DAC (임의 접근 제어)",
    "various": "다양한",
    "executive": "임원, 실행의",
    "separate": "분리된",
    "functionality": "기능성",
    "meet": "만족하다, 만나다",
    "emergency": "비상, 긴급",
    "interface": "인터페이스",
    "intended": "의도된",
    "solutions": "해결책들",
    "analyze": "분석하다",
    "distributed": "분산된",
    "cots": "COTS (상용 제품)",
    "extensible": "확장 가능한",
    "reviews": "검토들",
    "privileged": "특권을 가진",
    "greatest": "가장 큰",
    "involves": "포함한다",
    "authorized": "승인된",
    "regulations": "규정들",
    "designing": "설계하는",
    "found": "발견된",
    "assigned": "할당된",
    "iscm": "ISCM (정보 보안 연속 모니터링)",
    "pci": "PCI (결제 카드 산업)",
    "result": "결과",
    "idp": "IDP (침입 탐지 및 방지)",
    "structured": "구조화된",
    "technologies": "기술들",
    "events": "이벤트들",
    "maintenance": "유지보수",
    "discretionary": "임의의",
    "active": "활성의",
    "version": "버전",
    "done": "완료된",
    "box": "박스, 상자",
    "safety": "안전",
    "mission": "임무",
    "abac": "ABAC (속성 기반 접근 제어)"
}

def add_meanings():
    """의미 추가"""
    # 문제 단어 사전 로드
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미 추가
    added_count = 0
    for word, meaning in meanings_batch3.items():
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

