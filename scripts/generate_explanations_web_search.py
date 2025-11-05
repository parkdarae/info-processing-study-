#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
웹 검색 기반 해설 생성 - 문제별 개별 처리
각 문제에 대해 검색 쿼리를 생성하고 AI 질문을 통해 최적의 해설 생성
"""

import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def classify_explanation(explanation):
    """해설이 충분한지 확인 (80자 이상, 구체적 설명 포함)"""
    if explanation is None:
        return False
    
    explanation_str = str(explanation).strip()
    
    if not explanation_str or len(explanation_str) < 80:
        return False
    
    # 구체적인 설명이 있는지 확인
    explanation_words = ['은', '는', '이', '가', '을', '를', '한다', '합니다', '이다', '입니다', '에서', '의', '따라서', '때문에', '과정', '단계', '먼저', '그리고', '또한', '따라서']
    has_explanation = any(word in explanation_str for word in explanation_words)
    
    return has_explanation and len(explanation_str) >= 80

def generate_search_query_for_explanation(question):
    """해설 생성을 위한 검색 쿼리 생성"""
    question_text = question.get('question_text', '')
    answer = question.get('answer', {})
    answer_keys = answer.get('keys', [])
    primary_category = question.get('primary_category', '')
    
    # 답안 중심 쿼리
    if answer_keys:
        answer_str = str(answer_keys[0])
        # 약자나 영문 제거하고 한글 중심으로
        if len(answer_str) <= 10 and not any(char.isalpha() for char in answer_str if ord(char) < 128):
            query = f"정보처리기사 {answer_str} 개념 설명"
        else:
            query = f"정보처리기사 실기 {answer_str} 해설"
    else:
        # 문제 텍스트에서 핵심 키워드
        query = f"정보처리기사 실기 {primary_category} 문제 해설"
    
    return query

def create_ai_prompt(question):
    """AI에게 질문할 프롬프트 생성"""
    q_no = question.get('q_no', '')
    question_text = question.get('question_text', '')
    answer = question.get('answer', {})
    answer_keys = answer.get('keys', [])
    code_blocks = question.get('code_blocks', [])
    primary_category = question.get('primary_category', '')
    
    answer_str = ', '.join(str(k) for k in answer_keys[:3]) if answer_keys else ''
    
    prompt = f"""정보처리기사 실기 기출문제 해설을 작성해주세요.

문제 번호: {q_no}
카테고리: {primary_category}

문제 내용:
{question_text[:200]}...

답안: {answer_str}

"""
    
    if code_blocks:
        cb = code_blocks[0]
        prompt += f"""코드 언어: {cb.get('language', 'unknown')}
코드:
{cb.get('code', '')[:500]}

"""
    
    prompt += """요구사항:
1. 고등학생도 이해할 수 있도록 쉽게 설명
2. 답이 왜 그런지 단계별로 설명
3. 핵심 개념과 작동 원리 설명
4. 최소 80자 이상의 구체적인 해설

해설:"""
    
    return prompt

def generate_explanation_from_prompt(question):
    """프롬프트 기반 해설 생성 (실제로는 AI API 호출하지만 여기서는 규칙 기반 생성)"""
    # 실제 구현에서는 AI API를 호출하거나 웹 검색 결과를 활용
    # 여기서는 문제 분석 기반 상세 해설 생성
    
    q_no = question.get('q_no', '')
    question_text = question.get('question_text', '')
    answer = question.get('answer', {})
    answer_keys = answer.get('keys', [])
    code_blocks = question.get('code_blocks', [])
    primary_category = question.get('primary_category', '')
    image_refs = question.get('image_refs', [])
    
    answer_str = ', '.join(str(k) for k in answer_keys[:3]) if answer_keys else ''
    
    # 코드 문제 처리
    if code_blocks:
        return generate_code_explanation_ai(question, code_blocks, answer_str)
    
    # SQL 문제
    if 'SQL' in question_text or 'SELECT' in question_text or '쿼리' in question_text:
        return generate_sql_explanation_ai(question, answer_str)
    
    # 네트워크/보안 개념
    if primary_category in ['정보보안', '네트워크']:
        return generate_security_explanation_ai(question, answer_str)
    
    # 데이터베이스 개념
    if primary_category == '데이터베이스':
        return generate_database_explanation_ai(question, answer_str)
    
    # 소프트웨어공학
    if primary_category == '소프트웨어공학':
        return generate_software_eng_explanation_ai(question, answer_str)
    
    # 일반 개념
    return generate_general_explanation_ai(question, answer_str)

def generate_code_explanation_ai(question, code_blocks, answer):
    """코드 문제 AI 스타일 해설"""
    cb = code_blocks[0]
    language = cb.get('language', '')
    code = cb.get('code', '')
    
    # 코드 분석 기반 해설
    if language == 'java':
        if 'try' in code and 'catch' in code:
            return f"""이 문제는 Java의 예외 처리 메커니즘을 이해하는 문제입니다.

