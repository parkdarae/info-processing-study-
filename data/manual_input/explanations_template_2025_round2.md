# 2025년 2회 해설 작성

총 18개 문제의 해설 작성이 필요합니다.

---

## Q001

**문제**:
```
다음은 파일 구조와 관련된 설명이다.
설명을 읽고 괄호 안에 들어갈 가장 알맞은 용어를 작성하시오
.
데이터베이스의 물리 설계 시
,
레코드에 접근하는 방법은 순차 접근 방법
, [
]
방법
,
해싱 방법 등이 있다
.
이 중
[
]
방법은 레코드의 키 값과 포인터를 쌍으로 묶어 저장하며 검색 시 키 값을 기준으로 빠르게 탐색할 수 있도록 설계되어 있다
.
이 방식은 검색 속도가 빠르며
<
키 값
,
포인터
>
쌍으로 구성된 자료 구조를 사용하여 해당 키가 가리키는 주소를 통해 원하는 레코드를 직접 찾을 수 있다
.
```

**답안**:
```
인덱스
```

**현재 해설**: 색인(Index) 접근 방법

**상태**: ⚠️ 부족 (부족)

**이미지**: images/2025_round2/Q001.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q002

**문제**:
```
다음은 데이터베이스 릴레이션의 구성 요소 중 하나에 대한 설명이다.
설명을 읽고 보기에서 알맞은 기호를 골라 작성하시오
.
릴레이션
(Relation)
에서 열
(Column)
을 의미하며 데이터 항목의 속성
(Attribute)
또는 특성을 나타낸다
.
각 열은 고유한 이름을 가지며 특정 도메인
(Domain)
에서 정의된 값을 갖는다
.
예를 들어
"
학생
"
릴레이션에서 학번
,
이름
,
전공 등은 각각 하나의 열이며 이 열들은 학생의 고유한 속성을 나타낸다
.
이 개념은 파일 구조에서의 필드
(Field)
에 해당하며 릴레이션에서 행
(Row, Tuple)
의 구성 요소가 된다
.
ㄱ
. Cardinality
ㄷ
. Attribute
```

**답안**:
```
ㄷ
```

**현재 해설**: Attribute

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q003

**문제**:
```
다음은 정보보안 관련 문제이다.
아래 내용을 보고

 알맞는 단어를 작성하시오.
원격 접속과 관련된 보안 프로토콜이며 암호화된 통신을 제공하는 보안 접속용 프로토콜이다
.
공개키 기반의 인증 방식을 사용하며 암호화된 데이터 전송을 지원한다
.
주로 원격 서버에 안전하게 접속할 때 사용되며 기본 포트 번호는
22
번이다
.
Telnet 의 보안 취약점을 보완한 대안으로 널리 사용된다
.
```

**답안**:
```
SSH
```

**현재 해설**: Secure Shell

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q005

**문제**:
```
다음은 Java의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
BB
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q005.png

**코드 언어**: java

**코드**:
```java
public class Main {
    public static void change(String[] data, String s){
        data[0] = s;
        s = "Z";
    }
    public static void main(String[] args) {
        String data[] = { "A" };
        String s = "B";
        change(data, s);
        System.out.print(data[0] + s);
    }
}
```

**테이블**: table1

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q006

**문제**:
```
다음은 IP
주소와 서브넷 마스크에 관한 문제이다.
주어진 정보를 참고하여

 괄호 안에 들어갈 알맞은 값을 쓰시오
.
호스트의 IP
주소가
223.13.234.132
이고 서브넷 마스크가
255.255.255.192
일 때 다음 물음에 답하시오
.
이 호스트가 속한 네트워크 주소는
223.13.234.(

①
)
이다
.
이 네트워크에서 사용 가능한 호스트 수는
(
②
)
개이다
.
(
단
,
네트워크 주소와 브로드캐스트 주소는 제외한다
.)
```

**답안**:
```
① 128
② 62
```

**현재 해설**: 네트워크 주소와 호스트 수

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q007

**문제**:
```
다음은 디자인 패턴에 관한 문제이다.
아래 내용을 보고

 알맞는 단어를 작성하시오.
어떤 객체에 대한 접근을 제어하거나 추가적인 기능을 부여하기 위해 해당 객체의 대리 객체를 사용하는 방식의 디자인 패턴이다
.
실제 객체에 대한 접근 전에 필요한 작업을 수행할 수 있으며 실제 객체의 생성을 지연시켜 메모리와 자원을 절약할 수 있 다
.
또한
,
실제 객체를 감추어 정보은닉을 강화할 수 있다는 장점이 있다
.
```

**답안**:
```
Proxy
```

**현재 해설**: Proxy 패턴

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q009

**문제**:
```
다음은 Java언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
19
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q009.png

**코드 언어**: java

**코드**:
```java
public class Main {
    static interface F {
        int apply(int x) throws Exception;
    }
    public static int run(F f) {
        try {
            return f.apply(3);
        } catch (Exception e) {
            return 7;
        }
    }
    public static void main(String[] args) {
        F f = (x) -> {
            if (x > 2) {
                throw new Exception();
            }
            return x * 2;
        };
        System.out.print(run(f) + run((int n) -> n + 9));
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q010

**문제**:
```
다음은 Java언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
5P
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q010.png

**코드 언어**: java

