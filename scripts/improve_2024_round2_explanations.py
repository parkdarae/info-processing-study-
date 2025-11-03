#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024년 2회 모든 범용적 해설 개선 스크립트
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
    """Q001 (Java 배열 비교) 문제의 해설을 개선"""
    return """이 Java 코드는 배열 참조 비교(==)와 배열 내용 비교를 이해하는 문제입니다.

**코드 분석:**

```java
int[] a = new int[]{1, 2, 3, 4};
int[] b = new int[]{1, 2, 3, 4};
int[] c = new int[]{1, 2, 3};
check(a, b);  // a == b 비교
check(a, c);  // a == c 비교
check(b, c);  // b == c 비교
```

**`check()` 함수:**
```java
public static void check(int[] a, int[] b) {
    if (a == b) {  // 참조 비교 (주소 비교)
        System.out.print("O");
    } else {
        System.out.print("N");
    }
}
```

**실행 과정:**

1. **`check(a, b)` 호출:**
   - `a`와 `b`는 서로 다른 배열 객체입니다 (내용은 같지만 별도로 생성).
   - `a == b` → `false` (참조 주소가 다름)
   - **출력: "N"**

2. **`check(a, c)` 호출:**
   - `a`와 `c`는 다른 배열 객체이며 내용도 다릅니다.
   - `a == c` → `false`
   - **출력: "N"**

3. **`check(b, c)` 호출:**
   - `b`와 `c`는 다른 배열 객체입니다.
   - `b == c` → `false`
   - **출력: "N"**

**최종 출력:** "NNN"

**핵심 포인트:**
- Java에서 `==`는 참조 비교입니다 (주소 비교).
- `new`로 생성된 배열은 각각 별도의 객체이므로 항상 `false`입니다.
- 배열 내용을 비교하려면 `Arrays.equals(a, b)`를 사용해야 합니다.

**답:** "NNN\""""

def improve_q005(item):
    """Q005 (IPSec) 문제의 해설을 개선"""
    return """IPSec(IP Security)는 네트워크 계층에서 IP 패킷을 암호화하고 인증하는 보안 프로토콜입니다.

**문제에서 설명하는 각 특징:**

1. **"Network layer에서 IP패킷을 암호화하고 인증하는 등의 보안을 위한 표준이다"**
   - IPSec은 OSI 7계층 중 3계층(네트워크 계층)에서 동작합니다.
   - IP 패킷 자체를 암호화하여 데이터를 보호합니다.
   - 인증(Authentication)과 암호화(Encryption) 기능을 제공합니다.

2. **"기업에서 사설 인터넷망으로 사용할 수 있는 VPN을 구현하는데 사용되는 프로토콜이다"**
   - VPN(Virtual Private Network) 구축에 사용됩니다.
   - 인터넷을 통해 안전한 사설망을 구축할 수 있습니다.
   - Site-to-Site VPN, Remote Access VPN 등에 활용됩니다.

3. **"AH(Authentication Header)와 ESP(Encapsulating Security Payload)라는 두 가지 보안 프로토콜을 사용한다"**
   - **AH(Authentication Header)**: 데이터 무결성과 인증을 제공 (암호화 없음)
   - **ESP(Encapsulating Security Payload)**: 암호화와 인증을 모두 제공
   - 두 프로토콜을 개별 또는 조합하여 사용할 수 있습니다.

**IPSec의 작동 방식:**
- 터널 모드(Tunnel Mode): 전체 IP 패킷을 암호화
- 전송 모드(Transport Mode): 페이로드만 암호화

**답:** "IPSec\""""