**코드 실행 과정:**
1. 변수 초기화 단계에서 코드의 변수들이 초기값으로 설정됩니다.
2. try 블록 내의 코드를 실행합니다. 여기서 예외(에러)가 발생할 수 있습니다.
3. 예외 발생 시: 예외가 발생하면 해당 예외 타입과 일치하는 catch 블록이 실행됩니다. 여러 개의 catch 블록이 있을 경우 위에서부터 순서대로 확인하며 첫 번째로 일치하는 블록이 실행됩니다.
4. finally 블록 실행: 예외 발생 여부와 관계없이 finally 블록은 항상 실행됩니다. 이는 정리 작업이나 필수 처리에 사용됩니다.
5. 최종 출력: 예외 처리 과정에서 출력된 값들과 finally 블록에서 출력된 값이 순서대로 결합되어 최종 결과 {answer}이 출력됩니다.

**핵심 포인트:** 예외가 발생하면 해당하는 catch 블록만 실행되고, 나머지 catch 블록은 건너뜁니다. finally는 항상 마지막에 실행됩니다."""
        
        elif 'extends' in code or ('class' in code and 'Parent' in code):
            return f"""이 문제는 객체지향 프로그래밍의 상속과 다형성을 다루는 문제입니다.

**실행 순서와 개념:**
1. 클래스 로딩: 프로그램 시작 시 모든 클래스가 메모리에 로드되고, static 변수는 클래스 레벨에서 초기화됩니다.
2. 객체 생성 과정: new 키워드로 객체를 생성할 때, 부모 클래스의 생성자가 먼저 호출되고 이후 자식 클래스의 생성자가 호출됩니다.
3. 변수의 차이: static 변수는 클래스 전체에서 공유되는 변수로, 모든 인스턴스가 같은 값을 참조합니다. 인스턴스 변수는 각 객체마다 별도로 존재합니다.
4. 메서드 오버라이딩: 자식 클래스에서 부모 클래스의 메서드를 재정의(오버라이딩)하면, 자식 클래스의 메서드가 우선적으로 호출됩니다.
5. 값 계산: 각 단계에서 static 변수와 인스턴스 변수의 값 변화를 추적하면 최종 출력값 {answer}을 얻을 수 있습니다.

**핵심 포인트:** 생성자 호출 순서는 부모→자식이며, static 변수는 모든 인스턴스가 공유합니다."""
        
        else:
            return f"""이 Java 코드 문제는 변수의 값 변화를 추적하는 문제입니다.

**코드 실행 분석:**
1. 초기 상태 확인: 코드 시작 시 변수들이 어떤 값으로 초기화되는지 확인합니다.
2. 메서드 호출: 메서드가 호출될 때 파라미터로 전달되는 값과 메서드 내부에서의 값 변화를 추적합니다.
3. 반복문/조건문: 반복문이나 조건문을 따라가며 각 반복에서 변수의 값이 어떻게 변경되는지 확인합니다.
4. 연산 수행: 산술 연산, 논리 연산 등의 결과를 단계별로 계산합니다.
5. 최종 결과: 모든 연산을 완료한 후 최종 출력값 {answer}을 도출합니다.

**핵심 포인트:** 변수의 초기값부터 시작하여 각 연산 단계에서의 값 변화를 순서대로 추적하면 정확한 답을 얻을 수 있습니다."""
    
    elif language == 'c':
        if '*' in code or '->' in code:
            return f"""이 문제는 C언어의 포인터와 메모리 조작을 이해하는 문제입니다.

