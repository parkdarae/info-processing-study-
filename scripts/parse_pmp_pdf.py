import sys
import re
import json

# PDF 텍스트를 직접 입력받아 파싱
def parse_pmp_text_from_stdin():
    """표준 입력으로부터 PDF 텍스트를 읽어 파싱"""
    
    # PMP 라벨 키워드 매핑
    KNOWLEDGE_AREAS = {
        'project_integration': ['통합', 'integration', '프로젝트 헌장', 'project charter', '변경통제', 'change control'],
        'project_scope': ['범위', 'scope', 'WBS', '요구사항', 'requirements'],
        'project_schedule': ['일정', 'schedule', 'CPM', 'PERT', '크리티컬패스', 'critical path'],
        'project_cost': ['원가', 'cost', '예산', 'budget', 'EVM', '획득가치', 'earned value'],
        'project_quality': ['품질', 'quality', 'QA', 'QC'],
        'project_resource': ['자원', 'resource', '팀', 'team', 'RACI'],
        'project_communication': ['의사소통', 'communication', '커뮤니케이션', '보고'],
        'project_risk': ['위험', 'risk', '리스크'],
        'project_procurement': ['조달', 'procurement', '계약', 'contract'],
        'project_stakeholder': ['이해관계자', 'stakeholder', '고객', 'customer']
    }
    
    PROCESS_GROUPS = {
        'initiating': ['착수', '시작', 'initiate'],
        'planning': ['기획', '계획', 'planning'],
        'executing': ['실행', 'executing', '수행'],
        'monitoring': ['감시', '통제', 'monitoring', 'controlling'],
        'closing': ['종료', 'closing', '완료']
    }
    
    IMAGE_INDICATORS = ['figure', 'diagram', 'chart', 'graph', 'table', '그림', '도표', '차트', '표']
    
    def classify_labels(text):
        """텍스트 기반 라벨 분류"""
        labels = []
        text_lower = text.lower()
        
        for label, keywords in KNOWLEDGE_AREAS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                labels.append(label)
                
        for label, keywords in PROCESS_GROUPS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                labels.append(label)
        
        return labels if labels else ['project_integration']
    
    def has_image(text):
        """이미지 포함 여부 확인"""
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in IMAGE_INDICATORS)
    
    # 표준 입력에서 전체 텍스트 읽기
    print("PDF 텍스트를 입력하세요 (Ctrl+D 또는 Ctrl+Z로 종료):", file=sys.stderr)
    full_text = sys.stdin.read()
    
    questions = []
    
    # 문제 패턴 매칭
    question_pattern = re.compile(r'(\d+)\.\s+([^]*?)(?=\d+\.\s+|$)', re.MULTILINE)
    matches = list(question_pattern.finditer(full_text))
    
    for match in matches:
        q_no = match.group(1)
        q_text = match.group(2).strip()
        
        # 이미지 포함 문제 제외
        if has_image(q_text):
            continue
        
        # 선택지 추출
        choice_pattern = re.compile(r'([A-D])[).]\s*([^\n]+)')
        choices = choice_pattern.findall(q_text)
        
        if len(choices) < 4:
            continue
        
        # 정답 추출
        answer_pattern = re.compile(r'(?:정답|Answer)[\s:：]+([A-D])', re.IGNORECASE)
        answer_match = answer_pattern.search(q_text)
        
        if not answer_match:
            continue
        
        answer = answer_match.group(1).upper()
        
        # 해설 추출
        explanation_pattern = re.compile(r'(?:해설|Explanation)[\s:：]+([^]*?)(?=\d+\.|$)', re.IGNORECASE)
        explanation_match = explanation_pattern.search(q_text)
        explanation = explanation_match.group(1).strip() if explanation_match else ''
        
        # 문제 본문 추출 (첫 선택지 이전까지)
        first_choice_pos = q_text.find(f'{choices[0][0]}')
        question_text = q_text[:first_choice_pos].strip() if first_choice_pos > 0 else q_text
        
        # 라벨 분류
        labels = classify_labels(question_text + ' ' + explanation)
        
        # 정답 텍스트
        answer_text = next((c[1] for c in choices if c[0] == answer), '')
        
        question_data = {
            'id': f'PMP{q_no.zfill(3)}',
            'q_no': q_no,
            'question': question_text,
            'options': [f'{c[0]}. {c[1]}' for c in choices],
            'answer': answer,
            'answer_text': answer_text,
            'explanation': explanation or '해설이 없습니다.',
            'labels': labels,
            'difficulty': 'medium',
            'source': 'PMP-2025.07.30.pdf',
            'type': 'multiple_choice'
        }
        
        questions.append(question_data)
    
    return questions

if __name__ == '__main__':
    try:
        questions = parse_pmp_text_from_stdin()
        
        # JSONL 형식으로 출력
        for q in questions:
            print(json.dumps(q, ensure_ascii=False))
        
        print(f"\n총 {len(questions)}개 문제 추출 완료", file=sys.stderr)
        
    except Exception as e:
        print(f"오류 발생: {e}", file=sys.stderr)
        sys.exit(1)

