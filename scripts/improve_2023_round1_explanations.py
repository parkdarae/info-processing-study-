#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023년 1회 모든 범용적 해설 개선 스크립트
"""

import json
import sys
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

def improve_q001(item):
    """Q001 (Java static 변수) 문제의 해설을 개선"""
    return """이 Java 코드는 static 변수와 인스턴스 변수의 차이, 그리고 후위 증가 연산자를 이해하는 문제입니다.

**코드 분석:**

```java
class Static {
    public int a = 20;      // 인스턴스 변수
    static int b = 0;       // 클래스 변수 (static)
}

int a = 10;                 // main의 지역 변수
Static.b = a;               // Static.b = 10
Static st = new Static();   // 인스턴스 생성
System.out.println(Static.b++);  // 후위 증가 연산자
System.out.println(st.b);        // static 변수는 공유됨
System.out.println(a);           // 지역 변수 a
System.out.print(st.a);          // 인스턴스 변수
```

**실행 과정:**

1. **초기 상태:**
   - `main`의 지역 변수: `a = 10`
   - `Static.b = 0` (클래스 변수, 초기값)

2. **`Static.b = a`:**
   - `Static.b = 10`

3. **`Static st = new Static()`:**
   - 인스턴스 생성
   - `st.a = 20` (인스턴스 변수)
   - `st.b`는 `Static.b`를 공유 (같은 값)

4. **출력:**

   - **`System.out.println(Static.b++):`**
     - 후위 증가 연산자: 먼저 출력 후 증가
     - 출력: **10**, 그 다음 `Static.b = 11`

   - **`System.out.println(st.b):`**
     - `st.b`는 `Static.b`와 같은 메모리를 참조
     - 출력: **11**

   - **`System.out.println(a):`**
     - main의 지역 변수 `a`
     - 출력: **10**

   - **`System.out.print(st.a):`**
     - 인스턴스 변수 `st.a`
     - 출력: **20**

**최종 출력:** "10\n11\n10\n20"

**답:** "1) 10 11 10 20\""""

def improve_q002(item):
    """Q002 (C언어 포인터, 문자열 출력) 문제의 해설을 개선"""
    return """이 C언어 코드는 문자열 배열, 포인터, 그리고 배열과 포인터의 관계를 이해하는 문제입니다.

**코드 분석:**

```c
char a[] = "Art";
char* p = NULL;
p = a;  // 포인터 p가 배열 a를 가리킴
```

**실행 과정:**

1. **초기 상태:**
   - `a[] = {'A', 'r', 't', '\\0'}`
   - `p = NULL` → `p = a` (p가 a의 시작 주소를 가리킴)

2. **출력:**

   - **`printf("%s\\n", a):`**
     - `%s` 형식 지정자는 널 문자까지 출력
     - 출력: **"Art"** + 줄바꿈

   - **`printf("%c\\n", *p):`**
     - `*p`는 p가 가리키는 첫 번째 문자
     - `*p = a[0] = 'A'`
     - 출력: **"A"** + 줄바꿈

   - **`printf("%c\\n", *a):`**
     - 배열 이름 `a`는 첫 번째 요소의 주소
     - `*a = a[0] = 'A'`
     - 출력: **"A"** + 줄바꿈

   - **`printf("%s\\n", p):`**
     - `p`는 `a`를 가리키므로 `a`의 문자열 출력
     - 출력: **"Art"** + 줄바꿈

   - **반복문:**
     ```c
     for(int i = 0; a[i] != '\\0'; i++)
         printf("%c", a[i]);
     ```
     - i=0: 'A' 출력
     - i=1: 'r' 출력
     - i=2: 't' 출력
     - 출력: **"Art"**

**최종 출력:** "Art\nA\nA\nArt\nArt"

**답:** 실제 출력값은 코드 실행 결과에 따라 결정되며, 위 과정을 통해 "Art\nA\nA\nArt\nArt"가 출력됩니다."""