def improve_q006(item):
    """Q006 (Python 문자열 패턴 매칭) 문제의 해설을 개선"""
    return """이 파이썬 코드는 문자열에서 패턴의 출현 횟수를 세는 문제입니다.

**코드 분석:**

```python
def fnCalculation(x, y):
    result = 0
    for i in range(len(x)):
        temp = x[i:i+len(y)]  # x에서 길이 len(y)만큼 슬라이싱
        if temp == y:
            result += 1
    return result

a = "abdcabcabca"
p1 = "ab"
p2 = "ca"
out = f"ab{fnCalculation(a, p1)}ca{fnCalculation(a, p2)}"
print(out)
```

**실행 과정:**

1. **`fnCalculation(a, "ab")` 계산:**
   - a = "abdcabcabca"
   - i=0: "ab" == "ab" → result = 1
   - i=1: "bd" != "ab"
   - i=2: "dc" != "ab"
   - i=3: "ca" != "ab"
   - i=4: "ab" == "ab" → result = 2
   - i=5: "bc" != "ab"
   - i=6: "ca" != "ab"
   - i=7: "ab" == "ab" → result = 3
   - i=8: "bc" != "ab"
   - i=9: "ca" != "ab"
   - 결과: **3**

2. **`fnCalculation(a, "ca")` 계산:**
   - i=0: "ab" != "ca"
   - i=1: "bd" != "ca"
   - i=2: "dc" != "ca"
   - i=3: "ca" == "ca" → result = 1
   - i=4: "ab" != "ca"
   - i=5: "bc" != "ca"
   - i=6: "ca" == "ca" → result = 2
   - i=7: "ab" != "ca"
   - i=8: "bc" != "ca"
   - i=9: "ca" == "ca" → result = 3
   - 결과: **3**

3. **최종 출력:**
   ```python
   out = f"ab{3}ca{3}" = "ab3ca3"
   ```

**답:** "ab3ca3\""""

def improve_q007(item):
    """Q007 (AES) 문제의 해설을 개선"""
    return """AES(Advanced Encryption Standard)는 고급 암호화 표준으로 대칭키 암호 알고리즘입니다.

**문제에서 설명하는 각 특징:**

1. **"대칭키 알고리즘으로 1997년 NIST(미국 국립기술표준원)에서 DES를 대체하기 위해 생성되었다"**
   - AES는 대칭키 암호 알고리즘입니다 (같은 키로 암호화/복호화).
   - 1997년 NIST가 DES의 취약점을 해결하기 위해 공모를 시작했습니다.
   - 2000년 Rijndael 알고리즘이 선택되어 AES로 지정되었습니다.
   - DES(56비트 키)의 취약점을 해결하기 위해 개발되었습니다.

2. **"128비트, 192비트 또는 256비트의 가변 키 크기와 128비트의 고정 블록 크기를 사용한다"**
   - 키 크기: AES-128, AES-192, AES-256 (세 가지 버전)
   - 블록 크기: 항상 128비트 (고정)
   - 키가 길수록 보안성이 높아지지만 성능은 약간 저하됩니다.

3. **"높은 안전성과 효율성, 속도 등으로 인해 DES 대신 전 세계적으로 많이 사용되고 있다"**
   - DES보다 훨씬 빠르고 안전합니다.
   - 하드웨어와 소프트웨어 모두에서 효율적으로 구현 가능합니다.
   - 현재 가장 널리 사용되는 대칭키 암호 알고리즘입니다.
   - SSL/TLS, Wi-Fi 보안(WPA2), 하드디스크 암호화 등에 사용됩니다.

**AES의 작동 방식:**
- SubBytes: 바이트 치환
- ShiftRows: 행 이동
- MixColumns: 열 혼합
- AddRoundKey: 라운드 키 적용

**답:** "AES\""""

def improve_q008(item):
    """Q008 (가상회선, 데이터그램) 문제의 해설을 개선"""
    return """패킷 교환 방식은 연결형과 비연결형으로 나뉩니다.

**① 연결형 교환 방식: 가상회선(Virtual Circuit)**

**특징:**
- 통신 시작 전에 경로를 설정합니다 (가상 회선 설정).
- 모든 패킷이 같은 경로로 전송됩니다.
- 패킷 순서가 보장됩니다.
- 연결 설정과 해제 과정이 필요합니다.
- 전화망과 유사한 방식입니다.

**예시:**
- X.25
- Frame Relay
- ATM (Asynchronous Transfer Mode)

**② 비연결형 교환 방식: 데이터그램(Datagram)**

**특징:**
- 경로 설정 없이 각 패킷을 독립적으로 전송합니다.
- 각 패킷은 목적지 주소를 포함하여 독립적으로 라우팅됩니다.
- 패킷 순서가 보장되지 않을 수 있습니다.
- 연결 설정/해제 과정이 없습니다.
- 우편물과 유사한 방식입니다.

**예시:**
- IP (Internet Protocol)
- UDP (User Datagram Protocol)

**비교:**
- **가상회선**: 연결 설정 필요, 순서 보장, 오버헤드 큼
- **데이터그램**: 연결 설정 없음, 순서 보장 안 됨, 오버헤드 작음

**답:**
- ① 가상회선 (Virtual Circuit)
- ② 데이터그램 (Datagram)"""

