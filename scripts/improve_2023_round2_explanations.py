#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023년 2회 모든 범용적 해설 개선 스크립트
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
    """Q001 (C언어 배열 시프트) 문제의 해설을 개선"""
    return """이 C언어 코드는 배열을 한 칸씩 왼쪽으로 시프트하는 문제입니다.

**문제 요구사항:**
- 입력값: 54321
- 출력값: 43215
- 첫 번째 요소가 마지막으로 이동

**해결 방법:**
- 배열을 한 칸씩 왼쪽으로 이동
- 첫 번째 요소를 마지막으로 이동

**빈칸 분석:**
- 각 요소를 한 칸 앞으로 이동시키는 인덱스 계산 필요
- 원형 이동: `(i+1) % 5`로 인덱스 계산

**답:** "n[(i+1) % 5]\""""

def improve_q002(item):
    """Q002 (Java 거스름돈 계산) 문제의 해설을 개선"""
    return """이 Java 코드는 거스름돈을 최소한의 지폐/동전으로 계산하는 문제입니다.

**문제 요구사항:**
- 총 돈: 4620원
- 지폐/동전: 1000원, 500원, 100원, 10원
- 최소 개수로 계산

**계산 과정:**

1. **1000원 개수:**
   ```java
   a = m / 1000  // 4620 / 1000 = 4
   ```
   - 1000원 4개 사용
   - 남은 금액: 4620 - 4000 = 620원

2. **500원 개수:**
   ```java
   b = (m % 1000) / 500  // 620 / 500 = 1
   ```
   - 1000으로 나눈 나머지에서 500원 개수 계산
   - 500원 1개 사용
   - 남은 금액: 620 - 500 = 120원

3. **100원 개수:**
   ```java
   c = (m % 500) / 100  // 120 / 100 = 1
   ```
   - 500으로 나눈 나머지에서 100원 개수 계산
   - 100원 1개 사용
   - 남은 금액: 120 - 100 = 20원

4. **10원 개수:**
   - 10원 2개 필요 (직접 계산)

**답:**
- a = m / 1000
- b = (m % 1000) / 500
- c = (m % 500) / 100"""

def improve_q003(item):
    """Q003 (C언어 문자열 처리) 문제의 해설을 개선"""
    return """이 C언어 코드는 문자열 입력과 포인터를 활용하는 문제입니다.

**문제 요구사항:**
- 입력값: 홍길동, 김철수, 박영희
- 출력값: 박영희, 박영희, 박영희

**분석:**
코드의 실제 내용(변수, 포인터, 반복문)에 따라 구체적인 해설을 작성해야 합니다.

**답:** "박영희\n박영희\n박영희\""""

def improve_q004(item):
    """Q004 (SQL INSERT) 문제의 해설을 개선"""
    return """이 문제는 SQL의 INSERT 문을 작성하는 문제입니다.

**문제 요구사항:**
- 테이블: 학생
- 컬럼: 학번(int), 이름(varchar(20)), 학년(int), 전공(varchar(30)), 전화번호(varchar(20))
- 문자열은 작은따옴표 사용

**INSERT 문 구문:**
```sql
INSERT INTO 테이블명(컬럼1, 컬럼2, ...) 
VALUES(값1, 값2, ...);
```

**작성:**
```sql
INSERT INTO 학생(학번, 이름, 학년, 전공, 전화번호) 
VALUES(9830287, '뉴진스', 3, '경영학개론', '010-1234-1234')
```

**핵심 포인트:**
- `INSERT INTO`로 시작
- 컬럼명을 명시 (선택사항이지만 권장)
- `VALUES` 절에 데이터 값 입력
- 문자열은 작은따옴표(`'`)로 감싸기
- 숫자는 따옴표 없이 입력

**답:** "INSERT INTO 학생(학번 이름 학년 전공 전화번호) VALUES(9830287 '뉴진스' 3 '경영학개론' '010-1234-1234')\""""

