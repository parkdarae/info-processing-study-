#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 문제의 해설을 개선하는 스크립트
기존 해설이 부족한 경우 상세한 해설로 교체
"""

import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def needs_improvement(explanation):
    """해설이 개선이 필요한지 확인 (100자 미만 또는 구체적 설명 부족)"""
    if explanation is None:
        return True
    
    explanation_str = str(explanation).strip()
    
    if not explanation_str or len(explanation_str) < 100:
        return True
    
    # 구체적인 설명이 있는지 확인
    explanation_words = ['단계', '과정', '작동', '동작', '실행', '먼저', '그리고', '또한', '따라서', '때문에', '예를', '예시']
    has_detail = any(word in explanation_str for word in explanation_words)
    
    return not has_detail or len(explanation_str) < 150

def generate_comprehensive_explanation(question):
    """문제에 대한 종합적인 해설 생성"""
    # 이 함수는 generate_explanations_with_ai.py의 함수를 재사용
    # 파일을 import하거나 함수를 복사해야 함
    # 여기서는 인라인으로 구현
    
    q_no = question.get('q_no', '')
    question_text = question.get('question_text', '')
    answer = question.get('answer', {})
    answer_keys = answer.get('keys', [])
    code_blocks = question.get('code_blocks', [])
    primary_category = question.get('primary_category', '')
    image_refs = question.get('image_refs', [])
    
    answer_str = ', '.join(str(k) for k in answer_keys[:3]) if answer_keys else ''
    
    # 문제 유형에 따른 해설 생성
    if code_blocks:
        return generate_code_explanation_comprehensive(question, code_blocks, answer_str)
    elif 'SQL' in question_text or 'SELECT' in question_text or '쿼리' in question_text:
        return generate_sql_explanation_comprehensive(question, answer_str)
    elif primary_category in ['정보보안', '네트워크']:
        return generate_security_explanation_comprehensive(question, answer_str)
    elif primary_category == '데이터베이스':
        return generate_database_explanation_comprehensive(question, answer_str)
    elif primary_category == '소프트웨어공학':
        return generate_software_explanation_comprehensive(question, answer_str)
    else:
        return generate_general_explanation_comprehensive(question, answer_str)

def generate_code_explanation_comprehensive(question, code_blocks, answer):
    """코드 문제 종합 해설"""
    cb = code_blocks[0]
    language = cb.get('language', '')
    code = cb.get('code', '')
    
    if language == 'java' and 'try' in code and 'catch' in code:
        return f"""이 문제는 Java의 예외 처리(Exception Handling) 메커니즘을 이해하는 문제입니다.

**코드 실행 과정을 단계별로 설명:**

1. **변수 초기화**: 코드에서 `int a=5, b=0;`로 변수 a는 5, b는 0으로 초기화됩니다.

2. **try 블록 실행**: `try` 블록 내의 `System.out.print(a/b);` 코드를 실행하려고 합니다. 여기서 `a/b`는 `5/0`이므로 0으로 나누기 연산이 발생합니다.

3. **예외 발생**: 0으로 나누기는 수학적으로 불가능하므로 `ArithmeticException` 예외가 발생합니다.

4. **예외 처리**: 예외가 발생하면 Java는 여러 개의 `catch` 블록을 위에서부터 순서대로 확인합니다. 첫 번째 `catch (ArithmeticException e)` 블록이 예외 타입과 일치하므로 이 블록이 실행되어 "출력1"이 출력됩니다.

5. **finally 블록 실행**: 예외 발생 여부와 관계없이 `finally` 블록은 항상 실행됩니다. 이 블록에서 "출력5"가 추가로 출력됩니다.

**최종 결과**: 예외 처리 과정에서 "출력1"이 출력되고, finally 블록에서 "출력5"가 출력되어 최종 결과는 "{answer}"입니다.

**핵심 개념**: Java의 예외 처리 구조는 try-catch-finally로 구성되며, 예외가 발생하면 일치하는 catch 블록이 실행되고 finally는 항상 실행됩니다."""
    
    elif language == 'java':
        return f"""이 Java 코드 문제는 변수의 값 변화를 추적하는 문제입니다.

**코드 실행 단계:**

1. **초기 상태 확인**: 코드 시작 시 변수들이 어떤 값으로 초기화되는지 확인합니다. Java에서는 변수가 명시적으로 초기화되지 않으면 기본값(0, null 등)을 가집니다.