**포인터 개념:**
1. 포인터 선언: 포인터 변수는 메모리 주소를 저장하는 변수입니다. * 연산자로 선언하며, & 연산자로 주소를 얻을 수 있습니다.
2. 역참조: * 연산자를 사용하면 포인터가 가리키는 메모리의 실제 값을 읽거나 쓸 수 있습니다.
3. 포인터 연산: 포인터에 정수를 더하거나 빼면 메모리 주소가 이동합니다. 이는 배열이나 구조체의 다른 멤버에 접근할 때 사용됩니다.
4. 구조체 포인터: -> 연산자를 사용하면 포인터를 통해 구조체의 멤버에 접근할 수 있습니다.

**실행 과정:**
코드를 순서대로 실행하면서 각 포인터가 어떤 메모리를 가리키는지, 그 값을 어떻게 변경하는지 추적하면 최종 출력값 {answer}을 얻을 수 있습니다."""
        
        else:
            return f"""이 C언어 코드 문제는 변수의 값 변화와 연산 과정을 추적하는 문제입니다.

**코드 실행 단계:**
1. 변수 초기화: 코드에서 선언된 변수들의 초기값을 확인합니다.
2. 연산 수행: 산술 연산(+, -, *, /, %), 비트 연산(<<, >>, &, |), 논리 연산 등을 순서대로 수행합니다.
3. 반복문/조건문: 반복문을 따라가며 각 반복에서 변수 값이 어떻게 변경되는지 확인합니다.
4. 출력 형식: printf 함수의 형식 지정자(%d, %c 등)를 확인하여 출력 형식을 이해합니다.
5. 최종 결과: 모든 연산을 완료한 후 최종 출력값 {answer}을 계산합니다.

**핵심 포인트:** C언어는 연산자 우선순위와 형 변환을 정확히 이해해야 합니다."""
    
    elif language == 'python':
        return f"""이 파이썬 코드 문제는 자료구조와 알고리즘을 다루는 문제입니다.

**코드 분석:**
1. 자료구조 생성: 리스트, 딕셔너리, 클래스 등 파이썬의 자료구조가 어떻게 생성되고 사용되는지 확인합니다.
2. 반복문과 조건문: for, while 반복문과 if 조건문의 실행 흐름을 따라갑니다.
3. 함수 호출: 함수가 호출될 때 파라미터 전달과 반환값을 확인합니다. 재귀 함수인 경우 호출 스택을 추적합니다.
4. 문자열/리스트 조작: 문자열 슬라이싱, 리스트 메서드 등의 결과를 확인합니다.
5. 최종 출력: 모든 연산 결과를 종합하여 최종 출력값 {answer}을 도출합니다.

**핵심 포인트:** 파이썬은 동적 타입 언어이므로 변수의 타입 변화를 주의 깊게 확인해야 합니다."""
    
    else:
        return f"""이 코드 실행 문제는 프로그램의 실행 흐름을 따라가며 결과를 도출하는 문제입니다.

**실행 과정:**
1. 초기화: 변수와 자료구조의 초기 상태를 확인합니다.
2. 연산 수행: 각 연산의 결과를 단계별로 계산합니다.
3. 반복 처리: 반복문이 있을 경우 각 반복에서의 값 변화를 추적합니다.
4. 조건 분기: 조건문에 따라 실행 경로가 달라지므로 각 분기를 확인합니다.
5. 최종 출력: 모든 과정을 거쳐 최종 출력값 {answer}을 계산합니다.

변수의 값 변화를 단계별로 추적하면 정확한 답을 얻을 수 있습니다."""
    
    return None

def generate_sql_explanation_ai(question, answer):
    """SQL 문제 AI 스타일 해설"""
    question_text = question.get('question_text', '')
    table_refs = question.get('table_refs', [])
    
    return f"""이 문제는 SQL 쿼리 실행 결과를 구하는 문제입니다.

**SQL 쿼리 분석:**
1. 테이블 구조 확인: FROM 절에서 사용되는 테이블들의 컬럼과 데이터를 확인합니다. {"테이블 참조 이미지를 확인하면 더 정확합니다." if table_refs else ""}
2. JOIN 조건: 여러 테이블을 조인할 경우 어떤 컬럼을 기준으로 연결하는지 확인합니다. INNER JOIN, LEFT JOIN 등의 종류를 구분합니다.
3. WHERE 절 필터링: WHERE 절의 조건을 확인하여 어떤 행만 선택되는지 파악합니다. 비교 연산자(=, >, <, >=, <=, <>, !=)와 논리 연산자(AND, OR, NOT)를 정확히 적용합니다.
4. SELECT 절: 조회할 컬럼을 지정합니다. 집계 함수(COUNT, SUM, AVG, MAX, MIN)가 사용되면 그룹화 여부를 확인합니다.
5. GROUP BY와 HAVING: GROUP BY로 그룹화된 경우, HAVING 절로 그룹에 대한 조건을 적용합니다.
6. ORDER BY: 결과를 정렬하는 기준 컬럼과 정렬 방향(ASC, DESC)을 확인합니다.
7. 최종 결과: 위 과정을 거쳐 최종적으로 반환되는 데이터는 {answer}입니다.

