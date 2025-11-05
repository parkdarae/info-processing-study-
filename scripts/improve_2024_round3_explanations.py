#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024년 3회 모든 범용적 해설 개선 스크립트
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

def improve_q002(item):
    """Q002 (Python 리스트 역순) 문제의 해설을 개선"""
    return """이 파이썬 코드는 리스트를 역순으로 뒤집고 짝수 인덱스와 홀수 인덱스의 합 차이를 계산하는 문제입니다.

**코드 분석:**

```python
def func(lst):
    for i in range(len(lst) // 2):
        lst[i], lst[-i-1] = lst[-i-1], lst[i]  # 리스트 역순

lst = [1, 2, 3, 4, 5, 6]
func(lst)  # 역순으로 뒤집기
print(sum(lst[::2]) - sum(lst[1::2]))  # 짝수 인덱스 합 - 홀수 인덱스 합
```

**실행 과정:**

1. **초기 상태:**
   - `lst = [1, 2, 3, 4, 5, 6]`

2. **`func(lst)` 실행 (역순으로 뒤집기):**
   - `len(lst) // 2 = 6 // 2 = 3`
   - i=0: lst[0] ↔ lst[-1] → [6, 2, 3, 4, 5, 1]
   - i=1: lst[1] ↔ lst[-2] → [6, 5, 3, 4, 2, 1]
   - i=2: lst[2] ↔ lst[-3] → [6, 5, 4, 3, 2, 1]
   - **결과: `lst = [6, 5, 4, 3, 2, 1]`**

3. **합 차이 계산:**
   ```python
   sum(lst[::2])   # 짝수 인덱스 (0, 2, 4): 6 + 4 + 2 = 12
   sum(lst[1::2])  # 홀수 인덱스 (1, 3, 5): 5 + 3 + 1 = 9
   ```
   - `12 - 9 = 3`

**답:** 3"""

def improve_q004(item):
    """Q004 (LRU 페이지 교체) 문제의 해설을 개선"""
    return """LRU(Least Recently Used) 스케줄링은 가장 오래전에 사용된 페이지를 교체하는 알고리즘입니다.

**주어진 정보:**
- 할당된 프레임 수: 3개
- 페이지 참조 순서: 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1

**LRU 실행 과정:**

**초기 상태:** [빈, 빈, 빈]

| 참조 | 프레임 상태 | 페이지 부재 |
|------|------------|-----------|
| 7 | [7, 빈, 빈] | ✓ |
| 0 | [7, 0, 빈] | ✓ |
| 1 | [7, 0, 1] | ✓ |
| 2 | [0, 1, 2] | ✓ (7 제거, 가장 오래됨) |
| 0 | [0, 1, 2] | (히트) |
| 3 | [1, 2, 3] | ✓ (0 제거) |
| 0 | [2, 3, 0] | ✓ (1 제거) |
| 4 | [3, 0, 4] | ✓ (2 제거) |
| 2 | [0, 4, 2] | ✓ (3 제거) |
| 3 | [4, 2, 3] | ✓ (0 제거) |
| 0 | [2, 3, 0] | ✓ (4 제거) |
| 3 | [2, 3, 0] | (히트) |
| 2 | [2, 3, 0] | (히트) |
| 1 | [3, 0, 1] | ✓ (2 제거) |
| 2 | [0, 1, 2] | ✓ (3 제거) |
| 0 | [0, 1, 2] | (히트) |
| 1 | [0, 1, 2] | (히트) |
| 7 | [1, 2, 7] | ✓ (0 제거) |
| 0 | [2, 7, 0] | ✓ (1 제거) |
| 1 | [7, 0, 1] | ✓ (2 제거) |

**페이지 부재 횟수: 12**

**답:** 12"""

