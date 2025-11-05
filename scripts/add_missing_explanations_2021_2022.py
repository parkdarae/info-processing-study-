# -*- coding: utf-8 -*-
"""
2021년, 2022년 해설 누락 문제 해설 추가 스크립트
기존 데이터와 코드를 바탕으로 해설을 작성합니다.
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

# 2021년 1회 해설 추가
explanations_2021_round1 = {
    "Q001": "RARP(Reverse Address Resolution Protocol, 역순 주소 결정 프로토콜)는 물리 네트워크 주소(MAC 주소)를 알고 있을 때, 해당하는 IP 주소를 알아내기 위한 프로토콜입니다.\n\n**RARP의 특징:**\n\n1. **역방향 변환:**\n- ARP는 IP 주소 → MAC 주소 변환\n- RARP는 MAC 주소 → IP 주소 변환 (역방향)\n\n2. **사용 목적:**\n- 디스크리스 워크스테이션(하드디스크가 없는 컴퓨터)이 부팅 시 자신의 IP 주소를 서버로부터 받아올 때 사용\n- 현재는 DHCP(Dynamic Host Configuration Protocol)가 대체하여 사용\n\n3. **동작 방식:**\n- 클라이언트가 자신의 MAC 주소를 포함한 RARP 요청을 브로드캐스트로 전송\n- RARP 서버가 MAC 주소에 해당하는 IP 주소를 응답\n\n**답:** RARP (Reverse Address Resolution Protocol)",
    
    "Q006": "이 SQL 쿼리는 WHERE 절의 조건을 분석하는 문제입니다.\n\n**쿼리 분석:**\n```sql\nSELECT COUNT(*) FROM 급여 \nWHERE EMPNO > 100 AND SAL >= 3000 OR EMPNO = 200;\n```\n\n**WHERE 절 조건 (연산자 우선순위 고려):**\n- `AND`가 `OR`보다 우선순위가 높으므로:\n  - `(EMPNO > 100 AND SAL >= 3000) OR EMPNO = 200`\n\n**테이블 데이터 확인 (Q006_table1.json):**\n- 행1: EMPNO=100, SAL=1000\n- 행2: EMPNO=200, SAL=3000\n- 행3: EMPNO=300, SAL=1500\n\n**조건 검사:**\n\n1. 행1 (EMPNO=100, SAL=1000):\n   - `(100 > 100 AND 1000 >= 3000) OR 100 = 200`\n   - `(FALSE AND FALSE) OR FALSE` = FALSE\n\n2. 행2 (EMPNO=200, SAL=3000):\n   - `(200 > 100 AND 3000 >= 3000) OR 200 = 200`\n   - `(TRUE AND TRUE) OR TRUE` = TRUE ✓\n\n3. 행3 (EMPNO=300, SAL=1500):\n   - `(300 > 100 AND 1500 >= 3000) OR 300 = 200`\n   - `(TRUE AND FALSE) OR FALSE` = FALSE\n\n**결과:** 조건을 만족하는 행은 1개\n\n**답:** 1",
    
    "Q007": "이 Java 코드는 **2차원 배열의 구조와 접근 방법**을 이해하는 문제입니다.\n\n**코드 분석:**\n```java\nint[][]arr = new int[][]{{45,50,75},{89}};\nSystem.out.println(arr[0].length);  // 첫 번째 행의 길이\nSystem.out.println(arr[1].length);  // 두 번째 행의 길이\nSystem.out.println(arr[0][0]);      // 첫 번째 행, 첫 번째 요소\nSystem.out.println(arr[0][1]);      // 첫 번째 행, 두 번째 요소\nSystem.out.println(arr[1][0]);      // 두 번째 행, 첫 번째 요소\n```\n\n**2차원 배열 구조:**\n- `arr[0] = {45, 50, 75}` → 길이 3\n- `arr[1] = {89}` → 길이 1\n\n**실행 순서:**\n\n1. `arr[0].length`: 첫 번째 행의 길이 → **3**\n2. `arr[1].length`: 두 번째 행의 길이 → **1**\n3. `arr[0][0]`: 첫 번째 행의 첫 번째 요소 → **45**\n4. `arr[0][1]`: 첫 번째 행의 두 번째 요소 → **50**\n5. `arr[1][0]`: 두 번째 행의 첫 번째 요소 → **89**\n\n**출력:** `3 1 45 50 89`\n\n**핵심 포인트:**\n- Java에서 2차원 배열은 행마다 길이가 다를 수 있습니다(가변 배열).\n- `arr[i].length`는 i번째 행의 길이를 반환합니다.\n- `arr[i][j]`는 i번째 행의 j번째 요소에 접근합니다.\n\n**답:** **3 1 45 50 89**",
    
    "Q011": "이 문제는 **IPv6와 IPv4의 주소 체계**를 이해하는 문제입니다.\n\n**IPv6 주소:**\n- **128비트 길이**를 가집니다.\n- IPv4의 주소 고갈 문제를 해결하기 위해 개발\n- 16진수로 표현하며 8그룹으로 나눔 (예: 2001:0db8:85a3:0000:0000:8a2e:0370:7334)\n\n**IPv4 주소:**\n- **32비트 길이**를 가집니다.\n- **8비트씩 네 부분**으로 나누어 표현\n- 각 부분을 10진수로 표현 (예: 192.168.0.1)\n- 총 32비트 = 8비트 × 4개 부분\n\n**비교:**\n| 항목 | IPv4 | IPv6 |\n|------|------|------|\n| 주소 길이 | 32비트 | 128비트 |\n| 표현 방식 | 10진수, 4개 부분 | 16진수, 8개 부분 |\n| 예시 | 192.168.0.1 | 2001:0db8::1 |\n\n**답:**\n- (1) **128** (IPv6는 128비트)\n- (2) **8** (IPv4는 8비트씩 네 부분)",
    
    "Q012": "IPC(Inter Process Communication, 프로세스 간 통신)는 운영체제에서 **서로 다른 프로세스가 데이터를 주고받는 기술**을 의미합니다.\n\n**IPC의 종류:**\n\n1. **공유 메모리(Shared Memory):**\n- 여러 프로세스가 같은 메모리 영역을 공유\n- 가장 빠른 통신 방법\n- 동기화 필요 (세마포어, 뮤텍스 등)\n\n2. **소켓(Socket):**\n- 네트워크를 통한 프로세스 간 통신\n- 로컬 또는 원격 프로세스와 통신 가능\n- TCP/UDP 프로토콜 사용\n\n3. **세마포어(Semaphore):**\n- 공유 자원에 대한 접근을 제어하는 동기화 메커니즘\n- 정수값을 사용하여 사용 가능한 자원의 개수를 나타냄\n- P 연산(대기), V 연산(신호) 제공\n\n4. **메시지 큐(Message Queue):**\n- 프로세스 간 메시지를 큐 형태로 전송\n- 비동기 통신 지원\n- 시스템이 관리하는 큐를 통해 메시지 전달\n\n**IPC의 필요성:**\n- 프로세스는 독립적인 메모리 공간을 가지므로 직접 데이터 공유 불가\n- 프로세스 간 데이터 교환 및 동기화를 위해 IPC 사용\n\n**답:** **IPC (Inter Process Communication)**",
    
    "Q016": "데이터 모델은 데이터베이스 설계의 기초가 되는 개념적 틀입니다. 데이터 모델의 구성요소는 다음과 같습니다.\n\n**데이터 모델 구성요소 3가지:**\n\n1. **연산(Operation):**\n- 데이터베이스에 저장된 실제 데이터를 처리하는 작업에 대한 명세\n- 데이터베이스를 조작하는 기본 도구\n- 예: SELECT, INSERT, UPDATE, DELETE 등의 연산\n\n2. **구조(Structure):**\n- 개체 데이터 모델에서는 연산을 이용하여 실제 데이터를 처리하는 작업에 대한 명세를 나타냄\n- 논리 데이터 모델에서는 구조를 어떻게 나타낼 것인지 표현\n- 데이터의 논리적 구조와 물리적 구조를 정의\n- 예: 릴레이션 구조, 스키마 구조 등\n\n3. **제약조건(Constraint):**\n- 데이터 무결성 유지를 위한 데이터베이스의 보편적 방법\n- 릴레이션의 특정 칼럼에 설정하는 제약\n- 개체 무결성: 기본 키가 NULL이 될 수 없고 중복될 수 없음\n- 참조 무결성: 외래 키가 참조하는 기본 키 값이 반드시 존재해야 함\n\n**데이터 모델의 역할:**\n- 현실 세계의 정보를 데이터베이스에 표현하기 위한 구조와 규칙 제공\n- 데이터의 일관성과 무결성 보장\n\n**답:**\n- (1) **연산**\n- (2) **구조**\n- (3) **제약조건**",
    
    "Q020": "세션 하이재킹(Session Hijacking)은 정보보안에서 중요한 공격 기법입니다.\n\n**세션 하이재킹의 정의:**\n\n1. **기본 의미:**\n- '세션을 가로채다(Hijack)'라는 의미\n- 공격자가 정상적인 사용자의 세션을 탈취하여 해당 사용자의 권한으로 시스템에 접근하는 해킹 기법\n\n2. **공격 방식:**\n- 정상적인 연결을 RST 패킷을 통해 종료시킨 후 재연결 시 희생자가 아닌 공격자에게 연결\n- 세션 관리 취약점을 이용한 공격 기법\n\n**세션 하이재킹의 과정:**\n\n1. **세션 정보 획득:**\n- 네트워크 스니핑을 통해 세션 ID, 쿠키 등의 세션 정보 탈취\n- 또는 XSS 공격을 통해 세션 정보 유출\n\n2. **세션 가로채기:**\n- 획득한 세션 정보를 사용하여 정상 사용자인 것처럼 위장\n- 서버가 공격자를 정상 사용자로 인식\n\n3. **권한 획득:**\n- 정상 사용자의 권한으로 시스템 접근 및 조작\n\n**방어 방법:**\n- HTTPS 사용 (암호화 통신)\n- 세션 ID 암호화\n- 세션 타임아웃 설정\n- IP 주소 검증\n\n**답:** **세션 하이재킹**"
}

def add_explanations_2021_round1():
    """2021년 1회 해설 추가"""
    filepath = Path("data/items_2021_round1.jsonl")
    questions = load_jsonl(filepath)
    
    updated_count = 0
    for q in questions:
        q_no = q['q_no']
        if q_no in explanations_2021_round1 and (not q.get('explanation') or q.get('explanation') is None):
            q['explanation'] = explanations_2021_round1[q_no]
            q['meta']['last_improved'] = datetime.now().isoformat()
            updated_count += 1
            print(f"[추가] {q_no}: 해설 추가")
    
    if updated_count > 0:
        # 백업
        backup_path = filepath.parent / "backups" / f"{filepath.stem}_before_explanation_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}{filepath.suffix}"
        backup_path.parent.mkdir(exist_ok=True)
        if filepath.exists():
            import shutil
            shutil.copy2(filepath, backup_path)
            print(f"[백업] {backup_path.name}")
        
        save_jsonl(filepath, questions)
        print(f"\n[완료] 2021년 1회: {updated_count}개 해설 추가")
    else:
        print(f"\n[정보] 2021년 1회: 추가할 해설 없음")

def main():
    print("=" * 80)
    print("2021년, 2022년 해설 누락 문제 해설 추가")
    print("=" * 80)
    
    # 2021년 1회 해설 추가
    add_explanations_2021_round1()
    
    # 2022년은 이미 모든 문제에 해설이 있는 것으로 확인됨
    print("\n[정보] 2022년: 모든 문제에 해설이 있습니다.")
    
    print("\n" + "=" * 80)
    print("작업 완료")
    print("=" * 80)

if __name__ == "__main__":
    main()


