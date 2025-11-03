# 2024년 3회 해설 작성

총 19개 문제의 해설 작성이 필요합니다.

---

## Q001

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
OOAAA
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q001.png

**코드 언어**: java

**코드**:
```java
public class Main{
  static String[] s = new String[3];
  static void func(String[]s, int size){
    for(int i=1; i<size; i++){
      if(s[i-1].equals(s[i])){
        System.out.print("O");
      }else{
        System.out.print("N");
      }
    }
      for (String m : s){
        System.out.print(m);
      }
    }
  public static void main(String[] args){
    s[0] = "A";
    s[1] = "A";
    s[2] = new String("A");
    func(s, 3);
  }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q002

**문제**:
```
다음은 파이썬에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
3
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q002.png

**코드 언어**: python

**코드**:
```python
def func(lst):
  for i in range(len(lst) //2):
    lst[i], lst[-i-1] = lst[-i-1], lst[i]
lst = [1,2,3,4,5,6] 
func(lst)
print(sum(lst[::2]) - sum(lst[1::2]))
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q003

**문제**:
```
아래의 employee테이블과 project테이블을 참고하여

 보기의 SQL명령어에 알맞는 출력 값을 작성하시오.
```

**답안**:
```
1
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q003_1.png, images/2024_round3/Q003_2.png

**코드 언어**: sql

**코드**:
```sql
SELECT 
    count(*) 
FROM employee AS e JOIN project AS p ON e.project_id = p.project_id 
WHERE p.name IN (
    SELECT name FROM project p WHERE p.project_id IN (
        SELECT project_id FROM employee GROUP BY project_id HAVING count(*) < 2
    )
);
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q004

**문제**:
```
다음은 운영체제 페이지 순서를 참고하여

 할당된 프레임의 수가 3개일 때  LRU 알고리즘의 페이지 부재 횟수를 작성하시오.
페이지 참조 순서
: 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
```

**답안**:
```
12
```

**현재 해설**: LRU 페이지 부재 횟수

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q005

**문제**:
```
다음은 네트워크 취약점에 대한 문제이다.
아래 내용을 보고

 알맞는 용어를 작성하시오.

- IP나 ICMP의 특성을 악용하여 엄청난 양의 데이터를 한 사이트에 집중적으로 보냄으로써 네트워크의 일부를 불능 상태로 만드는 공격이다.

- 여러 호스트가 특정 대상에게 다량의 ICMP Echo Reply 를 보내게 하여 서비스거부(DoS)를 유발시키는 보안공격이다.