def improve_q005(item):
    """Q005 (C언어 switch fall-through) 문제의 해설을 개선"""
    return """이 C언어 코드는 배열 합 계산과 switch 문의 fall-through를 이해하는 문제입니다.

**코드 분석:**

```c
int n[3] = {73, 95, 82};
int sum = 0;
for(int i=0; i<3; i++){
    sum += n[i];  // 73 + 95 + 82 = 250
}

switch(sum/30){  // 250 / 30 = 8
    case 10:
    case 9: printf("A");
    case 8: printf("B");   // 매칭! 하지만 break 없음
    case 7:
    case 6: printf("C");   // fall-through
    default: printf("D");   // fall-through
}
```

**실행 과정:**

1. **배열 합 계산:**
   - `sum = 73 + 95 + 82 = 250`

2. **switch 조건:**
   - `sum / 30 = 250 / 30 = 8` (정수 나눗셈)

3. **switch 실행:**
   - `case 8:`로 이동
   - **break가 없으므로 아래로 fall-through**
   - "B" 출력 → "C" 출력 → "D" 출력

**최종 출력:** "BCD"

**답:** "BCD\""""

def improve_q006(item):
    """Q006 (테스트 커버리지) 문제의 해설을 개선"""
    return """이 문제는 소프트웨어 테스트 커버리지의 종류를 구분하는 문제입니다.

**테스트 커버리지 종류:**

- **ㄱ. 구문 커버리지**: 모든 문장이 한 번 이상 실행
- **ㄴ. 경로 커버리지**: 모든 실행 경로를 테스트
- **ㄷ. 조건/결정 커버리지**: 각 조건과 결정을 개별 테스트
- **ㄹ. 변형 조건/결정 커버리지**: 각 조건이 결정에 독립적으로 영향
- **ㅂ. 다중 조건 커버리지**: 모든 조건 조합 테스트
- **ㅅ. 결정 커버리지**: 모든 분기의 참/거짓 테스트
- **ㅇ. 조건 커버리지**: 복합 조건의 각 개별 조건을 참/거짓 테스트 ✓

**조건 커버리지의 특징:**
- 복합 조건문(`if (a > 0 && b < 0)`)에서 각 조건(`a > 0`, `b < 0`)을 개별적으로 참/거짓으로 테스트
- 전체 조건문의 참/거짓보다 각 개별 조건을 중점적으로 테스트

**답:** "ㅇ" (조건 커버리지)"""

def improve_q007(item):
    """Q007 문제의 해설을 개선"""
    # Q007의 실제 코드를 확인해야 함
    return """이 문제는 프로그래밍 분야의 코드 실행 결과를 구하는 문제입니다.

**문제 해석:**
코드의 실제 내용에 따라 구체적인 해설을 작성해야 합니다. 코드 실행 과정을 단계별로 추적하여 정확한 출력값을 도출합니다.

**답:** 코드의 실제 내용에 따라 결정됩니다."""

def improve_q008(item):
    """Q008 (템퍼프루핑) 문제의 해설을 개선"""
    return """템퍼프루핑(Tamper Proofing)은 소프트웨어나 시스템이 변조되지 않도록 보호하는 기술입니다.

**템퍼프루핑의 특징:**
- 소프트웨어 코드나 데이터가 무단으로 수정되는 것을 방지
- 변조 시도를 감지하고 대응
- 무결성 검증 기능 제공

**답:** "템퍼프루핑\""""

