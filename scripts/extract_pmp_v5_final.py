"""
PMP PDF 파싱 V5 - 최종 수정
핵심 전략:
1. "No. X" 패턴으로 문제 시작 지점 찾기
2. 문제 본문은 첫 선택지(A.) 이전까지
3. 선택지는 A. B. C. D. 패턴
4. 정답은 "정답: X" 패턴
5. 해설은 정답 이후 ~ 다음 "No. X" 이전까지
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

def has_image_strict(text):
    """명확한 이미지 지시어만 감지"""
    strict_indicators = [
        '그림을 참조', '도표를 참조', '차트를 참조',
        '아래 그림', '다음 그림', '위 그림',
        '아래 도표', '다음 도표', '위 도표',
        '다음 네트워크', '아래 네트워크',
        'refer to the figure', 'see the diagram',
        'shown in the figure', 'illustrated in'
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

# "No. X" 패턴으로 문제 시작 위치 찾기
question_starts = [(m.start(), m.group(1)) for m in re.finditer(r'No\.\s*(\d+)', full_text)]
print(f"문제 시작 위치 {len(question_starts)}개 발견\n")

questions = []
skipped_images = 0
skipped_errors = 0

for i, (start_pos, q_no) in enumerate(question_starts):
    try:
        # 다음 문제 시작 위치 (또는 파일 끝)
        end_pos = question_starts[i+1][0] if i+1 < len(question_starts) else len(full_text)
        
        # 현재 문제 블록 전체
        question_block = full_text[start_pos:end_pos]
        
        # "No. X" 제거
        question_block = re.sub(r'^No\.\s*\d+\s*', '', question_block).strip()
        question_block = re.sub(r'Page\s*\|\s*\d+', '', question_block)
        
        # 선택지 찾기 (A. B. C. D.)
        choice_pattern = r'([A-D])\.\s+([^\n]+?)(?=\s*[A-E]\.\s+|\s*정답:|\Z)'
        choices = re.findall(choice_pattern, question_block, re.DOTALL)
        
        if len(choices) < 3:
            skipped_errors += 1
            continue
        
        # 문제 본문: 첫 선택지 이전까지
        first_choice_match = re.search(r'[A-D]\.\s+', question_block)
        if not first_choice_match:
            skipped_errors += 1
            continue
        
        question_text = question_block[:first_choice_match.start()].strip()
        question_text = re.sub(r'\s+', ' ', question_text)
        
        if len(question_text) < 20:
            skipped_errors += 1
            continue
        
        # 이미지 감지
        if has_image_strict(question_text):
            print(f"  문제 {q_no}: 이미지 제외")
            skipped_images += 1
            continue
        
        # 정답 찾기
        answer_match = re.search(r'정답[\s:：]+([A-D])', question_block)
        if not answer_match:
            skipped_errors += 1
            continue
        
        answer = answer_match.group(1)
        
        # 해설: 정답 이후 텍스트
        explanation_start = answer_match.end()
        explanation = question_block[explanation_start:].strip()
        
        # 해설에서 "해설:" 제거
        explanation = re.sub(r'^해설[\s:：]+', '', explanation)
        
        # 해설 가독성 개선
        explanation = re.sub(r'\s+', ' ', explanation)
        explanation = re.sub(r'([.!?])\s+([A-Z가-힣])', r'\1\n\n\2', explanation)
        explanation = re.sub(r'\s*\*\s*', r'\n\n* ', explanation)
        explanation = re.sub(r'\n{3,}', '\n\n', explanation).strip()
        
        if len(explanation) < 10:
            explanation = '해설이 없습니다.'
        
        # 라벨 분류
        labels = classify_labels(question_text + ' ' + explanation)
        
        # 정답 텍스트
        answer_idx = ord(answer) - ord('A')
        answer_text = choices[answer_idx][1].strip() if answer_idx < len(choices) else ''
        
        # 선택지 정규화
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
        print(f"  [ERROR] 문제 {q_no} 오류: {e}")
        skipped_errors += 1
        continue

# 저장
output_path = Path(__file__).parent.parent / 'data' / 'items_pmp_final.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

print(f"\n[완료] {len(questions)}개 문제 추출")
print(f"저장 위치: {output_path}")
print(f"\n[통계]")
print(f"  이미지 제외: {skipped_images}개")
print(f"  파싱 오류: {skipped_errors}개")
print(f"  추출 비율: {len(questions)/len(question_starts)*100:.1f}%")

