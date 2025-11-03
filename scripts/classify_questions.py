#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
문제 자동 분류 스크립트
- 키워드 기반으로 각 문제를 9개 카테고리로 자동 분류
- primary_category, secondary_categories, tags, difficulty 자동 판정
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# 카테고리별 키워드 정의
CATEGORY_KEYWORDS = {
    "SQL": {
        "keywords": ["SELECT", "INSERT", "UPDATE", "DELETE", "JOIN", "WHERE", "GROUP BY", 
                    "ORDER BY", "ALTER", "CREATE TABLE", "DROP", "DISTINCT", "HAVING", 
                    "UNION", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "SQL", "쿼리"],
        "weight": 3
    },
    "데이터베이스": {
        "keywords": ["정규화", "제1정규형", "제2정규형", "제3정규형", "BCNF", "키", "기본키", 
                    "외래키", "후보키", "ERD", "스키마", "트랜잭션", "ACID", "인덱스", "뷰", 
                    "무결성", "참조무결성", "개체무결성", "도메인무결성", "이상", "삽입이상", 
                    "삭제이상", "갱신이상", "데이터베이스", "DB", "릴레이션", "테이블", 
                    "속성", "튜플", "카디널리티", "차수", "설계순서", "개념적설계", "논리적설계", 
                    "물리적설계", "요구사항분석", "구현"],
        "weight": 2
    },
    "프로그래밍": {
        "keywords": ["java", "c언어", "python", "파이썬", "자바", "변수", "함수", "메서드",
                    "클래스", "객체", "상속", "다형성", "캡슐화", "추상화", "오버로딩", 
                    "오버라이딩", "포인터", "배열", "문자열", "반복문", "조건문", "for", 
                    "while", "if", "switch", "printf", "System.out", "print", "main", 
                    "static", "void", "int", "char", "float", "double", "코드", "출력값", 
                    "실행결과", "소스코드", "싱글톤", "팩토리", "빌더"],
        "weight": 3
    },
    "자료구조": {
        "keywords": ["스택", "stack", "큐", "queue", "트리", "tree", "그래프", "graph",
                    "배열", "array", "연결리스트", "linked list", "해시", "hash", "힙", "heap",
                    "이진트리", "AVL", "B-tree", "push", "pop", "enqueue", "dequeue",
                    "순회", "전위", "중위", "후위"],
        "weight": 2
    },
    "알고리즘": {
        "keywords": ["정렬", "sort", "버블정렬", "선택정렬", "삽입정렬", "퀵정렬", "병합정렬",
                    "탐색", "search", "이진탐색", "선형탐색", "재귀", "recursion", "동적계획법",
                    "DP", "시간복잡도", "빅오", "O(n)", "O(logn)", "다익스트라", "Dijkstra",
                    "너비우선", "깊이우선", "BFS", "DFS"],
        "weight": 2
    },
    "운영체제": {
        "keywords": ["프로세스", "process", "스레드", "thread", "메모리", "memory", "페이징",
                    "paging", "세그먼테이션", "교착상태", "deadlock", "스케줄링", "scheduling",
                    "CPU", "PCB", "컨텍스트스위칭", "LRU", "LFU", "FIFO", "최적", "프레임",
                    "페이지부재", "세마포어", "뮤텍스", "임계구역", "동기화"],
        "weight": 2
    },
    "네트워크": {
        "keywords": ["TCP", "UDP", "IP", "라우터", "router", "스위치", "switch", "OSI", 
                    "HTTP", "HTTPS", "프로토콜", "protocol", "포트", "port", "DNS", "DHCP",
                    "서브넷", "subnet", "마스크", "게이트웨이", "gateway", "라우팅", "routing",
                    "OSPF", "BGP", "RIP", "MAC", "ARP", "ICMP", "패킷", "세그먼트",
                    "세션하이재킹", "네트워크"],
        "weight": 2
    },
    "정보보안": {
        "keywords": ["암호화", "encryption", "복호화", "해킹", "hacking", "방화벽", "firewall",
                    "인증", "authentication", "보안", "security", "SQL인젝션", "XSS", "CSRF",
                    "세션", "session", "공격", "attack", "취약점", "vulnerability", "DDoS",
                    "해시", "RSA", "AES", "DES", "대칭키", "비대칭키", "공개키", "개인키",
                    "루트킷", "rootkit", "템퍼프루핑", "워터링홀", "스니핑", "스푸핑"],
        "weight": 2
    },
    "소프트웨어공학": {
        "keywords": ["테스트", "test", "단위테스트", "통합테스트", "시스템테스트", "인수테스트",
                    "화이트박스", "블랙박스", "커버리지", "coverage", "구문커버리지", "결정커버리지",
                    "조건커버리지", "UML", "유스케이스", "클래스다이어그램", "시퀀스다이어그램",
                    "디자인패턴", "pattern", "애자일", "agile", "폭포수", "waterfall", 
                    "요구사항", "requirement", "설계", "design", "유지보수", "maintenance",
                    "결합도", "coupling", "응집도", "cohesion", "JUnit", "WSDL", "REST",
                    "SOAP", "API", "리팩토링"],
        "weight": 2
    }
}