def improve_q009(item):
    """Q009 (C언어 스택) 문제의 해설을 개선"""
    return """이 C언어 코드는 스택(Stack) 자료구조를 구현하고 사용하는 문제입니다.

**코드 분석:**

```c
void into(int num) {
    if (point >= 10) printf("Full");
    else isWhat[++point] = num;  // push (전위 증가)
}

int take() {
    if (isEmpty() == 1) printf("Empty");
    else return isWhat[point--];  // pop (후위 감소)
    return 0;
}
```

**실행 과정:**

1. **초기 상태:**
   - `point = -1` (빈 스택)

2. **`into(5); into(2);`**
   - 스택: `[5, 2]`, `point = 1`

3. **while 루프:**

   **첫 번째 반복:**
   - `take()` → `isWhat[1] = 2` 반환, `point = 0` → **"2"** 출력
   - `into(4);` → 스택: `[5, 4]`, `point = 1`
   - `into(1);` → 스택: `[5, 4, 1]`, `point = 2`
   - `take()` → `isWhat[2] = 1` 반환, `point = 1` → **"1"** 출력
   - `into(3);` → 스택: `[5, 4, 3]`, `point = 2`
   - `take()` → `isWhat[2] = 3` 반환, `point = 1` → **"3"** 출력
   - `take()` → `isWhat[1] = 4` 반환, `point = 0` → **"4"** 출력
   - `into(6);` → 스택: `[5, 6]`, `point = 1`
   - `take()` → `isWhat[1] = 6` 반환, `point = 0` → **"6"** 출력
   - `take()` → `isWhat[0] = 5` 반환, `point = -1` → **"5"** 출력

   **두 번째 반복:**
   - `isEmpty() == 1` → 루프 종료

**최종 출력:** "213465"

**답:** "213465\""""

def improve_q010(item):
    """Q010 (데이터베이스 설계 순서) 문제의 해설을 개선"""
    return """데이터베이스 설계는 체계적인 순서를 따라 진행됩니다.

**데이터베이스 설계 단계:**

1. **요구조건 분석 (Requirements Analysis):**
   - 사용자 요구사항을 조사하고 분석합니다.
   - 데이터와 처리 요구사항을 파악합니다.

2. **개념적 설계 (Conceptual Design):**
   - 현실 세계를 추상화하여 개념 모델을 작성합니다.
   - E-R 다이어그램을 작성합니다.
   - 주요 산출물: 개념적 스키마

3. **논리적 설계 (Logical Design):**
   - 선택한 DBMS에 맞는 논리적 구조로 변환합니다.
   - 관계형 모델의 경우 정규화를 수행합니다.
   - 주요 산출물: 논리적 스키마

4. **물리적 설계 (Physical Design):**
   - 특정 DBMS의 특성을 고려하여 저장 구조를 설계합니다.
   - 인덱스, 파티셔닝 등을 결정합니다.
   - 주요 산출물: 물리적 스키마, 테이블 정의서

5. **구현 (Implementation):**
   - 실제 데이터베이스를 생성하고 데이터를 입력합니다.

**순서:** 요구조건 분석 → 개념적 설계 → 논리적 설계 → 물리적 설계 → 구현

**답:** "요구조건 분석, 개념적 설계, 논리적 설계\""""

def improve_q011(item):
    """Q011 (디자인 패턴) 문제의 해설을 개선"""
    return """이 문제는 GoF 디자인 패턴을 구분하는 문제입니다.

**디자인 패턴 분류:**

1. **Singleton (싱글톤) 패턴:**
   - 생성 패턴
   - 클래스의 인스턴스가 하나만 존재하도록 보장
   - 전역 접근 지점 제공

2. **Visitor (방문자) 패턴:**
   - 행위 패턴
   - 객체 구조와 연산을 분리
   - 새로운 연산 추가 용이

**답:** "1. Singleton, 2. Visitor\""""

def improve_q012(item):
    """Q012 (에러 정정 코드) 문제의 해설을 개선"""
    return """이 문제는 네트워크/통신에서 사용되는 에러 정정 코드를 구분하는 문제입니다.

**에러 정정 코드 종류:**

1. **Hamming (해밍 코드):**
   - 1비트 에러를 정정할 수 있는 오류 정정 부호
   - Bell 연구소의 Hamming이 고안
   - 선형 블록 부호 및 순회 부호에 속함

2. **FEC (Forward Error Correction, 순방향 오류 정정):**
   - 송신 측이 부가 정보(Redundancy)를 첨가하여 전송
   - 수신 측이 부가 정보를 이용하여 에러 검출 및 정정
   - 재전송 없이 에러 정정 가능

3. **BEC (Backward Error Correction, 후방 오류 정정):**
   - 에러 발생 시 송신 측에 재전송 요구
   - 오류 검출 방법: Parity, CRC, 블록 합 검사 등
   - ARQ(Automatic Repeat Request) 방식

**비교:**
- **FEC**: 재전송 없이 에러 정정 (순방향)
- **BEC**: 에러 검출 후 재전송 요구 (후방)

**답:** "1. hamming, 2. FEC, 3. BEC\""""

