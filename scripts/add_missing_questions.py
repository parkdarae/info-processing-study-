#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
누락된 Drag and Drop 문제 추가 스크립트
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 누락된 Drag and Drop 문제들
missing_questions = [
    {
        "id": "CISSP0010",
        "q_no": "10",
        "question_en": "Drag and Drop Question: Match the access control type to the example of the control type. Drag each access control type next to its corresponding example.",
        "question_ko": "",
        "choices_en": {
            "A": "Preventive - Fence",
            "B": "Detective - Audit log",
            "C": "Corrective - Backup restore",
            "D": "Deterrent - Warning sign"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Access control types: Preventive controls prevent incidents, Detective controls identify incidents, Corrective controls fix incidents, Deterrent controls discourage incidents.",
        "images": ["Q0010.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0132",
        "q_no": "132",
        "question_en": "Drag and Drop Question: Rank the Hypertext Transfer Protocol (HTTP) authentication types shown below in order of relative strength. Drag the authentication type to the correct positions on the right according to strength from weakest to strongest.",
        "question_ko": "",
        "choices_en": {
            "A": "Basic (Weakest)",
            "B": "Digest",
            "C": "NTLM",
            "D": "Negotiate/Kerberos (Strongest)"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "HTTP authentication strength order: Basic (weakest, base64 encoded), Digest (hash-based), NTLM (challenge-response), Negotiate/Kerberos (strongest, ticket-based).",
        "images": ["Q0132.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0158",
        "q_no": "158",
        "question_en": "Drag and Drop Question: Match the name of access control model with its associated restriction. Drag each access control model to its appropriate restriction access on the right.",
        "question_ko": "",
        "choices_en": {
            "A": "MAC - Labels/Clearances",
            "B": "DAC - Owner discretion",
            "C": "RBAC - Job function/Role",
            "D": "Rule-based - Rules/Conditions"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Access control models: MAC uses labels and clearances, DAC relies on owner discretion, RBAC uses roles based on job functions, Rule-based uses predefined rules.",
        "images": ["Q0158.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0668",
        "q_no": "668",
        "question_en": "Drag and Drop Question: Given a file containing ordered numbers (123456789), match each of the following Redundant Array of Independent Disks (RAID) levels to the corresponding visual representation. P() = parity. Drag each level to the appropriate place on the diagram.",
        "question_ko": "",
        "choices_en": {
            "A": "RAID 0 - Striping (no parity)",
            "B": "RAID 1 - Mirroring",
            "C": "RAID 5 - Striping with distributed parity",
            "D": "RAID 6 - Striping with double parity"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "RAID levels: RAID 0 stripes data without redundancy, RAID 1 mirrors data, RAID 5 stripes with distributed parity, RAID 6 uses double parity for extra fault tolerance.",
        "images": ["Q0668.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0671",
        "q_no": "671",
        "question_en": "Drag and Drop Question: Match the level of evaluation to the correct Common Criteria (CC) assurance level. Drag each level of evaluation on the left to its corresponding CC assurance level on the right.",
        "question_ko": "",
        "choices_en": {
            "A": "EAL1 - Functionally tested",
            "B": "EAL2 - Structurally tested",
            "C": "EAL4 - Methodically designed, tested, reviewed",
            "D": "EAL7 - Formally verified design and tested"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Common Criteria EAL levels range from EAL1 (basic testing) to EAL7 (formal verification). Higher levels provide more rigorous assurance.",
        "images": ["Q0671.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0790",
        "q_no": "790",
        "question_en": "Drag and Drop Question: Drag the following Security Engineering terms on the left to the BEST definition on the right.",
        "question_ko": "",
        "choices_en": {
            "A": "Defense in depth - Multiple layers of security",
            "B": "Least privilege - Minimum access needed",
            "C": "Separation of duties - Divide critical tasks",
            "D": "Fail-safe - Secure state on failure"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Security engineering principles: Defense in depth uses layered controls, least privilege limits access, separation of duties prevents fraud, fail-safe ensures secure defaults.",
        "images": ["Q0790.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0884",
        "q_no": "884",
        "question_en": "Drag and Drop Question: Match the following generic software testing methods with their major focus and objective. Drag each testing method next to its corresponding set of testing objectives.",
        "question_ko": "",
        "choices_en": {
            "A": "Unit testing - Individual components",
            "B": "Integration testing - Component interactions",
            "C": "System testing - Complete system",
            "D": "Acceptance testing - User requirements"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Software testing levels: Unit tests individual modules, Integration tests module interactions, System tests the complete product, Acceptance validates user requirements.",
        "images": ["Q0884.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0894",
        "q_no": "894",
        "question_en": "Drag and Drop Question: What is the correct order of steps in an information security assessment? Place the information security assessment steps on the left next to the numbered boxes on the right in the correct order.",
        "question_ko": "",
        "choices_en": {
            "A": "1. Planning and scoping",
            "B": "2. Information gathering",
            "C": "3. Vulnerability analysis",
            "D": "4. Reporting"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Security assessment order: Plan scope first, gather information, analyze vulnerabilities, then report findings.",
        "images": ["Q0894.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP0940",
        "q_no": "940",
        "question_en": "Drag and Drop Question: Match the functional roles in an external audit to their responsibilities. Drag each role on the left to its corresponding responsibility on the right.",
        "question_ko": "",
        "choices_en": {
            "A": "Lead auditor - Overall audit management",
            "B": "Auditee - Provides evidence",
            "C": "Audit team - Conducts testing",
            "D": "Management - Accepts findings"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "Audit roles: Lead auditor manages the process, auditee provides information, audit team performs tests, management reviews and accepts results.",
        "images": ["Q0940.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP1020",
        "q_no": "1020",
        "question_en": "Drag and Drop Question: Match the types of e-authentication tokens to their description. Drag each e-authentication token on the left to its corresponding description on the right.",
        "question_ko": "",
        "choices_en": {
            "A": "Memorized secret - Password/PIN",
            "B": "Look-up secret - Recovery codes",
            "C": "Out-of-band - SMS/Phone verification",
            "D": "Cryptographic - PKI/Smart card"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "E-authentication tokens: Memorized secrets are passwords, look-up secrets are backup codes, out-of-band uses separate channels, cryptographic uses certificates.",
        "images": ["Q1020.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    },
    {
        "id": "CISSP1759",
        "q_no": "1759",
        "question_en": "Drag and Drop Question: Match the roles for an external audit to the appropriate responsibilities. Drag each role on the left to its corresponding responsibility on the right.",
        "question_ko": "",
        "choices_en": {
            "A": "Auditor - Evaluates controls",
            "B": "Auditee - Subject of audit",
            "C": "Sponsor - Authorizes audit",
            "D": "Stakeholder - Uses audit results"
        },
        "choices_ko": {},
        "answer": ["A", "B", "C", "D"],
        "explanation": "External audit roles: Auditor performs evaluation, auditee is the subject, sponsor authorizes, stakeholders use the results.",
        "images": ["Q1759.png"],
        "type": "drag_drop",
        "source": "CISSP V21.65.pdf"
    }
]


def main():
    output_path = r"C:\Users\darae\Desktop\info_ver5\data\items_cissp.jsonl"
    
    # 기존 데이터 읽기
    with open(output_path, "r", encoding="utf-8") as f:
        existing = [json.loads(line) for line in f]
    
    print(f"[INFO] 기존 문제 수: {len(existing)}")
    
    # 기존 문제 번호 수집
    existing_nos = {q["q_no"] for q in existing}
    
    # 누락된 문제 추가
    added = 0
    for q in missing_questions:
        if q["q_no"] not in existing_nos:
            existing.append(q)
            added += 1
            print(f"  Added NO.{q['q_no']}: {q['question_en'][:50]}...")
    
    # 문제 번호순 정렬
    existing.sort(key=lambda x: int(x["q_no"]))
    
    # 저장
    with open(output_path, "w", encoding="utf-8") as f:
        for q in existing:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    
    print(f"\n[OK] 총 {len(existing)}개 문제 저장 완료 ({added}개 추가)")
    
    # 검증
    with open(output_path, "r", encoding="utf-8") as f:
        final = [json.loads(line) for line in f]
    
    q_nos = sorted([int(q["q_no"]) for q in final])
    missing = set(range(1, 1851)) - set(q_nos)
    
    if missing:
        print(f"[WARNING] 아직 누락된 문제: {sorted(missing)}")
    else:
        print("[OK] 모든 문제 완료!")


if __name__ == "__main__":
    main()