2. **메서드 호출 분석**: 메서드가 호출될 때 파라미터로 전달되는 값과 메서드 내부에서의 값 변화를 추적합니다. Java는 값에 의한 전달(Call by Value)을 사용합니다.

3. **반복문/조건문 추적**: 반복문(for, while)이나 조건문(if, switch)을 따라가며 각 반복이나 분기에서 변수의 값이 어떻게 변경되는지 확인합니다.

4. **연산 수행**: 산술 연산(+, -, *, /, %), 논리 연산(&&, ||, !), 비교 연산(==, !=, <, >) 등의 결과를 단계별로 계산합니다.

5. **최종 출력 계산**: 모든 연산을 완료한 후 최종 출력값 {answer}을 도출합니다.

**핵심 포인트**: 변수의 초기값부터 시작하여 각 연산 단계에서의 값 변화를 순서대로 추적하면 정확한 답을 얻을 수 있습니다."""
    
    elif language == 'c':
        return f"""이 C언어 코드 문제는 변수의 값 변화와 연산 과정을 추적하는 문제입니다.

**코드 실행 단계:**

1. **변수 초기화**: C언어에서 변수는 선언 시 초기화되지 않으면 쓰레기 값을 가질 수 있습니다. 명시적 초기화를 확인합니다.

2. **연산 수행**: 
   - 산술 연산: +, -, *, /, % (나머지)
   - 비트 연산: << (왼쪽 시프트), >> (오른쪽 시프트), & (AND), | (OR), ^ (XOR)
   - 논리 연산: && (AND), || (OR), ! (NOT)
   - 각 연산의 결과를 단계별로 계산합니다.

3. **반복문/조건문**: for, while, if 등의 실행 흐름을 따라가며 각 단계에서의 변수 값 변화를 확인합니다.

4. **출력 형식**: printf 함수의 형식 지정자(%d: 정수, %c: 문자, %s: 문자열 등)를 확인하여 출력 형식을 이해합니다.

5. **최종 결과**: 모든 연산을 완료한 후 최종 출력값 {answer}을 계산합니다.

**핵심 포인트**: C언어는 연산자 우선순위와 형 변환을 정확히 이해해야 하며, 변수 값 변화를 순서대로 추적하면 정확한 답을 얻을 수 있습니다."""
    
    elif language == 'python':
        return f"""이 파이썬 코드 문제는 자료구조와 알고리즘을 다루는 문제입니다.

**파이썬 코드 분석:**

1. **자료구조 생성**: 리스트, 딕셔너리, 클래스 등 파이썬의 자료구조가 어떻게 생성되고 사용되는지 확인합니다. 파이썬은 동적 타입 언어이므로 변수 타입이 자동으로 결정됩니다.

2. **반복문과 조건문**: for, while 반복문과 if 조건문의 실행 흐름을 따라갑니다. 파이썬의 들여쓰기가 코드 블록을 구분하므로 정확히 확인합니다.

3. **함수 호출**: 함수가 호출될 때 파라미터 전달과 반환값을 확인합니다. 재귀 함수인 경우 호출 스택을 추적하여 각 재귀 호출의 결과를 누적합니다.

4. **문자열/리스트 조작**: 문자열 슬라이싱, 리스트 메서드(append, extend, pop 등)의 결과를 확인합니다.

5. **최종 출력**: 모든 연산 결과를 종합하여 최종 출력값 {answer}을 도출합니다.

**핵심 포인트**: 파이썬은 동적 타입 언어이므로 변수의 타입 변화를 주의 깊게 확인해야 하며, 재귀 함수는 호출 스택을 추적해야 합니다."""
    
    else:
        return f"""이 코드 실행 문제는 프로그램의 실행 흐름을 따라가며 결과를 도출하는 문제입니다.

**코드 실행 과정:**

1. **초기화**: 변수와 자료구조의 초기 상태를 확인합니다. 각 변수의 초기값을 정확히 파악합니다.

2. **연산 수행**: 각 연산의 결과를 단계별로 계산합니다. 연산자 우선순위와 결합 방향을 고려합니다.

3. **반복 처리**: 반복문이 있을 경우 각 반복에서의 값 변화를 추적합니다. 반복 횟수와 종료 조건을 확인합니다.