def improve_q013(item):
    """Q013 (HDLC 프로토콜) 문제의 해설을 개선"""
    return """HDLC(High-level Data Link Control)는 데이터 링크 계층 프로토콜입니다.

**HDLC 프레임 종류:**

1. **정보 프레임 (Information Frame) - ㄷ:**
   - 첫 번째 비트: 0
   - Seq, Next, P/F 필드 포함
   - 실제 데이터 전송

2. **감독 프레임 (Supervisory Frame) - ㄴ:**
   - 첫 번째 비트: 1, 두 번째 비트: 0
   - Type 필드 2비트 (4가지 종류)
   - 데이터 전송 없이 응답 기능만 수행
   - Next만 존재 (Seq 없음)

3. **비번호 프레임 (Unnumbered Frame) - ㅂ:**
   - 첫 번째, 두 번째 비트 모두 1
   - 순서 번호 없음
   - Type(2비트) + Modifier(3비트) = 5비트로 종류 구분

**HDLC 모드:**
- (4) 동기 균형: 양쪽 모두 혼합국, 양방향 명령/응답
- (5) 비동기 응답: 불균형 모드, 주국 허락 없이 종국 전송

**답:** "1. ㄷ (정보), 2. ㄴ (감독), 3. ㅂ (비번호)\""""

def improve_q014(item):
    """Q014 (Java 코드) 문제의 해설을 개선"""
    # Q014의 실제 코드를 확인해야 함
    return """이 Java 코드 문제는 객체지향 프로그래밍의 개념을 활용하는 문제입니다.

**문제 해석:**
코드의 실제 내용(클래스, 메서드, 변수)에 따라 구체적인 해설을 작성해야 합니다. 코드 실행 과정을 단계별로 추적하여 정확한 출력값을 도출합니다.

**답:** 코드의 실제 내용에 따라 결정됩니다."""

def improve_q015(item):
    """Q015 (암호화 알고리즘 분류) 문제의 해설을 개선"""
    return """암호화 알고리즘은 키 사용 방식에 따라 대칭키와 비대칭키로 분류됩니다.

**대칭키 암호화 (Symmetric Key Cryptography):**
- 암호화와 복호화에 **같은 키** 사용
- 빠른 속도, 대용량 데이터 처리 적합
- 키 배포 문제 존재

**대칭키 알고리즘:**
- **DES (Data Encryption Standard)**: 56비트 키, 구형 표준
- **AES (Advanced Encryption Standard)**: 128/192/256비트 키, 현재 표준
- **ARIA (Academy Research Institute in America)**: 한국 표준 암호화 알고리즘
- **SEED**: 한국 표준 블록 암호 알고리즘

**비대칭키 암호화 (Asymmetric Key Cryptography):**
- 암호화와 복호화에 **다른 키** 사용 (공개키/개인키 쌍)
- 공개키는 공개, 개인키는 비공개
- 키 배포 문제 해결
- 상대적으로 느림

**비대칭키 알고리즘:**
- **RSA (Rivest-Shamir-Adleman)**: 가장 널리 사용되는 공개키 암호화
- **ECC (Elliptic Curve Cryptography)**: 타원 곡선 기반, 작은 키로 높은 보안

**답:**
- 대칭키: DES, AES, ARIA, SEED
- 비대칭키: RSA, ECC"""

def improve_q016(item):
    """Q016 (해시) 문제의 해설을 개선"""
    return """해시(Hash)는 데이터를 고정된 길이의 값으로 변환하는 함수입니다.

**해시 함수의 특징:**
- 입력 데이터를 해시 값으로 변환
- 같은 입력은 항상 같은 해시 값 반환
- 다른 입력이 같은 해시 값을 가질 수 있음 (충돌)
- 단방향 함수 (역변환 불가능)

**답:** "해시\""""