- 공격 대상 호스트는 다량으로 유입되는 패킷으로 인해 서비스 불능 상태에 빠진다.
```

**답안**:
```
스머프
```

**현재 해설**: Smurf 또는 Smurfing

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q006

**문제**:
```
다음은 GoF 디자인 패턴과 관련된 문제이다.
괄호안에 알맞는 용어를 작성하시오.
(        ) 패턴은 클래스나 객체들이 서로 상호작용하는 방법이나 책임 분배 방법을 정의하는 패턴이다.
(        ) 패턴은 객체들 간의 통신 방법을 정의하고 알고리즘을 캡슐화하여 객체 간의 결합도를 낮춘다.
(        ) 패턴은 Chain of Responsibility나 Command 또는 Observer 패턴이 있다.
```

**답안**:
```
행위
```

**현재 해설**: 행위 패턴

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q007

**문제**:
```
다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
20
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q007.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
int func(){
 static int x =0; 
  x+=2; 
  return x;
}
int main(){
  int x = 1; 
  int sum=0; 
  for(int i=0;i<4;i++) {
    x++; 
    sum+=func();
  } 
  printf("%d", sum);
  return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q008

**문제**:
```
다음은 무결성제약조건에 대한 문제이다.
아래 표에서 어떠한 (       ) 무결성을 위반하였는지 작성하시오.
```

**답안**:
```
개체
```

**현재 해설**: 개체 무결성

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q008.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q009

**문제**:
```
다음은 URL 구조에 관한 문제이다.
아래  보기의 순서대로 URL에 해당하는 번호를 작성하시오.
query
: 서버에 전달할 추가 데이터 path
: 서버 내의 특정 자원을 가리키는 경로 scheme
: 리소스에 접근하는 방법이나 프로토콜 authority
: 사용자 정보, 호스트명, 포트 번호 fragment
: 특정 문서 내의 위치
```

**답안**:
```
43125
```

**현재 해설**: URL 구조

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q009.png

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q010

**문제**:
```
다음은 파이썬에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
45
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q010.png

**코드 언어**: python

**코드**:
```python
def func(value):
    if type(value) == type(100):
        return 100
    elif type(value) == type(""):
        return len(value) 
    else:
        return 20
a = '100.0'
b = 100.0
c = (100, 200)
print(func(a) + func(b) + func(c))
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q011

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
52
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q011.png

**코드 언어**: java

**코드**:
```java
public class Main{
  public static void main(String[] args){
    Base a =  new Derivate();
    Derivate b = new Derivate();
    System.out.print(a.getX() + a.x + b.getX() + b.x);
  }
}
class Base{
  int x = 3;
  int getX(){
     return x * 2; 
  }
}
class Derivate extends Base{
  int x = 7;
  int getX(){
     return x * 3;
  }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q012

**문제**:
```
다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
312
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q012.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
struct Node {
 int value;
 struct Node* next;
};
void func(struct Node* node){
  while(node != NULL && node->next != NULL){
     int t = node->value;
     node->value = node->next->value;
     node->next->value = t;
     node = node->next->next;
  }
}
int main(){
  struct Node n1 = {1, NULL};
  struct Node n2 = {2, NULL};
  struct Node n3 = {3, NULL};
  n1.next = &n3;
  n3.next = &n2;
  func(&n1);  
  struct Node* current = &n1;
  while(current != NULL){
    printf("%d", current->value);
    current = current->next;
 }
 return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q013

**문제**:
```
다음은 테스트 커버리지에 대한 문제이다.
아래 내용에 알맞는 답을 보기에서 골라 작성하시오.

1. 테스트를 통해 프로그램의 모든 문장을 최소한 한 번씩 실행했는지를 측정

2. 프로그램 내의 모든 분기(조건문)의 각 분기를 최소한 한 번씩 실행했는지를 측정

3. 복합 조건 내의 각 개별 조건이 참과 거짓으로 평가되는 경우를 모두 테스트했는지를 측정

ㄱ. 조건

ㄴ. 경로

ㄷ. 결정

ㄹ. 분기

ㅁ.함수

ㅂ. 문장

ㅅ. 루프
```

**답안**:
```
1. 문장
2. 분기
3. 조건
```

**현재 해설**: 테스트 커버리지

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q015

**문제**:
```
다음은 데이터베이스에 관한 문제이다.
아래 내용을 읽고 알맞는 답을 보기에서 찾아 골라 작성하시오.

(1) 다른 테이블, 릴레이션의 기본 키를 참조하는 속성 또는 속성들의 집합
(2) 테이블에서 각 행을 유일하게 식별할 수 있는 최소한의 속성들의 집합
(3) 후보 키 중에서 선정된 기본 키를 제외한 나머지 후보 키
(4) 테이블에서 각 행을 유일하게 식별할 수 있는 속성들의 집합

ㄱ. 슈퍼키

ㄴ. 외래키

ㄷ. 대체키

ㄹ. 후보키
```

**답안**:
```
(1) 외래키
(2) 후보키
(3) 대체키
(4) 슈퍼키
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q016

**문제**:
```
다음은 C언어에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
1
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q016.png

**코드 언어**: c

**코드**:
```c
#include <stdio.h>
void func(int** arr, int size){
  for(int i=0; i<size; i++){
     *(*arr + i) = (*(*arr+i) + i) % size;
  }
}
int main(){
  int arr[] = {3,1, 4, 1, 5};
  int* p = arr;
  int** pp = &p;
  int num = 6;
  func(pp, 5);  
  num = arr[2];
  printf("%d", num);  
  return 0;
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q017

**문제**:
```
다음 아래 내용을 보고

 알맞는 용어를 작성하시오.

 (3글자로 작성)

- 공용 네트워크를 통해 사설 네트워크를 확장하는 기술이다.

- 사용자의 IP 주소를 숨기고, 사용자가 어디에서 접속하는지를 추적하기 어렵게 만든다.

- 종류로는 IPsec 또는 SSL, L2TP 등이 있다.
```

**답안**:
```
VPN
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: 없음

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q018

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
101
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q018.png

**코드 언어**: java

**코드**:
```java
public class ExceptionHandling {
  public static void main(String[] args) {
      int sum = 0;
      try {
          func();
      } catch (NullPointerException e) {
          sum = sum + 1;
      } catch (Exception e) {
          sum = sum + 10;
      } finally {
          sum = sum + 100;
      }
      System.out.print(sum);
  }
  static void func() throws Exception {
      throw new NullPointerException(); 
  }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q019

**문제**:
```
다음은 Java 코드에 대한 문제이다.
아래 코드를 확인하여

 알맞는 출력값을 작성하시오.
```

**답안**:
```
B0
```

**현재 해설**: 없음

**상태**: ❌ 없음 (없음)

**이미지**: images/2024_round3/Q019.png

**코드 언어**: java

**코드**:
```java
class Main {
  public static class Collection<T>{
    T value;
    public Collection(T t){
        value = t;
    }
    public void print(){
       new Printer().print(value);
    }
   class Printer{
      void print(Integer a){
        System.out.print("A" + a);
      }
      void print(Object a){
        System.out.print("B" + a);
      } 
      void print(Number a){
        System.out.print("C" + a);
      }
   }
 }
  public static void main(String[] args) {
      new Collection<>(0).print();
  }
}
```

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

## Q020

**문제**:
```
다음은 네트워크에 대한 문제이다.
아래 내용을 보고

 알맞는 용어를 작성하시오.

- 중앙 관리나 고정된 인프라 없이 임시로 구성되는 네트워크이다.

- 일반적으로 무선 통신을 통해 노드들이 직접 연결되어 데이터를 주고받는다.

- 긴급 구조, 긴급 회의, 군사적인 상황 등에서 유용하게 활용될 수 있다.

[보기]

ㄱ.Infrastructure Network

ㄴ. Firmware Network

ㄷ. Peer-to-Peer Network

ㄹ. Ad-hoc Network

ㅁ. Mesh Network

ㅂ.Sensor Network

ㅅ.Virtual Private Network
```

**답안**:
```
ㄹ
```

**현재 해설**: Ad-hoc Network

**상태**: ⚠️ 부족 (부족)

**이미지**: 없음

**테이블**: table1

**작성할 해설**:
[여기에 고등학생 수준의 해설 작성]

---