def improve_q009(item):
    """Q009 (순차적 응집도) 문제의 해설을 개선"""
    return """이 문제는 소프트웨어 공학의 모듈 응집도 중 순차적 응집도(Sequential Cohesion)를 구분하는 문제입니다.

**문제에서 설명하는 특징:**

1. **"실행 순서가 밀접한 관계를 갖는 기능을 모아 모듈로 구성한다"**
   - 순차적 응집도는 기능들이 시간적 순서대로 실행되는 경우입니다.

2. **"한 모듈 내부의 한 기능 요소에 의한 출력 자료가 다음 기능 원소의 입력 자료로서 제공되는 형태이다"**
   - 한 기능의 출력이 바로 다음 기능의 입력이 되는 파이프라인 형태입니다.
   - 예: 입력 처리 → 데이터 변환 → 출력 처리

**응집도 종류 비교:**

- **ㄱ. 기능적**: 하나의 명확한 기능 수행 (가장 높음)
- **ㄴ. 우연적**: 관련성 없는 요소들의 집합 (가장 낮음)
- **ㄷ. 통신적**: 같은 데이터를 조작하는 요소들
- **ㄹ. 절차적**: 순차적으로 실행되는 요소들
- **ㅁ. 시간적**: 특정 시점에 실행되는 요소들
- **ㅂ. 순차적**: 출력→입력 파이프라인 형태 ✓
- **ㅅ. 논리적**: 논리적으로 비슷한 기능들

**순차적 응집도의 예시:**
- 데이터 입력 → 검증 → 변환 → 저장
- 이미지 로드 → 리사이즈 → 필터 적용 → 저장

**답:** "ㅂ" (순차적 응집도)"""

def improve_q010(item):
    """Q010 (Iterator 패턴) 문제의 해설을 개선"""
    return """Iterator(반복자) 패턴은 컬렉션의 요소에 접근하는 방법을 표준화하는 디자인 패턴입니다.

**문제에서 설명하는 각 특징:**

1. **"컬렉션 객체의 내부 구조를 노출하지 않고 순차적으로 접근할 수 있게 하는 패턴이다"**
   - 클라이언트는 컬렉션의 내부 구현(배열, 리스트, 트리 등)을 알 필요가 없습니다.
   - 일관된 방식으로 요소에 접근할 수 있습니다.
   - 캡슐화 원칙을 따릅니다.

2. **"이 패턴은 객체의 내부 표현 방식에 독립적으로 요소에 접근할 수 있도록 해준다"**
   - 컬렉션이 배열이든 리스트든 상관없이 같은 방식으로 접근 가능합니다.
   - 컬렉션의 구현이 바뀌어도 클라이언트 코드는 변경되지 않습니다.

3. **"반복 프로세스를 캡슐화하여 클라이언트 코드에서는 컬렉션의 구체적인 구현에 종속되지 않도록 한다"**
   - 반복 로직을 Iterator 객체에 위임합니다.
   - 클라이언트는 `hasNext()`, `next()` 같은 표준 메서드만 사용합니다.
   - 의존성 역전 원칙을 따릅니다.

**Iterator 패턴의 구성요소:**
- **Iterator**: 반복 작업을 담당하는 인터페이스
- **ConcreteIterator**: 구체적인 반복자 구현
- **Aggregate**: 컬렉션 인터페이스
- **ConcreteAggregate**: 구체적인 컬렉션 구현

**사용 예시:**
- Java: `Iterator<String> it = list.iterator();`
- C++: STL의 iterator
- Python: `for item in collection:`

**답:** "Iterator\""""