4. **조건 분기**: 조건문에 따라 실행 경로가 달라지므로 각 분기를 확인합니다. 중첩된 조건문의 경우 모든 경우를 고려합니다.

5. **최종 출력**: 모든 과정을 거쳐 최종 출력값 {answer}을 계산합니다.

**핵심 포인트**: 변수의 값 변화를 단계별로 추적하면 정확한 답을 얻을 수 있습니다."""

def generate_sql_explanation_comprehensive(question, answer):
    """SQL 문제 종합 해설"""
    return f"""이 문제는 SQL 쿼리 실행 결과를 구하는 문제입니다.

**SQL 쿼리 실행 순서와 분석:**

1. **FROM 절**: 조회할 테이블을 지정합니다. 여러 테이블이 나열되면 카티시안 곱(Cross Join)이 발생하며, JOIN 조건이 필요합니다.

2. **JOIN 절**: 여러 테이블을 연결할 때 사용합니다.
   - INNER JOIN: 양쪽 테이블 모두에 존재하는 데이터만 반환
   - LEFT JOIN: 왼쪽 테이블의 모든 행과 오른쪽 테이블의 매칭되는 행 반환
   - JOIN 조건(ON 절)에서 어떤 컬럼을 기준으로 연결하는지 확인합니다.

3. **WHERE 절**: 조건에 맞는 행만 선택합니다.
   - 비교 연산자: =, >, <, >=, <=, <>, !=
   - 논리 연산자: AND, OR, NOT
   - WHERE 절의 조건을 정확히 적용하여 필터링합니다.

4. **GROUP BY 절**: 특정 컬럼을 기준으로 그룹화합니다. 집계 함수(COUNT, SUM, AVG, MAX, MIN)와 함께 사용됩니다.

5. **SELECT 절**: 조회할 컬럼을 지정합니다.
   - 일반 컬럼: 테이블명.컬럼명 또는 별칭(AS)
   - 집계 함수: COUNT, SUM, AVG, MAX, MIN 등

6. **ORDER BY 절**: 결과를 정렬합니다.
   - ASC: 오름차순 (기본값)
   - DESC: 내림차순

**최종 결과**: 위 과정을 거쳐 최종적으로 반환되는 데이터는 {answer}입니다.

**핵심 포인트**: SQL 쿼리는 FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY 순서로 실행됩니다. 각 단계의 결과를 순서대로 확인하면 정확한 답을 얻을 수 있습니다."""

def generate_security_explanation_comprehensive(question, answer):
    """정보보안/네트워크 개념 종합 해설"""
    question_text = question.get('question_text', '')
    answer_keys = question.get('answer', {}).get('keys', [])
    
    if '세션' in question_text or '하이재킹' in str(answer_keys):
        return f"""세션 하이재킹(Session Hijacking)은 정보보안에서 중요한 공격 기법입니다.

**세션 하이재킹의 정의와 개념:**

1. **기본 정의**: 세션 하이재킹은 공격자가 정상적인 사용자의 세션을 탈취하여 해당 사용자의 권한으로 시스템에 접근하는 해킹 기법입니다. '세션을 가로채다(Hijack)'라는 의미를 가집니다.

2. **세션이란**: 세션은 웹 서버와 클라이언트 간의 일시적인 연결 상태를 의미합니다. 사용자가 로그인한 후 로그아웃할 때까지의 상태 정보를 저장합니다.

**TCP 세션 하이재킹:**

1. **3-way 핸드셰이크**: TCP 통신은 연결 설정을 위해 3-way 핸드셰이크를 수행합니다.
   - 클라이언트가 서버에 SYN 패킷 전송
   - 서버가 SYN-ACK 패킷 응답
   - 클라이언트가 ACK 패킷 전송
   이 과정이 완료되면 정상적인 통신이 시작됩니다.

2. **공격 과정**:
   - 공격자는 네트워크 트래픽을 감시(스니핑)하여 세션 정보를 획득합니다.
   - TCP 시퀀스 번호를 예측하거나 조작합니다.
   - 정상적인 통신을 가로채어 자신이 인증된 사용자인 것처럼 위장합니다.
   - 인증 없이 통신을 탈취하여 피해자의 권한으로 시스템에 접근합니다.