def improve_q005(item):
    """Q005 (스머프 공격) 문제의 해설을 개선"""
    return """스머프(Smurf) 공격은 IP와 ICMP의 특성을 악용한 DDoS 공격입니다.

**문제에서 설명하는 각 특징:**

1. **"IP나 ICMP의 특성을 악용하여 엄청난 양의 데이터를 한 사이트에 집중적으로 보냄으로써 네트워크의 일부를 불능 상태로 만드는 공격이다"**
   - 스머프 공격은 IP 브로드캐스트 주소를 악용합니다.
   - 공격자는 피해자의 IP 주소를 위조(spoofing)하여 브로드캐스트 주소로 ICMP Echo Request를 전송합니다.
   - 브로드캐스트 네트워크의 모든 호스트가 응답하여 트래픽이 증폭됩니다.

2. **"여러 호스트가 특정 대상에게 다량의 ICMP Echo Reply를 보내게 하여 서비스거부(DoS)를 유발시키는 보안공격이다"**
   - 공격자는 피해자의 IP를 소스로 위조한 ICMP Echo Request를 브로드캐스트합니다.
   - 네트워크의 모든 호스트가 피해자에게 ICMP Echo Reply를 전송합니다.
   - 결과적으로 피해자는 엄청난 양의 응답 패킷을 받게 됩니다.

3. **"공격 대상 호스트는 다량으로 유입되는 패킷으로 인해 서비스 불능 상태에 빠진다"**
   - 수신 대역폭이 포화되어 정상적인 통신이 불가능해집니다.
   - DoS(Denial of Service) 상태에 빠집니다.

**스머프 공격의 방어 방법:**
- 라우터에서 브로드캐스트 주소로 향하는 패킷을 차단
- ICMP 패킷 필터링
- IP 스푸핑 방지

**답:** "스머프\""""

def improve_q006(item):
    """Q006 (행위 패턴) 문제의 해설을 개선"""
    return """행위(Behavioral) 패턴은 객체 간의 상호작용과 책임 분배를 정의하는 GoF 디자인 패턴입니다.

**문제에서 설명하는 각 특징:**

1. **"클래스나 객체들이 서로 상호작용하는 방법이나 책임 분배 방법을 정의하는 패턴이다"**
   - 행위 패턴은 객체 간의 통신 방식을 정의합니다.
   - 각 객체의 역할과 책임을 명확히 분리합니다.
   - 예: Observer 패턴에서 주제와 관찰자의 상호작용

2. **"객체들 간의 통신 방법을 정의하고 알고리즘을 캡슐화하여 객체 간의 결합도를 낮춘다"**
   - 통신 방법을 표준화하여 결합도를 낮춥니다.
   - 알고리즘을 객체로 캡슐화합니다.
   - 예: Strategy 패턴에서 알고리즘을 독립적인 객체로 분리

3. **"Chain of Responsibility나 Command 또는 Observer 패턴이 있다"**
   - Chain of Responsibility: 요청을 객체 체인으로 전달
   - Command: 요청을 객체로 캡슐화
   - Observer: 객체 간 일대다 의존성 정의

**GoF 패턴 분류:**
- **생성 패턴(Creational)**: 객체 생성 담당 (Singleton, Factory 등)
- **구조 패턴(Structural)**: 클래스/객체 조합 (Adapter, Decorator 등)
- **행위 패턴(Behavioral)**: 객체 간 상호작용 (Observer, Command 등) ✓

**답:** "행위\""""