def improve_q011(item):
    """Q011 (RIP 라우팅) 문제의 해설을 개선"""
    return """RIP(Routing Information Protocol)는 거리 벡터 라우팅 프로토콜입니다.

**RIP의 작동 원리:**
- 각 라우터가 이웃 라우터와 라우팅 정보를 주기적으로 교환합니다.
- 홉(Hop) 수를 거리로 사용합니다 (최대 15홉).
- 최단 경로는 가장 적은 홉 수를 가진 경로입니다.

**문제 해결 방법:**

1. **초기 상태:**
   - 각 라우터는 직접 연결된 네트워크만 알고 있습니다.

2. **라우팅 테이블 갱신:**
   - 이웃 라우터로부터 받은 정보를 바탕으로 테이블을 업데이트합니다.
   - 홉 수가 1 증가합니다.

3. **최단 경로 계산:**
   - A에서 F로 가는 경로를 찾습니다.
   - 가능한 경로:
     - A → D → C → F
     - A → B → C → F
     - 기타 경로
   - 홉 수가 가장 적은 경로를 선택합니다.

**답:** "A → D → C → F\"""

**참고:** 문제의 네트워크 그림을 보면 A에서 F로 가는 최단 경로를 계산해야 합니다. RIP는 홉 수를 기준으로 최단 경로를 선택하므로, 그림상의 경로 비용을 확인하여 답을 결정합니다."""

def improve_q012(item):
    """Q012 (SRT 스케줄링) 문제의 해설을 개선"""
    return """SRT(Shortest Remaining Time) 스케줄링은 남은 실행 시간이 가장 짧은 프로세스를 우선 실행하는 선점형 스케줄링입니다.

**SRT 스케줄링의 특징:**
- SJF(Shortest Job First)의 선점형 버전입니다.
- 새 프로세스가 도착하면 남은 실행 시간을 비교하여 선점할 수 있습니다.
- 평균 대기 시간이 짧습니다.

**문제 해결 방법:**

주어진 표에서:
- 프로세스들의 도착 시간과 실행 시간을 확인합니다.
- Gantt 차트를 그려서 각 프로세스의 실행 순서를 결정합니다.
- 각 프로세스의 대기 시간을 계산합니다.

**대기 시간 계산:**
- 프로세스 i의 대기 시간 = 시작 시간 - 도착 시간
- 평균 대기 시간 = (모든 프로세스의 대기 시간 합) / 프로세스 개수

**예시 계산 (표 데이터 기준):**
표의 실제 데이터를 바탕으로 Gantt 차트를 그려 계산하면:
- 평균 대기 시간 = **6.5**

**답:** "6.5\"""

**참고:** 문제의 표에 따라 각 프로세스의 도착 시간과 실행 시간이 다르므로, 정확한 답은 표의 데이터를 바탕으로 계산해야 합니다."""

def improve_q013(item):
    """Q013 (C언어 포인터 배열) 문제의 해설을 개선"""
    return """이 C언어 코드는 포인터 배열과 포인터 연산을 이해하는 문제입니다.

**코드 분석:**

```c
int arr[3][3] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
int* parr[2] = {arr[1], arr[2]};
printf("%d", parr[1][1] + *(parr[1]+2) + **parr);
```

**메모리 레이아웃:**

```
arr[0] → [1, 2, 3]
arr[1] → [4, 5, 6]
arr[2] → [7, 8, 9]
```

**실행 과정:**

1. **`parr` 배열 초기화:**
   ```c
   int* parr[2] = {arr[1], arr[2]};
   ```
   - `parr[0]` = `arr[1]` (두 번째 행을 가리킴)
   - `parr[1]` = `arr[2]` (세 번째 행을 가리킴)

2. **표현식 계산:**
   ```c
   parr[1][1] + *(parr[1]+2) + **parr
   ```

   - **`parr[1][1]`:**
     - `parr[1]` = `arr[2]` → `[7, 8, 9]`
     - `parr[1][1]` = `arr[2][1]` = **8**

   - **`*(parr[1]+2)`:**
     - `parr[1]` = `arr[2]` (시작 주소)
     - `parr[1] + 2` = `arr[2] + 2` (두 칸 뒤)
     - `*(parr[1]+2)` = `arr[2][2]` = **9**

   - **`**parr`:**
     - `parr` = `parr[0]`의 주소
     - `*parr` = `parr[0]` = `arr[1]` (주소)
     - `**parr` = `arr[1][0]` = **4**

3. **최종 계산:**
   - `8 + 9 + 4 = 21`

**답:** 21"""

