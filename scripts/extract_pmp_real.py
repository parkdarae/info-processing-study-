"""
PMP PDF 실제 파싱 스크립트
pdfplumber를 사용하여 PDF에서 문제/답/해설 추출
"""

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요: pip install pdfplumber")
    exit(1)

import re
import json
from pathlib import Path

# PMP 라벨 키워드 매핑
KNOWLEDGE_AREAS = {
    'project_integration': ['통합', 'integration', '프로젝트 헌장', 'project charter', '변경통제', 'change control', '변경 관리'],
    'project_scope': ['범위', 'scope', 'WBS', '요구사항', 'requirements', '범위정의'],
    'project_schedule': ['일정', 'schedule', 'CPM', 'PERT', '크리티컬패스', 'critical path', '활동', 'activity'],
    'project_cost': ['원가', 'cost', '예산', 'budget', 'EVM', '획득가치', 'earned value', 'CPI', 'SPI'],
    'project_quality': ['품질', 'quality', 'QA', 'QC', '품질보증', '품질통제'],
    'project_resource': ['자원', 'resource', '팀', 'team', '인적자원', 'RACI', '역할'],
    'project_communication': ['의사소통', 'communication', '커뮤니케이션', '보고', 'reporting'],
    'project_risk': ['위험', 'risk', '리스크', '위험관리', '몬테카를로'],
    'project_procurement': ['조달', 'procurement', '계약', 'contract', 'RFP', '구매'],
    'project_stakeholder': ['이해관계자', 'stakeholder', '고객', 'customer', '스폰서']
}

PROCESS_GROUPS = {
    'initiating': ['착수', '시작', 'initiate', '프로젝트헌장'],
    'planning': ['기획', '계획', 'planning', '계획서', '정의', '수립'],
    'executing': ['실행', 'executing', '수행', '실시'],
    'monitoring': ['감시', '통제', 'monitoring', 'controlling', '측정'],
    'closing': ['종료', 'closing', '완료', '인수']
}

IMAGE_INDICATORS = [
    'figure', 'diagram', 'chart', 'graph', 'table', 'image',
    '그림', '도표', '차트', '표', '다이어그램', '도식',
    'see figure', 'refer to', '아래 그림', '다음 도표',
    'shown below', 'illustrated', 'depicted',
    '아래에 나타낸', '다음과 같이', '보기와 같이',
    'network diagram', 'gantt', 'flowchart', 'organizational chart',
    '네트워크 다이어그램', '간트', '흐름도', '조직도'
]

def classify_labels(text):
    """텍스트 기반 PMP 라벨 분류"""
    labels = []
    text_lower = text.lower()
    
    # 지식 영역 분류
    for label, keywords in KNOWLEDGE_AREAS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            if label not in labels:
                labels.append(label)
    
    # 프로세스 그룹 분류
    for label, keywords in PROCESS_GROUPS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            if label not in labels:
                labels.append(label)
    
    # 기본값
    if not labels:
        labels.append('project_integration')
    
    return labels

def has_image(text):
    """이미지 포함 여부 확인 (더 엄격한 검사)"""
    text_lower = text.lower()
    
    # 명확한 이미지 지시어가 있는 경우
    for indicator in IMAGE_INDICATORS:
        if indicator.lower() in text_lower:
            return True
    
    # "보기" 다음에 숫자나 항목이 나열되는 경우 (이미지일 가능성)
    if re.search(r'보기.*?[①②③④⑤⑥]', text_lower):
        return True
    
    # "다음 중", "아래", "위" 등 + 그림/도표/차트 조합
    if re.search(r'(다음|아래|위|following).{0,20}(그림|도표|차트|diagram|figure)', text_lower):
        return True
    
    return False

def extract_text_from_pdf(pdf_path):
    """PDF에서 전체 텍스트 추출"""
    full_text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"총 {len(pdf.pages)} 페이지 읽는 중...")
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
            if i % 10 == 0:
                print(f"  {i} 페이지 처리 완료...")
    
    return full_text

