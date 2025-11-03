# 2025년 1회 해설 작성

총 19개 문제의 해설 작성이 필요합니다.

---

## Q001

**문제**:
```
다음은 네트워크 보완에 관련된 문제이다.
괄호안에 알맞는 용어를 작성하시오.
(   )은/는 '세션을 가로채다.' 라는 의미로 다른 사람의 세션 상태를 훔치거나 도용하여 액세스하는 해킹 기법이다.
TCP (   )은/는 TCP의 3-way 핸드셰이크가 완료된 후에 공격자가 시퀀스 번호 등을 조작하여 정상적인 세션을 가로채고 인증 없이 통신을 탈취하는 공격 공격이다.
```

**답안**:
```
세션 하이재킹
```

**현재 해설**: Session Hijacking

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q002

**문제**:
```
다음은 제약조건과 관련된 문제이다.
괄호안에 알맞는 용어를 보기에 골라 작성하시오.
개체, 참조, 도메인
```

**답안**:
```
ㄱ. 도메인
ㄴ. 개체
ㄷ. 참조
```

**현재 해설**: 제약조건

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q002.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q003

**문제**:
```
아래의 내용에서 설명 글의 괄호안의 용어를 영문 약자로 작성하시오.
(        ) 은/는 3글자의 영어 약자로 이루어진 오류 기법으로 데이터를 전송하거나 저장할 때 데이터의 오류를 감지하는 데 사용되는 오류 검출 코드이다.
(        ) 은/는 데이터에 체크섬을 추가하여 데이터를 전송하거나 저장한 후, 수신 또는 읽을 때 이 체크섬을 다시 계산하여 데이터가 변경되었는지 확인하는 기법이다.
(        ) 은/는 데이터 전송의 안정성을 높이는 데 중요한 역할을 한다.
데이터는 이진수(0과 1)로 표현되며 정해진 다항식(x³ + x + 1)을 기반으로 데이터를 2진수 나눗셈하고나머지를 (       ) 값으로 삼는다.
```

**답안**:
```
CRC
```

**현재 해설**: Cyclic Redundancy Check

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q004

**문제**:
```
다음은 악성코드 관련된 문제이다.
아래 내용을 확인하여

 보기에 골라 작성하시오.
사용자가 원치 않는 소프트웨어를 구매하도록 조작하기 위해 사회 공학을 사용하여 충격, 불안 또는 위협에 대한 인식을 유발하는 악성 소프트웨어의 한 형태이다.
‘겁을 주다’라는 영어 단어에서 유래한 것으로 공포를 이용하여 피해자를 속여 대가를 지불 하거나 특정 행동을 유도하는 랜섬웨어이다.
가짜 바이러스 경고나 시스템 문제를 표시하여 사용자가 돈을 지불하거나 특정 소프트웨어를 설치하도록 속이는 방식으로 작동한다.

[보기]

ㄱ. 컴포넌트 웨어

ㄴ. 유즈웨어

ㄷ. 셔블웨어

ㄹ. 스캐어 웨어

ㅁ. 안티 스파이 웨어

ㅂ. 네트웨어

ㅅ. 그룹웨어

ㅇ. 애드웨어
```

**답안**:
```
ㄹ
```

**현재 해설**: 스캐어 웨어 (Scareware)

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q005

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
출력1출력5
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q005.png

**코드 언어**: java

**코드**:
```java
public class Main {
  public static void main(String[] args) {
    int a=5,b=0;
    try{
      System.out.print(a/b);
    }catch(ArithmeticException e){
      System.out.print("출력1");
    }catch(ArrayIndexOutOfBoundsException e) {
      System.out.print("출력2");
    }catch(NumberFormatException e) {
      System.out.print("출력3");
    }catch(Exception e){
      System.out.print("출력4");
    }finally{
      System.out.print("출력5");
    }
  }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q006

**문제**:
```
아래 내용은 ARP/RARP에 대한 설명이다. 각 설명에 해당하는 것을 작성하시오.

(1) 은/는 네트워크상에서 IP 주소를 MAC 주소로 변환하는 프로토콜이고,
( 2 ) 은/는 MAC 주소를 IP 주소로 변환하는 프로토콜이다.
```

**답안**:
```
(1) ARP
(2) RARP
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q007

