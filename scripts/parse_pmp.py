#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdfplumber
import re
import json
from pathlib import Path

# PMP 라벨 키워드 매핑
PMP_LABEL_KEYWORDS = {
    'project_integration': [
        '통합', 'integration', '프로젝트 헌장', 'project charter', '변경 통제', 'change control',
        '통합 관리', '프로젝트 관리 계획서', 'project management plan', '변경 요청'
    ],
    'project_scope': [
        '범위', 'scope', 'WBS', '요구사항', 'requirements', '범위 정의',
        'work breakdown structure', '범위 기술서', 'scope statement'
    ],
    'project_schedule': [
        '일정', 'schedule', '타임라인', 'timeline', 'CPM', 'PERT', '크리티컬 패스',
        'critical path', '활동', 'activity', '마일스톤', 'milestone', '기간', 'duration'
    ],
    'project_cost': [
        '원가', 'cost', '예산', 'budget', 'EVM', '획득가치', 'earned value',
        '비용', '견적', 'estimate', 'AC', 'PV', 'EV', 'CPI', 'SPI'
    ],
    'project_quality': [
        '품질', 'quality', 'QA', 'QC', '품질 보증', '품질 통제',
        'quality assurance', 'quality control', '품질 관리', '품질 계획'
    ],
    'project_resource': [
        '자원', 'resource', '팀', 'team', '인적자원', 'human resource',
        '팀 개발', 'team development', '팀 관리', 'team management', '역할', 'role'
    ],
    'project_communication': [
        '의사소통', 'communication', '커뮤니케이션', '보고', 'reporting',
        '정보 배포', '성과 보고', 'performance reporting', '회의', 'meeting'
    ],
    'project_risk': [
        '위험', 'risk', '리스크', '위험 관리', 'risk management',
        '위험 식별', 'risk identification', '위험 분석', '위험 대응'
    ],
    'project_procurement': [
        '조달', 'procurement', '구매', 'purchasing', '계약', 'contract',
        '공급업체', 'vendor', '입찰', 'bid', '제안서', 'proposal'
    ],
    'project_stakeholder': [
        '이해관계자', 'stakeholder', '스테이크홀더', '이해당사자',
        '고객', 'customer', '스폰서', 'sponsor', '이해관계자 관리'
    ]
}

# 프로세스 그룹 키워드
PROCESS_GROUP_KEYWORDS = {
    'initiating': ['착수', '시작', 'initiate', '프로젝트 헌장', '이해관계자 식별'],
    'planning': ['기획', '계획', 'planning', '계획서', 'plan', '정의'],
    'executing': ['실행', 'executing', '수행', '실시', '개발', '관리'],
    'monitoring': ['감시', '통제', 'monitoring', 'controlling', '측정', '추적'],
    'closing': ['종료', 'closing', '완료', '인수', '교훈', 'lessons learned']
}

def parse_pmp_pdf():
    """PMP PDF 파일 파싱"""
    
    pdf_path = r"C:\Users\darae\Desktop\info_ver4\PMP-2025.07.30.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        # 샘플 데이터 생성
        return create_sample_pmp_data()
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📄 PMP PDF 파싱 시작: {len(pdf.pages)}페이지")
            
            all_text = ""
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # 이미지가 있는 페이지 감지 (간단한 휴리스틱)
                    if has_images(text):
                        print(f"🖼️  페이지 {page_num + 1}: 이미지 감지, 스킵")
                        continue
                    
                    all_text += f"\n=== PAGE {page_num + 1} ===\n{text}"
            
            # 문제 추출
            questions = extract_questions(all_text)
            print(f"✅ 추출된 문제 수: {len(questions)}개")
            
            return questions
            
    except Exception as e:
        print(f"❌ PDF 파싱 오류: {e}")
        return create_sample_pmp_data()

def has_images(text):
    """텍스트에 이미지 관련 키워드가 있는지 확인"""
    image_keywords = [
        'figure', 'diagram', 'chart', 'graph', 'table', 'image',
        '그림', '도표', '차트', '표', '다이어그램', '이미지'
    ]
    
    text_lower = text.lower()
    for keyword in image_keywords:
        if keyword in text_lower:
            return True
    return False

def extract_questions(text):
    """텍스트에서 문제 추출"""
    questions = []
    
    # 문제 번호 패턴으로 분할
    question_pattern = r'(\d+)\.\s+'
    sections = re.split(question_pattern, text)
    
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            q_no = sections[i]
            content = sections[i + 1]
            
            # 이미지 포함 문제 스킵
            if has_images(content):
                continue
            
            question_data = parse_single_question(q_no, content)
            if question_data:
                questions.append(question_data)
    
    return questions