**코드**:
```java
public class Main{
    public static class Parent {
        public int x(int i) { return i + 2; }
        public static String id() { return "P";}
    }
    public static class Child extends Parent {
        public int x(int i) { return i + 3; }
        public String x(String s) { return s + "R"; }
        public static String id() { return "C"; }
    }
    public static void main(String[] args) {
        Parent ref = new Child();
        System.out.println(ref.x(2) + ref.id());
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q011

**문제**:
```
다음 아래 제어 흐름 그래프가 분기 커버리지를 만족하기 위한 테스팅 순서를 쓰시오.
```

**답안**:
```
1234561
124567
```

**현재 해설**: 분기 커버리지

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q011.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q012

**문제**:
```
다음은 C언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
2 그리고 3
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q012.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
#define SIZE 3
typedef struct {
    int a[SIZE];
    int front;
    int rear;
} Queue;
void enq(Queue* q, int val){
    q->a[q->rear] = val; 
    q->rear = (q->rear + 1) % SIZE;
}
int deq(Queue* q) {
    int val = q->a[q->front];
    q->front = (q->front + 1) % SIZE;
    return val;
}
int main() {
    Queue q = {{0}, 0, 0};
    enq(&q,1); enq(&q,2); deq(&q); enq(&q, 3);
    int first = deq(&q);
    int second = deq(&q);
    printf("%d 그리고 %d", first, second);
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q013

**문제**:
```
라운드로빈(RR) 방식을 이용하고 아래 내용을 참고하여

 평균대기시간을 구하시오.
운영체제에서 라운드로빈
(Round Robin, RR)
스케줄링은 각 프로세스에 동일한 시간 할당량
(
타임 퀀텀
)
을 순차적으로 부여하며 CPU
를 할당하는 방식이다
.
다음은
4
개의 프로세스가 서로 다른 시간에 도착하며 각기 다른 실행 시간을 가지는 상황이다.
이때 시간 할당량은
4ms 이고 컨텍스트 스위칭 시간은 무시한다고 가정한다
.
아래 정보를 바탕으로 라운드로빈
(RR)
방식으로 CPU
스케줄링을 수행할 경우 모든 프로세스의 평균 대기시간
(Average Waiting Time)
은 얼마인가
?
```

**답안**:
```
11.75
```

**현재 해설**: 라운드로빈 평균 대기시간

**상태**: ⚠️ 부족 (부족)

**이미지**: images/2025_round2/Q013.png

**테이블**: table1

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q014

**문제**:
```
다음은 C언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
5 그리고 6
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q014.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
struct dat {
    int x;
    int y;
};
int main() {
    struct dat a[] = {{1, 2}, {3, 4}, {5, 6}};
    struct dat* ptr = a;
    struct dat** pptr = &ptr;
    (*pptr)[1] = (*pptr)[2];
    printf("%d 그리고 %d", a[1].x, a[1].y);
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q015

**문제**:
```
다음은 Java언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
1a3b3
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q015.png

**코드 언어**: java

**코드**:
```java
public class Main{
    public static class BO {
        public int v;
        public BO(int v) {
            this.v = v;
        }
    }
    public static void main(String[] args) {
        BO a = new BO(1);
        BO b = new BO(2);
        BO c = new BO(3);
        BO[] arr = {a, b, c};
        BO t = arr[0];
        arr[0] = arr[2];
        arr[2] = t;
        arr[1].v = arr[0].v;
        System.out.println(a.v + "a" + b.v + "b" + c.v);
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q016

**문제**:
```
다음은 C언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
3 1 2
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/q016.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
#include <stdlib.h>
struct node {
    int p;
    struct node* n;
};
int main() {
    struct node a = {1, NULL};
    struct node b = {2, NULL};
    struct node c = {3, NULL};
    a.n = &b; b.n = &c; c.n = NULL;
    c.n = &a; a.n = &b; b.n = NULL;
    struct node* head = &c;
    printf("%d %d %d", head->p, head->n->p, head->n->n->p);
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q017

**문제**:
```
다음은 Pyhon언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
2
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/q017.png

**코드 언어**: python

**코드**:
```python
lst = [1,2,3]
dst = {i : i* 2 for i in lst}
s = set(dst.values())
lst[0] = 99 
dst[2]=7
s.add(99)
print(len(s & set(dst.values())))
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q018

**문제**:
```
다음은 C언어의 문제이다.
아래 코드를 보고

 알맞는 출력값을 작성하시오.
```

**답안**:
```
TSEB
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/q018.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
#include <stdlib.h>
struct node {
    char c;
    struct node* p;
};
struct node* func(char* s) {
    struct node* h = NULL, *n;
    while(*s) {
        n = malloc(sizeof(struct node));
        n->c = *s++;
        n->p = h;
        h = n;
    }
    return h;
}
int main() {
    struct node* n = func("BEST");
    while(n) {
        putchar(n->c);
        struct node* t = n;
        n = n->p;
        free(t);
    }
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q019

**문제**:
```
다음은 TCP
통신 과정에서 발생할 수 있는 보안 취약점에 대한 설명이다.
이를 이용한 공격 기법으로 옳은 것은
?
TCP 는 연결을 수립하기 위해 클라이언트가 서버에 SYN
패킷을 보내고 서버는 SYN-ACK 패킷으로 응답한 후 클라이언트가 다시 ACK
패킷을 보내는
3-way-handshake 과정을 거친다
.
이때 공격자는 클라이언트 역할로 수많은 SYN
패킷을 서버에 전송한 뒤 마지막 ACK
를 고의로 보내지 않아 서버가 연결 대기 상태를 계속 유지하게 만든다
.
이로 인해 서버의 연결 대기 큐가 가득 차면서 정상적인 접속 요청을 처리하지 못하게 되어 서비스 거부 상태가 발생한다
.
```

**답안**:
```
SYN Flooding
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q020

**문제**:
```
다음 테이블에서 πTTL(employee)에 대한 연산 결과 값을 작성하시오.
[employee테이블]
```

**답안**:
```
TTL
부장
대리
과장
차장
```

**현재 해설**: 프로젝션 연산

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round2/Q020.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

