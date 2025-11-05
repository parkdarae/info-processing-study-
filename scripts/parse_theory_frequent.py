#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import os

def parse_theory_frequent():
    """필수암기최빈출.txt 파일을 파싱하여 50개 항목을 추출하고 라벨링"""
    
    # 라벨 분류 매핑
    label_mapping = {
        'sql': ['트랜잭션', 'ACID', 'SQL', 'JOIN', 'SELECT', '데이터베이스', 'DB'],
        'database': ['트랜잭션', 'ACID', '정규화', '이상현상', '회복', '체크포인트', '로그', '병행제어', '갱신손실'],
        'programming': ['알고리즘', '자료구조', '프로그래밍', '코드', '함수', '변수', '배열'],
        'os': ['스케줄링', '프로세스', '운영체제', 'CPU', 'RR', 'SJF', 'FCFS', 'HRN', 'SRT', '선점', '비선점'],
        'network': ['OSI', '계층', '프로토콜', 'TCP', 'UDP', 'IP', 'ARP', 'ICMP', '네트워크', '통신'],
        'security': ['암호화', 'RSA', 'AES', 'DES', 'SHA', 'MD5', '해시', '보안', '기밀성', '무결성', '가용성'],
        'software_engineering': ['응집도', '결합도', '모듈', '독립성', '유지보수', '형상관리', 'EAI', 'UML', '다이어그램'],
        'data_structure': ['스택', '큐', '트리', '그래프', '배열', '리스트'],
        'algorithm': ['정렬', '탐색', '알고리즘', '시간복잡도', '공간복잡도']
    }
    
    # 파일 경로 설정
    input_file = 'C:/Users/darae/Desktop/info_ver4/필수암기최빈출.txt'
    
    try:
        # 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"파일 읽기 성공: {len(content)} 문자")
        
        # 항목별로 파싱
        items = []
        lines = content.split('\n')
        current_item = {}
        item_counter = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 숫자로 시작하는 제목 찾기 (예: "1. 트랜잭션 특성 - ACID")
            if re.match(r'^\d+\.', line):
                if current_item:  # 이전 항목 저장
                    items.append(current_item)
                
                item_counter += 1
                current_item = {
                    'id': item_counter,
                    'title': line,
                    'content': '',
                    'labels': [],
                    'type': 'flashcard',
                    'difficulty': 'medium'
                }
                
                # 다음 줄들을 내용으로 수집
                i += 1
                content_lines = []
                while i < len(lines) and not re.match(r'^\d+\.', lines[i].strip()) and lines[i].strip():
                    content_lines.append(lines[i].strip())
                    i += 1
                
                current_item['content'] = '\n'.join(content_lines)
                
                # 라벨 분류
                text_for_labeling = (current_item['title'] + ' ' + current_item['content']).lower()
                for label, keywords in label_mapping.items():
                    for keyword in keywords:
                        if keyword.lower() in text_for_labeling:
                            if label not in current_item['labels']:
                                current_item['labels'].append(label)
                
                # 라벨이 없으면 기타로 분류
                if not current_item['labels']:
                    current_item['labels'] = ['other']
                
                continue
            
            i += 1
        
        # 마지막 항목 저장
        if current_item:
            items.append(current_item)
        
        print(f'총 {len(items)}개 항목 파싱 완료')
        
        # 처음 5개 항목 미리보기
        for item in items[:5]:
            print(f'ID: {item["id"]}, Title: {item["title"][:50]}..., Labels: {item["labels"]}')
        
        return items
        
    except Exception as e:
        print(f"파일 파싱 중 오류 발생: {e}")
        return []

if __name__ == "__main__":
    items = parse_theory_frequent()
    print(f"\n파싱 완료: {len(items)}개 항목")