# 태그 정의
DETAILED_TAGS = {
    "프로그래밍": {
        "java": ["java", "자바", "class", "public", "static"],
        "c": ["c언어", "#include", "stdio.h", "printf", "scanf"],
        "python": ["python", "파이썬", "def", "print(", "import"],
        "객체지향": ["클래스", "객체", "상속", "다형성", "캡슐화"],
        "싱글톤": ["싱글톤", "singleton", "_inst", "get()"],
        "포인터": ["포인터", "*", "->", "&"],
    },
    "데이터베이스": {
        "정규화": ["정규화", "제1정규형", "제2정규형", "제3정규형", "BCNF"],
        "ERD": ["ERD", "개체관계도", "엔티티"],
        "설계순서": ["설계순서", "개념적설계", "논리적설계", "물리적설계"],
        "무결성": ["무결성", "참조무결성", "개체무결성", "도메인무결성"],
    },
    "네트워크": {
        "IP": ["IP", "주소", "서브넷", "마스크"],
        "라우팅": ["라우팅", "라우터", "OSPF", "BGP", "RIP"],
        "TCP/IP": ["TCP", "UDP", "3-way", "핸드셰이크"],
    },
    "정보보안": {
        "해킹": ["해킹", "공격", "취약점"],
        "암호화": ["암호화", "복호화", "AES", "DES", "RSA"],
        "세션": ["세션", "하이재킹", "쿠키"],
    },
    "소프트웨어공학": {
        "화이트박스": ["화이트박스", "구문커버리지", "결정커버리지"],
        "블랙박스": ["블랙박스", "동등분할", "경곗값"],
        "디자인패턴": ["디자인패턴", "싱글톤", "팩토리", "빌더"],
    }
}

def calculate_category_score(text: str, category: str) -> float:
    """카테고리별 점수 계산"""
    config = CATEGORY_KEYWORDS[category]
    keywords = config["keywords"]
    weight = config["weight"]
    
    score = 0
    text_upper = text.upper()
    
    for keyword in keywords:
        keyword_upper = keyword.upper()
        # 정확한 단어 매칭 (대소문자 구분 없음)
        count = len(re.findall(r'\b' + re.escape(keyword_upper) + r'\b', text_upper))
        if count == 0:
            # 정확한 매칭이 없으면 부분 문자열 매칭
            count = text_upper.count(keyword_upper)
        score += count
    
    return score * weight

def classify_question(question: Dict) -> Tuple[str, List[str]]:
    """문제를 분류하여 primary_category와 secondary_categories 반환"""
    question_text = question.get("question_text", "") or ""
    explanation = question.get("explanation", "") or ""
    text = question_text + " " + explanation
    
    # 각 카테고리별 점수 계산
    scores = {}
    for category in CATEGORY_KEYWORDS.keys():
        scores[category] = calculate_category_score(text, category)
    
    # 점수 순으로 정렬
    sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # primary: 가장 높은 점수
    primary = sorted_categories[0][0] if sorted_categories[0][1] > 0 else "기타"
    
    # secondary: 2~3위 중 점수가 primary의 50% 이상인 것
    secondary = []
    if len(sorted_categories) > 1:
        primary_score = sorted_categories[0][1]
        for cat, score in sorted_categories[1:3]:
            if score > 0 and score >= primary_score * 0.5:
                secondary.append(cat)
    
    return primary, secondary