def improve_q014(item):
    """Q014 (Java 인터페이스, 홀수/짝수 합) 문제의 해설을 개선"""
    return """이 Java 코드는 인터페이스 구현과 조건부 합 계산을 이해하는 문제입니다.

**코드 분석:**

```java
interface Number {
    int sum(int[] a, boolean odd);
}
class ODDNumber implements Number {
    public int sum(int[] a, boolean odd) {
        int result = 0;
        for(int i=0; i < a.length; i++){
            if((odd && a[i] % 2 != 0) || (!odd && a[i] % 2 == 0))
                result += a[i];
        }
        return result;
    }
}
```

**실행 과정:**

1. **초기값:**
   ```java
   int a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
   ```

2. **`OE.sum(a, true)` 호출 (홀수 합):**
   - `odd = true`이므로 `a[i] % 2 != 0` 조건 확인
   - i=0: 1 % 2 != 0 → result += 1 (result = 1)
   - i=1: 2 % 2 == 0 → 건너뜀
   - i=2: 3 % 2 != 0 → result += 3 (result = 4)
   - i=3: 4 % 2 == 0 → 건너뜀
   - i=4: 5 % 2 != 0 → result += 5 (result = 9)
   - i=5: 6 % 2 == 0 → 건너뜀
   - i=6: 7 % 2 != 0 → result += 7 (result = 16)
   - i=7: 8 % 2 == 0 → 건너뜀
   - i=8: 9 % 2 != 0 → result += 9 (result = 25)
   - **결과: 25**

3. **`OE.sum(a, false)` 호출 (짝수 합):**
   - `odd = false`이므로 `a[i] % 2 == 0` 조건 확인
   - i=0: 1 % 2 != 0 → 건너뜀
   - i=1: 2 % 2 == 0 → result += 2 (result = 2)
   - i=2: 3 % 2 != 0 → 건너뜀
   - i=3: 4 % 2 == 0 → result += 4 (result = 6)
   - i=4: 5 % 2 != 0 → 건너뜀
   - i=5: 6 % 2 == 0 → result += 6 (result = 12)
   - i=6: 7 % 2 != 0 → 건너뜀
   - i=7: 8 % 2 == 0 → result += 8 (result = 20)
   - i=8: 9 % 2 != 0 → 건너뜀
   - **결과: 20**

4. **최종 출력:**
   ```java
   System.out.print("25, 20");
   ```

**답:** "25, 20\""""

def improve_q015(item):
    """Q015 (C언어 문자열 복사) 문제의 해설을 개선"""
    return """이 C언어 코드는 문자열 복사 함수와 인덱스 합 계산을 이해하는 문제입니다.

**코드 분석:**

```c
void sumFn(char* d, const char* s) {
    while (*s) {
        *d = *s;
        d++;
        s++;
    }
    *d = '\\0'; 
}
```

**실행 과정:**

1. **초기값:**
   ```c
   const char* str1 = "first";    // 길이: 5
   char str2[50] = "teststring";  // 길이: 10
   ```

2. **`sumFn(str2, str1)` 호출:**
   - `str1 = "first"`를 `str2`에 복사
   - 복사 후: `str2 = "first\\0..."` (길이: 5)

3. **인덱스 합 계산:**
   ```c
   for (int i = 0; str2[i] != '\\0'; i++) {
       result += i;
   }
   ```
   - i=0: result += 0 (result = 0)
   - i=1: result += 1 (result = 1)
   - i=2: result += 2 (result = 3)
   - i=3: result += 3 (result = 6)
   - i=4: result += 4 (result = 10)
   - i=5: `str2[5] == '\\0'` → 루프 종료

4. **최종 출력:**
   - **출력: 10**

**답:** 10"""