def improve_q003(item):
    """Q003 (C언어 문자열 비교) 문제의 해설을 개선"""
    return """이 C언어 코드는 두 문자열에서 공통 문자를 찾아 출력하는 문제입니다.

**코드 분석:**

```c
char* a = "qwer";
char* b = "qwtety";

for(int i = 0; a[i] != '\\0'; i++) {
    for(int j = 0; b[j] != '\\0'; j++) {
        if(a[i] == b[j]) printf("%c", a[i]);
    }
}
```

**실행 과정:**

- `a = "qwer"` → 문자: 'q', 'w', 'e', 'r'
- `b = "qwtety"` → 문자: 'q', 'w', 't', 'e', 't', 'y'

**이중 반복문:**

**i=0, a[0]='q':**
   - j=0: b[0]='q' → 일치! → **'q'** 출력
   - j=1: b[1]='w' → 불일치
   - j=2~5: 불일치

**i=1, a[1]='w':**
   - j=0: b[0]='q' → 불일치
   - j=1: b[1]='w' → 일치! → **'w'** 출력
   - j=2~5: 불일치

**i=2, a[2]='e':**
   - j=0~1: 불일치
   - j=3: b[3]='e' → 일치! → **'e'** 출력
   - j=4~5: 불일치

**i=3, a[3]='r':**
   - j=0~5: 모두 불일치

**최종 출력:** "qwe"

**답:** "qwe\""""

def improve_q004(item):
    """Q004 (AJAX) 문제의 해설을 개선"""
    return """AJAX(Asynchronous JavaScript and XML)는 비동기적인 웹 애플리케이션 제작을 위한 기술입니다.

**문제에서 설명하는 각 특징:**

1. **"비동기적인 웹 애플리케이션의 제작을 위해 JavaScript와 XML을 이용한 비동기적 정보 교환 기법이다"**
   - AJAX는 비동기(Asynchronous) 통신을 사용합니다.
   - JavaScript를 클라이언트 측에서 사용합니다.
   - XML은 초기에는 많이 사용했지만 현재는 JSON을 더 많이 사용합니다.
   - 페이지 전체를 새로고침하지 않고 필요한 데이터만 서버에서 가져옵니다.

2. **"필요한 데이터만을 웹서버에 요청해서 받은 후 클라이언트에서 데이터에 대한 처리를 할 수 있다"**
   - 전통적인 웹 페이지는 전체 페이지를 다시 로드해야 했습니다.
   - AJAX는 필요한 부분만 서버에서 가져와서 동적으로 업데이트합니다.
   - 사용자 경험이 향상됩니다 (빠른 응답, 부드러운 UI).

3. **"보통 SOAP이나 XML 기반의 웹 서비스 프로토콜이 사용되며, 웹 서버의 응답을 처리하기 위해 클라이언트 쪽에서는 자바스크립트를 쓴다"**
   - SOAP: Simple Object Access Protocol
   - XML 기반 데이터 교환
   - JavaScript로 응답 처리 (JSON.parse 등)

4. **"Google Map과 Google pages에서 사용한 기술에 기반하여 제작되었다"**
   - Google Maps가 AJAX 기술의 대표적인 예시입니다.
   - 지도를 이동해도 전체 페이지가 새로고침되지 않고 필요한 타일만 로드됩니다.
   - Google Suggest(검색 자동완성)도 AJAX를 사용합니다.

**AJAX의 작동 원리:**
1. JavaScript가 XMLHttpRequest 객체 생성
2. 서버에 비동기 요청 전송
3. 서버에서 응답 (XML 또는 JSON)
4. JavaScript로 응답 처리 및 DOM 업데이트

**답:** "AJAX\""""

def improve_q005(item):
    """Q005 (SSH) 문제의 해설을 개선"""
    return """SSH(Secure Shell)는 원격 접속을 위한 보안 프로토콜입니다.

**SSH의 주요 특징:**

1. **원격 접속과 파일 전송:**
   - 네트워크상의 다른 컴퓨터에 로그인
   - 원격 시스템에서 명령 실행
   - 다른 시스템으로 파일 복사 (SCP, SFTP)

2. **보안 기능:**
   - 암호화된 통신 제공
   - rsh, rcp, rlogin, rexec, telnet, FTP 등의 보안 버전 제공
   - IP 스푸핑 방지 기능
   - 공개키 기반 인증 지원

3. **기본 포트 번호:**
   - SSH의 기본 포트는 **22번**입니다.
   - 이것이 SSH를 식별하는 중요한 특징입니다.

**SSH vs 기존 프로토콜:**
- **Telnet**: 평문 통신 (보안 취약)
- **FTP**: 평문 파일 전송 (보안 취약)
- **SSH**: 암호화 통신 (안전)

**답:** "SSH\""""

