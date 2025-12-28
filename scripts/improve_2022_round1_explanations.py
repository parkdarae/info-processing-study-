#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2022년 1회 모든 범용적 해설 개선 스크립트 (가독성 향상 포함)
"""

import json
import sys
from pathlib import Path
import shutil
from datetime import datetime

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

def backup_file(file_path):
    """파일 백업"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{file_path}_backup_{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"[백업] {backup_path}")

def improve_q001(item):
    """Q001 (RAID 0) 문제의 해설을 개선"""
    return """이 문제는 **RAID 0 (스트라이핑)**에 대한 문제입니다.

**RAID 0 (스트라이핑)의 특징:**

1. **Striping (스트라이핑) 구현:**
   - 데이터를 여러 디스크에 분산 저장하는 방식
   - 데이터를 블록 단위로 분할하여 각 디스크에 저장

2. **성능 향상:**
   - I/O 로드 분산으로 읽기/쓰기 속도가 매우 빠름
   - 여러 디스크에 동시에 접근하므로 병렬 처리 가능

3. **데이터 저장 방식:**
   - 데이터를 블록으로 분할
   - 각 블록은 다른 디스크로 분산 저장

**문제에서 설명하는 특징:**
- "스트라이핑 구현 방식" → RAID 0
- "I/O 로드의 분산으로 매우 빠른 속도" → RAID 0
- "데이터를 블럭으로 분할 저장하며, 각 블럭은 다른 디스크로 나뉘어 저장" → RAID 0

**답:** **RAID 0**

**참고:** RAID 0은 패리티(검증 데이터)나 미러링 없이 순수하게 성능 향상만을 위한 방식입니다. 디스크 하나가 고장 나면 모든 데이터를 잃게 되므로 안정성은 낮습니다."""

def improve_q006(item):
    """Q006 (파이썬 기본값 매개변수) 문제의 해설을 개선"""
    return """이 파이썬 코드는 **함수의 기본값 매개변수(Default Parameter)**를 이해하는 문제입니다.

**코드 분석:**

```python
def exam(num1, num2=2):
    print('a=', num1, 'b=', num2)

exam(20)
```

**실행 과정:**

1. **함수 정의:**
   - `exam(num1, num2=2)`: `num1`은 필수 매개변수, `num2`는 기본값이 2로 설정된 선택적 매개변수입니다.

2. **함수 호출:**
   - `exam(20)`: 첫 번째 인자 20만 전달
   - `num1 = 20` (전달된 값)
   - `num2 = 2` (기본값 사용, 인자 미전달)

3. **출력:**
   - `print('a=', 20, 'b=', 2)`
   - **출력: "a= 20 b= 2"**

**핵심 포인트:**
- 기본값이 설정된 매개변수는 함수 호출 시 인자를 생략하면 기본값이 사용됩니다.
- 여기서는 `num2`에 값을 전달하지 않았으므로 기본값 2가 사용되었습니다.

**답:** **a= 20 b= 2**"""

def improve_q007(item):
    """Q007 (리스트 메서드) 문제의 해설을 개선"""
    return """이 문제는 파이썬 **리스트 메서드**의 기능을 이해하는 문제입니다.

**각 메서드의 기능:**

1. **`extend(iterable)`:**
   - 요소를 확장해준다는 의미
   - 반복 가능한 객체(리스트, 튜플 등)의 모든 항목을 하나씩 추가
   - 예: `[1, 2].extend([3, 4])` → `[1, 2, 3, 4]`
   - `append()`와 차이: `append([3, 4])`는 `[1, 2, [3, 4]]`가 됨

2. **`pop([index])`:**
   - 리스트 내부 요소를 꺼내주는 함수
   - 해당 요소는 리스트에서 삭제하고 그 값을 반환
   - 인덱스를 지정하지 않으면 마지막 요소를 반환
   - 예: `[1, 2, 3].pop()` → `3` 반환, 리스트는 `[1, 2]`가 됨

3. **`reverse()`:**
   - 리스트 내부 요소의 순서를 뒤집는 역할
   - 원본 리스트를 직접 수정 (반환값 없음)
   - 예: `[1, 2, 3].reverse()` → 리스트가 `[3, 2, 1]`로 변경

**답:**
- (1) **extend**
- (2) **pop**
- (3) **reverse**"""