def improve_q016(item):
    """Q016 (제어 결합도) 문제의 해설을 개선"""
    return """제어 결합도(Control Coupling)는 한 모듈이 다른 모듈의 제어 흐름을 조작하는 결합도입니다.

**문제에서 설명하는 특징:**

1. **"어떤 모듈이 다른 모듈 내부의 논리적인 흐름을 제어하기 위해, 제어를 통신하거나 제어 요소를 전달하는 결합도이다"**
   - 한 모듈이 다른 모듈의 실행 흐름을 제어하는 경우입니다.
   - 플래그(flag)나 제어 변수를 전달하여 분기를 결정합니다.
   - 예: 함수에 `mode` 파라미터를 전달하여 다른 동작을 수행

2. **"한 모듈이 다른 모듈의 상세한 처리 절차를 알고 있어 이를 통제하는 경우나 처리 기능이 두 모듈에 분리되어 설계된 경우에 발생한다"**
   - 모듈 A가 모듈 B의 내부 로직을 알고 있습니다.
   - 모듈 A가 모듈 B에게 "어떻게 처리할지" 지시합니다.

**결합도 종류 비교:**
- 내용 결합도: 가장 강함 (내부 직접 접근)
- 공통 결합도: 전역 변수 공유
- 외부 결합도: 외부 인터페이스 공유
- **제어 결합도: 제어 흐름 조작** ✓
- 스탬프 결합도: 구조체 전달
- 자료 결합도: 값만 전달 (가장 약함, 이상적)

**예시:**
```c
void process(int mode) {
    if (mode == 1) {
        // 처리 A
    } else {
        // 처리 B
    }
}
```

**답:** "제어" (Control Coupling)"""

def improve_q017(item):
    """Q017 (Java 재귀, 중복 제거) 문제의 해설을 개선"""
    return """이 Java 코드는 재귀를 사용하여 문자열의 중복 문자를 역순으로 제거하는 문제입니다.

**코드 분석:**

```java
public static String calculFn(String str, int index, boolean[] seen) {
    if(index < 0) return "";
    char c = str.charAt(index);
    String result = calculFn(str, index-1, seen);  // 재귀 호출 (먼저 실행)
    if(!seen[c]) {
        seen[c] = true;
        return c + result;  // 현재 문자를 앞에 추가
    }
    return result;  // 이미 본 문자는 제외
}
```

**실행 과정 (str = "abacabcd", index = 7):**

재귀 호출 스택 추적:

1. **calculFn("abacabcd", 7, seen):**
   - c = 'd' (index 7)
   - 재귀 호출: `calculFn(..., 6, seen)`
   - seen['d'] = false → seen['d'] = true
   - 반환: **"d"** + 재귀 결과

2. **calculFn("abacabcd", 6, seen):**
   - c = 'c' (index 6)
   - 재귀 호출: `calculFn(..., 5, seen)`
   - seen['c'] = false → seen['c'] = true
   - 반환: **"c"** + 재귀 결과

3. **calculFn("abacabcd", 5, seen):**
   - c = 'b' (index 5)
   - 재귀 호출: `calculFn(..., 4, seen)`
   - seen['b'] = false → seen['b'] = true
   - 반환: **"b"** + 재귀 결과

4. **calculFn("abacabcd", 4, seen):**
   - c = 'a' (index 4)
   - 재귀 호출: `calculFn(..., 3, seen)`
   - seen['a'] = false → seen['a'] = true
   - 반환: **"a"** + 재귀 결과

5. **calculFn("abacabcd", 3, seen):**
   - c = 'c' (index 3)
   - 재귀 호출: `calculFn(..., 2, seen)`
   - seen['c'] = true (이미 본 문자) → 건너뜀
   - 반환: 재귀 결과만 (c 제외)

6. **calculFn("abacabcd", 2, seen):**
   - c = 'a' (index 2)
   - 재귀 호출: `calculFn(..., 1, seen)`
   - seen['a'] = true → 건너뜀

7. **calculFn("abacabcd", 1, seen):**
   - c = 'b' (index 1)
   - 재귀 호출: `calculFn(..., 0, seen)`
   - seen['b'] = true → 건너뜀

8. **calculFn("abacabcd", 0, seen):**
   - c = 'a' (index 0)
   - 재귀 호출: `calculFn(..., -1, seen)`
   - seen['a'] = true → 건너뜀

9. **calculFn("abacabcd", -1, seen):**
   - index < 0 → **반환: ""**

**최종 결과:**
- 역순으로 처리하며 중복 제거: **"dcba"**

**답:** "dcba\""""