def improve_q007(item):
    """Q007 (C언어 static 변수) 문제의 해설을 개선"""
    return """이 C언어 코드는 static 변수의 특성을 이해하는 문제입니다.

**코드 분석:**

```c
int func() {
    static int x = 0;  // static 변수 (초기화는 한 번만!)
    x += 2;
    return x;
}

int main() {
    int x = 1;  // 지역 변수 (func의 x와 별개)
    int sum = 0;
    for(int i=0; i<4; i++) {
        x++;      // 지역 변수 x 증가
        sum += func();  // func() 호출
    }
    printf("%d", sum);
}
```

**실행 과정:**

1. **초기값:**
   - `main`의 지역 변수: `x = 1`
   - `func`의 static 변수: `x = 0` (초기화는 프로그램 시작 시 한 번만)

2. **반복문 실행:**

   **i=0:**
   - `x++` → `x = 2` (main의 지역 변수)
   - `func()` 호출:
     - static `x = 0` (유지됨)
     - `x += 2` → `x = 2`
     - 반환: **2**
   - `sum = 0 + 2 = 2`

   **i=1:**
   - `x++` → `x = 3`
   - `func()` 호출:
     - static `x = 2` (이전 값 유지!)
     - `x += 2` → `x = 4`
     - 반환: **4**
   - `sum = 2 + 4 = 6`

   **i=2:**
   - `x++` → `x = 4`
   - `func()` 호출:
     - static `x = 4`
     - `x += 2` → `x = 6`
     - 반환: **6**
   - `sum = 6 + 6 = 12`

   **i=3:**
   - `x++` → `x = 5`
   - `func()` 호출:
     - static `x = 6`
     - `x += 2` → `x = 8`
     - 반환: **8**
   - `sum = 12 + 8 = 20`

3. **최종 출력:**
   - **출력: 20**

**핵심 포인트:**
- static 변수는 함수가 종료되어도 메모리에 유지됩니다.
- static 변수의 초기화는 프로그램 시작 시 한 번만 실행됩니다.
- 함수를 여러 번 호출해도 static 변수는 이전 값을 유지합니다.

**답:** 20"""

def improve_q009(item):
    """Q009 (URL 구조) 문제의 해설을 개선"""
    return """URL(Uniform Resource Locator)의 구조를 이해하는 문제입니다.

**URL 구조 예시:**
```
https://user:pass@example.com:8080/path/to/resource?query=value#fragment
│      │     │     │              │   │                  │       │
│      │     │     │              │   │                  │       └─ fragment
│      │     │     │              │   │                  └─ query
│      │     │     │              │   └─ path
│      │     │     │              └─ port
│      │     │     └─ hostname
│      │     └─ password
│      └─ username
└─ scheme
```

**각 구성 요소:**

1. **scheme (3번)**: 리소스에 접근하는 방법이나 프로토콜
   - 예: `http`, `https`, `ftp`, `mailto`
   - URL의 가장 앞에 위치합니다.

2. **authority (4번)**: 사용자 정보, 호스트명, 포트 번호
   - 형식: `[username:password@]hostname[:port]`
   - 예: `user:pass@example.com:8080`

3. **path (1번)**: 서버 내의 특정 자원을 가리키는 경로
   - 예: `/path/to/resource`
   - 서버의 파일 시스템 경로를 나타냅니다.

4. **query (2번)**: 서버에 전달할 추가 데이터
   - 형식: `?key=value&key2=value2`
   - GET 요청의 파라미터를 전달합니다.

5. **fragment (5번)**: 특정 문서 내의 위치
   - 형식: `#section`
   - HTML 문서의 앵커를 가리킵니다.

**순서:**
1. scheme → 2. authority → 3. path → 4. query → 5. fragment

**보기 매칭:**
- query: 1
- path: 2
- scheme: 3
- authority: 4
- fragment: 5

**답:** "43125\""""

def improve_q010(item):
    """Q010 (Python type 체크) 문제의 해설을 개선"""
    return """이 파이썬 코드는 `type()` 함수를 사용한 타입 체크를 이해하는 문제입니다.

**코드 분석:**

```python
def func(value):
    if type(value) == type(100):        # int 타입 체크
        return 100
    elif type(value) == type(""):      # str 타입 체크
        return len(value)
    else:
        return 20

a = '100.0'    # 문자열
b = 100.0      # float (실수)
c = (100, 200) # tuple

print(func(a) + func(b) + func(c))
```

**실행 과정:**

1. **`func('100.0')` 호출:**
   - `type('100.0') == type("")` → `True` (문자열)
   - 반환: `len('100.0') = 5`

2. **`func(100.0)` 호출:**
   - `type(100.0) == type(100)` → `False` (float ≠ int)
   - `type(100.0) == type("")` → `False` (float ≠ str)
   - else 블록 실행 → 반환: **20**

3. **`func((100, 200))` 호출:**
   - `type((100, 200)) == type(100)` → `False` (tuple ≠ int)
   - `type((100, 200)) == type("")` → `False` (tuple ≠ str)
   - else 블록 실행 → 반환: **20**

4. **최종 계산:**
   - `5 + 20 + 20 = 45`

**핵심 포인트:**
- `type()` 함수는 객체의 타입을 반환합니다.
- `type(100)`은 `int` 타입 객체를 반환합니다.
- `100.0`은 `float` 타입이므로 `int`와 다릅니다.

**답:** 45"""