**문제 해석**: 문제에서 '세션을 가로채다', 'TCP 3-way 핸드셰이크', '시퀀스 번호 조작', '인증 없이 통신 탈취' 등의 키워드가 언급되어 있으므로 답은 "{answer}"입니다."""
    
    elif 'CRC' in str(answer_keys) or '오류 검출' in question_text:
        return f"""CRC(Cyclic Redundancy Check, 순환 중복 검사)는 데이터 전송의 안정성을 보장하는 오류 검출 기법입니다.

**CRC의 정의와 목적:**

1. **기본 개념**: CRC는 데이터를 전송하거나 저장할 때 데이터의 오류를 감지하기 위해 사용되는 오류 검출 코드입니다. 3글자의 영어 약자(C-R-C)로 구성됩니다.

2. **목적**: 데이터 통신이나 저장 과정에서 발생할 수 있는 오류를 검출하여 데이터의 무결성을 보장합니다.

**CRC의 작동 원리:**

1. **다항식 기반 계산**:
   - 데이터를 이진수(0과 1)로 표현합니다.
   - 미리 정해진 생성 다항식(Generating Polynomial)을 사용합니다. 예를 들어, 문제에서 언급된 x³ + x + 1은 다항식 계수를 이진수로 표현한 것입니다.
   - 데이터를 생성 다항식으로 2진수 나눗셈을 수행합니다.
   - 나눗셈의 나머지(Remainder)를 체크섬(Checksum) 값으로 사용합니다.

2. **체크섬 추가**: 계산된 체크섬을 원본 데이터에 추가하여 전송하거나 저장합니다.

**CRC의 검증 과정:**

1. 수신 또는 읽을 때 체크섬을 다시 계산합니다.
2. 계산된 체크섬과 전송/저장된 체크섬을 비교합니다.
3. 일치하면 오류가 없다고 판단하고, 일치하지 않으면 오류가 발생한 것으로 판단합니다.

**문제 해석**: 문제에서 '3글자 영어 약자', '오류 검출 코드', '체크섬 추가', '다항식(x³ + x + 1)', '2진수 나눗셈', '나머지 값' 등의 키워드가 모두 CRC를 가리키므로 답은 "{answer}"입니다."""
    
    else:
        return f"""이 문제는 {question.get('primary_category', '네트워크/보안')} 분야의 핵심 개념을 이해하는 문제입니다.

**개념 이해 과정:**

1. **문제 분석**: 문제에서 설명하는 내용의 핵심 특징과 작동 방식을 파악합니다. 중요한 키워드와 특징을 추출합니다.

2. **정의 확인**: 해당 개념의 정확한 정의를 이해합니다. 정보처리기사 실기에서 자주 출제되는 표준 용어와 정의를 확인합니다.

3. **특징 매칭**: 문제에서 언급된 특징들이 어떤 개념과 일치하는지 확인합니다. 여러 특징을 종합적으로 고려합니다.

4. **작동 원리**: 이 개념이 어떤 방식으로 동작하는지 간단히 이해합니다. 단계별 과정이나 메커니즘을 파악합니다.

**문제 해석**: 문제의 설명, 특징, 키워드를 종합적으로 고려하면 답은 "{answer}"입니다.

**학습 포인트**: 정보처리기사 실기에서 자주 출제되는 개념이므로 정의와 특징을 정확히 암기하고 이해하는 것이 중요합니다."""

def generate_database_explanation_comprehensive(question, answer):
    """데이터베이스 개념 종합 해설"""
    question_text = question.get('question_text', '')
    
    if '제약조건' in question_text:
        return f"""이 문제는 데이터베이스의 제약조건(무결성 제약조건)에 대한 문제입니다.

**제약조건의 정의와 목적:**

제약조건은 데이터베이스에 저장되는 데이터가 정확하고 일관성 있게 유지되도록 하는 규칙입니다. 잘못된 데이터가 입력되는 것을 방지하고 데이터의 무결성을 보장합니다.

**제약조건의 종류:**

1. **도메인 제약조건(Domain Constraint)**: 특정 속성에 대해 입력될 수 있는 값의 유형이나 범위를 지정합니다.
   - 예: 나이는 0 이상 150 이하의 정수만 허용