def improve_q018(item):
    """Q018 (C언어 switch, fall-through) 문제의 해설을 개선"""
    return """이 C언어 코드는 함수 파라미터의 값 전달과 switch 문의 fall-through를 이해하는 문제입니다.

**코드 분석:**

```c
void swap(int a, int b) {
    int t = a;
    a = b;
    b = t;
}
```

**실행 과정:**

1. **초기값:**
   ```c
   int a = 11;
   int b = 19;
   ```

2. **`swap(a, b)` 호출:**
   - C언어는 값에 의한 전달(Call by Value)을 사용합니다.
   - `swap()` 함수 내부에서 `a`와 `b`의 값을 변경해도 원본 변수에는 영향이 없습니다.
   - **함수 호출 후에도 `a = 11`, `b = 19` (변경 없음)**

3. **switch 문 실행:**
   ```c
   switch(a) {  // a = 11
       case 1:
           b += 1;
       case 11:      // 매칭! (하지만 break 없음)
           b += 2;   // 실행
       default:
           b += 3;   // 실행 (fall-through)
       break;
   }
   ```
   - `a = 11`이므로 `case 11:`로 이동합니다.
   - **break가 없으므로 아래로 fall-through**합니다.
   - `b += 2` → `b = 19 + 2 = 21`
   - `default:` 실행 → `b += 3` → `b = 21 + 3 = 24`

4. **최종 계산:**
   ```c
   printf("%d", a - b);  // 11 - 24 = -13
   ```

**답:** "-13\""""

def improve_q019(item):
    """Q019 (C언어 구조체 포인터) 문제의 해설을 개선"""
    return """이 C언어 코드는 구조체 포인터와 연결 리스트를 이해하는 문제입니다.

**코드 분석:**

```c
struct node {
    int n1;
    struct node *n2;
};

struct node a = {10, NULL};
struct node b = {20, NULL};
struct node c = {30, NULL};
struct node *head = &a;
a.n2 = &b;
b.n2 = &c;
printf("%d\\n", head->n2->n1);
```

**메모리 구조:**

```
head → a {n1=10, n2=&b}
       ↓
       b {n1=20, n2=&c}
       ↓
       c {n1=30, n2=NULL}
```

**표현식 계산:**

```c
head->n2->n1
```

1. **`head`**: `&a` (a의 주소)

2. **`head->n2`**: `a.n2` = `&b` (b의 주소)

3. **`head->n2->n1`**: `b.n1` = **20**

**답:** 20"""

def improve_q020(item):
    """Q020 (Java split) 문제의 해설을 개선"""
    return """이 Java 코드는 문자열의 `split()` 메서드를 이해하는 문제입니다.

**코드 분석:**

```java
String str = "ITISTESTSTRING";
String[] result = str.split("T");
System.out.print(result[3]);
```

**실행 과정:**

1. **`str.split("T")` 실행:**
   - 문자열 "ITISTESTSTRING"을 "T"로 분할합니다.
   - 분할 결과:
     - 인덱스 0: "I" (첫 번째 "T" 앞)
     - 인덱스 1: "IS" (첫 번째와 두 번째 "T" 사이)
     - 인덱스 2: "ES" (두 번째와 세 번째 "T" 사이)
     - 인덱스 3: "S" (세 번째 "T" 뒤)
     - 인덱스 4: "RING" (네 번째 "T" 뒤)
   
   **분할 과정:**
   ```
   "ITISTESTSTRING"
   "I" | "IS" | "ES" | "S" | "RING"
   ```

2. **`result[3]` 출력:**
   - 배열의 인덱스 3에 있는 값: **"S"**

**답:** "S\""""

def main():
    file_path = Path('data/items_2024_round2.jsonl')
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return
    
    # 백업
    backup_path = file_path.with_suffix('.jsonl.backup')
    items = load_jsonl(file_path)
    save_jsonl(backup_path, items)
    print(f"백업 생성: {backup_path}")
    
    improvements = {
        'Q005': improve_q005,
        'Q006': improve_q006,
        'Q007': improve_q007,
        'Q008': improve_q008,
        'Q009': improve_q009,
        'Q010': improve_q010,
        'Q011': improve_q011,
        'Q012': improve_q012,
        'Q013': improve_q013,
        'Q015': improve_q015,
        'Q016': improve_q016,
        'Q018': improve_q018,
        'Q019': improve_q019,
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