def improve_q010(item):
    """Q010 (정적 분석 vs 동적 분석) 문제의 해설을 개선"""
    return """이 문제는 소프트웨어 **코드 분석 도구**의 종류를 묻는 문제입니다.

**정적 분석 (Static Analysis):**

1. **특징:**
   - 소스 코드의 실행 없이 코드의 의미를 분석
   - 코드 자체를 읽어서 결함을 찾아내는 원시적 코드 분석 기법
   - 컴파일 타임에 수행

2. **장점:**
   - 실행 환경이 필요 없음
   - 빠른 분석 가능
   - 모든 코드 경로 분석 가능

3. **예시 도구:**
   - SonarQube, ESLint, Pylint 등

**동적 분석 (Dynamic Analysis):**

1. **특징:**
   - 소스 코드를 실행하여 프로그램 동작이나 반응을 추적
   - 실행 중에 코드에 존재하는 메모리 누수, 스레드 결함 등을 분석
   - 런타임에 수행

2. **장점:**
   - 실제 실행 환경에서 문제 발견 가능
   - 성능 문제, 메모리 누수 등 실제 동작 문제 발견

3. **예시 도구:**
   - Valgrind, JProfiler, Chrome DevTools 등

**답:**
- (1) **static**
- (2) **dynamic**"""

def improve_q012(item):
    """Q012 (JUnit) 문제의 해설을 개선"""
    return """이 문제는 Java 테스트 프레임워크인 **JUnit**에 대한 문제입니다.

**JUnit이란?**
- Java 프로그래밍 언어를 이용한 xUnit 테스트 기법
- 숨겨진 단위 테스트를 끌어내어 정형화시켜 단위 테스트를 쉽게 해주는 테스트용 Framework

**JUnit의 특징:**
1. **단위 테스트 자동화:**
   - 각 메서드나 클래스의 기능을 개별적으로 테스트
   - 테스트 케이스를 자동으로 실행하고 결과를 확인

2. **정형화된 테스트:**
   - `@Test` 어노테이션으로 테스트 메서드 표시
   - `assertEquals()`, `assertTrue()` 등으로 검증

3. **xUnit 패턴:**
   - 여러 언어로 포팅된 테스트 프레임워크 패턴
   - Java용은 JUnit, Python용은 PyUnit, C#용은 NUnit 등

**예시:**
```java
@Test
public void testAddition() {
    assertEquals(5, calculator.add(2, 3));
}
```

**답:** **JUnit**"""

def improve_q013(item):
    """Q013 (블랙박스 테스트 기법) 문제의 해설을 개선"""
    return """이 문제는 **블랙박스 테스트 기법**을 선택하는 문제입니다.

**블랙박스 테스트란?**
- 소프트웨어의 내부 구조를 알지 못한 상태에서 입력과 출력만을 확인하는 테스트
- 시스템의 기능이 요구사항에 맞게 동작하는지 검증

**블랙박스 테스트 기법 종류:**

1. **동치 분할 (Equivalence Partitioning):**
   - 입력 데이터를 유사한 도메인별로 그룹핑하여 대표값으로 테스트
   - 예: 0~100 범위면 0, 50, 100 등으로 테스트

2. **경계값 분석 (Boundary Value Analysis):**
   - 입력 조건의 경계값을 테스트 케이스로 선정
   - 예: 0 <= x <= 10이면 -1, 0, 10, 11을 테스트

3. **원인-효과 그래프 (Cause-Effect Graphing):**
   - 입력 조건과 출력 결과 간의 인과관계를 그래프로 표현하여 테스트 케이스 생성

4. **오류 예측 (Error Guessing):**
   - 과거 경험이나 직관으로 오류를 예측하여 테스트

5. **비교 검사 (Comparison Testing):**
   - 여러 버전의 프로그램에 동일한 입력을 제공하여 결과 비교

**문제에서 요구하는 기법:**
- 보기에서 블랙박스 테스트 기법 3가지를 선택해야 합니다.

**답:** **ㄷ, ㄹ, ㅂ** (보기에 나열된 블랙박스 테스트 기법 3개)"""