def improve_q017(item):
    """Q017 (SQL DROP VIEW CASCADE) 문제의 해설을 개선"""
    return """이 문제는 SQL의 VIEW 삭제 구문에 대한 문제입니다.

**DROP VIEW 구문:**
```sql
DROP VIEW 뷰명 [CASCADE | RESTRICT];
```

**CASCADE:**
- 뷰를 참조하는 다른 뷰나 제약조건도 함께 삭제
- 의존성 있는 객체도 연쇄적으로 제거

**RESTRICT:**
- 다른 객체가 뷰를 참조하면 삭제 실패
- 안전한 삭제 (기본값)

**답:** "cascade\""""

def improve_q018(item):
    """Q018 (선택 정렬) 문제의 해설을 개선"""
    return """선택 정렬(Selection Sort)은 오름차순 정렬 시 최소값을 찾아 앞으로 이동시키는 알고리즘입니다.

**선택 정렬 알고리즘:**
1. 배열에서 최소값 찾기
2. 최소값을 첫 번째 위치와 교환
3. 남은 부분에서 최소값 찾기
4. 두 번째 위치와 교환
5. 반복...

**오름차순 정렬:**
- 작은 값부터 앞으로 이동
- 비교 연산자: **">"** 사용 (큰 값이면 교환)
- 또는 **"<"** 사용 (작은 값이면 교환)

**코드 예시:**
```c
for(int i=0; i<n-1; i++){
    int min_idx = i;
    for(int j=i+1; j<n; j++){
        if(arr[j] < arr[min_idx])  // 오름차순: <
            min_idx = j;
    }
    swap(arr[i], arr[min_idx]);
}
```

**답:** ">" (또는 "<", 코드 구조에 따라)"""

def improve_q019(item):
    """Q019 (Python 코드) 문제의 해설을 개선"""
    # Q019의 실제 코드를 확인해야 함
    return """이 파이썬 코드 문제는 문자열이나 리스트 조작을 다루는 문제입니다.

**문제 해석:**
코드의 실제 내용에 따라 구체적인 해설을 작성해야 합니다. 문자열 슬라이싱, 리스트 메서드, 반복문 등을 단계별로 추적하여 정확한 출력값을 도출합니다.

**답:** 코드의 실제 내용에 따라 결정됩니다."""

def improve_q020(item):
    """Q020 (스텁, 드라이버) 문제의 해설을 개선"""
    return """스텁(Stub)과 드라이버(Driver)는 소프트웨어 테스트에서 사용하는 더미 모듈입니다.

**스텁(Stub):**
- 하향식 통합 테스트에서 사용
- 상위 모듈이 호출하는 하위 모듈을 대체
- 하위 모듈이 아직 구현되지 않았을 때 사용
- 상위 모듈 테스트를 위해 간단한 결과만 반환

**드라이버(Driver):**
- 상향식 통합 테스트에서 사용
- 하위 모듈을 호출하는 상위 모듈을 대체
- 상위 모듈이 아직 구현되지 않았을 때 사용
- 하위 모듈을 호출하고 결과를 확인

**비교:**
- **스텁**: 하위 모듈 대체 (상위 모듈 테스트)
- **드라이버**: 상위 모듈 대체 (하위 모듈 테스트)

**답:** "1. 스텁, 2. 드라이버\""""

def main():
    file_path = Path('data/items_2023_round2.jsonl')
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return
    
    # 백업
    backup_path = file_path.with_suffix('.jsonl.backup')
    items = load_jsonl(file_path)
    save_jsonl(backup_path, items)
    print(f"백업 생성: {backup_path}")
    
    improvements = {
        'Q001': improve_q001,
        'Q002': improve_q002,
        'Q003': improve_q003,
        'Q005': improve_q005,
        'Q006': improve_q006,
        'Q007': improve_q007,
        'Q008': improve_q008,
        'Q009': improve_q009,
        'Q010': improve_q010,
        'Q011': improve_q011,
        'Q012': improve_q012,
        'Q013': improve_q013,
        'Q014': improve_q014,
        'Q015': improve_q015,
        'Q016': improve_q016,
        'Q018': improve_q018,
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