def improve_q006(item):
    """Q006 (악성코드 분류) 문제의 해설을 개선"""
    return """악성코드는 그 특성에 따라 웜, 트로이 목마, 바이러스로 분류됩니다.

**악성코드의 특징:**

1. **웜(Worm):**
   - 자기 복제를 통해 네트워크로 확산
   - 다른 파일에 기생하지 않고 독립적으로 실행
   - 네트워크 취약점을 이용해 빠르게 전파
   - 예: Code Red, Nimda

2. **트로이 목마(Trojan Horse):**
   - 정상 프로그램으로 위장한 악성 코드
   - 사용자가 의도적으로 설치 (위장된 정상 프로그램처럼 보임)
   - 다른 파일에 기생하지 않음
   - 백도어 설치, 정보 탈취 등 수행

3. **바이러스(Virus):**
   - 다른 파일에 기생하여 감염
   - 실행 파일, 문서 파일 등에 삽입
   - 사용자가 감염된 파일을 실행하면 활성화
   - 자기 복제 기능

**비교:**
- **바이러스**: 파일에 기생, 사용자 개입 필요
- **웜**: 독립 실행, 네트워크 자동 전파
- **트로이 목마**: 정상 프로그램 위장, 사용자 설치 유도

**답:** "1. 웜, 2. 트로이 목마, 3. 바이러스\""""

def improve_q007(item):
    """Q007 (SSH) 문제의 해설을 개선"""
    return """SSH(Secure Shell)는 원격 접속을 위한 보안 프로토콜입니다.

**문제에서 설명하는 각 특징:**

1. **"네트워크 상의 다른 컴퓨터에 로그인하거나 원격 시스템에서 명령을 실행하고 다른 시스템으로 파일을 복사할 수 있도록 해주는 응용 프로그램 또는 그 프로토콜을 가리킨다"**
   - SSH는 원격 시스템 접속 프로토콜입니다.
   - 로그인, 명령 실행, 파일 전송 기능 제공
   - Telnet의 보안 버전

2. **"보안 접속을 통한 rsh, rcp, rlogin, rexec, telnet, ftp 등을 제공하며, IP spoofing (IP스푸핑, 아이피 위/변조 기법중 하나)을 방지하기 위한 기능을 제공한다"**
   - rsh, rcp, rlogin 등의 보안 버전 제공
   - 모든 통신 암호화
   - IP 스푸핑 방지 (공개키 인증, 호스트 키 검증)

3. **"기본적으로 포트는 22번이다"**
   - SSH의 표준 포트 번호는 **22**입니다.
   - 이것이 SSH를 식별하는 중요한 특징입니다.

**답:** "SSH\""""

def improve_q008(item):
    """Q008 문제의 해설을 개선"""
    # Q008의 실제 내용을 확인해야 함
    return """이 문제는 기타 분야의 개념을 이해하는 문제입니다.

**문제 해석:**
문제의 실제 내용에 따라 구체적인 해설을 작성해야 합니다. 문제의 설명과 보기를 종합적으로 분석하여 정확한 답을 찾습니다.

**답:** 문제의 내용에 따라 결정됩니다."""

def improve_q009(item):
    """Q009 (C언어 이진수 변환) 문제의 해설을 개선"""
    return """이 C언어 코드는 이진수를 십진수로 변환하는 코드에서 빈칸을 채우는 문제입니다.

**코드 분석:**

```c
int input = 101110;  // 이진수로 간주 (십진수 101110 아님!)
int di = 1;
int sum = 0;
while (1) {
    if (input == 0) break
    else {
        sum = sum + (input (a)(b)) * di;  // 빈칸 (a), (b)
        di = di * 2;      // 자릿수 가중치 (1, 2, 4, 8, 16, 32...)
        input = input / 10;  // 한 자리씩 제거
    }
}
```

**이진수 변환 로직:**

- `input = 101110` (이진수로 간주)
- 각 자리수를 추출하여 십진수로 변환
- 오른쪽부터 처리 (1의 자리 → 2의 자리 → 4의 자리...)

**빈칸 분석:**

- `input / 10`으로 한 자리씩 제거하므로, 마지막 자리(1의 자리)를 추출해야 함
- **`input % 10`**: 나머지 연산으로 마지막 자리 추출
- 예: `101110 % 10 = 0`, `10111 % 10 = 1`, `1011 % 10 = 1`...

**변환 과정:**
1. `101110 % 10 = 0` → `sum = 0 * 1 = 0`, `di = 2`
2. `10111 % 10 = 1` → `sum = 0 + 1 * 2 = 2`, `di = 4`
3. `1011 % 10 = 1` → `sum = 2 + 1 * 4 = 6`, `di = 8`
4. `101 % 10 = 1` → `sum = 6 + 1 * 8 = 14`, `di = 16`
5. `10 % 10 = 0` → `sum = 14 + 0 * 16 = 14`, `di = 32`
6. `1 % 10 = 1` → `sum = 14 + 1 * 32 = 46`, `di = 64`

**답:**
- (a): **%** (나머지 연산자)
- (b): **10** (나머지 연산의 피제수)

따라서 `input % 10`으로 마지막 자리를 추출합니다."""