def improve_q014(item):
    """Q014 (팩토리얼 재귀 함수) 문제의 해설을 개선"""
    return """이 C언어 코드는 **팩토리얼(Factorial)**을 계산하는 재귀 함수 문제입니다.

**팩토리얼이란?**
- n! = n × (n-1) × (n-2) × ... × 2 × 1
- 예: 5! = 5 × 4 × 3 × 2 × 1 = 120

**코드 실행 단계:**

```c
int func(int a) {
    if (a <= 1) return 1;        // 기저 조건
    return a * func(a - 1);      // 재귀 호출
}
```

**입력값이 5일 때:**

1. **`func(5)` 호출:**
   - 5 <= 1? 아니오 → `return 5 * func(4)`

2. **`func(4)` 호출:**
   - 4 <= 1? 아니오 → `return 4 * func(3)`

3. **`func(3)` 호출:**
   - 3 <= 1? 아니오 → `return 3 * func(2)`

4. **`func(2)` 호출:**
   - 2 <= 1? 아니오 → `return 2 * func(1)`

5. **`func(1)` 호출:**
   - 1 <= 1? 예 → `return 1` (기저 조건)

6. **값 반환 과정:**
   - `func(1)` = 1
   - `func(2)` = 2 × 1 = 2
   - `func(3)` = 3 × 2 = 6
   - `func(4)` = 4 × 6 = 24
   - `func(5)` = 5 × 24 = **120**

**최종 출력:** **120**

**핵심 포인트:**
- 재귀 함수는 자기 자신을 호출하여 문제를 해결합니다.
- 기저 조건(`a <= 1`)에서 재귀가 종료됩니다."""

def improve_q015(item):
    """Q015 (정수 역순 출력) 문제의 해설을 개선"""
    return """이 C언어 코드는 **정수를 역순으로 출력**하는 문제입니다.

**코드 분석:**

```c
int number = 1234;
int div = 10;
int result = 0;
while (number (1) 0) {
    result = result * div;
    result = result + number (2) div;
    number = number (3) div;
}
```

**목표:**
- 입력: 1234
- 출력: 4321

**빈칸 분석:**

1. **`while (number (1) 0)`:**
   - 반복 조건: `number`가 0보다 큰 동안 반복
   - `(1)` = **>** (크다)

2. **`number (2) div`:**
   - 마지막 자릿수를 구하기 위해 나머지 연산 필요
   - `number % div` = 일의 자리 숫자
   - `(2)` = **%** (나머지)

3. **`number = number (3) div`:**
   - 마지막 자릿수를 제거하기 위해 나누기 연산 필요
   - `number / div` = 마지막 자릿수 제거
   - `(3)` = **/** (나누기)

**실행 과정 (number = 1234):**

| 반복 | number | result | 설명 |
|------|--------|--------|------|
| 초기 | 1234 | 0 | - |
| 1 | 123 | 4 | result = 0*10 + 1234%10 = 4, number = 1234/10 = 123 |
| 2 | 12 | 43 | result = 4*10 + 123%10 = 43, number = 123/10 = 12 |
| 3 | 1 | 432 | result = 43*10 + 12%10 = 432, number = 12/10 = 1 |
| 4 | 0 | 4321 | result = 432*10 + 1%10 = 4321, number = 1/10 = 0 |

**최종 출력:** **4321**

**답:**
- (1) **>**
- (2) **%**
- (3) **/**"""

def improve_q016(item):
    """Q016 (ISMS) 문제의 해설을 개선"""
    return """이 문제는 정보보안 관리체계인 **ISMS**에 대한 문제입니다.

**ISMS란?**
- **Information Security Management System**의 약자
- 정보보안 관리체계

**ISMS의 목적:**
- 조직의 정보자산을 보호하기 위한 체계적인 관리 시스템
- 정보보안 위험을 관리하고 통제

**ISMS 인증:**
- 한국인터넷진흥원(KISA)에서 시행하는 정보보안 관리체계 인증
- ISO/IEC 27001 국제표준 기반

**답:** **ISMS (Information Security Management System)**"""

def improve_q018(item):
    """Q018 (워터링홀 공격) 문제의 해설을 개선"""
    return """이 문제는 **워터링홀(Watering Hole) 공격**에 대한 문제입니다.

**워터링홀 공격이란?**
- APT(Advanced Persistent Threat) 공격에서 주로 사용되는 공격 기법
- 공격 대상이 방문할 가능성이 있는 합법적인 웹 사이트를 미리 감염시킴
- 잠복하고 있다가 공격 대상이 방문하면 대상의 컴퓨터에 악성코드를 설치

**워터링홀 공격의 특징:**

1. **타겟팅:**
   - 특정 그룹이나 조직이 자주 방문하는 합법적인 웹사이트를 선택

2. **감염:**
   - 선택한 웹사이트를 악성코드로 감염시킴

3. **잠복:**
   - 공격 대상이 방문할 때까지 대기

4. **자동 설치:**
   - 방문 시 드라이브바이 다운로드(Drive-by Download)로 악성코드 자동 설치

**다른 공격과의 차이:**
- 피싱: 이메일 등으로 직접 공격
- 워터링홀: 합법적 사이트를 경유하여 간접 공격

**답:** **watering hole (워터링홀)**"""

