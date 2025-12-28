#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도 상위 100개 단어에 한글 의미 추가"""

import json
import sys

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 상위 100개 단어의 한글 의미 (CISSP 맥락에 맞게)
meanings_batch1 = {
    "security": "보안",
    "following": "다음의, 다음",
    "data": "데이터, 자료",
    "access": "접근",
    "system": "시스템",
    "organization": "조직",
    "information": "정보",
    "management": "관리",
    "software": "소프트웨어",
    "best": "최선의, 최고의",
    "service": "서비스",
    "based": "기반의, 기초한",
    "controls": "통제, 제어",
    "user": "사용자",
    "business": "비즈니스, 사업",
    "use": "사용하다",
    "used": "사용된",
    "process": "프로세스, 과정",
    "code": "코드",
    "testing": "테스트, 시험",
    "systems": "시스템들",
    "ensure": "보장하다, 확보하다",
    "layer": "계층",
    "analysis": "분석",
    "key": "키, 열쇠, 핵심",
    "level": "수준, 레벨",
    "web": "웹",
    "development": "개발",
    "using": "사용하여",
    "review": "검토, 리뷰",
    "users": "사용자들",
    "requirements": "요구사항",
    "time": "시간",
    "server": "서버",
    "identity": "신원, 정체성",
    "internet": "인터넷",
    "test": "테스트, 시험",
    "type": "유형, 타입",
    "devices": "장치들",
    "provide": "제공하다",
    "program": "프로그램",
    "vulnerabilities": "취약점들",
    "primary": "주요한, 1차적인",
    "cloud": "클라우드",
    "new": "새로운",
    "plan": "계획",
    "site": "사이트, 장소",
    "company": "회사",
    "change": "변경, 변화",
    "first": "첫 번째",
    "address": "주소, 처리하다",
    "disaster": "재해, 재난",
    "password": "비밀번호",
    "one": "하나",
    "owner": "소유자",
    "provider": "제공자, 공급자",
    "technology": "기술",
    "report": "보고서, 보고하다",
    "file": "파일",
    "party": "당사자, 파티",
    "applications": "애플리케이션들",
    "device": "장치",
    "provides": "제공한다",
    "effective": "효과적인",
    "protection": "보호",
    "within": "내부에, 안에",
    "third": "세 번째",
    "impact": "영향, 충격",
    "important": "중요한",
    "processes": "프로세스들",
    "environment": "환경",
    "traffic": "트래픽, 통신량",
    "critical": "중요한, 비판적인",
    "perform": "수행하다",
    "internal": "내부의",
    "other": "다른",
    "soc": "SOC (보안 운영 센터)",
    "team": "팀",
    "attacks": "공격들",
    "operations": "운영, 작업",
    "virtual": "가상의",
    "design": "설계, 디자인",
    "open": "열린, 공개된",
    "between": "사이에",
    "digital": "디지털",
    "potential": "잠재적인",
    "determine": "결정하다",
    "unauthorized": "무단의, 승인되지 않은",
    "policies": "정책들",
    "solution": "해결책, 솔루션",
    "source": "소스, 출처",
    "common": "일반적인, 공통의",
    "appropriate": "적절한",
    "media": "미디어, 매체",
    "storage": "저장소, 저장",
    "resources": "자원들",
    "services": "서비스들",
    "method": "방법",
    "public": "공개된, 공공의",
    "model": "모델"
}

def add_meanings():
    """의미 추가"""
    # 문제 단어 사전 로드
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미 추가
    added_count = 0
    for word, meaning in meanings_batch1.items():
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