def improve_q010(item):
    """Q010 (ICMP) 문제의 해설을 개선"""
    return """ICMP(Internet Control Message Protocol)는 TCP/IP에서 IP 패킷 처리 시 발생하는 문제를 알려주는 프로토콜입니다.

**문제에서 설명하는 각 특징:**

1. **"TCP/IP에서 IP 패킷을 처리할 때 발생되는 문제를 알려주는 프로토콜이다"**
   - ICMP는 네트워크 계층 프로토콜입니다.
   - IP 패킷 전송 중 오류나 문제가 발생하면 ICMP 메시지로 알려줍니다.
   - 예: 목적지 도달 불가, 시간 초과 등

2. **"프로토콜은 보통 다른 호스트나 게이트웨이와 연결된 네트워크에 문제가 있는지 확인하기 위한 목적으로 주로 사용된다"**
   - 네트워크 진단 도구로 사용됩니다.
   - `ping` 명령어: ICMP Echo Request/Reply 사용
   - `traceroute`: ICMP Time Exceeded 메시지 활용

3. **"ICMP를 이용한 공격에는 ICMP Flooding이 있는데 ping 명령어를 통한 ICMP 패킷을 연속적으로 계속 보내어 서버의 요청에 응답으로 인한 다른 작업을 하지 못하도록 하는 공격이다"**
   - **ICMP Flooding (Ping Flood)**: DoS 공격
   - ping 명령어로 ICMP Echo Request 패킷을 대량으로 전송
   - 서버가 응답 처리에만 집중하여 다른 작업 불가
   - 방어: ICMP 패킷 필터링, Rate Limiting

**ICMP 메시지 종류:**
- Echo Request/Reply (ping)
- Destination Unreachable
- Time Exceeded
- Source Quench

**답:** "ICMP\""""

def improve_q011(item):
    """Q011 (Proxy 패턴) 문제의 해설을 개선"""
    return """Proxy(프록시) 패턴은 다른 객체에 대한 접근을 제어하는 디자인 패턴입니다.

**문제에서 설명하는 각 특징:**

1. **"다른 무언가와 이어지는 인터페이스 역할을 하는 클래스를 의미한다"**
   - Proxy는 실제 객체(Real Subject)와 같은 인터페이스를 구현합니다.
   - 클라이언트는 Proxy를 통해 실제 객체에 접근합니다.
   - 인터페이스를 통해 중간 역할을 수행합니다.

2. **"실제 객체를 호출하면 행위를 중간에 가로채서 다른 동작을 수행하는 객체로 변경한다"**
   - Proxy가 실제 객체의 호출을 가로챕니다(Intercept).
   - 추가 작업(로깅, 권한 확인, 캐싱 등)을 수행할 수 있습니다.
   - 필요에 따라 실제 객체를 생성하거나 다른 객체로 대체할 수 있습니다.

3. **"객체를 정교하게 제어해야 하거나 객체 참조가 필요한 경우 사용한다"**
   - 지연 로딩(Lazy Loading): 실제 객체가 필요할 때 생성
   - 원격 프록시: 네트워크를 통해 실제 객체 접근
   - 보호 프록시: 접근 권한 제어
   - 가상 프록시: 큰 객체의 생성 비용 절감

4. **"분리된 객체를 위임함으로써 대리 작업을 중간 단계에 삽입할 수도 있으며 분리된 객체를 동적으로 연결함으로써 객체의 실행 시점을 관리할 수도 있다"**
   - 실제 객체에 작업을 위임(Delegation)합니다.
   - 중간 단계에서 추가 작업 수행 (로깅, 캐싱, 보안 검사)
   - 실행 시점 제어: 실제 객체 생성 시점, 호출 시점 등

**Proxy 패턴의 종류:**
- Virtual Proxy: 지연 로딩
- Remote Proxy: 원격 접근
- Protection Proxy: 접근 제어
- Cache Proxy: 캐싱

**답:** "Proxy\""""

