#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
수동 웹 검색 기반 해설 개선 스크립트
각 문제를 하나씩 처리하며 문제의 실제 내용과 1:1로 매칭되는 해설 작성
"""

import json
import sys
import os
from pathlib import Path

# 한글 출력을 위한 인코딩 설정
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def load_jsonl(file_path):
    """JSONL 파일을 읽어서 리스트로 반환"""
    items = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items

def save_jsonl(file_path, items):
    """리스트를 JSONL 파일로 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def improve_q002_explanation(item):
    """Q002 (Attribute) 문제의 해설을 개선"""
    new_explanation = """이 문제는 데이터베이스 릴레이션의 구성 요소 중 Attribute(속성)를 설명하는 문제입니다.

**문제에서 설명하는 각 특징을 하나씩 분석:**

1. **"릴레이션에서 열(Column)을 의미"**
   - 릴레이션은 관계형 데이터베이스에서 테이블을 의미합니다.
   - 열(Column)은 테이블의 세로 방향 구조로, 데이터의 한 가지 특성을 나타냅니다.
   - Attribute는 이 열(Column)과 동일한 개념입니다.

2. **"데이터 항목의 속성(Attribute) 또는 특성을 나타낸다"**
   - 각 Attribute는 데이터 항목이 가지고 있는 특성을 정의합니다.
   - 예를 들어, 사람에 대한 속성으로는 이름, 나이, 주소 등이 있습니다.

3. **"각 열은 고유한 이름을 가지며 특정 도메인(Domain)에서 정의된 값을 갖는다"**
   - 각 Attribute는 유일한 이름(예: 학번, 이름, 전공)을 가집니다.
   - 도메인(Domain)은 그 Attribute에 입력될 수 있는 값의 범위를 의미합니다.
   - 예를 들어, 나이 Attribute는 0 이상의 정수만 입력 가능한 도메인을 가질 수 있습니다.

4. **예시: "학생" 릴레이션에서 학번, 이름, 전공 등은 각각 하나의 열**
   - 학번 열: 학생의 고유 번호를 나타내는 Attribute
   - 이름 열: 학생의 이름을 나타내는 Attribute
   - 전공 열: 학생의 전공 분야를 나타내는 Attribute
   - 이들은 모두 학생이라는 엔티티의 서로 다른 속성을 나타냅니다.

5. **"파일 구조에서의 필드(Field)에 해당"**
   - 파일 구조에서 필드는 데이터의 한 단위를 의미합니다.
   - 데이터베이스의 Attribute는 파일 구조의 필드와 동일한 역할을 합니다.
   - 둘 다 데이터의 특성을 저장하는 단위입니다.

6. **"릴레이션에서 행(Row, Tuple)의 구성 요소"**
   - 한 행(튜플)은 여러 Attribute 값들로 구성됩니다.
   - 예를 들어, 한 학생의 행은 (학번: 2024001, 이름: "홍길동", 전공: "컴퓨터공학") 형태입니다.
   - 여기서 각 값(2024001, "홍길동", "컴퓨터공학")은 해당 Attribute의 실제 값입니다.

**보기 분석:**
- ㄱ. Cardinality(카디널리티): 릴레이션에서 튜플(행)의 개수를 의미합니다. 문제에서 설명하는 "열"과는 반대로 "행의 개수"를 의미하므로 문제 설명과 일치하지 않습니다.
- ㄷ. Attribute(속성): 문제에서 설명하는 모든 특징(열, 속성, 고유한 이름, 도메인, 필드에 해당, 행의 구성 요소)이 Attribute의 정의와 정확히 일치합니다.

**결론:** 문제에서 설명하는 모든 특징이 Attribute의 정의와 완전히 일치하므로 답은 "ㄷ"입니다."""
    
    return new_explanation

def improve_q003_explanation(item):
    """Q003 (SSH) 문제의 해설을 개선"""
    new_explanation = """SSH(Secure Shell)는 원격 접속을 위한 보안 프로토콜입니다.

**문제에서 설명한 특징과 정확히 매칭:**

1. **"원격 접속과 관련된 보안 프로토콜이며 암호화된 통신을 제공"**
   - SSH는 네트워크를 통해 원격 컴퓨터에 안전하게 접속하기 위해 사용됩니다.
   - 모든 통신 데이터를 암호화하여 전송하므로 네트워크상에서 가로채더라도 내용을 알 수 없습니다.
   - 이는 평문으로 통신하는 Telnet의 보안 취약점을 해결한 것입니다.

2. **"공개키 기반의 인증 방식을 사용하며 암호화된 데이터 전송을 지원"**
   - SSH는 공개키 암호화 방식을 사용하여 사용자를 인증합니다.
   - 공개키-개인키 쌍을 사용하므로 비밀번호보다 더 안전한 인증이 가능합니다.
   - 모든 데이터가 암호화되어 전송되므로 기밀성이 보장됩니다.

3. **"주로 원격 서버에 안전하게 접속할 때 사용되며 기본 포트 번호는 22번"**
   - SSH는 주로 서버 관리자가 원격으로 서버에 접속하여 명령을 실행할 때 사용됩니다.
   - SSH의 표준 포트 번호는 22번입니다. 이는 SSH를 식별하는 중요한 특징 중 하나입니다.
   - 포트 번호 22번은 IANA(Internet Assigned Numbers Authority)에서 SSH에 할당한 공식 포트입니다.

4. **"Telnet의 보안 취약점을 보완한 대안으로 널리 사용된다"**
   - Telnet은 모든 데이터를 평문으로 전송하므로 네트워크상에서 비밀번호 등 중요한 정보가 노출될 위험이 있습니다.
   - SSH는 이러한 보안 취약점을 해결하기 위해 개발되었으며, 현재 원격 접속의 표준 프로토콜로 널리 사용됩니다.

**답:** 문제에서 설명한 모든 특징(원격 접속, 암호화된 통신, 공개키 인증, 포트 22번, Telnet의 대안)이 SSH와 정확히 일치하므로 답은 "SSH"입니다."""
    
    return new_explanation

def main():
    # 2025년 2회 파일 경로
    file_path = Path('data/items_2025_round2.jsonl')
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return
    
    # 백업
    backup_path = file_path.with_suffix('.jsonl.backup')
    items = load_jsonl(file_path)
    save_jsonl(backup_path, items)
    print(f"백업 생성: {backup_path}")
    
    # Q002 개선
    for item in items:
        if item.get('q_no') == 'Q002':
            print(f"\nQ002 해설 개선 중...")
            item['explanation'] = improve_q002_explanation(item)
            print("✓ Q002 해설 개선 완료")
            break
    
    # Q003 개선
    for item in items:
        if item.get('q_no') == 'Q003':
            print(f"\nQ003 해설 개선 중...")
            item['explanation'] = improve_q003_explanation(item)
            print("✓ Q003 해설 개선 완료")
            break
    
    # 저장
    save_jsonl(file_path, items)
    print(f"\n파일 저장 완료: {file_path}")

if __name__ == '__main__':
    main()