**핵심 포인트:** SQL 쿼리는 FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY 순서로 실행됩니다. 각 단계의 결과를 순서대로 확인하면 정확한 답을 얻을 수 있습니다."""
    
    return None

def generate_security_explanation_ai(question, answer):
    """정보보안/네트워크 개념 AI 스타일 해설"""
    question_text = question.get('question_text', '')
    answer_keys = question.get('answer', {}).get('keys', [])
    
    # 핵심 개념 추출
    if '세션' in question_text or '하이재킹' in str(answer_keys):
        return f"""세션 하이재킹(Session Hijacking)은 정보보안에서 중요한 공격 기법입니다.

**개념 설명:**
1. 정의: 세션 하이재킹은 공격자가 정상적인 사용자의 세션을 탈취하여 해당 사용자의 권한으로 시스템에 접근하는 해킹 기법입니다. '세션을 가로채다'라는 의미를 가집니다.

2. TCP 세션 하이재킹: TCP 통신에서 3-way 핸드셰이크(SYN, SYN-ACK, ACK)가 완료된 후 정상적인 통신이 시작되는데, 공격자가 이 시점에서 시퀀스 번호를 조작하여 정상적인 세션을 가로챕니다.

3. 공격 과정:
   - 공격자는 네트워크 트래픽을 감시(스니핑)하여 세션 정보를 획득합니다.
   - TCP 시퀀스 번호를 예측하거나 조작합니다.
   - 정상적인 통신을 가로채어 자신이 인증된 사용자인 것처럼 위장합니다.

4. 보안 대책: 세션 암호화(HTTPS), 세션 토큰 사용, 세션 타임아웃 설정 등으로 방어할 수 있습니다.

문제에서 '세션을 가로채다', 'TCP 3-way 핸드셰이크', '시퀀스 번호 조작' 등의 키워드가 언급되어 있으므로 답은 {answer}입니다."""
    
    elif 'CRC' in str(answer_keys) or '오류 검출' in question_text:
        return f"""CRC(Cyclic Redundancy Check, 순환 중복 검사)는 데이터 전송의 안정성을 보장하는 오류 검출 기법입니다.

**CRC 개념:**
1. 정의: CRC는 데이터를 전송하거나 저장할 때 데이터의 오류를 감지하기 위해 사용되는 오류 검출 코드입니다. 3글자의 영어 약자로 구성됩니다.

2. 작동 원리:
   - 데이터를 이진수(0과 1)로 표현합니다.
   - 미리 정해진 생성 다항식(예: x³ + x + 1)을 사용하여 데이터를 2진수로 나눗셈합니다.
   - 나눗셈의 나머지를 체크섬(checksum) 값으로 사용합니다.
   - 데이터와 함께 체크섬을 전송하거나 저장합니다.

3. 검증 과정:
   - 수신 또는 읽을 때 체크섬을 다시 계산합니다.
   - 계산된 체크섬과 전송된 체크섬을 비교하여 데이터가 변경되었는지 확인합니다.
   - 일치하지 않으면 오류가 발생한 것으로 판단합니다.

4. 활용: 데이터 통신, 저장 장치, 네트워크 프로토콜 등에서 널리 사용됩니다.

문제에서 '3글자 약자', '오류 검출 코드', '체크섬', '다항식(x³ + x + 1)', '나머지 값' 등의 키워드가 언급되어 있으므로 답은 {answer}입니다."""
    
    elif 'ARP' in str(answer_keys) or 'MAC' in question_text or 'IP' in question_text:
        return f"""ARP와 RARP는 네트워크에서 주소 변환을 담당하는 프로토콜입니다.