def improve_q012(item):
    """Q012 (C언어 연결 리스트 값 교환) 문제의 해설을 개선"""
    return """이 C언어 코드는 연결 리스트에서 인접한 노드 쌍의 값을 교환하는 문제입니다.

**코드 분석:**

```c
void func(struct Node* node) {
    while(node != NULL && node->next != NULL) {
        int t = node->value;
        node->value = node->next->value;
        node->next->value = t;           // 인접 노드 값 교환
        node = node->next->next;         // 두 칸 건너뛰기
    }
}
```

**실행 과정:**

1. **초기 리스트 구성:**
   ```c
   n1 = {1, NULL}
   n2 = {2, NULL}
   n3 = {3, NULL}
   n1.next = &n3;
   n3.next = &n2;
   ```
   - 리스트: **1 → 3 → 2 → NULL**

2. **`func(&n1)` 실행:**

   **첫 번째 반복 (node = &n1):**
   - node != NULL ✓, node->next != NULL ✓
   - 교환: n1.value(1) ↔ n3.value(3)
   - 리스트: **3 → 1 → 2 → NULL**
   - `node = node->next->next` = `n3->next` = `&n2`

   **두 번째 반복 (node = &n2):**
   - node != NULL ✓, node->next == NULL ✗
   - 루프 종료

3. **출력:**
   ```c
   while(current != NULL) {
       printf("%d", current->value);
       current = current->next;
   }
   ```
   - 출력: **"312"**

**답:** "312\""""

def improve_q013(item):
    """Q013 (테스트 커버리지) 문제의 해설을 개선"""
    return """이 문제는 소프트웨어 테스트 커버리지(Test Coverage)의 종류를 구분하는 문제입니다.

**문제에서 설명하는 각 커버리지:**

1. **"테스트를 통해 프로그램의 모든 문장을 최소한 한 번씩 실행했는지를 측정"**
   - **문장 커버리지(Statement Coverage)** 또는 **구문 커버리지**
   - 모든 실행 가능한 문장이 한 번 이상 실행되었는지 확인합니다.
   - 가장 기본적인 커버리지입니다.
   - 예: `if-else` 문에서 각 분기가 실행되었는지 확인

2. **"프로그램 내의 모든 분기(조건문)의 각 분기를 최소한 한 번씩 실행했는지를 측정"**
   - **분기 커버리지(Branch Coverage)** 또는 **결정 커버리지(Decision Coverage)**
   - 모든 조건문의 참/거짓 분기를 실행했는지 확인합니다.
   - 문장 커버리지보다 엄격합니다.
   - 예: `if (a > 0)`의 참과 거짓 경우를 모두 테스트

3. **"복합 조건 내의 각 개별 조건이 참과 거짓으로 평가되는 경우를 모두 테스트했는지를 측정"**
   - **조건 커버리지(Condition Coverage)**
   - 복합 조건문(`if (a > 0 && b < 0)`)의 각 조건을 개별적으로 테스트합니다.
   - 각 조건이 참과 거짓으로 평가되었는지 확인합니다.

**커버리지 종류:**
- ㄱ. 조건 커버리지 ✓ (3번)
- ㄴ. 경로 커버리지: 모든 실행 경로를 테스트
- ㄷ. 결정 커버리지: 분기 커버리지와 유사
- ㄹ. 분기 커버리지 ✓ (2번)
- ㅁ. 함수 커버리지: 모든 함수 호출
- ㅂ. 문장 커버리지 ✓ (1번)
- ㅅ. 루프 커버리지: 모든 루프 실행

**답:**
- 1. 문장 (ㅂ)
- 2. 분기 (ㄹ)
- 3. 조건 (ㄱ)"""

