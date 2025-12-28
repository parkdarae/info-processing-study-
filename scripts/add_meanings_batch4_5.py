#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빈도 301-500번째 단어에 한글 의미 추가 (배치 4-5)"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 301-500번째 단어의 한글 의미
meanings_batch4_5 = {
    # 301-400
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
    
    # 401-500
    "specific": "특정한",
    "multiple": "다중의",
    "physical": "물리적인",
    "application": "애플리케이션",
    "control": "통제, 제어",
    "network": "네트워크",
    "security": "보안",
    "data": "데이터",
    "access": "접근",
    "system": "시스템",
    "information": "정보",
    "management": "관리",
    "software": "소프트웨어",
    "service": "서비스",
    "based": "기반의",
    "controls": "통제들",
    "user": "사용자",
    "business": "비즈니스",
    "use": "사용하다",
    "used": "사용된",
    "process": "프로세스",
    "code": "코드",
    "testing": "테스트",
    "systems": "시스템들",
    "ensure": "보장하다",
    "layer": "계층",
    "analysis": "분석",
    "key": "키",
    "level": "수준",
    "web": "웹",
    "development": "개발",
    "using": "사용하여",
    "review": "검토",
    "users": "사용자들",
    "requirements": "요구사항",
    "time": "시간",
    "server": "서버",
    "identity": "신원",
    "internet": "인터넷",
    "test": "테스트",
    "type": "유형",
    "devices": "장치들",
    "provide": "제공하다",
    "program": "프로그램",
    "vulnerabilities": "취약점들",
    "primary": "주요한",
    "cloud": "클라우드",
    "new": "새로운",
    "plan": "계획",
    "site": "사이트",
    "company": "회사",
    "change": "변경",
    "first": "첫 번째",
    "address": "주소",
    "disaster": "재해",
    "password": "비밀번호",
    "one": "하나",
    "owner": "소유자",
    "provider": "제공자",
    "technology": "기술",
    "report": "보고서",
    "file": "파일",
    "party": "당사자",
    "applications": "애플리케이션들",
    "device": "장치",
    "provides": "제공한다",
    "effective": "효과적인",
    "protection": "보호",
    "within": "내부에",
    "third": "세 번째",
    "impact": "영향",
    "important": "중요한",
    "processes": "프로세스들",
    "environment": "환경",
    "traffic": "트래픽",
    "critical": "중요한",
    "perform": "수행하다",
    "internal": "내부의",
    "other": "다른",
    "soc": "SOC",
    "team": "팀",
    "attacks": "공격들",
    "operations": "운영",
    "virtual": "가상의",
    "design": "설계",
    "open": "열린",
    "between": "사이에",
    "digital": "디지털",
    "potential": "잠재적인",
    "determine": "결정하다",
    "unauthorized": "무단의",
    "policies": "정책들",
    "solution": "해결책",
    "source": "소스",
    "common": "일반적인",
    "appropriate": "적절한",
    "media": "미디어",
    "storage": "저장소",
    "resources": "자원들",
    "services": "서비스들",
    "method": "방법",
    "public": "공개된",
    "model": "모델"
}

def add_meanings():
    """의미 추가"""
    # 문제 단어 사전 로드
    with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 의미 추가
    added_count = 0
    skipped_count = 0
    not_found_count = 0
    
    for word, meaning in meanings_batch4_5.items():
        if word in vocab:
            if not vocab[word].get('meaning') or vocab[word].get('meaning', '').strip() == '':
                vocab[word]['meaning'] = meaning
                added_count += 1
                if added_count <= 20:  # 처음 20개만 출력
                    print(f"[OK] {word}: {meaning}")
            else:
                skipped_count += 1
        else:
            not_found_count += 1
    
    # 저장
    with open('data/cissp_problem_vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
    
    print(f"\n총 {added_count}개 단어에 의미가 추가되었습니다.")
    if skipped_count > 0:
        print(f"이미 의미가 있는 단어: {skipped_count}개")
    if not_found_count > 0:
        print(f"사전에 없는 단어: {not_found_count}개")

if __name__ == '__main__':
    add_meanings()

