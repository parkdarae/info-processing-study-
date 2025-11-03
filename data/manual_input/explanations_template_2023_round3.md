# 2023년 3회 해설 작성

총 20개 문제의 해설 작성이 필요합니다.

---

## Q001

**문제**:
```
다음은 Java 코드이다.
올바른 출력 결과를 작성하시오.
```

**답안**:
```
BDCDD
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/1.png

**코드 언어**: java

**코드**:
```java
public class main{
    public static void main(String[] args) {
        A b = new B();
        b.paint();
        b.draw();
    }
}
class A {
    public void paint() {
        System.out.print("A");
        draw();
    }
    public void draw() {
        System.out.print("B");
        draw();
    }
}
class B extends A {
    public void paint() {
        super.draw();
        System.out.print("C");
        this.draw();
    }
    public void draw() {
        System.out.print("D");
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q002

**문제**:
```
다음 설명하는 용어를 보기에 맞게 골라 기호를 작성하시오.
```

**답안**:
```
ㅇ
```

**현재 해설**: OAuth

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/2.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q003

**문제**:
```
리눅스(Linux)에서 사용자에게 읽기/쓰기/실행 권한을 부여하고, 그룹에게는 읽기/실행을 부여하고, 그 이외에는 실행 권한을 test.txt 파일에 부여하는 위한 명령어는 다음과 같다. 빈칸에 들어갈 답을 작성하시오.

 (8진법 사용)
(

(1)    ) (    (2)    ) test.txt
```

**답안**:
```
(1) chmod
(2) 751
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q004

**문제**:
```
다음은 C 언어 코드이다.
알맞는 출력 결과를 작성하시오.
```

**답안**:
```
34
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/4.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
int test(int n) {
    int i, sum = 0;
    for (i = 1; i <= n / 2; i++){
        if (n % i == 0)
        sum += i;
    }
    if (n == sum) 
        return 1;
    ​
    return 0;
}
int main(){
    int i, sum=0;
    for (i = 2; i <= 100; i++){ 
        if (test(i))
        sum += i;
    }
    printf("%d ", sum); 
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q005

**문제**:
```
C언어에서 구조체의 멤버에 접근하기 위해 괄호안의 기호를 작성하시오.
```

**답안**:
```
→
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/5.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
#include <stdlib.h>
typedef struct Data{
    char c;
    int *numPtr; 
} Data;
int main(){
    int num = 10;
    Data d1;    
    Data *d2 = malloc(sizeof(struct Data));
    d1.numPtr = &num;  
   d2 ( ) numPtr = &num; 
    printf("%d\n", *d1.numPtr); 
    printf("%d\n", *d2 ( ) numPtr);
    free(d2); 
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q006

**문제**:
```
다음 빈칸에 들어갈 UNION 연산의 결과값을 작성하시오.
```

**답안**:
```
4
3
2
1
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/6.png

**테이블**: table1, table2

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q007

**문제**:
```
다음 설명은 서버 접근 통제의 유형이다.
괄호 안에 들어갈 용어를 작성하시오.

 (영어 약자로 작성하시오.

)
```

**답안**:
```
(1) MAC
(2) RBAC
(3) DAC
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q008

**문제**:
```
다음 C언어 코드에 알맞는 출력값을 작성하시오.
```

**답안**:
```
5040
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/8.png

**코드 언어**: c

**코드**:
```c
#include
int f(int n) {
    if(n<=1) return 1;
    else return n*f(n-1);
}
int main() {
    printf("%d", f(7));
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q009

**문제**:
```
다음 설명에 대해 괄호 안에 알맞는 용어를 작성하시오.

 (영어 약자로 작성하시오.

)
```

**답안**:
```
ATM
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q010

**문제**:
```
다음은 C언어의 포인터 문제이다.
알맞는 출력값을 작성하시오.
```

**답안**:
```
KOREA
OREA
K
E
O
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/10.png

**코드 언어**: c

**코드**:
```c
#include
int main() {
    char* p = "KOREA";
    printf("%s\n", p);
    printf("%s\n", p+1);
    printf("%c\n", *p);
    printf("%c\n", *(p+3));
    printf("%c\n", *p+4);
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q011

**문제**:
```
다음은 Java 코드에 대한 알맞는 출력값을 작성하시오.
```

**답안**:
```
2
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/11.png

**코드 언어**: java

**코드**:
```java
class Parent {
    int compute(int num) {
        if(num <= 1)
            return num;
        return compute(num-1) + compute(num-2);
    }
}
class Child extends Parent {
    int compute(int num) {
        if(num <= 1)
            return num;
        return compute(num-1) + compute(num-3);
    }
}
public class main {
    public static void main(String args[]) {
        Parent obj = new Child();
        System.out.print(obj.compute(7));
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q012

**문제**:
```
IP 패킷에서 외부의 공인 IP주소와 포트 주소에 해당하는 내부 IP주소를 재기록하여 라우터를 통해 네트워크 트래픽을 주고받는 기술은 무엇인가?
```

**답안**:
```
NAT
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q013

**문제**:
```
다음 자바 코드를 실행할 경우 에러가 발생이 된다. 에러가 발생하는 라인명을 작성하시오.
```

**답안**:
```
7
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/13.png

**코드 언어**: java

**코드**:
```java
class Person {
    private String name;
    public Person(String val) {
        name = val;
    }
    public static String get() {
    return name;
    }
    public void print() {
        System.out.println(name);
    }
}
public class main {
    public static void main(String[] args) {
        Person obj = new Person("Kim");
        obj.print();
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q014

**문제**:
```
다음은 파이썬에 대한 문제이다.
밑줄친 부분에 알맞는 답을 작성하시오.
입력값은 2와 3이다.
파이썬 입력출에 대한 문제입니다.
2 3
2 + 3 = 5
```

**답안**:
```
split
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/14.png

**코드 언어**: python

**코드**:
```python
print("파이썬 입출력에 대한 문제입니다.")
num1, num2 = input()._____()
num1 = int(num1)
num2 = int(num2)
print(num1,num2)
num3 = num1 + num2
print(num1 + " + "  + num2 + " = " + num3)
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q015

**문제**:
```
다음은 판매와 관련된 다이어그램이다.
해당 다이어그램의 명칭을 쓰시오.
```

**답안**:
```
패키지
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/15.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q016

**문제**:
```
다음 설명에 알맞는 답을 보기에서 골라 작성하시오.
```

**답안**:
```
ㄱ
```

**현재 해설**: Equivalence Partitioning

**상태**: ⚠️ 부족 (부족)

**이미지**: images/2023_round3/16.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q017

**문제**:
```
다음은 클라우드에 대한 유형 문제이다.
괄호안에 알맞는 답을 보기에 골라 작성하시오.
```

**답안**:
```
(1) IaaS
(2) PaaS
(3) SaaS
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/17.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q018

**문제**:
```
다음은 프로토콜 종류에 관한 설명이다.
알맞는 답을 작성하시오.
```

**답안**:
```
RIP
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q019

**문제**:
```
다음은 관계 대수에 대한 내용이다.
보기에 알맞는 기호를 작성하시오.

1. join :

(1)

2. project :   (   2   )

3. select :   (   3   )

4. division :   (   4   )
```

**답안**:
```
(1) ㄷ
(2) ㄴ
(3) ㄱ
(4) ㄹ
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2023_round3/19.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q020

**문제**:
```
다음은 데이터베이스에 관련된 문제이다.
괄호 안에 알맞는 답을 작성하시오.
```

**답안**:
```
참조
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**테이블**: table1

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