def improve_q016(item):
    """Q016 (C언어 이중 포인터) 문제의 해설을 개선"""
    return """이 C언어 코드는 이중 포인터와 배열 연산을 이해하는 문제입니다.

**코드 분석:**

```c
void func(int** arr, int size) {
    for(int i=0; i<size; i++) {
        *(*arr + i) = (*(*arr+i) + i) % size;
    }
}

int main() {
    int arr[] = {3, 1, 4, 1, 5};
    int* p = arr;
    int** pp = &p;
    func(pp, 5);
    num = arr[2];
    printf("%d", num);
}
```

**실행 과정:**

1. **초기 상태:**
   - `arr = {3, 1, 4, 1, 5}`
   - `p = arr` (arr의 시작 주소)
   - `pp = &p` (p의 주소)

2. **`func(pp, 5)` 호출:**
   - `arr` 파라미터는 `pp`이므로 `**arr = *p = arr[0]`

   **i=0:**
   - `*(*arr + 0) = arr[0] = 3`
   - `(3 + 0) % 5 = 3`
   - `arr[0] = 3`

   **i=1:**
   - `*(*arr + 1) = arr[1] = 1`
   - `(1 + 1) % 5 = 2`
   - `arr[1] = 2`

   **i=2:**
   - `*(*arr + 2) = arr[2] = 4`
   - `(4 + 2) % 5 = 1`
   - `arr[2] = 1`

   **i=3:**
   - `*(*arr + 3) = arr[3] = 1`
   - `(1 + 3) % 5 = 4`
   - `arr[3] = 4`

   **i=4:**
   - `*(*arr + 4) = arr[4] = 5`
   - `(5 + 4) % 5 = 4`
   - `arr[4] = 4`

   **최종 배열:** `{3, 2, 1, 4, 4}`

3. **출력:**
   ```c
   num = arr[2] = 1
   printf("%d", 1);
   ```

**답:** 1"""

def improve_q017(item):
    """Q017 (VPN) 문제의 해설을 개선"""
    return """VPN(Virtual Private Network)은 공용 네트워크를 통해 사설 네트워크를 확장하는 기술입니다.

**문제에서 설명하는 각 특징:**

1. **"공용 네트워크를 통해 사설 네트워크를 확장하는 기술이다"**
   - 인터넷 같은 공용 네트워크 위에 가상의 사설 네트워크를 구축합니다.
   - 물리적으로 멀리 떨어진 네트워크를 하나의 사설망처럼 사용할 수 있습니다.
   - Site-to-Site VPN, Remote Access VPN 등이 있습니다.

2. **"사용자의 IP 주소를 숨기고, 사용자가 어디에서 접속하는지를 추적하기 어렵게 만든다"**
   - VPN 서버를 통해 트래픽을 중계하므로 실제 IP가 숨겨집니다.
   - 위치 추적이 어려워집니다.
   - 프라이버시 보호에 도움이 됩니다.

3. **"종류로는 IPsec 또는 SSL, L2TP 등이 있다"**
   - **IPsec (IP Security)**: 네트워크 계층 암호화
   - **SSL/TLS VPN**: 애플리케이션 계층 암호화
   - **L2TP (Layer 2 Tunneling Protocol)**: 데이터 링크 계층 터널링

**VPN의 주요 용도:**
- 원격 접근: 외부에서 회사 내부 네트워크 접속
- 사이트 간 연결: 지사 간 안전한 통신
- 프라이버시 보호: IP 주소 숨김

**답:** "VPN\""""