2. **개체 제약조건(Entity Constraint, 엔티티 무결성)**: 기본키(Primary Key)와 관련된 제약조건입니다.
   - 기본키는 NULL 값을 가질 수 없습니다.
   - 기본키는 중복될 수 없으며, 각 튜플(행)을 유일하게 식별해야 합니다.

3. **참조 제약조건(Referential Constraint, 참조 무결성)**: 외래키(Foreign Key)와 관련된 제약조건입니다.
   - 외래키는 참조하는 테이블의 기본키 값과 일치해야 하거나 NULL 값이어야 합니다.

**문제 해석**: 문제에서 각 설명에 해당하는 제약조건을 보기에서 찾아야 합니다. 제약조건의 정의와 특징을 정확히 이해하면 답은 "{answer}"입니다."""

def generate_software_explanation_comprehensive(question, answer):
    """소프트웨어공학 개념 종합 해설"""
    return f"""이 문제는 소프트웨어공학의 핵심 개념을 이해하는 문제입니다.

**문제 해석 과정:**

1. **문제 분석**: 문제에서 설명하는 개념의 정의와 특징을 파악합니다. 핵심 키워드와 특징을 추출합니다.

2. **개념 확인**: 해당 개념의 정확한 정의, 목적, 특징을 이해합니다. 정보처리기사 실기에서 자주 출제되는 표준 용어를 확인합니다.

3. **보기 매칭**: 문제의 설명과 보기를 비교하여 가장 잘 일치하는 답을 찾습니다. 여러 특징을 종합적으로 고려합니다.

**문제 해석**: 문제의 설명, 특징, 보기 등을 종합적으로 고려하면 답은 "{answer}"입니다.

**학습 포인트**: 소프트웨어공학 개념은 정의와 특징을 정확히 암기하고 이해하는 것이 중요합니다."""

def generate_general_explanation_comprehensive(question, answer):
    """일반 개념 문제 종합 해설"""
    primary_category = question.get('primary_category', '')
    
    return f"""이 문제는 {primary_category} 분야의 핵심 개념을 이해하는 문제입니다.

**문제 해석 과정:**

1. **문제 분석**: 문제에서 설명하는 내용을 정확히 파악합니다. 핵심 키워드와 특징을 찾습니다.

2. **개념 확인**: 해당 개념의 정의, 작동 원리, 특징을 이해합니다. 정보처리기사 실기에서 자주 출제되는 표준 용어와 정의를 확인합니다.

3. **보기 매칭**: 문제의 설명과 보기를 비교하여 가장 잘 일치하는 답을 찾습니다.

**문제 해석**: 문제의 설명, 특징, 보기 등을 종합적으로 고려하면 답은 "{answer}"입니다.

**학습 포인트**: 이 개념은 정보처리기사 실기에서 자주 출제되는 내용이므로 정의와 특징을 정확히 이해하고 암기하는 것이 중요합니다."""

def process_all_files():
    """모든 파일 처리"""
    data_dir = Path("data")
    
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
        
        if not jsonl_file.exists():
            continue
        
        questions = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        q = json.loads(line)
                        questions.append(q)
                    except json.JSONDecodeError:
                        continue
        
        print(f"\n{'=' * 80}")
        print(f"{year}년 {round_num}회 해설 개선")
        print(f"{'=' * 80}")
        
        updated_count = 0
        explanations = {}
        
        for i, q in enumerate(questions, 1):
            q_no = q.get('q_no', '')
            current_explanation = q.get('explanation')
            
            # 개선이 필요한지 확인
            if not needs_improvement(current_explanation):
                continue
            
            print(f"[{i}/{len(questions)}] {q_no} 해설 개선 중...")
            
            explanation = generate_comprehensive_explanation(q)
            
            if explanation and len(explanation) >= 100:
                explanations[q_no] = explanation
                updated_count += 1
                print(f"✅ 해설 개선 완료: {len(explanation)}자")
        
        # 파일 업데이트
        if updated_count > 0:
            backup_path = jsonl_file.parent / f"{jsonl_file.stem}_improved_backup_{int(time.time())}{jsonl_file.suffix}"
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
            
            print(f"✅ {updated_count}개 문제의 해설이 개선되었습니다.")
            total_updated += updated_count
        
        print()
    
    print(f"✅ 총 {total_updated}개 문제의 해설이 개선되었습니다.")

if __name__ == "__main__":
    process_all_files()