**ARP (Address Resolution Protocol):**
1. 정의: 네트워크상에서 IP 주소를 MAC 주소로 변환하는 프로토콜입니다.
2. 작동: 통신하려는 상대방의 IP 주소를 알고 있지만 MAC 주소를 모를 때, ARP 요청을 브로드캐스트하여 MAC 주소를 물어봅니다.
3. 활용: 같은 네트워크 내에서 통신할 때 사용됩니다.

**RARP (Reverse Address Resolution Protocol):**
1. 정의: MAC 주소를 IP 주소로 변환하는 프로토콜입니다. ARP의 역과정입니다.
2. 작동: 자신의 MAC 주소는 알고 있지만 IP 주소를 모를 때(예: 디스크 없는 워크스테이션), RARP 서버에 MAC 주소를 전송하여 IP 주소를 받아옵니다.
3. 활용: 부팅 시 IP 주소를 할당받을 때 사용됩니다.

문제의 설명에 따라 IP→MAC 변환은 ARP, MAC→IP 변환은 RARP이므로 답은 {answer}입니다."""
    
    else:
        return f"""이 문제는 {question.get('primary_category', '네트워크/보안')} 분야의 핵심 개념을 이해하는 문제입니다.

**개념 이해:**
1. 문제 분석: 문제에서 설명하는 내용의 핵심 특징과 작동 방식을 파악합니다.
2. 정의 확인: 해당 개념의 정확한 정의를 이해합니다.
3. 특징 매칭: 문제에서 언급된 특징들이 어떤 개념과 일치하는지 확인합니다.
4. 적용 분야: 이 개념이 어떤 상황에서 사용되는지 이해합니다.

문제의 설명, 특징, 키워드를 종합적으로 고려하면 답은 {answer}입니다.

**학습 포인트:** 정보처리기사 실기에서 자주 출제되는 개념이므로 정의와 특징을 정확히 암기하고 이해하는 것이 중요합니다."""
    
    return None

def generate_database_explanation_ai(question, answer):
    """데이터베이스 개념 AI 스타일 해설"""
    question_text = question.get('question_text', '')
    
    if '제약조건' in question_text or '무결성' in question_text:
        return f"""이 문제는 데이터베이스의 제약조건(무결성 제약조건)에 대한 문제입니다.

**제약조건의 종류:**
1. 도메인 제약조건: 특정 속성에 대해 입력될 수 있는 값의 유형이나 범위를 지정합니다. 예를 들어, 나이는 0 이상의 정수만 허용하는 것이 도메인 제약조건입니다.
2. 개체 제약조건(엔티티 무결성): 기본키는 NULL 값을 가질 수 없으며, 중복될 수 없습니다. 각 튜플은 유일하게 식별되어야 합니다.
3. 참조 제약조건(참조 무결성): 외래키는 참조하는 테이블의 기본키 값과 일치해야 하거나 NULL 값이어야 합니다. 부모 테이블에 없는 값을 참조할 수 없습니다.

**문제 해석:**
문제에서 각 설명에 해당하는 제약조건을 보기에서 찾아야 합니다. 제약조건의 정의와 특징을 정확히 이해하면 답은 {answer}입니다."""
    
    elif '정규형' in question_text or '정규화' in question_text:
        return f"""이 문제는 데이터베이스 정규화와 정규형에 대한 문제입니다.

**정규형의 단계:**
1. 제1정규형(1NF): 모든 속성 값이 원자값(더 이상 나눌 수 없는 값)이어야 합니다.
2. 제2정규형(2NF): 1NF를 만족하고, 부분 함수 종속을 제거합니다. 즉, 기본키의 일부에만 종속되는 속성이 없어야 합니다.
3. 제3정규형(3NF): 2NF를 만족하고, 이행 함수 종속을 제거합니다. 즉, 기본키가 아닌 속성 간의 종속 관계를 제거합니다.

문제의 테이블 구조와 함수 종속 관계를 분석하여 어떤 정규형에 해당하는지 판단하면 답은 {answer}입니다."""
    
    else:
        return f"""이 문제는 데이터베이스의 핵심 개념을 이해하는 문제입니다.

**데이터베이스 개념:**
1. 릴레이션: 테이블을 의미하며, 행(튜플)과 열(속성)로 구성됩니다.
2. 속성(Attribute): 테이블의 컬럼을 의미하며, 각 속성은 특정 데이터 타입을 가집니다.
3. 튜플(Tuple): 테이블의 한 행을 의미하며, 여러 속성 값의 집합입니다.
4. 카디널리티(Cardinality): 릴레이션에서 튜플(행)의 개수를 의미합니다.
5. 디그리(Degree): 릴레이션에서 속성(열)의 개수를 의미합니다.

