# 2024년 1회 해설 작성

총 23개 문제의 해설 작성이 필요합니다.

---

## Q001

**문제**:
```
다음 Java 코드에서 알맞는 출력 값을 작성하시오.
```

**답안**:
```
4
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q001.png

**코드 언어**: java

**코드**:
```java
class Connection {
    private static Connection _inst = null;
    private int count = 0;
    static public Connection get() {
        if(_inst == null) {
            _inst = new Connection();
            return _inst;
        }
        return _inst;
    }
    public void count() {
         count++; 
    }
    public int getCount() {
         return count; 
    }
}
public class main {  
    public static void main(String[] args) {
        Connection conn1 = Connection.get();
        conn1.count();
        Connection conn2 = Connection.get();
        conn2.count();
        Connection conn3 = Connection.get();
        conn3.count();
        conn1.count();
        System.out.print(conn1.getCount());
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q002

**문제**:
```
다음 C언어 코드에서 알맞는 출력 값을 작성하시오.
```

**답안**:
```
151
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q002.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
int main() {
    int v1 = 0, v2 = 35, v3 = 29;
    if(v1 > v2 ? v2 : v1) {
        v2 = v2 << 2;
    }else{
        v3 = v3 << 2;
    }
    printf("%d", v2+v3);
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q003

**문제**:
```
다음은 응집도와 관련해서 보기에서 응집도가 높은 순으로 나열하시오.
```

**답안**:
```
ㄱ
ㄴ
ㄹ
ㄷ
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
다음은 C언어에 대한 문제이다.
알맞는 출력 값을 작성하시오.
```

**답안**:
```
GECA
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q004.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
#include <string.h>
void reverse(char* str){
    int len = strlen(str);
    char temp;
    char*p1 = str;
    char*p2 = str + len - 1;
    while(p1<p2){
        temp = *p1;
        *p1 = *p2;
        *p2 = temp;
        p1++;
        p2--;
    }
}
int main(int argc, char* argv[]){
    char str[100] = "ABCDEFGH";
    reverse(str);
    int len = strlen(str);
    for(int i=1; i<len; i+=2){
        printf("%c",str[i]);
    }
    printf("\n");
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q005

**문제**:
```
아래 그림에서의 네트워크에서 라우터을 통한 할당 가능한
2번, 4번, 5번의 IP를 작성하시오.
1) 192.168.35.3/24
3) 129.200.10.16/22
6) 192.168.36.24/24
192.168.35.0
192.168.35.72
192.168.36.0
192.168.36.249
129.200.8.0
129.200.8.249
```

**답안**:
```
192.168.35.72
129.200.8.249
192.168.36.249
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q005.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q006

**문제**:
```
아래 표에서 나타나고 있는 정규형을 작성하시오.
```

**답안**:
```
제 3정규형
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q006.png

**테이블**: table1

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q007

**문제**:
```
아래의 내용에서 설명하는 네트워크 용어를 영문 약자로 작성하시오.
```

**답안**:
```
OSPF
```

**현재 해설**: Open Shortest Path First

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q001

**문제**:
```
대표적인 링크 상태 라우팅 프로토콜이다. 이것은 인터넷에서 연결된 링크의 상태를 감시하여 최적의 경로를 선택한다는것이다.

2. 단일 자율 시스템 내에서 라우팅 정보를 배포하는 데 사용되는 내부 게이트웨이 프로토콜이다.

3. 모든 대상에 도달하기 위한 최단 경로를 구축하고 계산하며 최단 경로는 Dijkstra 알고리즘을 사용하여 계산된다.
```

**답안**:
```
4
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q001.png

**코드 언어**: java

**코드**:
```java
class Connection {
    private static Connection _inst = null;
    private int count = 0;
    static public Connection get() {
        if(_inst == null) {
            _inst = new Connection();
            return _inst;
        }
        return _inst;
    }
    public void count() {
         count++; 
    }
    public int getCount() {
         return count; 
    }
}
public class main {  
    public static void main(String[] args) {
        Connection conn1 = Connection.get();
        conn1.count();
        Connection conn2 = Connection.get();
        conn2.count();
        Connection conn3 = Connection.get();
        conn3.count();
        conn1.count();
        System.out.print(conn1.getCount());
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q008

**문제**:
```
아래 내용의 각각의 설명에 대한 답을 작성하시오.

(1) 조인에 참여하는 두 릴레이션의 속성 값을 비교하여 조건을 만족하는 튜플만 반환한다.
(2) 조건이 정확하게 '=' 등호로 일치하는 결과를 반환한다.
(3) ( (2) ) 조인에서 조인에 참여한 속성이 두 번 나오지 않도록 중복된 속성을 제거한 결과를 반환한다.
```

**답안**:
```
(1) 세타 조인
(2) 동등 조인
(3) 자연 조인
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q009

**문제**:
```
다음은 운영체제 페이지 순서를 참고하여 할당된 프레임의 수가 3개일 때 LRU와 LFU 알고리즘의 페이지 부재 횟수를 작성하시오.
페이지 참조 순서 : 1, 2, 3, 1, 2, 4, 1, 2, 5, 7

(1) LRU :
(2) LFU :
```

**답안**:
```
(1) 6
(2) 6
```

**현재 해설**: LRU와 LFU 페이지 부재 횟수

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q010

**문제**:
```
아래 JAVA언어 코드의 실행 순서를 중복 번호없이 작성하시오.
실행 순서 : 5 → ( ) → ( ) → ( ) → ( ) → ( )
```

**답안**:
```
6
3
1
7
2
```

**현재 해설**: 실행 순서

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q010.png

**코드 언어**: java

**코드**:
```java
class Parent {
    int x, y;
    Parent(int x, int y) { ①
        this.x=x;
        this y=y;
    }
    int getT() { ②
        return x*y;
    }
}
​class Child extend Parent {
    int x;
    Child (int x) { ③
        super(x+1, x);
        this.x=x;
    }
    int getT(int n){ ④
        return super.getT()+n;
    }
}
class Main {
    public static void main(String[] args) { ⑤
        Parent parent = new Child(3); ⑥
        System.out.println(parent.getT()); ⑦
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q011

**문제**:
```
다음 C언어의 알맞는 출력값을 작성하시오.
```

**답안**:
```
9981 and 2795.10
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q011.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
typedef struct{
    int accNum;
    double bal;
}BankAcc;
double sim_pow(double base, int year){
    int i;
    double r = 1.0;
    for(i=0; i<year; i++){
        r = r*base;
    }
    return r;
} 
void initAcc(BankAcc *acc, int x, double y){
    acc -> accNum = x;
    acc -> bal = y;
}
void xxx(BankAcc *acc, double *en){
    if (*en > 0 && *en < acc -> bal) {
        acc -> bal = acc -> bal-*en;
    }else{
        acc -> bal = acc -> bal+*en;
    }
}
void yyy(BankAcc *acc){
    acc -> bal = acc -> bal * sim_pow((1+0.1),3);
}
int main(){
    BankAcc myAcc;
    initAcc(&myAcc, 9981, 2200.0);
    double amount = 100.0;
    xxx(&myAcc, &amount);
    yyy(&myAcc);
    printf("%d and %.2f", myAcc.accNum, myAcc.bal);
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q012

**문제**:
```
다음 파이썬 코드에 대한 알맞는 출력 값을 작성하시오.
```

**답안**:
```
Seynaau
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q012.png

**코드 언어**: python

**코드**:
```python
a = ["Seoul", "Kyeonggi", "Incheon", "Daejun", "Daegu", "Pusan"] 
str = "S"
for i in a:
    str = str + i[1]
print(str)
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q013

**문제**:
```
아래 보기의 SQL 문장과 테이블을 참고하여

 출력 값을 표로 작성하시오.
```

**답안**:
```
a
b
```

**현재 해설**: B 컬럼의 결과값

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q013.png

**코드 언어**: unknown

**코드**:
```unknown
SELECT
    B
FROM
    R1
WHERE
    C IN (SELECT C FROM R2 WHERE D="k");
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q014

**문제**:
```
아래는 애플리케이션 테스트 관리에 대한 내용이다.
설명하는 답을 보기에서 골라 작성하시오.
```

**답안**:
```
ㄹ
```

**현재 해설**: 변경 조건/결정 커버리지

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q001

**문제**:
```
모든 분기와 조건의 조합을 고려하나 모든 조합을 테스트하는 대신에 테스트가 필요한 중요한 조합을 찾아내는데에 중점을 둔다.

2. 특정 조건을 수행할 때 다른 조건과는 상관없이 전체 결과에 영향을 미치는 조건만을 테스트한다.

3. 각각의 파라미터는 적어도 한 번은 최종 결과에 영향을 주어야 한다.

[보기]

ㄱ. 구문 커버리지

ㄴ. 결정 커버리지

ㄷ. 조건 커버리지

ㄹ. 변경 조건/결정 커버리지

ㅁ.다중 조건 커버리지

ㅂ.경로 커버리지

ㅅ.조건/결정 커버리지
```

**답안**:
```
4
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q001.png

**코드 언어**: java

**코드**:
```java
class Connection {
    private static Connection _inst = null;
    private int count = 0;
    static public Connection get() {
        if(_inst == null) {
            _inst = new Connection();
            return _inst;
        }
        return _inst;
    }
    public void count() {
         count++; 
    }
    public int getCount() {
         return count; 
    }
}
public class main {  
    public static void main(String[] args) {
        Connection conn1 = Connection.get();
        conn1.count();
        Connection conn2 = Connection.get();
        conn2.count();
        Connection conn3 = Connection.get();
        conn3.count();
        conn1.count();
        System.out.print(conn1.getCount());
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q015

**문제**:
```
다음 아래 내용을 보고

  보기에서 알맞는 용어를 골라 작성하시오.
인터넷 공격자의 존재를 숨기면서 이 공격자에게 시스템에 대한 무제한 접근 권한을 부여하는 악성 프로그램이다.
해커가 자신의 존재를 숨기면서 허가되지 않은 컴퓨터나 소프트웨어에 접근할 수 있도록 설계된 도구이다.
일반적으로 펌웨어, 가상화 계층 등의 다양한 시스템 영역에서 작동하며, 운영체제의 시스템콜을 해킹하여 악성코드의 실행여부를 숨겨 안티바이러스 탐지를 우회할 수 있다.
```

**답안**:
```
ㅅ
```

**현재 해설**: Rootkit

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q016

**문제**:
```
다음 Java 코드를 보고

 알맞는 출력 값을 작성하시오.
```

**답안**:
```
9
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q016.png

**코드 언어**: java

**코드**:
```java
class classOne {
    int a, b;
    public classOne(int a, int b) {
        this.a = a;
        this.b = b;
    }
    public void print() {
        System.out.println(a + b);
    }
}
class classTwo extends classOne {
    int po = 3;
    public classTwo(int i) {
        super(i, i+1);
    }
    public void print() {
        System.out.println(po*po);
    }
}
public class main {  
    public static void main(String[] args) {
        classOne one = new classTwo(10);
        one.print();
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q017

**문제**:
```
다음 아래 내용을 보고

  보기에서 알맞는 용어를 골라 작성하시오.
```

**답안**:
```
ㅅ
```

**현재 해설**: APT

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q001

**문제**:
```
불특정 다수가 아닌 명확한 표적을 정하여 지속적인 정보수집 후 공격감행할 수 있다.

2. 시스템에 직접 침투하는 것뿐 아니라 표적 내부직원들이 이용하는 다양한 단말을 대상으로 한다.

3. 한가지 기술만이 아닌 Zero-day 취약점, 악성코드 등 다양한 보안 위협 공격 기술을 사용한다.

4. 일반적으로 공격은 침투, 검색, 수집 및 유출의 4단계로 실행되며, 각 단계별로 다양한 공격 기술을 사용한다.
```

**답안**:
```
4
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q001.png

**코드 언어**: java

**코드**:
```java
class Connection {
    private static Connection _inst = null;
    private int count = 0;
    static public Connection get() {
        if(_inst == null) {
            _inst = new Connection();
            return _inst;
        }
        return _inst;
    }
    public void count() {
         count++; 
    }
    public int getCount() {
         return count; 
    }
}
public class main {  
    public static void main(String[] args) {
        Connection conn1 = Connection.get();
        conn1.count();
        Connection conn2 = Connection.get();
        conn2.count();
        Connection conn3 = Connection.get();
        conn3.count();
        conn1.count();
        System.out.print(conn1.getCount());
    }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q018

**문제**:
```
아래의 SQL 코드와 테이블을 참고하여

 결과 값을 작성하시오.
```

**답안**:
```
1
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q018.png

**코드 언어**: unknown

**코드**:
```unknown
SELECT 
    COUNT(*) 
FROM 
    TABLE 
WHERE 
    EMPNO > 100 
AND 
    SAL >= 3000 OR EMPNO = 200
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q019

**문제**:
```
다음 C언어 코드의 알맞는 출력 값을 작성하시오.
```

**답안**:
```
Nd sc 1
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round1/Q019.png

**코드 언어**: c

**코드**:
```c
#include<stdio.h>
#include<ctype.h>
int main(){
    char*p = "It is 8";
    char result[100];
    int i;
    for(i=0; p[i]!='\0'; i++){
        if(isupper(p[i]))
            result[i] = (p[i]-'A'+5)% 25 + 'A';
        else if(islower(p[i]))
            result[i] = (p[i]-'a'+10)% 26 + 'a';
        else if(isdigit(p[i]))
            result[i] = (p[i]-'0'+3)% 10 + '0';
        else if(!(isupper(p[i]) || islower(p[i]) || isdigit(p[i])))    
            result[i] = p[i];
    }
    result[i] = '\0';
    printf("%s\n",result);
    return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q020

**문제**:
```
다음 아래의 내용을 보고

 알맞는 용어를 작성하시오.
구체적인 클래스에 의존하지 않고 서로 연관되거나 의존적인 객체들의 조합을 만드는 인터페이스를 제공하는 패턴이다.
연관성이 있는 객체 군이 여러개 있을 경우 이들을 묶어 추상화하고, 어떤 구체적인 상황이 주어지면 팩토리 객체에서 집합으로 묶은 객체 군을 구현화 하는 생성 패턴이다 관련성 있는 여러 종류의 객체를 일관된 방식으로 생성하는 경우에 유용하다.
kit라고도 불린다.
```

**답안**:
```
Abstract Factory
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**테이블**: table1

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

