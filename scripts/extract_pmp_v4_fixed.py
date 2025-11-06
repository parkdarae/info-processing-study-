"""
PMP PDF 파싱 V4 - 문제/해설 혼동 문제 수정
핵심: 문제 본문은 물음표(?)로 끝나야 하고, 해설은 정답 이후에 나옴
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

def has_image_strict(text, choices_count):
    """명확한 이미지 지시어만 감지"""
    if choices_count >= 4:
        return False
    
    strict_indicators = [
        '그림을 참조', '도표를 참조', '차트를 참조',
        '아래 그림', '다음 그림', '위 그림',
        '아래 도표', '다음 도표', '위 도표',
        '다음 네트워크', '아래 네트워크',
        'refer to the figure', 'see the diagram',
        'shown in the figure', 'illustrated in',
        '보기와 같이', '다음과 같은 그림'
    ]
    
    text_lower = text.lower()
    return any(ind in text_lower for ind in strict_indicators)

# PDF 전체 텍스트 추출
pdf_path = Path(__file__).parent.parent / 'PMP-2025.07.30.pdf'

print(f"PDF 파일 읽는 중...")
with pdfplumber.open(pdf_path) as pdf:
    print(f"총 {len(pdf.pages)} 페이지")
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

print(f"텍스트 추출 완료: {len(full_text)} 문자\n")

# 정답 기준으로 문제 블록 분리
answer_pattern = r'정답:\s*([A-E])'
answer_positions = [(m.start(), m.group(1)) for m in re.finditer(answer_pattern, full_text)]

print(f"정답 위치 {len(answer_positions)}개 발견\n")

questions = []
skipped_images = []
skipped_no_choices = []
parsing_errors = []

for i, (answer_pos, answer) in enumerate(answer_positions):
    try:
        # 현재 정답 이전 텍스트 (문제+선택지)
        start_pos = answer_positions[i-1][0] + 200 if i > 0 else 0
        question_block = full_text[start_pos:answer_pos]
        
        # 문제 번호 찾기
        no_match = re.search(r'No\.\s*(\d+)', question_block)
        if no_match:
            q_no = no_match.group(1)
        else:
            q_no = str(i + 1)
        
        # 선택지 추출 (A. ~ D. 패턴)
        choice_pattern = r'([A-D])\.\s+([^\n]+?)(?=\s*[A-D]\.\s+|정답:|$)'
        choices = re.findall(choice_pattern, question_block, re.DOTALL)
        
        # 선택지가 4개 미만이면 스킵
        if len(choices) < 3:
            skipped_no_choices.append(q_no)
            continue
        
        # 문제 본문 추출: 첫 선택지 이전까지
        first_choice_pos = question_block.find(f'{choices[0][0]}.')
        if first_choice_pos > 0:
            question_text = question_block[:first_choice_pos].strip()
        else:
            question_text = question_block.strip()
        
        # No. X, Page | X 제거
        question_text = re.sub(r'No\.\s*\d+\s*', '', question_text)
        question_text = re.sub(r'Page\s*\|\s*\d+', '', question_text)
        question_text = re.sub(r'\s+', ' ', question_text).strip()
        
        # 문제 본문이 너무 짧으면 스킵
        if len(question_text) < 20:
            skipped_no_choices.append(q_no)
            continue
        
        # 문제 본문이 물음표로 끝나는지 확인
        if not question_text.endswith(('?', '가', '는가', '인가', '까')):
            # 물음표가 없으면 마지막 물음표까지만 추출
            last_question_mark = question_text.rfind('?')
            if last_question_mark > 0:
                question_text = question_text[:last_question_mark+1].strip()
            else:
                # 물음표가 전혀 없으면 문제가 아닐 가능성
                parsing_errors.append(f"문제 {q_no}: 물음표 없음")
        
        # 이미지 감지
        if has_image_strict(question_text, len(choices)):
            print(f"  문제 {q_no}: 이미지 제외")
            skipped_images.append(q_no)
            continue
        
        # 해설 추출 (정답 이후 ~ 다음 문제 이전)
        explanation_start = answer_pos + 10
        explanation_end = answer_positions[i+1][0] - 100 if i+1 < len(answer_positions) else len(full_text)
        explanation = full_text[explanation_start:explanation_end].strip()
        
        # 해설에서 "정답: X" 부분 제거
        explanation = re.sub(r'^정답[\s:：]+[A-E]\s*', '', explanation)
        explanation = re.sub(r'해설[\s:：]+', '', explanation)
        
        # 다음 문제 번호가 포함되면 그 이전까지만
        next_no_match = re.search(r'\n\nNo\.\s*\d+', explanation)
        if next_no_match:
            explanation = explanation[:next_no_match.start()].strip()
        
        # 해설 가독성 개선
        explanation = re.sub(r'\s+', ' ', explanation)
        explanation = re.sub(r'([.!?])\s+([A-Z가-힣])', r'\1\n\n\2', explanation)
        explanation = re.sub(r'\s*([1-9])\)\s*', r'\n\n\1) ', explanation)
        explanation = re.sub(r'\s*([①②③④⑤⑥⑦⑧⑨⑩])\s*', r'\n\n\1 ', explanation)
        explanation = re.sub(r'\n{3,}', '\n\n', explanation).strip()
        
        # 해설이 너무 짧거나 없으면 표시
        if len(explanation) < 10:
            explanation = '해설이 없습니다.'
        
        # 라벨 분류
        labels = classify_labels(question_text + ' ' + explanation)
        
        # 정답 텍스트
        answer_idx = ord(answer) - ord('A')
        answer_text = choices[answer_idx][1].strip() if answer_idx < len(choices) else ''
        
        # 선택지 정규화 (4개)
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
            'explanation': explanation,
            'labels': labels,
            'difficulty': 'medium',
            'source': 'PMP-2025.07.30.pdf',
            'type': 'multiple_choice'
        }
        
        questions.append(question_data)
        
        if int(q_no) % 100 == 0:
            print(f"  [OK] 문제 {q_no} 추출")
        
    except Exception as e:
        print(f"  [ERROR] 문제 {i+1} 오류: {e}")
        parsing_errors.append(f"문제 {i+1}: {str(e)}")
        continue

# 저장
output_path = Path(__file__).parent.parent / 'data' / 'items_pmp_fixed.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"\n[완료] {len(questions)}개 문제 추출")
print(f"저장 위치: {output_path}")
print(f"\n[통계]")
print(f"  이미지 제외: {len(skipped_images)}개")
print(f"  선택지 부족: {len(skipped_no_choices)}개")
print(f"  파싱 오류: {len(parsing_errors)}개")
print(f"  총 제외: {len(skipped_images) + len(skipped_no_choices)}개")
print(f"  추출 비율: {len(questions)/799*100:.1f}%")

if parsing_errors:
    print(f"\n[파싱 오류 상세]")
    for error in parsing_errors[:10]:
        print(f"  {error}")