def parse_questions(text):
    """텍스트에서 문제 파싱"""
    questions = []
    
    # 문제 번호로 분리 (여러 패턴 시도)
    patterns = [
        r'No\.\s*(\d+)\s+(.*?)(?=No\.\s*\d+|$)',  # No. 1, No. 2
        r'(\d+)\.\s+(.*?)(?=\d+\.\s+|$)',  # 1. 2. 3.
        r'문제\s*(\d+)[.:]\s*(.*?)(?=문제\s*\d+|$)',  # 문제 1: 문제 2:
        r'Q(\d+)[.:]\s*(.*?)(?=Q\d+|$)',  # Q1: Q2:
    ]
    
    matches = []
    for pattern in patterns:
        matches = list(re.finditer(pattern, text, re.MULTILINE | re.DOTALL))
        if matches:
            print(f"패턴 매칭 성공: {len(matches)}개 문제 발견")
            break
    
    if not matches:
        print("[경고] 문제 패턴을 찾을 수 없습니다.")
        return questions
    
    for match in matches:
        try:
            q_no = match.group(1)
            q_text = match.group(2).strip()
            
            # 이미지 포함 문제 제외
            if has_image(q_text):
                print(f"  문제 {q_no}: 이미지 감지, 제외")
                continue
            
            # 선택지 추출 (개선된 패턴)
            # A. B. C. D. 형식 (점 뒤에 공백 있음)
            choice_pattern = r'([A-E])\.\s+([^\n]+?)(?=\s*[A-E]\.\s+|\s*정답:|\s*No\.\s*\d+|$)'
            choices = re.findall(choice_pattern, q_text, re.DOTALL)
            
            # 선택지가 부족하면 다른 패턴 시도
            if len(choices) < 4:
                # A) B) C) D) 형식
                choice_pattern = r'([A-E])\)\s+([^\n]+?)(?=\s*[A-E]\)\s+|\s*정답:|\s*No\.\s*\d+|$)'
                choices = re.findall(choice_pattern, q_text, re.DOTALL)
            
            if len(choices) < 4:
                print(f"  문제 {q_no}: 선택지 부족 ({len(choices)}개)")
                continue
            
            # 정답 추출 (복수 정답 지원)
            answer_patterns = [
                r'정답[\s:：]+([A-D, ]+)',  # 정답: A, B, C 형식
                r'(?:정답|Answer)[\s:：]+([A-D①②③④1-4])',
                r'정답\s*[:\-]\s*([A-D①②③④1-4])',
                r'Correct\s*Answer[\s:：]+([A-D])',
            ]
            
            answer = None
            for ap in answer_patterns:
                answer_match = re.search(ap, q_text, re.IGNORECASE)
                if answer_match:
                    answer_raw = answer_match.group(1).upper().strip()
                    
                    # 복수 정답 처리 (A, B, C 형식)
                    if ',' in answer_raw:
                        # 첫 번째 정답만 사용 (복수 정답은 나중에 병합 시 처리)
                        answer = answer_raw.split(',')[0].strip()
                    else:
                        answer = answer_raw
                    
                    # 번호를 문자로 변환
                    if answer == '①' or answer == '1': answer = 'A'
                    elif answer == '②' or answer == '2': answer = 'B'
                    elif answer == '③' or answer == '3': answer = 'C'
                    elif answer == '④' or answer == '4': answer = 'D'
                    break
            
            if not answer or answer not in ['A', 'B', 'C', 'D', 'E']:
                print(f"  문제 {q_no}: 정답 없음 또는 형식 오류")
                continue
            
            # 해설 추출
            explanation_patterns = [
                r'(?:해설|Explanation)[\s:：]+(.*?)(?=\d+\.|문제\s*\d+|Q\d+|$)',
                r'해설\s*[:\-]\s*(.*?)(?=\d+\.|$)',
            ]
            
            explanation = ''
            for ep in explanation_patterns:
                exp_match = re.search(ep, q_text, re.IGNORECASE | re.DOTALL)
                if exp_match:
                    explanation = exp_match.group(1).strip()
                    # 정답 부분 제거
                    explanation = re.sub(r'(?:정답|Answer)[\s:：]+[A-D①②③④1-4]', '', explanation).strip()
                    break
            
            # 해설 가독성 개선
            if explanation:
                # 연속 공백 정리
                explanation = re.sub(r'\s+', ' ', explanation)
                # 문장 구분 개선 (마침표 뒤 대문자나 한글로 시작하는 경우 줄바꿈)
                explanation = re.sub(r'([.!?])\s+([A-Z가-힣])', r'\1\n\n\2', explanation)
                # 번호 목록 개선 (1), 2), 3) 형식)
                explanation = re.sub(r'\s*([1-9])\)\s*', r'\n\n\1) ', explanation)
                # 항목 기호 개선 (①, ②, ③ 형식)
                explanation = re.sub(r'\s*([①②③④⑤⑥⑦⑧⑨⑩])\s*', r'\n\n\1 ', explanation)
                explanation = explanation.strip()
            
            # 문제 본문 추출 (첫 선택지 이전까지)
            first_choice_match = re.search(r'[A-D①②③④1-4][).]', q_text)
            if first_choice_match:
                question_text = q_text[:first_choice_match.start()].strip()
            else:
                question_text = q_text[:500]  # 최대 500자로 확장
            
            # 문제 번호 제거
            question_text = re.sub(r'^\d+\.\s*|^문제\s*\d+[.:]\s*|^Q\d+[.:]\s*', '', question_text).strip()
            
            # 가독성 개선: 불필요한 공백 정리
            question_text = re.sub(r'\s+', ' ', question_text)  # 연속 공백을 하나로
            question_text = re.sub(r'\s*([.,?!])\s*', r'\1 ', question_text)  # 구두점 뒤 공백
            # 괄호 안 공백 정리
            question_text = re.sub(r'\(\s+', '(', question_text)
            question_text = re.sub(r'\s+\)', ')', question_text)
            question_text = question_text.strip()
            
            # 라벨 분류
            labels = classify_labels(question_text + ' ' + explanation)
            
            # 정답 텍스트
            answer_idx = ord(answer) - ord('A')
            answer_text = choices[answer_idx][1] if answer_idx < len(choices) else ''
            
            # 선택지 정규화 및 가독성 개선
            normalized_choices = []
            for i, (letter, text) in enumerate(choices[:4]):
                choice_letter = chr(ord('A') + i)
                # 선택지 텍스트 정리
                choice_text = text.strip()
                choice_text = re.sub(r'\s+', ' ', choice_text)  # 연속 공백 제거
                normalized_choices.append(f'{choice_letter}. {choice_text}')
            
            question_data = {
                'id': f'PMP{q_no.zfill(3)}',
                'q_no': q_no,
                'question': question_text,
                'options': normalized_choices,
                'answer': answer,
                'answer_text': answer_text.strip(),
                'explanation': explanation if explanation else '해설이 없습니다.',
                'labels': labels,
                'difficulty': 'medium',
                'source': 'PMP-2025.07.30.pdf',
                'type': 'multiple_choice'
            }
            
            questions.append(question_data)
            print(f"  [OK] 문제 {q_no} 추출 완료")
            
        except Exception as e:
            print(f"  [ERROR] 문제 {q_no} 파싱 오류: {e}")
            continue
    
    return questions