def improve_q018(item):
    """Q018 (Java 예외 처리, finally) 문제의 해설을 개선"""
    return """이 Java 코드는 예외 처리 메커니즘과 finally 블록의 실행 순서를 이해하는 문제입니다.

**코드 분석:**

```java
public static void main(String[] args) {
    int sum = 0;
    try {
        func();  // NullPointerException 발생
    } catch (NullPointerException e) {
        sum = sum + 1;  // sum = 1
    } catch (Exception e) {
        sum = sum + 10;
    } finally {
        sum = sum + 100;  // 항상 실행
    }
    System.out.print(sum);
}

static void func() throws Exception {
    throw new NullPointerException();
}
```

**실행 과정:**

1. **try 블록 실행:**
   - `func()` 호출
   - `NullPointerException` 발생

2. **예외 처리:**
   - Java는 첫 번째로 일치하는 catch 블록을 찾습니다.
   - `catch (NullPointerException e)` → **일치!**
   - `sum = 0 + 1 = 1`

3. **finally 블록 실행:**
   - 예외 발생 여부와 관계없이 **항상 실행**됩니다.
   - `sum = 1 + 100 = 101`

4. **최종 출력:**
   - **출력: 101**

**핵심 포인트:**
- 예외 처리 순서: try → catch(일치하는 예외) → finally
- finally 블록은 반드시 실행됩니다.
- `NullPointerException`은 `Exception`의 자식 클래스이므로, 더 구체적인 catch 블록이 먼저 매칭됩니다.

**답:** 101"""

def improve_q020(item):
    """Q020 (Ad-hoc Network) 문제의 해설을 개선"""
    return """Ad-hoc Network(애드혹 네트워크)는 중앙 관리나 고정된 인프라 없이 임시로 구성되는 네트워크입니다.

**문제에서 설명하는 각 특징:**

1. **"중앙 관리나 고정된 인프라 없이 임시로 구성되는 네트워크이다"**
   - 중앙 서버나 라우터 없이 노드들이 직접 통신합니다.
   - 인프라가 필요 없어 빠르게 구성 가능합니다.
   - 동적으로 네트워크를 형성합니다.

2. **"일반적으로 무선 통신을 통해 노드들이 직접 연결되어 데이터를 주고받는다"**
   - 무선 기술(Wi-Fi, Bluetooth 등)을 사용합니다.
   - P2P(Peer-to-Peer) 방식으로 직접 통신합니다.
   - 각 노드가 라우터 역할을 할 수 있습니다.

3. **"긴급 구조, 긴급 회의, 군사적인 상황 등에서 유용하게 활용될 수 있다"**
   - 인프라가 없는 상황에서도 통신 가능
   - 재난 상황, 야전 환경 등에서 활용
   - 임시 네트워크 구축에 적합

**보기 분석:**
- ㄱ. Infrastructure Network: 인프라 기반 네트워크 (Wi-Fi AP 필요)
- ㄴ. Firmware Network: 펌웨어 네트워크 (일반적 용어 아님)
- ㄷ. Peer-to-Peer Network: P2P (일부 특징 유사하지만 Ad-hoc과 다름)
- **ㄹ. Ad-hoc Network**: 중앙 인프라 없이 임시 구성 ✓
- ㅁ. Mesh Network: 메시 네트워크 (Ad-hoc의 확장 형태)
- ㅂ. Sensor Network: 센서 네트워크 (IoT)
- ㅅ. Virtual Private Network: VPN (가상 사설망)

**답:** "ㄹ" (Ad-hoc Network)"""

def main():
    file_path = Path('data/items_2024_round3.jsonl')
    
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
        'Q004': improve_q004,
        'Q005': improve_q005,
        'Q006': improve_q006,
        'Q007': improve_q007,
        'Q009': improve_q009,
        'Q010': improve_q010,
        'Q012': improve_q012,
        'Q013': improve_q013,
        'Q016': improve_q016,
        'Q017': improve_q017,
        'Q018': improve_q018,
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



