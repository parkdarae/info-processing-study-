# -*- coding: utf-8 -*-
"""
범용적이거나 실질적이지 않은 해설 개선 스크립트
2021년, 2022년 기출문제의 품질 낮은 해설을 개선합니다.
"""
import json
from pathlib import Path
from datetime import datetime

def load_jsonl(filepath: Path):
    """JSONL 파일 로드"""
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    return questions

def save_jsonl(filepath: Path, questions):
    """JSONL 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')

# 개선할 해설들
improved_explanations_2021 = {
    "Q002": "이 문제는 **데이터베이스 설계 절차**를 이해하는 문제입니다.\n\n**데이터베이스 설계 절차:**\n\n1. **요구사항 분석:**\n- 사용자 요구사항을 파악하고 분석\n- 시스템이 처리해야 할 데이터와 기능 정의\n\n2. **개념적 설계:**\n- 현실 세계에 대한 인식을 추상적, 개념적으로 표현\n- 개념적 구조를 도출하는 과정\n- 주요 산출물: E-R 다이어그램\n- 엔티티와 속성, 관계를 정의\n\n3. **논리적 설계:**\n- 목표 DBMS에 맞는 스키마 설계\n- 트랜잭션 인터페이스 설계\n- 정규화 과정 수행\n- 관계형 데이터 모델로 변환\n\n4. **물리적 설계:**\n- 특정 DBMS의 특성 및 성능을 고려하여 데이터베이스 저장 구조로 변환\n- 인덱스 설계, 저장 공간 할당\n- 결과 산출물: 테이블 정의서 등\n\n5. **구현:**\n- 실제 데이터베이스 생성 및 응용 프로그램 개발\n\n**문제에서 요구하는 답:**\n- (1) 물리적 설계: 테이블 정의서 등 명세서 생성\n- (2) 개념적 설계: E-R 다이어그램 등 개념적 구조 도출\n- (3) 논리적 설계: 정규화 과정 수행\n\n**답:** 1. 물리적 설계, 2. 개념적 설계, 3. 논리적 설계",
    
    "Q005": "이 파이썬 코드는 **문자열 리스트의 각 요소에서 첫 번째 문자를 추출**하는 문제입니다.\n\n**코드 분석:**\n```python\nclass good :\n    li = [\"seoul\", \"kyeonggi\", \"inchon\", \"daejeon\", \"daegu\", \"pusan\"]\ng = good()\nstr01 = ''\nfor i in g.li:\n    str01 = str01 + i[0]\nprint(str01)\n```\n\n**실행 과정:**\n\n1. **클래스 정의 및 인스턴스 생성:**\n   - `good` 클래스의 클래스 변수 `li`에 도시명 리스트 저장\n   - `g = good()`로 인스턴스 생성\n\n2. **반복문 실행:**\n   - `for i in g.li`: 리스트의 각 요소를 순회\n   - 각 도시명 문자열에서 첫 번째 문자(`i[0]`) 추출\n\n3. **문자 추출 과정:**\n   - `i = \"seoul\"` → `i[0] = 's'` → `str01 = 's'`\n   - `i = \"kyeonggi\"` → `i[0] = 'k'` → `str01 = 'sk'`\n   - `i = \"inchon\"` → `i[0] = 'i'` → `str01 = 'ski'`\n   - `i = \"daejeon\"` → `i[0] = 'd'` → `str01 = 'skid'`\n   - `i = \"daegu\"` → `i[0] = 'd'` → `str01 = 'skidd'`\n   - `i = \"pusan\"` → `i[0] = 'p'` → `str01 = 'skiddp'`\n\n**최종 출력:** `skiddp`\n\n**핵심 포인트:**\n- 문자열 인덱싱: `문자열[0]`은 첫 번째 문자를 반환합니다.\n- 문자열 연결: `str01 = str01 + i[0]`는 기존 문자열에 새 문자를 추가합니다.\n\n**답:** **skiddp**",
    
    "Q008": "이 문제는 **비정규화(반정규화/역정규화)**에 대한 문제입니다.\n\n**비정규화란?**\n- 정규화된 엔티티, 속성, 관계에 대해 성능 향상과 개발 운영의 단순화를 위해 중복, 통합, 분리 등을 수행하는 데이터 모델링 기법\n- 정규화의 반대 개념으로, 성능을 위해 의도적으로 정규화 원칙을 완화\n\n**비정규화 방법:**\n\n1. **테이블 통합:**\n- 관련된 여러 테이블을 하나로 통합\n- 조인 연산 감소로 성능 향상\n\n2. **테이블 분할:**\n- 하나의 테이블을 여러 테이블로 분할\n- 수직 분할: 컬럼 단위 분할\n- 수평 분할: 행 단위 분할\n\n3. **중복 테이블 추가:**\n- 조회 성능 향상을 위해 중복 테이블 생성\n- 집계 테이블, 통계 테이블 등\n\n4. **중복 속성 추가:**\n- 조인 없이 접근하기 위해 중복 컬럼 추가\n- 계산된 값 저장\n\n**비정규화의 목적:**\n- 조회 성능 향상\n- 개발 및 운영 단순화\n- 응답 시간 단축\n\n**주의사항:**\n- 데이터 일관성 관리 필요\n- 저장 공간 증가\n- 데이터 중복으로 인한 업데이트 비용 증가\n\n**답:** **비정규화 (반정규화/역정규화)**",
    
    "Q009": "이 문제는 **블랙박스 테스트 기법**을 이해하는 문제입니다.\n\n**블랙박스 테스트란?**\n- 소프트웨어의 내부 구조를 알지 못한 상태에서 입력과 출력만을 확인하는 테스트\n- 시스템의 기능이 요구사항에 맞게 동작하는지 검증\n\n**블랙박스 테스트 종류:**\n\n1. **동치 분할 검사(동등분할 테스트, Equivalence Partitioning):**\n- 입력 데이터를 유사한 도메인별로 그룹핑하여 대표값으로 테스트\n- 동일한 결과를 낼 것으로 예상되는 입력값들을 하나의 그룹으로 묶음\n- 예: 0~100 범위면 0, 50, 100 등으로 테스트\n\n2. **경계값 분석(Boundary Value Analysis):**\n- 입력 조건의 경계값을 테스트 케이스로 선정\n- 경계와 그 근처 값을 테스트\n- 예: 0 <= x <= 10이면 -1, 0, 10, 11을 테스트\n\n3. **원인-효과 그래프 검사(Cause-Effect Graphing):**\n- 입력 조건과 출력 결과 간의 인과관계를 그래프로 표현하여 테스트 케이스 생성\n\n4. **오류 예측 검사(Error Guessing):**\n- 과거 경험이나 직관으로 오류를 예측하여 테스트\n\n5. **비교 검사(Comparison Testing):**\n- 여러 버전의 프로그램에 동일한 입력을 제공하여 결과 비교\n\n**문제에서 요구하는 기법:**\n- 블랙박스 기법 두 가지: **경계값 분석**, **동등분할 테스트**\n\n**답:** 1. 경계값 분석, 2. 동등분할 테스트",
    
    "Q010": "이 문제는 **테스트 종류**를 이해하는 문제입니다.\n\n**각 테스트 레벨의 정의:**\n\n1. **단위 테스트(Unit Test):**\n- 개별 모듈, 서브루틴이 정상적으로 실행되는지 확인\n- 가장 작은 단위(함수, 메서드)를 독립적으로 테스트\n- 화이트박스 테스트 기법 사용\n- 개발자가 수행\n\n2. **통합 테스트(Integration Test):**\n- 인터페이스 간 시스템이 정상적으로 실행되는지 확인\n- 여러 모듈을 결합하여 테스트\n- 모듈 간 인터페이스와 상호작용 검증\n\n**다른 테스트 레벨:**\n\n3. **시스템 테스트(System Test):**\n- 구현된 시스템이 정해진 요건에 적합한지 여부를 평가\n- 실제 운용과 같은 환경에서 시스템 전체에 대해 수행\n- 기능적 요구사항과 비기능적 요구사항 검증\n\n4. **인수 테스트(Acceptance Test):**\n- 사용자나 고객이 수행하는 최종 테스트\n- 시스템이 사용자의 요구사항을 만족하는지 확인\n\n**테스트 순서:**\n단위 테스트 → 통합 테스트 → 시스템 테스트 → 인수 테스트\n\n**답:**\n- (1) **단위 테스트**: 개별 모듈 확인\n- (2) **통합 테스트**: 인터페이스 간 시스템 확인",
    
    "Q014": "이 문제는 데이터베이스의 **Cardinality와 Degree**를 구하는 문제입니다.\n\n**Cardinality (카디널리티):**\n- 릴레이션(테이블)에서 **튜플(행)의 개수**\n- 데이터의 행 수\n- 예: 테이블에 5개의 행이 있으면 Cardinality = 5\n\n**Degree (차수):**\n- 릴레이션(테이블)에서 **속성(컬럼)의 개수**\n- 테이블의 컬럼 수\n- 예: 테이블에 4개의 컬럼이 있으면 Degree = 4\n\n**문제에서 요구하는 답:**\n주어진 테이블을 확인하면:\n- 행(Row)의 개수: 5개 → **Cardinality = 5**\n- 컬럼(Column)의 개수: 4개 → **Degree = 4**\n\n**기억하기:**\n- Cardinality = 데이터 행 수 (카운트)\n- Degree = 속성 컬럼 수 (도메인)\n\n**답:**\n- **Cardinality : 5**\n- **Degree : 4**",
    
    "Q015": "이 C언어 코드는 **구조체 배열과 포인터**를 이해하는 문제입니다.\n\n**코드 분석:**\n```c\nstruct good {\n    char name[10];\n    int age;\n};\nvoid main(){\n    struct good s[] = {\"Kim\",28,\"Lee\",38,\"Seo\",50,\"Park\",35};\n    struct good *p;\n    p = s;\n    p++;\n    printf(\"%s\\n\", p->name);\n    printf(\"%d\\n\", p->age);\n}\n```\n\n**실행 과정:**\n\n1. **구조체 배열 초기화:**\n   - `s[0] = {\"Kim\", 28}`\n   - `s[1] = {\"Lee\", 38}`\n   - `s[2] = {\"Seo\", 50}`\n   - `s[3] = {\"Park\", 35}`\n\n2. **포인터 설정:**\n   - `p = s` → `p`는 배열의 첫 번째 요소(`s[0]`)를 가리킴\n\n3. **포인터 증가:**\n   - `p++` → 포인터가 다음 구조체를 가리킴 (`s[1]`)\n   - 구조체 포인터는 구조체 크기만큼 이동\n\n4. **출력:**\n   - `p->name`: `s[1].name` = **\"Lee\"**\n   - `p->age`: `s[1].age` = **38**\n\n**핵심 포인트:**\n- 구조체 포인터의 `++` 연산은 구조체 크기만큼 증가합니다.\n- `p->` 연산자는 포인터가 가리키는 구조체의 멤버에 접근합니다.\n\n**답:** **Lee 38**",
    
    "Q017": "이 Java 코드는 **반복문을 이용한 누적 합계**를 계산하는 문제입니다.\n\n**코드 분석:**\n```java\nint i, j;\nfor(j=0, i=0; i<=5; i++){\n    j += i;\n    System.out.print(i);\n    if(i==5){\n        System.out.print(\"=\");\n        System.out.print(j);\n    }else{\n        System.out.print(\"+\");\n    }\n}\n```\n\n**실행 과정:**\n\n1. **초기화:**\n   - `i = 0`, `j = 0`\n\n2. **반복문 실행 (i=0부터 i=5까지):**\n\n   | 반복 | i 값 | j 값 | j += i 후 | 출력 |\n   |------|------|------|----------|------|\n   | 초기 | 0 | 0 | - | - |\n   | 1회 | 0 | 0 | j = 0 + 0 = 0 | `0+` |\n   | 2회 | 1 | 0 | j = 0 + 1 = 1 | `1+` |\n   | 3회 | 2 | 1 | j = 1 + 2 = 3 | `2+` |\n   | 4회 | 3 | 3 | j = 3 + 3 = 6 | `3+` |\n   | 5회 | 4 | 6 | j = 6 + 4 = 10 | `4+` |\n   | 6회 | 5 | 10 | j = 10 + 5 = 15 | `5=15` |\n\n3. **최종 출력:**\n   - `0+1+2+3+4+5=15`\n   - 하지만 문제에서 요구하는 것은 숫자만이므로: **15**\n\n**핵심 포인트:**\n- `j += i`는 `j = j + i`와 같습니다 (누적 합계).\n- 반복문이 끝날 때 `j`는 0부터 5까지의 합인 15가 됩니다.\n\n**답:** **15**"
}

improved_explanations_2022 = {
    "Q002": "이 문제는 데이터베이스 **트랜잭션의 복구 기법**에 대한 문제입니다.\n\n**문제에서 설명하는 내용:**\n\n1. **오류가 발생하기 전까지의 사항을 로그로 기록해 놓고, 이전 상태로 되돌아간 후, 실패가 발생하기 전까지의 과정을 그대로 따라가는 현상**\n   - 이것은 **REDO (재실행)**입니다.\n   - 트랜잭션이 커밋된 후 갱신 사항이 데이터베이스에 반영되지 못한 경우\n   - 로그 파일의 기록을 이용하여 다시 실행하는 복구 방법\n\n2. **작업을 취소하여 트랜잭션을 이전 상태로 되돌리는 것**\n   - 이것은 **UNDO (취소)**입니다.\n   - 트랜잭션이 롤백될 때 변경 사항을 취소하는 복구 방법\n   - 변경 전 값으로 복원\n\n**REDO와 UNDO의 차이:**\n\n| 구분 | UNDO | REDO |\n|------|------|------|\n| 목적 | 트랜잭션 취소 | 트랜잭션 재실행 |\n| 시점 | 롤백 시 | 커밋 후 미반영 시 |\n| 방향 | 과거로 되돌림 | 앞으로 진행 |\n| 로그 | Before Image 사용 | After Image 사용 |\n\n**답:**\n- 1) **redo** (재실행)\n- 2) **undo** (취소)",
    
    "Q003": "이 Java 코드는 **클래스 객체의 참조 전달**과 **메서드를 통한 값 변경**을 이해하는 문제입니다.\n\n**코드 분석:**\n```java\nclass A {\n    int a;\n    int b;\n}\npublic class Main {\n    static void func1(A m){\n        m.a *= 10;\n    }\n    static void func2(A m){\n        m.a += m.b;\n    }\n    public static void main(String args[]){\n        A m = new A();\n        m.a = 100;\n        func1(m);\n        m.b = m.a;\n        func2(m);\n        System.out.printf(\"%d\", m.a);\n    }\n}\n```\n\n**실행 과정:**\n\n1. **객체 생성 및 초기화:**\n   - `A m = new A()` → `m.a = 0`, `m.b = 0` (기본값)\n   - `m.a = 100` → `m.a = 100`, `m.b = 0`\n\n2. **func1(m) 호출:**\n   - `m.a *= 10` → `m.a = 100 * 10 = 1000`\n   - 현재 상태: `m.a = 1000`, `m.b = 0`\n\n3. **m.b 값 설정:**\n   - `m.b = m.a` → `m.b = 1000`\n   - 현재 상태: `m.a = 1000`, `m.b = 1000`\n\n4. **func2(m) 호출:**\n   - `m.a += m.b` → `m.a = 1000 + 1000 = 2000`\n   - 현재 상태: `m.a = 2000`, `m.b = 1000`\n\n5. **출력:**\n   - `System.out.printf(\"%d\", m.a)` → **2000**\n\n**핵심 포인트:**\n- Java에서 객체는 참조로 전달되므로, 메서드 내에서 객체의 필드를 변경하면 원본 객체도 변경됩니다.\n- `m.a *= 10`은 `m.a = m.a * 10`과 같습니다.\n\n**답:** **2000**",
    
    "Q004": "이 문제는 **SQL ORDER BY 절**을 작성하는 문제입니다.\n\n**쿼리 분석:**\n```sql\nSELECT name, score FROM 성적\n(1) BY (2) (3)\n```\n\n**문제에서 요구하는 것:**\n- 결과를 점수(score) 기준으로 내림차순 정렬\n- ORDER BY 절 작성\n\n**ORDER BY 절:**\n- `ORDER BY 컬럼명 [ASC|DESC]`\n- `ASC`: 오름차순 (기본값, 생략 가능)\n- `DESC`: 내림차순\n\n**정답:**\n```sql\nSELECT name, score FROM 성적\nORDER BY score DESC\n```\n\n**빈칸 채우기:**\n- (1) **ORDER**: ORDER BY 절 시작\n- (2) **score**: 정렬할 컬럼명\n- (3) **DESC**: 내림차순 정렬\n\n**실행 결과:**\n점수가 높은 순서대로 학생 이름과 점수가 출력됩니다.\n\n**답:**\n- 1) **ORDER**\n- 2) **score**\n- 3) **DESC**",
    
    "Q005": "이 문제는 데이터베이스의 **삭제 이상(Deletion Anomaly)**에 대한 문제입니다.\n\n**삭제 이상이란?**\n- 데이터를 삭제할 때 **의도치 않은 다른 데이터도 함께 삭제**되는 이상 현상\n- 정규화되지 않은 테이블에서 발생하는 문제점 중 하나\n\n**삭제 이상의 예시:**\n\n예를 들어, 학생-과목 테이블에서:\n| 학번 | 이름 | 과목코드 | 과목명 |\n|------|------|----------|--------|\n| 001 | 김철수 | C101 | 데이터베이스 |\n| 001 | 김철수 | C102 | 운영체제 |\n| 002 | 이영희 | C101 | 데이터베이스 |\n\n만약 이영희가 데이터베이스 과목을 취소(삭제)하면:\n- 이영희의 행이 삭제됨\n- **문제**: C101(데이터베이스) 과목 정보도 함께 사라질 수 있음\n- 만약 C101을 듣는 학생이 이영희뿐이었다면, 과목 정보 자체가 삭제됨\n\n**해결 방법:**\n- 정규화를 통해 테이블을 분리\n- 학생 테이블, 과목 테이블, 수강 테이블로 분리\n\n**다른 이상 현상:**\n- **삽입 이상**: 데이터 삽입 시 불필요한 데이터도 함께 삽입해야 함\n- **갱신 이상**: 데이터 수정 시 여러 곳을 수정해야 하거나 일관성 문제 발생\n\n**답:** **삭제 이상**",
    
    "Q011": "이 Java 코드는 **Thread 클래스의 생성자**와 **Runnable 인터페이스 구현**을 이해하는 문제입니다.\n\n**코드 분석:**\n```java\nclass Car implements Runnable{\n    int a;\n    public void run(){\n        system.out.println(\"message\")\n    }\n}\npublic class Main{\n    public static void main(String args[]){\n        Thread t1 = new Thread(new ___());\n        t1.start();\n    }\n}\n```\n\n**문제 해결:**\n\n1. **Thread 생성자:**\n   - `Thread(Runnable target)`: Runnable 인터페이스를 구현한 객체를 받음\n   - `new Thread(new Car())` 형식으로 호출\n\n2. **Runnable 인터페이스:**\n   - `Car` 클래스가 `implements Runnable`로 구현\n   - `run()` 메서드를 구현하여 스레드가 실행할 작업 정의\n\n3. **빈칸에 들어갈 코드:**\n   - `new Thread(new Car())` → 빈칸은 **Car**\n   - `Car` 클래스의 인스턴스를 생성하여 Thread 생성자에 전달\n\n4. **실행 흐름:**\n   - `t1.start()` 호출 → 새 스레드 시작\n   - `Car` 클래스의 `run()` 메서드 실행\n   - \"message\" 출력\n\n**핵심 포인트:**\n- Thread는 Runnable 인터페이스를 구현한 객체를 받아 실행합니다.\n- `start()` 메서드로 스레드를 시작하면 `run()` 메서드가 자동 실행됩니다.\n\n**답:** **Car**"
}

def improve_file(filepath: Path, improvements: dict, year: str, round_num: str):
    """파일의 해설 개선"""
    questions = load_jsonl(filepath)
    updated_count = 0
    
    for q in questions:
        q_no = q['q_no']
        if q_no in improvements:
            q['explanation'] = improvements[q_no]
            q['meta']['last_improved'] = datetime.now().isoformat()
            updated_count += 1
    
    if updated_count > 0:
        # 백업
        backup_path = filepath.parent / "backups"
        backup_path.mkdir(exist_ok=True)
        backup_name = f"{filepath.stem}_before_improvement_{datetime.now().strftime('%Y%m%d_%H%M%S')}{filepath.suffix}"
        import shutil
        shutil.copy2(filepath, backup_path / backup_name)
        
        save_jsonl(filepath, questions)
        print(f"[개선] {filepath.name}: {updated_count}개 해설 개선 완료")
        return updated_count
    
    return 0

def main():
    print("=" * 80)
    print("범용적이거나 실질적이지 않은 해설 개선")
    print("=" * 80)
    
    data_dir = Path("data")
    total_improved = 0
    
    # 2021년 1회 개선
    filepath_2021 = data_dir / "items_2021_round1.jsonl"
    if filepath_2021.exists():
        count = improve_file(filepath_2021, improved_explanations_2021, "2021", "1")
        total_improved += count
    
    # 2022년 1회 개선
    filepath_2022 = data_dir / "items_2022_round1.jsonl"
    if filepath_2022.exists():
        count = improve_file(filepath_2022, improved_explanations_2022, "2022", "1")
        total_improved += count
    
    print(f"\n[완료] 총 {total_improved}개 해설 개선 완료")
    print("=" * 80)

if __name__ == "__main__":
    main()