def extract_tags(question: Dict, primary_category: str) -> List[str]:
    """문제에서 세부 태그 추출"""
    question_text = question.get("question_text", "") or ""
    explanation = question.get("explanation", "") or ""
    text = question_text + " " + explanation
    text_upper = text.upper()
    
    tags = []
    
    if primary_category in DETAILED_TAGS:
        for tag_name, tag_keywords in DETAILED_TAGS[primary_category].items():
            for keyword in tag_keywords:
                if keyword.upper() in text_upper:
                    tags.append(tag_name)
                    break
    
    # code_blocks에서 언어 태그 추출
    if question.get("code_blocks"):
        for code_block in question["code_blocks"]:
            lang = code_block.get("language", "")
            if lang and lang not in tags:
                tags.append(lang)
    
    return list(set(tags))[:5]  # 최대 5개

def determine_difficulty(question: Dict) -> str:
    """난이도 자동 판정"""
    text = question.get("question_text", "")
    answer_keys = question.get("answer", {}).get("keys", [])
    code_blocks = question.get("code_blocks", [])
    
    score = 0
    
    # 코드 블록 존재 및 길이
    if code_blocks:
        for block in code_blocks:
            code_length = len(block.get("code", "").split("\n"))
            if code_length > 30:
                score += 3
            elif code_length > 15:
                score += 2
            else:
                score += 1
    
    # 답안 개수
    if len(answer_keys) >= 3:
        score += 2
    elif len(answer_keys) >= 2:
        score += 1
    
    # 복잡도 키워드
    complex_keywords = ["포인터", "재귀", "상속", "다형성", "정규화", "트랜잭션", "교착상태"]
    for keyword in complex_keywords:
        if keyword in text:
            score += 1
    
    # 판정
    if score >= 5:
        return "어려움"
    elif score >= 2:
        return "보통"
    else:
        return "쉬움"

def estimate_time(difficulty: str, has_code: bool) -> int:
    """예상 소요 시간 (분)"""
    base_time = {"쉬움": 2, "보통": 3, "어려움": 5}
    time = base_time[difficulty]
    if has_code:
        time += 2
    return time

def main():
    print("=" * 80)
    print("문제 자동 분류 시작")
    print("=" * 80)
    
    ROUNDS = [
        (2021, 1), (2022, 1), (2022, 2), (2022, 3),
        (2023, 1), (2023, 2), (2023, 3),
        (2024, 1), (2024, 2), (2024, 3),
        (2025, 1), (2025, 2)
    ]
    
    total_questions = 0
    category_stats = {cat: 0 for cat in CATEGORY_KEYWORDS.keys()}
    category_stats["기타"] = 0
    
    for year, round_num in ROUNDS:
        doc_id = f"{year}_round{round_num}"
        jsonl_path = Path(f"data/items_{doc_id}.jsonl")
        
        if not jsonl_path.exists():
            print(f"\n[건너뜀] {doc_id}: 파일 없음")
            continue
        
        print(f"\n[처리중] {doc_id}")
        
        # JSONL 읽기
        questions = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        # 분류 및 메타데이터 추가
        for q in questions:
            primary, secondary = classify_question(q)
            tags = extract_tags(q, primary)
            difficulty = determine_difficulty(q)
            has_code = len(q.get("code_blocks", [])) > 0
            est_time = estimate_time(difficulty, has_code)
            
            q["primary_category"] = primary
            q["secondary_categories"] = secondary
            q["tags"] = tags
            q["difficulty"] = difficulty
            q["estimated_time"] = est_time
            
            category_stats[primary] += 1
            total_questions += 1
            
            print(f"  {q['q_no']}: {primary} | 난이도: {difficulty} | 태그: {', '.join(tags[:3])}")
        
        # JSONL 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"  ✅ {len(questions)}개 문제 분류 완료")
    
    print("\n" + "=" * 80)
    print("카테고리별 문제 수")
    print("=" * 80)
    for cat, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_questions * 100) if total_questions > 0 else 0
        print(f"  {cat:15s}: {count:3d}개 ({percentage:5.1f}%)")
    
    print(f"\n총 {total_questions}개 문제 분류 완료!")

if __name__ == "__main__":
    main()