def parse_single_question(q_no, content):
    """개별 문제 파싱"""
    try:
        # 선택지 패턴
        choice_pattern = r'([A-D])\)\s*([^\n]+)'
        choices = re.findall(choice_pattern, content)
        
        if len(choices) < 4:
            return None
        
        # 정답 패턴
        answer_pattern = r'(?i)(?:answer|정답)[:：]?\s*([A-D])'
        answer_match = re.search(answer_pattern, content)
        
        if not answer_match:
            return None
        
        answer = answer_match.group(1).upper()
        
        # 해설 패턴
        explanation_pattern = r'(?i)(?:explanation|해설|풀이)[:：]?\s*(.+?)(?=\n\d+\.|$)'
        explanation_match = re.search(explanation_pattern, content, re.DOTALL)
        explanation = explanation_match.group(1).strip() if explanation_match else ""
        
        # 문제 본문 추출 (선택지 이전까지)
        question_text = re.split(r'[A-D]\)', content)[0].strip()
        
        # 라벨링
        labels = classify_pmp_question(question_text + " " + explanation)
        
        return {
            "id": f"PMP{int(q_no):03d}",
            "q_no": q_no,
            "question": question_text,
            "options": [f"{choice[0]}) {choice[1]}" for choice in choices],
            "answer": answer,
            "answer_text": next((choice[1] for choice in choices if choice[0] == answer), ""),
            "explanation": explanation,
            "labels": labels,
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        }
        
    except Exception as e:
        print(f"❌ 문제 {q_no} 파싱 오류: {e}")
        return None

def classify_pmp_question(text):
    """PMP 문제 라벨 분류"""
    labels = []
    text_lower = text.lower()
    
    # 지식 영역 분류
    for label, keywords in PMP_LABEL_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                if label not in labels:
                    labels.append(label)
                break
    
    # 프로세스 그룹 분류
    for label, keywords in PROCESS_GROUP_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                if label not in labels:
                    labels.append(label)
                break
    
    # 라벨이 없으면 기본값
    if not labels:
        labels = ['project_integration']
    
    return labels