def improve_q019(item):
    """Q019 (테스트 단계) 문제의 해설을 개선"""
    return """이 문제는 소프트웨어 **테스트 단계(V-모델)**에 대한 문제입니다.

**V-모델 테스트 단계:**

1. **단위 테스트 (Unit Test):**
   - 개별 모듈, 서브루틴이 정상적으로 실행되는지 확인
   - 가장 작은 단위의 컴포넌트 테스트
   - 예: 함수, 클래스 메서드 등

2. **통합 테스트 (Integration Test):**
   - 인터페이스 간 시스템이 정상적으로 실행되는지 확인
   - 여러 모듈을 결합하여 테스트
   - 예: API 연결, 데이터베이스 연동 등

3. **시스템 테스트 (System Test):**
   - 구현된 시스템이 정해진 요건에 적합한지 여부를 평가
   - 실제 운용과 같은 환경에서 시스템 전체 테스트
   - 예: 성능 테스트, 보안 테스트 등

4. **인수 테스트 (Acceptance Test):**
   - 계약상의 요구 사항이 만족되었는지 확인
   - 구입자(고객)에 의해 실시되는 최종 테스트

**문제에서 요구하는 답:**
- (1) 단위 테스트
- (2) 통합 테스트
- (3) 시스템 테스트

**답:**
- (1) **단위 테스트**
- (2) **통합 테스트**
- (3) **시스템 테스트**"""

def improve_q020(item):
    """Q020 (V-모델 테스트 단계) 문제의 해설을 개선"""
    return """이 문제는 **V-모델**에서의 테스트 단계에 대한 문제입니다.

**V-모델이란?**
- 소프트웨어 개발 생명주기 모델 중 하나
- 개발 단계와 테스트 단계가 대칭적으로 구성됨
- V자 형태로 표현됨

**V-모델 테스트 단계 (하향식):**

1. **단위 테스트 (Unit Test):**
   - 개별 모듈을 독립적으로 테스트
   - 개발자가 직접 수행
   - 화이트박스 테스트 기법 사용

2. **통합 테스트 (Integration Test):**
   - 여러 모듈을 결합하여 테스트
   - 모듈 간 인터페이스 검증
   - 점진적 통합 방식 사용

3. **시스템 테스트 (System Test):**
   - 완성된 시스템 전체를 테스트
   - 요구사항 명세서 기준 검증
   - 실제 운영 환경과 유사한 환경에서 수행

4. **인수 테스트 (Acceptance Test):**
   - 최종 사용자가 시스템을 승인하기 위한 테스트
   - 비즈니스 요구사항 만족 여부 확인

**답:**
- (1) **단위 테스트**
- (2) **통합 테스트**
- (3) **시스템 테스트**"""

# 개선 함수 매핑
IMPROVEMENTS = {
    'Q001': improve_q001,
    'Q006': improve_q006,
    'Q007': improve_q007,
    'Q010': improve_q010,
    'Q012': improve_q012,
    'Q013': improve_q013,
    'Q014': improve_q014,
    'Q015': improve_q015,
    'Q016': improve_q016,
    'Q018': improve_q018,
    'Q019': improve_q019,
    'Q020': improve_q020,
}

def main():
    jsonl_path = 'data/items_2022_round1.jsonl'
    
    # 백업
    backup_file(jsonl_path)
    
    # 파일 로드
    items = load_jsonl(jsonl_path)
    
    updated_count = 0
    
    for item in items:
        q_no = item.get('q_no', '')
        if q_no in IMPROVEMENTS:
            new_explanation = IMPROVEMENTS[q_no](item)
            item['explanation'] = new_explanation
            updated_count += 1
            print(f"[개선] {q_no}")
    
    # 저장
    save_jsonl(jsonl_path, items)
    
    print(f"\n총 {updated_count}개 문제의 해설이 개선되었습니다.")

if __name__ == '__main__':
    main()