**문제**:
```
다음은 SQL 문제이다.
아래 두 테이블을 참고하여

 보기에 쿼리 실행 결과를 작성하시오.
SELECT name, incentive FROM emp, sal WHERE emp.id = sal.id and incentives >= 500
```

**답안**:
```
이순신
1000
```

**현재 해설**: SQL JOIN 결과

**상태**: ⚠️ 부족 (부족)

**이미지**: images/2025_round1/Q007.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q009

**문제**:
```
IP 주소가 192.168.35.10, 서브넷 255.255.252.0인 PC에서 브로드캐스팅으로 다른 IP로 정보를 전달한다고 할 때 수신할 수 있는 알맞는 IP를 보기에서 골라 모두 작성하시오.

[보기]

ㄱ. 192.168.34.1

ㄴ. 192.168.32.19

ㄷ. 192.168.35.200

ㄹ. 192.168.33.138

ㅁ. 192.168.35.50
```

**답안**:
```
ㄱ,ㄴ,ㄷ,ㄹ,ㅁ
```

**현재 해설**: 서브넷 브로드캐스팅

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q010

**문제**:
```
다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
4
BACDE
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q010.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
char Data[5] = {'B', 'A', 'D', 'E'};
char c;
int main(){
    int i, temp, temp2;
    c = 'C';
    printf("%d\n", Data[3]-Data[1]);
    for(i=0;i<5;++i){
        if(Data[i]>c)
            break;
    }
    temp = Data[i];
    Data[i] = c;
    i++;
    for(;i<5;++i){
        temp2 = Data[i];
        Data[i] = temp;
        temp = temp2;
    }
    for(i=0;i<5;i++){
        printf("%c", Data[i]);
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q011

**문제**:
```
다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
13
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q011.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
#include <stdlib.h>
void set(int** arr, int* data, int rows, int cols) {
    for (int i = 0; i < rows * cols; ++i) {
        arr[((i + 1) / rows) % rows][(i + 1) % cols] = data[i];
    }
}
int main() {
    int rows = 3, cols = 3, sum = 0;
    int data[] = {5, 2, 7, 4, 1, 8, 3, 6, 9}; 
    int** arr;
    arr = (int**) malloc(sizeof(int*) * rows);
    for (int i = 0; i < cols; i++) {
        arr[i] = (int*) malloc(sizeof(int) * cols);
    }
    set(arr, data, rows, cols);
    for (int i = 0; i < rows * cols; i++) {
        sum += arr[i / rows][i % cols] * (i % 2 == 0 ? 1 : -1);
    }
    for(int i=0; i<rows; i++) {
        free(arr[i]);
    }
    free(arr);
    printf("%d", sum);
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q012

**문제**:
```
다음은 결합도와 관련된 내용이다.
보기에 알맞는 답을 골라 작성하시오.

(1) 다른 모듈 내부에 있는 변수나 기능을 다른 모듈에서 사용하는 경우의 결합도
(2) 모듈 간의 인터페이스로 배열이나 오브젝트, 자료구조 등이 전달되는 경우의 결합도
(3) 파라미터가 아닌 모듈 밖에 선언되어 있는 전역 변수를 참조하고 전역 변수를 갱신하는 식으로 상호작용하는 경우의 결합도

[보기]

ㄱ. 자료 결합도

ㄴ. 스탬프 결합도

ㄷ. 제어 결합도

ㄹ. 공통 결합도

ㅁ. 내용 결합도

ㅂ. 외부 결합도
```

**답안**:
```
(1) ㅁ
(2) ㄴ
(3) ㄹ
```

**현재 해설**: 내용 결합도, 스탬프 결합도, 공통 결합도

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q013

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
54
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q013.png

**코드 언어**: java

**코드**:
```java
public class Main {
    public static void main(String[] args) {
        new Child();
        System.out.println(Parent.total);
    }
}
class Parent {
    static int total = 0;
    int v = 1;
    public Parent() {
        total += (++v);
        show();    
    }
    public void show() {
        total += total;
    }
}
class Child extends Parent {
    int v = 10;
    public Child() {
        v += 2;
        total += v++;
        show();
    }
    @Override
    public void show() {
        total += total * 2;
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q014

**문제**:
```
아래는 디자인 패턴에 대한 설명이다.
알맞는 답을 보기에 골라 작성하시오.
서로 다른 인터페이스를 가진 클래스들을 연결해 사용 가능하게 한다.
기존 클래스(Adaptee)를 원하는 인터페이스(Target)에 맞게 변환하는 어댑터(Adapter)를 만든다.
기존 클래스를 감싸서(wrapper) 인터페이스를 변환해주는 역할을 한다.
```

**답안**:
```
Adapter
```

**현재 해설**: Adapter 패턴

**상태**: ⚠️ 부족 (부족)

**이미지**: images/2025_round1/Q014.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q015

**문제**:
```
문장(Statement) 커버리지 테스트를 수행하려고 한다. 코드를 아래의 제어 흐름도 빈칸에 연결되도록 작성하고 문장 커버리지 순서대로 작성하시오.
```

**답안**:
```
(1) int a = 0
(2) a < m || b[a] < x
(3) b[a] < 0
(4) b[a] = -b[a];
(5) a++;
(6) return 1;
(7) ③ → ④ → ⑤ → ② → ⑥
```

**현재 해설**: 문장 커버리지

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q015_1.png

**코드 언어**: unknown

**코드**:
```unknown
int Main(int b[], int m, int x) {
    int a = 0;
    while (a < m || b[a] < x) {
        if (b[a] < 0)
            b[a] = -b[a];
        a++;
    }
    return 1;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q001

**문제**:
```
(

①    )

2. (    ②    )

3. (    ③    )

4. (    ④    )    5. (    ⑤    )  6. (    ⑥    )
문장 커버리지 순서 1 → 2
→ (          ⑦           )
```

**답안**:
```
세션 하이재킹
```

**현재 해설**: Session Hijacking

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q016

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
20
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q016.png

**코드 언어**: java

**코드**:
```java
public class Main {
    public static void main(String[] args) {
        int[] data = {3, 5, 8, 12, 17};
        System.out.println(func(data, 0, data.length - 1));
    }
    static int func(int[] a, int st, int end) {
        if (st >= end) return 0;
        int mid = (st + end) / 2;
        return a[mid] + Math.max(func(a, st, mid), func(a, mid + 1, end));
    } 
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q017

**문제**:
```
다음은 파이썬에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
13
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**코드 언어**: python

**코드**:
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
def tree(li):
    nodes = [Node(i) for i in li]
    for i in range(1, len(li)):
        nodes[(i - 1) // 2].children.append(nodes[i])
    return nodes[0]
def calc(node, level=0):
    if node is None:
        return 0
    return (node.value if level % 2 == 1 else 0) + sum(calc(n, level + 1) for n in node.children)
li = [3, 5, 8, 12, 15, 18, 21]
root = tree(li)
print(calc(root))
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q018

**문제**:
```
다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
19.다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
35421
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q018.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>   
#include <stdlib.h>  
typedef struct Data {
    int value;
    struct Data *next;
} Data;
Data* insert(Data* head, int value) {
    Data* new_node = (Data*)malloc(sizeof(Data));
    new_node->value = value;
    new_node->next = head;
    return new_node;
}
Data* reconnect(Data* head, int value) {
    if (head == NULL || head->value == value) return head;
    Data *prev = NULL, *curr = head;
    while (curr != NULL && curr->value != value) {
        prev = curr;
        curr = curr->next;
    }
    if (curr != NULL && prev != NULL) {
        prev->next = curr->next;
        curr->next = head;
        head = curr;
    }
    return head;
}
int main() {
    Data *head = NULL, *curr;
    for (int i = 1; i <= 5; i++)
        head = insert(head, i);
    head = reconnect(head, 3);
    for (curr = head; curr != NULL; curr = curr->next)
        printf("%d", curr->value);
    return 0; 
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q020

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
4
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2025_round1/Q020.png

**코드 언어**: java

**코드**:
```java
public class Main {
  public static void main(String[] args) {
    System.out.println(calc("5"));
  }
  static int calc(int value) {
    if (value <= 1) return value;
    return calc(value - 1) + calc(value - 2);
  }
  static int calc(String str) {
    int value = Integer.valueOf(str);
    if (value <= 1) return value;
    return calc(value - 1) + calc(value - 3);
  }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