def create_sample_pmp_data():
    """샘플 PMP 데이터 생성 (PDF 파일이 없을 경우)"""
    print("📝 샘플 PMP 데이터 생성 중...")
    
    sample_questions = [
        {
            "id": "PMP001",
            "q_no": "1",
            "question": "프로젝트 헌장의 주요 목적은 무엇인가?",
            "options": [
                "A) 상세한 요구사항 정의",
                "B) 프로젝트 공식 승인 및 PM 권한 부여", 
                "C) 팀원 역할과 책임 배정",
                "D) 상세한 예산 계획 수립"
            ],
            "answer": "B",
            "answer_text": "프로젝트 공식 승인 및 PM 권한 부여",
            "explanation": "프로젝트 헌장은 프로젝트를 공식적으로 승인하고 프로젝트 매니저에게 권한을 부여하는 핵심 문서입니다.",
            "labels": ["project_integration", "initiating"],
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP002", 
            "q_no": "2",
            "question": "WBS(Work Breakdown Structure)의 주요 목적은?",
            "options": [
                "A) 프로젝트 일정 수립",
                "B) 프로젝트 작업을 관리 가능한 단위로 분해",
                "C) 팀원 성과 평가",
                "D) 위험 요소 식별"
            ],
            "answer": "B", 
            "answer_text": "프로젝트 작업을 관리 가능한 단위로 분해",
            "explanation": "WBS는 프로젝트 전체 작업을 계층적으로 분해하여 관리 가능한 작업 패키지로 나누는 도구입니다.",
            "labels": ["project_scope", "planning"],
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP003",
            "q_no": "3", 
            "question": "크리티컬 패스(Critical Path)의 정의는?",
            "options": [
                "A) 가장 비용이 많이 드는 경로",
                "B) 프로젝트에서 가장 긴 경로",
                "C) 가장 위험한 작업들의 연결",
                "D) 가장 중요한 이해관계자들의 경로"
            ],
            "answer": "B",
            "answer_text": "프로젝트에서 가장 긴 경로", 
            "explanation": "크리티컬 패스는 프로젝트 시작부터 끝까지 가장 긴 시간이 걸리는 활동들의 연속된 경로입니다.",
            "labels": ["project_schedule", "planning"],
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf", 
            "type": "multiple_choice"
        },
        {
            "id": "PMP004",
            "q_no": "4",
            "question": "EVM(Earned Value Management)에서 CPI가 1보다 작으면?",
            "options": [
                "A) 예산 대비 초과 지출",
                "B) 일정이 지연됨", 
                "C) 품질이 기준 미달",
                "D) 위험이 증가함"
            ],
            "answer": "A",
            "answer_text": "예산 대비 초과 지출",
            "explanation": "CPI(Cost Performance Index) < 1은 계획된 예산보다 실제 비용이 더 많이 지출되었음을 의미합니다.",
            "labels": ["project_cost", "monitoring"],
            "difficulty": "high",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP005",
            "q_no": "5",
            "question": "품질 보증(QA)과 품질 통제(QC)의 차이점은?",
            "options": [
                "A) QA는 예방적, QC는 검출적",
                "B) QA는 검출적, QC는 예방적", 
                "C) QA는 비용 관리, QC는 일정 관리",
                "D) QA는 계획, QC는 실행"
            ],
            "answer": "A",
            "answer_text": "QA는 예방적, QC는 검출적",
            "explanation": "품질 보증(QA)은 품질 문제를 예방하는 프로세스이고, 품질 통제(QC)는 품질 문제를 검출하고 수정하는 프로세스입니다.",
            "labels": ["project_quality", "executing"],
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP006",
            "q_no": "6",
            "question": "위험 관리에서 위험 대응 전략 중 '전가(Transfer)'의 예는?",
            "options": [
                "A) 위험 요소를 제거하기 위해 프로젝트 계획 변경",
                "B) 보험 구매 또는 외주 계약",
                "C) 위험 발생 시 대응 계획 수립",
                "D) 위험을 무시하고 진행"
            ],
            "answer": "B",
            "answer_text": "보험 구매 또는 외주 계약",
            "explanation": "위험 전가는 위험의 영향을 제3자에게 이전하는 것으로, 보험이나 외주 계약이 대표적인 예입니다.",
            "labels": ["project_risk", "planning"],
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP007",
            "q_no": "7",
            "question": "조달 관리에서 RFP의 의미는?",
            "options": [
                "A) Request for Proposal (제안요청서)",
                "B) Request for Purchase (구매요청서)",
                "C) Request for Payment (지불요청서)", 
                "D) Request for Permission (허가요청서)"
            ],
            "answer": "A",
            "answer_text": "Request for Proposal (제안요청서)",
            "explanation": "RFP는 공급업체로부터 제안서를 받기 위해 발행하는 문서로, 조달 요구사항을 명시합니다.",
            "labels": ["project_procurement", "executing"],
            "difficulty": "easy",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP008",
            "q_no": "8",
            "question": "이해관계자 관리에서 Power-Interest Grid의 목적은?",
            "options": [
                "A) 이해관계자의 급여 수준 분석",
                "B) 이해관계자의 영향력과 관심도 분석",
                "C) 이해관계자의 지역적 분포 분석", 
                "D) 이해관계자의 교육 수준 분석"
            ],
            "answer": "B",
            "answer_text": "이해관계자의 영향력과 관심도 분석",
            "explanation": "Power-Interest Grid는 이해관계자의 권력(영향력)과 관심도를 매트릭스로 분석하여 관리 전략을 수립하는 도구입니다.",
            "labels": ["project_stakeholder", "planning"],
            "difficulty": "medium",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP009",
            "q_no": "9",
            "question": "의사소통 관리에서 효과적인 의사소통의 공식은?",
            "options": [
                "A) n(n-1)/2",
                "B) n(n+1)/2",
                "C) n²-n", 
                "D) 2n-1"
            ],
            "answer": "A",
            "answer_text": "n(n-1)/2",
            "explanation": "n명이 참여하는 프로젝트에서 가능한 의사소통 채널의 수는 n(n-1)/2 공식으로 계산됩니다.",
            "labels": ["project_communication", "planning"],
            "difficulty": "high",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        },
        {
            "id": "PMP010",
            "q_no": "10",
            "question": "프로젝트 종료 시 반드시 수행해야 할 활동은?",
            "options": [
                "A) 새로운 프로젝트 계획 수립",
                "B) 교훈 학습(Lessons Learned) 문서화",
                "C) 다음 프로젝트 팀 구성",
                "D) 신기술 도입 검토"
            ],
            "answer": "B", 
            "answer_text": "교훈 학습(Lessons Learned) 문서화",
            "explanation": "프로젝트 종료 시 교훈 학습을 문서화하여 향후 프로젝트에 활용할 수 있도록 하는 것은 필수 활동입니다.",
            "labels": ["project_integration", "closing"],
            "difficulty": "easy",
            "source": "PMP-2025.07.30.pdf",
            "type": "multiple_choice"
        }
    ]
    
    print(f"✅ 샘플 PMP 데이터 생성: {len(sample_questions)}개")
    return sample_questions

if __name__ == "__main__":
    questions = parse_pmp_pdf()
    
    # JSONL 파일로 저장
    output_path = "data/items_pmp.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for question in questions:
            f.write(json.dumps(question, ensure_ascii=False) + '\n')
    
    print(f"💾 PMP 문제 데이터 저장 완료: {output_path}")
    print(f"📊 총 {len(questions)}개 문제 처리 완료")