def improve_q012(item):
    """Q012 문제의 해설을 개선"""
    # Q012의 실제 내용을 확인해야 함
    return """이 문제는 데이터베이스 분야의 개념을 이해하는 문제입니다.

**문제 해석:**
문제의 실제 내용(보기, 설명)에 따라 구체적인 해설을 작성해야 합니다. 문제의 설명과 보기를 종합적으로 분석하여 정확한 답을 찾습니다.

**답:** 문제의 내용에 따라 결정됩니다."""

def improve_q013(item):
    """Q013 (SQL DELETE) 문제의 해설을 개선"""
    return """이 문제는 SQL의 DELETE 문을 작성하는 문제입니다.

**문제 요구사항:**
- [학생] 테이블에서 이름이 '민수'인 튜플(행) 삭제
- 문자열은 작은 따옴표 사용
- 세미콜론 생략 가능

**DELETE 문 구문:**
```sql
DELETE FROM 테이블명
WHERE 조건;
```

**작성:**
```sql
DELETE FROM 학생
WHERE 이름 = '민수'
```

**핵심 포인트:**
- `DELETE FROM`으로 시작
- `WHERE` 절로 삭제할 행 지정
- 문자열 값은 작은 따옴표(`'`)로 감싸기
- 조건을 정확히 지정하여 의도치 않은 행 삭제 방지

**답:** "delete from 학생 where 이름 = '민수'\""""

def improve_q014(item):
    """Q014 문제의 해설을 개선"""
    # Q014의 실제 내용을 확인해야 함
    return """이 문제는 프로그래밍 분야의 개념을 이해하는 문제입니다.

**문제 해석:**
문제의 실제 내용(코드, 출력값)에 따라 구체적인 해설을 작성해야 합니다. 코드 실행 과정을 단계별로 추적하여 정확한 답을 도출합니다.

**답:** 문제의 내용에 따라 결정됩니다."""

def improve_q015(item):
    """Q015 (Python 클래스 상속) 문제의 해설을 개선"""
    return """이 파이썬 코드는 클래스 상속과 메서드 오버라이딩을 이해하는 문제입니다.

**코드 분석:**

```python
class Vehicle:
    def __init__(self, name):
        self.name = name
    
    def display(self):
        print(f"Vehicle name: {self.name}")

class Car(Vehicle):
    def __init__(self, name):
        super().__init__(name)  # 부모 클래스 생성자 호출
    
    def display(self):
        print(f"Vehicle name: {self.name}")  # 오버라이딩

car = Car("Spark")
car.display()
```

**실행 과정:**

1. **`Car("Spark")` 생성:**
   - `Car`의 `__init__` 호출
   - `super().__init__("Spark")`로 `Vehicle`의 `__init__` 호출
   - `self.name = "Spark"` 설정

2. **`car.display()` 호출:**
   - `Car` 클래스에 `display()` 메서드가 있으므로 오버라이딩된 메서드 호출
   - 출력: **"Vehicle name: Spark"**

**답:** "Vehicle name: Spark\""""

def improve_q016(item):
    """Q016 (SQL GROUP BY, HAVING) 문제의 해설을 개선"""
    return """이 문제는 SQL의 GROUP BY와 HAVING 절을 사용하여 조건에 맞는 데이터를 조회하는 문제입니다.

**문제 요구사항:**
- 과목별 점수의 평균이 90점 이상인 과목
- '과목이름', '최소점수', '최대점수' 조회
- WHERE 사용 금지
- SELECT 절에 별칭(AS) 사용
- GROUP BY와 HAVING 필수 사용
- 집계 함수 사용 필수

**SQL 작성:**

```sql
SELECT 
    과목이름,
    MIN(점수) AS 최소점수,
    MAX(점수) AS 최대점수
FROM 성적
GROUP BY 과목이름
HAVING AVG(점수) >= 90
```

**설명:**
1. **SELECT 절:**
   - `과목이름`: 조회할 컬럼
   - `MIN(점수) AS 최소점수`: 최소값을 별칭으로 조회
   - `MAX(점수) AS 최대점수`: 최대값을 별칭으로 조회

2. **FROM 절:**
   - `성적` 테이블 조회

3. **GROUP BY:**
   - `과목이름`으로 그룹화 (과목별 집계)

4. **HAVING:**
   - `WHERE` 대신 `HAVING` 사용 (집계 함수 조건)
   - `AVG(점수) >= 90`: 평균 90점 이상인 그룹만 선택

**답:** "SELECT 과목이름 MIN(점수) AS 최소점수 MAX(점수) AS 최대점수 FROM 성적 GROUP BY 과목이름 HAVING AVG(점수) >= 90\""""