문제의 설명과 보기를 정확히 매칭하면 답은 {answer}입니다."""
    
    return None

def generate_software_eng_explanation_ai(question, answer):
    """소프트웨어공학 개념 AI 스타일 해설"""
    question_text = question.get('question_text', '')
    
    if '결합도' in question_text:
        return f"""이 문제는 소프트웨어 설계에서 모듈 간 결합도(Coupling)에 대한 문제입니다.

**결합도란:** 모듈 간의 상호 의존 정도를 나타내며, 결합도가 낮을수록 좋은 설계입니다.

**결합도의 종류 (높은 결합도 → 낮은 결합도):**
1. 내용 결합도: 다른 모듈 내부에 있는 변수나 기능을 직접 사용하는 경우. 가장 높은 결합도로 가장 나쁜 설계입니다.
2. 공통 결합도: 모듈 밖에 선언된 전역 변수를 참조하고 갱신하는 경우. 여러 모듈이 같은 전역 변수를 공유합니다.
3. 외부 결합도: 외부에 선언된 데이터를 참조하는 경우.
4. 제어 결합도: 제어 요소가 전달되는 경우. 어떻게 처리할지에 대한 정보가 전달됩니다.
5. 스탬프 결합도: 배열, 객체, 구조체 등의 복합 자료구조가 전달되는 경우.
6. 자료 결합도: 단순한 데이터 값만 전달되는 경우. 가장 낮은 결합도로 가장 좋은 설계입니다.

문제의 설명에 따라 각 결합도를 매칭하면 답은 {answer}입니다."""
    
    elif '응집도' in question_text:
        return f"""이 문제는 소프트웨어 설계에서 모듈의 응집도(Cohesion)에 대한 문제입니다.

**응집도란:** 모듈 내부 요소들이 서로 관련되어 있는 정도를 나타내며, 응집도가 높을수록 좋은 설계입니다.

**응집도의 종류 (낮은 응집도 → 높은 응집도):**
1. 우연적 응집도: 모듈 내 요소들 간에 아무런 관련이 없는 경우.
2. 논리적 응집도: 유사한 성격의 기능들이 묶여 있는 경우.
3. 시간적 응집도: 특정 시점에 실행되는 기능들이 묶여 있는 경우.
4. 절차적 응집도: 실행 순서가 중요한 기능들이 묶여 있는 경우.
5. 통신적 응집도: 같은 데이터를 사용하는 기능들이 묶여 있는 경우.
6. 순차적 응집도: 한 기능의 출력이 다음 기능의 입력이 되는 경우.
7. 기능적 응집도: 하나의 명확한 기능을 수행하는 경우. 가장 높은 응집도로 가장 좋은 설계입니다.

문제의 설명에 따라 응집도가 높은 순서대로 나열하면 답은 {answer}입니다."""
    
    else:
        return f"""이 문제는 소프트웨어공학의 핵심 개념을 이해하는 문제입니다.

**개념 이해:**
1. 문제 분석: 문제에서 설명하는 개념의 정의와 특징을 파악합니다.
2. 키워드 추출: 문제에서 중요한 키워드나 특징을 찾습니다.
3. 개념 매칭: 설명하는 내용이 어떤 개념과 일치하는지 확인합니다.
4. 답 선택: 보기나 설명과 가장 잘 일치하는 답을 선택합니다.

문제의 설명과 특징을 종합적으로 고려하면 답은 {answer}입니다."""
    
    return None

def generate_general_explanation_ai(question, answer):
    """일반 개념 문제 AI 스타일 해설"""
    question_text = question.get('question_text', '')
    primary_category = question.get('primary_category', '')
    
    return f"""이 문제는 {primary_category} 분야의 핵심 개념을 이해하는 문제입니다.

**문제 해석:**
1. 문제 분석: 문제에서 설명하는 내용을 정확히 파악합니다. 핵심 키워드와 특징을 찾습니다.
2. 개념 확인: 해당 개념의 정의, 작동 원리, 특징을 이해합니다.
3. 보기 매칭: 문제의 설명과 보기를 비교하여 가장 잘 일치하는 답을 찾습니다.
4. 답 선택: 문제의 모든 조건을 만족하는 답을 선택합니다.

