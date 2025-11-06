"""
PMP PDF 최종 파싱 스크립트 - 개선된 버전
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

IMAGE_INDICATORS = [
    'figure', 'diagram', 'chart', 'graph', 'table', 'image',
    '그림', '도표', '차트', '표', '다이어그램',
    'see figure', 'refer to', '아래 그림', '다음 도표'
]

def classify_labels(text):
    """텍스트 기반 PMP 라벨 분류"""
    labels = []
    text_lower = text.lower()
    
    for label, keywords in KNOWLEDGE_AREAS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            if label not in labels:
                labels.append(label)
    
    for label, keywords in PROCESS_GROUPS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            if label not in labels:
                labels.append(label)
    
    if not labels:
        labels.append('project_integration')
    
    return labels

def has_image(text):
    """이미지 포함 여부 확인"""
    text_lower = text.lower()
    return any(indicator in text_lower for indicator in IMAGE_INDICATORS)

def extract_text_from_pdf(pdf_path):
    """PDF에서 전체 텍스트 추출"""
    full_text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"총 {len(pdf.pages)} 페이지 읽는 중...")
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
            if i % 50 == 0:
                print(f"  {i} 페이지 처리 완료...")
    
    return full_text

def parse_questions(text):
    """텍스트에서 문제 파싱 - 개선된 버전"""
    questions = []
    
    # No. 숫자 패턴으로 문제 분리
    pattern = r'No\.\s*(\d+)\s+(.*?)(?=No\.\s*\d+|$)'
    matches = list(re.finditer(pattern, text, re.MULTILINE | re.DOTALL))
    
    print(f"패턴 매칭 성공: {len(matches)}개 문제 발견\n")
    
    for match in matches:
        try:
            q_no = match.group(1)
            q_text = match.group(2).strip()
            
            # 이미지 포함 문제 제외
            if has_image(q_text):
                print(f"  문제 {q_no}: 이미지 감지, 제외")
                continue
            
            # 선택지 추출 - 간단한 패턴
            choice_pattern = r'([A-E])\.\s+([^\n]+)'
            choices = re.findall(choice_pattern, q_text)
            
            if len(choices) < 4:
                print(f"  문제 {q_no}: 선택지 부족 ({len(choices)}개)")
                continue
            
            # 정답 추출
            answer_pattern = r'정답[\s:：]+([A-E])'
            answer_match = re.search(answer_pattern, q_text, re.IGNORECASE)
            
            if not answer_match:
                print(f"  문제 {q_no}: 정답 없음")
                continue
            
            answer = answer_match.group(1).upper()
            
            # 해설 추출
            explanation_pattern = r'정답[\s:：]+[A-E]\s*(.*?)(?=No\.\s*\d+|$)'
            exp_match = re.search(explanation_pattern, q_text, re.IGNORECASE | re.DOTALL)
            explanation = exp_match.group(1).strip() if exp_match else ''
            
            # 문제 본문 추출 (첫 선택지 이전까지)
            first_choice_pos = q_text.find(f'{choices[0][0]}.')
            question_text = q_text[:first_choice_pos].strip() if first_choice_pos > 0 else q_text[:500]
            
            # 가독성 개선
            question_text = re.sub(r'\s+', ' ', question_text)
            question_text = question_text.strip()
            
            if explanation:
                explanation = re.sub(r'\s+', ' ', explanation)
                explanation = re.sub(r'([.!?])\s+([A-Z가-힣])', r'\1\n\n\2', explanation)
                explanation = explanation.strip()
            
            # 라벨 분류
            labels = classify_labels(question_text + ' ' + explanation)
            
            # 정답 텍스트
            answer_idx = ord(answer) - ord('A')
            answer_text = choices[answer_idx][1].strip() if answer_idx < len(choices) else ''
            
            # 선택지 정규화
            normalized_choices = []
            for i in range(min(4, len(choices))):
                choice_letter = chr(ord('A') + i)
                choice_text = choices[i][1].strip()
                choice_text = re.sub(r'\s+', ' ', choice_text)
                normalized_choices.append(f'{choice_letter}. {choice_text}')
            
            question_data = {
                'id': f'PMP{q_no.zfill(3)}',
                'q_no': q_no,
                'question': question_text,
                'options': normalized_choices,
                'answer': answer,
                'answer_text': answer_text,
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
    pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'
    
    if not pdf_path.exists():
        print(f"[오류] PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print(f"[PDF 파싱] 파일 읽기 시작: {pdf_path.name}\n")
    
    # 텍스트 추출
    full_text = extract_text_from_pdf(pdf_path)
    print(f"[완료] 텍스트 추출 완료: {len(full_text)} 문자\n")
    
    # 문제 파싱
    print("[파싱] 문제 파싱 시작...\n")
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
        print(f"   라벨: {', '.join(q['labels'])}")
    
    # 최종 통계
    print(f"\n[통계] 파싱 결과:")
    print(f"   전체 문제 수: 811개")
    print(f"   추출된 텍스트 문제: {len(questions)}개")
    print(f"   제외된 이미지 문제: {811 - len(questions)}개")
    print(f"\n[안내] 이미지 문제는 별도로 캡처하여 병합 예정")

if __name__ == '__main__':
    main()

