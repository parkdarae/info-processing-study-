#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
정처기 실기 이론 텍스트 파일 파싱 스크립트
"""

import json
import re
from pathlib import Path

# 카테고리 키워드 매핑
CATEGORY_KEYWORDS = {
    'SQL': ['sql', 'select', 'insert', 'delete', 'update', 'join', 'where', '쿼리', '질의'],
    '데이터베이스': ['데이터베이스', 'database', 'db', 'dbms', '트랜잭션', '정규화', '반정규화', '스키마', 
                  '테이블', '릴레이션', 'erd', '개체', '속성', '키', 'acid', 'rollback', 'commit'],
    '프로그래밍': ['프로그래밍', '코드', '변수', '함수', '클래스', '객체', '메서드', 
                 'java', 'python', 'c언어', 'javascript'],
    '자료구조': ['자료구조', '스택', 'stack', '큐', 'queue', '트리', 'tree', '그래프', 'graph', 
              '리스트', 'list', '배열', 'array', '해시', 'hash'],
    '알고리즘': ['알고리즘', '정렬', 'sort', '탐색', 'search', '순회', '다익스트라', 
              '시간복잡도', '공간복잡도', 'dfs', 'bfs', '하둡', '맵리듀스'],
    '운영체제': ['운영체제', 'os', '프로세스', 'process', '스레드', 'thread', '스케줄링', 
              '메모리', '페이지', '세그먼트', 'cpu', '교착상태', 'deadlock', 'ipc'],
    '네트워크': ['네트워크', 'network', 'tcp', 'udp', 'ip', 'http', 'https', 'osi', 
              '프로토콜', 'protocol', 'dns', 'dhcp', 'nat', '라우팅', 'icmp', 'arp', 
              'ipv4', 'ipv6', 'ajax', 'soap', 'eai'],
    '정보보안': ['보안', '암호화', 'encryption', '해시', '접근통제', '인증', 'authentication',
              '방화벽', 'firewall', 'xss', 'csrf', 'injection', '스니핑', '스푸핑',
              '공격', 'attack', 'md5', 'sha', '랜드어택', 'ipsec'],
    '소프트웨어공학': ['소프트웨어', '방법론', '테스트', 'test', '설계', 'design', '패턴', 'pattern',
                   '형상관리', '리팩토링', 'refactoring', '릴리즈', 'uml', '블랙박스', '화이트박스',
                   '응집도', '결합도', '오라클', '살충제패러독스']
}

def categorize_by_keywords(text):
    """키워드 매칭으로 카테고리 자동 분류"""
    text_lower = text.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    return '기타'

def extract_abbreviations(term_part):
    """용어에서 약어 추출"""
    abbreviations = []
    
    # 괄호 안의 내용 추출: (DAC:Discretionary Access Control)
    paren_match = re.findall(r'\(([^)]+)\)', term_part)
    for match in paren_match:
        # : 로 구분된 약어들 추출
        parts = match.split(':')
        for part in parts:
            cleaned = part.strip()
            if cleaned:
                abbreviations.append(cleaned)
    
    return abbreviations

def parse_theory_file(input_file):
    """텍스트 파일 파싱"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    items = []
    doc_id = 1
    
    # 빈 줄로 구분된 섹션으로 분리
    sections = re.split(r'\n\n\n+', content)
    
    current_category = None
    current_subcategory = None
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        if not lines:
            continue
        
        # 제목(분류) 감지: ':'로 끝나는 줄
        title_line = lines[0]
        if title_line.endswith(':'):
            current_subcategory = title_line[:-1].strip()
            lines = lines[1:]  # 제목 제외
            
            # 카테고리 자동 분류
            current_category = categorize_by_keywords(current_subcategory)
        
        # 제목만 있고 내용이 없으면 스킵
        if not lines:
            continue
        
        # 항목이 번호나 용어로 시작하는 경우
        for line in lines:
            # '-' 구분자로 분리
            if ' - ' in line:
                parts = line.split(' - ', 1)
                term_part = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ""
                
                # 번호 제거 (1. 2. 3. 등)
                term_part = re.sub(r'^\d+\.\s*', '', term_part)
                
                # 약어 추출
                abbreviations = extract_abbreviations(term_part)
                
                # 괄호와 내용 제거하여 순수 용어 추출
                term = re.sub(r'\s*\([^)]+\)', '', term_part).strip()
                
                # 정답으로 인정할 답안 목록
                accept_answers = [term]
                accept_answers.extend(abbreviations)
                
                # 중복 제거
                accept_answers = list(dict.fromkeys(accept_answers))
                
                item = {
                    "doc_id": f"theory_{doc_id:03d}",
                    "category": current_category or "기타",
                    "subcategory": current_subcategory or "일반",
                    "term": term,
                    "abbreviations": abbreviations,
                    "description": description,
                    "accept_answers": accept_answers
                }
                
                items.append(item)
                doc_id += 1
            
            # '-' 구분자가 없는 경우 (단독 설명)
            elif current_subcategory and not line.endswith(':'):
                # 제목이 용어이고 본문이 설명인 경우
                term = current_subcategory
                description = line
                
                # 약어 추출
                abbreviations = extract_abbreviations(term)
                
                # 괄호 제거
                term_clean = re.sub(r'\s*\([^)]+\)', '', term).strip()
                
                accept_answers = [term_clean]
                accept_answers.extend(abbreviations)
                accept_answers = list(dict.fromkeys(accept_answers))
                
                item = {
                    "doc_id": f"theory_{doc_id:03d}",
                    "category": current_category or "기타",
                    "subcategory": current_subcategory,
                    "term": term_clean,
                    "abbreviations": abbreviations,
                    "description": description,
                    "accept_answers": accept_answers
                }
                
                items.append(item)
                doc_id += 1
                
                # 한 번만 추가
                break
    
    return items

def save_to_jsonl(items, output_file):
    """JSONL 파일로 저장"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    input_file = Path('정처기실기이론.txt')
    output_file = Path('data/items_theory.jsonl')
    
    print(f"파싱 시작: {input_file}")
    items = parse_theory_file(input_file)
    
    print(f"총 {len(items)}개 항목 파싱 완료")
    
    # 카테고리별 통계
    category_stats = {}
    for item in items:
        cat = item['category']
        category_stats[cat] = category_stats.get(cat, 0) + 1
    
    print("\n카테고리별 통계:")
    for cat, count in sorted(category_stats.items()):
        print(f"  {cat}: {count}개")
    
    # 저장
    output_file.parent.mkdir(parents=True, exist_ok=True)
    save_to_jsonl(items, output_file)
    print(f"\n저장 완료: {output_file}")
    
    # 샘플 출력
    print("\n=== 샘플 데이터 (처음 3개) ===")
    for item in items[:3]:
        print(f"\n[{item['doc_id']}] {item['category']} > {item['subcategory']}")
        print(f"용어: {item['term']}")
        print(f"약어: {item['abbreviations']}")
        print(f"설명: {item['description'][:50]}...")
        print(f"정답 인정: {item['accept_answers']}")

if __name__ == '__main__':
    main()