def main():
    # PDF 파일 경로
    pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'
    
    if not pdf_path.exists():
        print(f"[오류] PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print(f"[PDF 파싱] 파일 읽기 시작: {pdf_path.name}")
    
    # 텍스트 추출
    full_text = extract_text_from_pdf(pdf_path)
    print(f"[완료] 텍스트 추출 완료: {len(full_text)} 문자")
    
    # 문제 파싱
    print("\n[파싱] 문제 파싱 시작...")
    questions = parse_questions(full_text)
    
    if not questions:
        print("\n[오류] 추출된 문제가 없습니다.")
        return
    
    # JSONL 파일 저장
    output_path = Path(__file__).parent.parent / 'data' / 'items_pmp.jsonl'
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"\n[성공] 파싱 완료!")
    print(f"   총 문제 수: {len(questions)}개")
    print(f"   저장 위치: {output_path}")
    
    # 통계 출력
    print("\n[통계] 라벨 분포:")
    label_counts = {}
    for q in questions:
        for label in q['labels']:
            label_counts[label] = label_counts.get(label, 0) + 1
    
    for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {label}: {count}개")
    
    # 샘플 문제 출력
    print("\n[샘플] 샘플 문제 (첫 3개):")
    for i, q in enumerate(questions[:3], 1):
        print(f"\n[샘플 {i}]")
        print(f"   문제 {q['q_no']}: {q['question'][:80]}...")
        print(f"   선택지: {len(q['options'])}개")
        print(f"   정답: {q['answer']} - {q['answer_text'][:30]}...")
        print(f"   해설: {'있음' if q['explanation'] != '해설이 없습니다.' else '없음'}")
        print(f"   라벨: {', '.join(q['labels'])}")
    
    # 이미지 제외 통계
    print(f"\n[통계] 파싱 결과:")
    print(f"   전체 문제 수: 811개")
    print(f"   추출된 텍스트 문제: {len(questions)}개")
    print(f"   제외된 이미지 문제: {811 - len(questions)}개")
    print(f"\n[안내] 이미지 문제는 별도로 캡처하여 병합 예정")
    print(f"   - 텍스트 문제 ID: PMP001 ~ PMP{len(questions):03d}")
    print(f"   - 이미지 문제는 나중에 병합 시 ID 매칭 가능")

if __name__ == '__main__':
    main()