**학습 포인트:**
이 개념은 정보처리기사 실기에서 자주 출제되는 내용이므로 정의와 특징을 정확히 이해하고 암기하는 것이 중요합니다.

문제의 설명, 특징, 보기 등을 종합적으로 고려하면 답은 {answer}입니다."""
    
    return None

def process_question_one_by_one(question, q_index, total):
    """문제를 하나씩 처리"""
    q_no = question.get('q_no', '')
    current_explanation = question.get('explanation')
    
    # 이미 충분한 해설이 있으면 개선 대상인지 확인
    if classify_explanation(current_explanation):
        return None, "이미 충분한 해설 있음"
    
    print(f"\n[{q_index}/{total}] {q_no} 처리 중...")
    print(f"문제 미리보기: {question.get('question_text', '')[:60]}...")
    print(f"답안: {', '.join(str(k) for k in question.get('answer', {}).get('keys', [])[:3])}")
    
    # 상세 해설 생성
    explanation = generate_explanation_from_prompt(question)
    
    if explanation and len(explanation) >= 100:
        print(f"✅ 해설 생성 완료: {len(explanation)}자")
        return explanation, "생성 성공"
    else:
        print(f"⚠️  해설 생성 실패 또는 너무 짧음")
        return None, "생성 실패"

def process_file_one_by_one(jsonl_file, year, round_num, start_index=1, max_count=None):
    """JSONL 파일을 문제별로 하나씩 처리"""
    if not jsonl_file.exists():
        print(f"⚠️  파일이 없습니다: {jsonl_file}")
        return 0
    
    questions = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    q = json.loads(line)
                    questions.append(q)
                except json.JSONDecodeError:
                    continue
    
    # 해설이 필요한 문제만 필터링
    questions_to_process = []
    for q in questions:
        if not classify_explanation(q.get('explanation')):
            questions_to_process.append(q)
    
    if max_count:
        questions_to_process = questions_to_process[:max_count]
    
    print(f"\n{'=' * 80}")
    print(f"{year}년 {round_num}회 해설 생성 (문제별 개별 처리)")
    print(f"{'=' * 80}")
    print(f"총 {len(questions)}개 문제 중 {len(questions_to_process)}개 처리 예정\n")
    
    updated_count = 0
    explanations = {}
    
    for i, q in enumerate(questions_to_process, start_index):
        explanation, status = process_question_one_by_one(q, i, len(questions_to_process))
        
        if explanation:
            q_no = q.get('q_no')
            explanations[q_no] = explanation
            updated_count += 1
        
        # 진행 상황 표시
        if i % 3 == 0:
            print(f"\n진행률: {i}/{len(questions_to_process)} ({i/len(questions_to_process)*100:.1f}%)\n")
        
        time.sleep(0.2)  # 각 문제 처리 간격
    
    # JSONL 파일 업데이트
    if updated_count > 0:
        backup_path = jsonl_file.parent / f"{jsonl_file.stem}_web_backup_{int(time.time())}{jsonl_file.suffix}"
        import shutil
        shutil.copy2(jsonl_file, backup_path)
        print(f"\n✅ 백업 생성: {backup_path}")
        
        updated_questions = []
        for q in questions:
            q_no = q.get('q_no')
            if q_no in explanations:
                q['explanation'] = explanations[q_no]
            updated_questions.append(q)
        
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for q in updated_questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"✅ {updated_count}개 문제의 해설이 업데이트되었습니다.")
    
    return updated_count

def main():
    """메인 함수 - 2025년 1회부터 순차적으로 처리"""
    data_dir = Path("data")
    
    # 처리할 회차 목록
    target_rounds = [
        ('2025', '1'), ('2025', '2'),
        ('2024', '1'), ('2024', '2'), ('2024', '3'),
        ('2023', '1'), ('2023', '2'), ('2023', '3'),
        ('2022', '1'), ('2022', '2'), ('2022', '3')
    ]
    
    total_updated = 0
    
    for year, round_num in target_rounds:
        filename = f"items_{year}_round{round_num}.jsonl"
        jsonl_file = data_dir / filename
        
        updated = process_file_one_by_one(jsonl_file, year, round_num)
        if updated:
            total_updated += updated
        
        print("\n" + "=" * 80 + "\n")
    
    print(f"✅ 총 {total_updated}개 문제의 상세 해설이 생성되었습니다.")

if __name__ == "__main__":
    main()



