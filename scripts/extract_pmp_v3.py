"""
PMP PDF 파싱 V3 - 개선된 이미지 감지 로직
선택지가 4개 이상 있으면 텍스트 문제로 간주
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 설치 필요")
    exit(1)

import re
import json
from pathlib import Path

# 라벨 매핑
KNOWLEDGE_AREAS = {
    'project_integration': ['통합', 'integration', '헌장', 'charter', '변경'],
    'project_scope': ['범위', 'scope', 'WBS', '요구사항'],
    'project_schedule': ['일정', 'schedule', 'CPM', 'PERT'],
    'project_cost': ['원가', 'cost', '예산', 'budget', 'EVM'],
    'project_quality': ['품질', 'quality', 'QA', 'QC'],
    'project_resource': ['자원', 'resource', '팀', 'team'],
    'project_communication': ['의사소통', 'communication', '보고'],
    'project_risk': ['위험', 'risk', '리스크'],
    'project_procurement': ['조달', 'procurement', '계약'],
    'project_stakeholder': ['이해관계자', 'stakeholder', '고객']
}

PROCESS_GROUPS = {
    'initiating': ['착수', '시작'],
    'planning': ['기획', '계획'],
    'executing': ['실행', '수행'],
    'monitoring': ['감시', '통제'],
    'closing': ['종료', '완료']
}

def classify_labels(text):
    labels = []
    text_lower = text.lower()
    
    for label, keywords in KNOWLEDGE_AREAS.items():
        if any(kw in text_lower for kw in keywords):
            if label not in labels:
                labels.append(label)
    
    for label, keywords in PROCESS_GROUPS.items():
        if any(kw in text_lower for kw in keywords):
            if label not in labels:
                labels.append(label)
    
    return labels if labels else ['project_integration']

def has_image_strict(question_text, choices_count):
    """
    개선된 이미지 감지:
    1. 선택지가 4개 이상 있으면 텍스트 문제로 간주
    2. 명확한 이미지 지시어만 감지
    """
    # 선택지가 4개 이상 있으면 텍스트 문제
    if choices_count >= 4:
        return False
    
    # 명확한 이미지 지시어
    strict_indicators = [
        '그림을 참조', '도표를 참조', '차트를 참조',
        '아래 그림', '다음 그림', '위 그림',
        '아래 도표', '다음 도표', '위 도표',
        '다음 네트워크', '아래 네트워크',
        'refer to the figure', 'see the diagram',
        'shown in the figure', 'illustrated in',
        '보기와 같이', '다음과 같은 그림'
    ]
    
    text_lower = question_text.lower()
    return any(ind in text_lower for ind in strict_indicators)

# PDF 전체 텍스트 추출
pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'

with pdfplumber.open(pdf_path) as pdf:
    print(f"PDF 읽는 중... ({len(pdf.pages)} 페이지)")
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

print(f"텍스트 추출 완료: {len(full_text)} 문자\n")

# 정답 기준으로 문제 분리
answer_pattern = r'정답:\s*([A-E])'
answer_positions = [(m.start(), m.group(1)) for m in re.finditer(answer_pattern, full_text)]

print(f"정답 위치 {len(answer_positions)}개 발견\n")

questions = []
skipped_images = []
skipped_no_choices = []

for i, (answer_pos, answer) in enumerate(answer_positions):
    try:
        # 현재 정답 이전 텍스트 (문제+선택지)
        start_pos = answer_positions[i-1][0] + 50 if i > 0 else 0
        question_block = full_text[start_pos:answer_pos]
        
        # No. X 패턴 찾기
        no_match = re.search(r'No\.\s*(\d+)', question_block)
        if no_match:
            q_no = no_match.group(1)
        else:
            q_no = str(i + 1)
        
        # 선택지 추출 (먼저 확인)
        choices = re.findall(r'([A-E])\.\s+([^\n]+)', question_block)
        
        # 선택지 개수 확인
        if len(choices) < 3:
            skipped_no_choices.append(q_no)
            continue
        
        # 문제 본문 (첫 선택지 이전)
        first_choice_pos = question_block.find(f'{choices[0][0]}.')
        question_text = question_block[:first_choice_pos].strip() if first_choice_pos > 0 else ""
        
        # No. X 제거
        question_text = re.sub(r'No\.\s*\d+\s*', '', question_text).strip()
        question_text = re.sub(r'Page\s*\|\s*\d+', '', question_text).strip()
        question_text = re.sub(r'\s+', ' ', question_text)
        
        if len(question_text) < 10:
            skipped_no_choices.append(q_no)
            continue
        
        # 개선된 이미지 감지
        if has_image_strict(question_text, len(choices)):
            print(f"  문제 {q_no}: 이미지 제외 (명확한 이미지 지시어)")
            skipped_images.append(q_no)
            continue
        
        # 해설 추출 (정답 이후)
        explanation_start = answer_pos + 10
        explanation_end = answer_positions[i+1][0] - 100 if i+1 < len(answer_positions) else len(full_text)
        explanation = full_text[explanation_start:explanation_end].strip()
        explanation = re.sub(r'No\.\s*\d+.*$', '', explanation, flags=re.DOTALL).strip()
        explanation = re.sub(r'\s+', ' ', explanation)[:1000]
        
        # 라벨
        labels = classify_labels(question_text + ' ' + explanation)
        
        # 정답 텍스트
        answer_idx = ord(answer) - ord('A')
        answer_text = choices[answer_idx][1].strip() if answer_idx < len(choices) else ''
        
        # 선택지 정규화 (4개만)
        normalized_choices = []
        for j in range(min(4, len(choices))):
            choice_letter = chr(ord('A') + j)
            choice_text = re.sub(r'\s+', ' ', choices[j][1].strip())
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
        if int(q_no) % 50 == 0:
            print(f"  [OK] 문제 {q_no} 추출")
        
    except Exception as e:
        print(f"  [ERROR] 문제 {i+1} 오류: {e}")
        continue

# 저장
output_path = Path(__file__).parent.parent / 'data' / 'items_pmp.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"\n[완료] {len(questions)}개 문제 추출")
print(f"저장 위치: {output_path}")
print(f"\n[통계]")
print(f"  이미지 제외: {len(skipped_images)}개")
print(f"  선택지 부족: {len(skipped_no_choices)}개")
print(f"  총 제외: {len(skipped_images) + len(skipped_no_choices)}개")
print(f"  추출 비율: {len(questions)/799*100:.1f}%")