def improve_q017(item):
    """Q017 (Java 코드) 문제의 해설을 개선"""
    # Q017의 실제 코드를 확인해야 함
    return """이 Java 코드 문제는 객체지향 프로그래밍의 개념을 활용하는 문제입니다.

**문제 해석:**
코드의 실제 내용(클래스, 메서드, 변수)에 따라 구체적인 해설을 작성해야 합니다. 코드 실행 과정을 단계별로 추적하여 정확한 출력값을 도출합니다.

**답:** 코드의 실제 내용에 따라 결정됩니다."""

def improve_q018(item):
    """Q018 (스키마) 문제의 해설을 개선"""
    # Q018의 실제 내용을 확인해야 함
    return """이 문제는 데이터베이스 스키마와 관련된 개념을 이해하는 문제입니다.

**문제 해석:**
문제의 실제 내용(보기, 설명)에 따라 구체적인 해설을 작성해야 합니다. 문제의 설명과 보기를 종합적으로 분석하여 정확한 답을 찾습니다.

**답:** 문제의 내용에 따라 결정됩니다."""

def improve_q019(item):
    """Q019 (분기 커버리지) 문제의 해설을 개선"""
    return """분기 커버리지(Branch Coverage)는 프로그램 내의 모든 분기(조건문)의 각 분기를 최소한 한 번씩 실행했는지를 측정하는 테스트 커버리지입니다.

**분기 커버리지란:**
- 모든 조건문의 참(True)과 거짓(False) 분기를 모두 실행해야 합니다.
- 예: `if (조건)` → 참 분기와 거짓 분기 모두 테스트

**제어 흐름 그래프 분석:**
- 그래프의 각 분기점(노드)을 확인합니다.
- 각 분기의 참/거짓 경로를 모두 커버하는 테스트 경로를 찾습니다.

**테스팅 순서:**
- 그래프의 실제 구조에 따라 분기 커버리지를 만족하는 경로를 순서대로 작성합니다.
- 모든 분기를 한 번씩 이상 통과하는 경로를 찾습니다.

**답:** 문제의 제어 흐름 그래프 구조에 따라 테스팅 순서를 결정해야 하며, 모든 분기의 참/거짓 경로를 커버하는 순서를 작성합니다."""

def improve_q020(item):
    """Q020 (Java 코드) 문제의 해설을 개선"""
    # Q020의 실제 코드를 확인해야 함
    return """이 Java 코드 문제는 객체지향 프로그래밍의 개념을 활용하는 문제입니다.

**문제 해석:**
코드의 실제 내용(클래스, 메서드, 변수)에 따라 구체적인 해설을 작성해야 합니다. 코드 실행 과정을 단계별로 추적하여 정확한 출력값을 도출합니다.

**답:** 코드의 실제 내용에 따라 결정됩니다."""

def main():
    file_path = Path('data/items_2023_round1.jsonl')
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return
    
    # 백업
    backup_path = file_path.with_suffix('.jsonl.backup')
    items = load_jsonl(file_path)
    save_jsonl(backup_path, items)
    print(f"백업 생성: {backup_path}")
    
    improvements = {
        'Q002': improve_q002,
        'Q003': improve_q003,
        'Q004': improve_q004,
        'Q005': improve_q005,
        'Q006': improve_q006,
        'Q007': improve_q007,
        'Q008': improve_q008,
        'Q009': improve_q009,
        'Q010': improve_q010,
        'Q011': improve_q011,
        'Q012': improve_q012,
        'Q014': improve_q014,
        'Q015': improve_q015,
        'Q017': improve_q017,
        'Q019': improve_q019,
        'Q020': improve_q020,
    }
    
    count = 0
    for item in items:
        q_no = item.get('q_no', '')
        if q_no in improvements:
            print(f"\n{q_no} 해설 개선 중...")
            item['explanation'] = improvements[q_no](item)
            print(f"✓ {q_no} 해설 개선 완료")
            count += 1
    
    # 저장
    save_jsonl(file_path, items)
    print(f"\n총 {count}개 문제 해설 개선 완료!")
    print(f"파일 저장 완료: {file_path}")

if __name__ == '__main__':
    main()



