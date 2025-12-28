#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CISSP 문제 파싱 스크립트 v2
추출된 텍스트에서 문제를 파싱하여 JSONL로 저장합니다.
"""

import re
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')


def parse_cissp_questions(text_path, output_path):
    """텍스트 파일에서 CISSP 문제를 파싱"""
    
    if not os.path.exists(text_path):
        print(f"[ERROR] 텍스트 파일을 찾을 수 없습니다: {text_path}")
        return []
    
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 페이지 구분자 및 헤더 제거
    text = re.sub(r'=== PAGE \d+ ===\n', '', text)
    text = re.sub(r'IT Certification Guaranteed, The Easy Way!\n', '', text)
    text = re.sub(r'^\d+\n', '', text, flags=re.MULTILINE)  # 페이지 번호 제거
    
    # 문제 패턴: NO.숫자 로 시작하는 문제 찾기
    question_pattern = r'NO\.(\d+)\s+(.*?)(?=NO\.\d+|$)'
    
    matches = re.findall(question_pattern, text, re.DOTALL)
    
    questions = []
    
    print(f"[INFO] 총 {len(matches)}개 문제 패턴 발견")
    
    for q_no, content in matches:
        try:
            question_data = parse_single_question(q_no, content)
            if question_data:
                questions.append(question_data)
        except Exception as e:
            print(f"[WARNING] 문제 {q_no} 파싱 실패: {e}")
    
    print(f"[OK] {len(questions)}개 문제 파싱 완료")
    
    # JSONL로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"[OK] 저장 완료: {output_path}")
    
    return questions


def parse_single_question(q_no, content):
    """단일 문제 파싱"""
    
    content = content.strip()
    
    # Answer 추출 - Answer: 다음에 오는 알파벳만 추출 (Explanation 전까지)
    # "Answer: C" 또는 "Answer: A, C" 형식
    answer_match = re.search(r'Answer:\s*([A-F](?:\s*,\s*[A-F])*)', content)
    if not answer_match:
        return None
    
    answer_text = answer_match.group(1).strip()
    # 정답 추출 (쉼표로 구분된 경우 처리)
    answers = [a.strip().upper() for a in re.split(r'[,\s]+', answer_text) if a.strip() and a.strip().upper() in 'ABCDEF']
    
    if not answers:
        return None
    
    # Answer 이전 텍스트와 이후 텍스트 분리
    answer_pos = answer_match.start()
    before_answer = content[:answer_pos].strip()
    after_answer = content[answer_match.end():].strip()
    
    # Explanation 추출 (있는 경우)
    explanation = ""
    explanation_match = re.search(r'Explanation:\s*(.*?)(?=NO\.\d+|$)', after_answer, re.DOTALL)
    if explanation_match:
        explanation = explanation_match.group(1).strip()
        # 줄바꿈 정리
        explanation = re.sub(r'\n+', '\n', explanation).strip()
        # 다음 문제 번호가 포함되어 있으면 제거
        explanation = re.sub(r'NO\.\d+.*$', '', explanation, flags=re.DOTALL).strip()
    
    # 선택지 추출 (A., B., C., D., E., F.)
    # 개선된 패턴: 줄의 시작 또는 공백 후 A. 형식
    choice_pattern = r'(?:^|\n)\s*([A-F])\.\s*(.*?)(?=(?:^|\n)\s*[A-F]\.|Answer:|Explanation:|$)'
    choice_matches = re.findall(choice_pattern, before_answer, re.DOTALL | re.MULTILINE)
    
    if not choice_matches:
        # A) B) C) D) 형식 시도
        choice_pattern = r'(?:^|\n)\s*([A-F])\)\s*(.*?)(?=(?:^|\n)\s*[A-F]\)|Answer:|Explanation:|$)'
        choice_matches = re.findall(choice_pattern, before_answer, re.DOTALL | re.MULTILINE)
    
    choices = {}
    for key, value in choice_matches:
        # 줄바꿈을 공백으로 변환하고 정리
        cleaned_value = re.sub(r'\s+', ' ', value).strip()
        choices[key.upper()] = cleaned_value
    
    # 문제 본문 추출 (첫 번째 선택지 이전)
    question_text = before_answer
    if choices:
        # 첫 번째 선택지 위치 찾기
        first_choice_pattern = r'(?:^|\n)\s*[A-F][.\)]'
        first_choice_match = re.search(first_choice_pattern, before_answer, re.MULTILINE)
        if first_choice_match:
            question_text = before_answer[:first_choice_match.start()].strip()
    
    # 줄바꿈 정리
    question_text = re.sub(r'\s+', ' ', question_text).strip()
    
    # Drag and Drop 문제 처리
    is_drag_drop = 'Drag' in question_text and 'Drop' in question_text
    
    # 이미지 참조 확인
    images = []
    if is_drag_drop or 'exhibit' in question_text.lower() or 'image' in question_text.lower() or 'diagram' in question_text.lower():
        images.append(f"Q{q_no.zfill(4)}.png")
    
    # 유효성 검사
    if not question_text or not choices:
        return None
    
    # 최소 2개 선택지 필요
    if len(choices) < 2:
        return None
    
    return {
        "id": f"CISSP{q_no.zfill(4)}",
        "q_no": q_no,
        "question_en": question_text,
        "question_ko": "",
        "choices_en": choices,
        "choices_ko": {},
        "answer": answers,
        "explanation": explanation[:1000] if explanation else "",  # 해설 길이 제한
        "images": images,
        "type": "drag_drop" if is_drag_drop else "multiple_choice",
        "source": "CISSP V21.65.pdf"
    }


def validate_questions(questions):
    """파싱된 문제 검증"""
    
    print("\n[VALIDATION] 문제 검증:")
    
    # 통계
    total = len(questions)
    with_explanation = sum(1 for q in questions if q.get('explanation'))
    with_images = sum(1 for q in questions if q.get('images'))
    multi_answer = sum(1 for q in questions if len(q.get('answer', [])) > 1)
    drag_drop = sum(1 for q in questions if q.get('type') == 'drag_drop')
    
    print(f"   총 문제 수: {total}")
    print(f"   해설 포함: {with_explanation}")
    print(f"   이미지 참조: {with_images}")
    print(f"   복수 정답: {multi_answer}")
    print(f"   Drag & Drop: {drag_drop}")
    
    # 선택지 개수 분포
    choice_counts = {}
    for q in questions:
        count = len(q.get('choices_en', {}))
        choice_counts[count] = choice_counts.get(count, 0) + 1
    
    print(f"   선택지 개수 분포: {choice_counts}")
    
    # 정답 검증 (E, F 제외)
    invalid_answers = []
    for q in questions:
        for ans in q.get('answer', []):
            if ans not in 'ABCD' and ans not in q.get('choices_en', {}):
                invalid_answers.append((q['q_no'], ans))
    
    if invalid_answers:
        print(f"   잘못된 정답 (선택지에 없음): {len(invalid_answers)}개")
    
    # 문제 번호 연속성 확인
    q_nos = sorted([int(q['q_no']) for q in questions])
    if q_nos:
        print(f"   문제 번호 범위: {q_nos[0]} ~ {q_nos[-1]}")
        missing = set(range(q_nos[0], q_nos[-1] + 1)) - set(q_nos)
        if missing and len(missing) < 50:
            print(f"   누락된 문제: {sorted(missing)}")
        elif missing:
            print(f"   누락된 문제 수: {len(missing)}")
    
    # 샘플 출력 (해설 포함 문제)
    print("\n[SAMPLE] 해설 포함 문제 샘플:")
    samples_with_exp = [q for q in questions if q.get('explanation')][:2]
    for q in samples_with_exp:
        print(f"\n--- Q{q['q_no']} ---")
        print(f"문제: {q['question_en'][:80]}...")
        print(f"선택지: {list(q['choices_en'].keys())}")
        print(f"정답: {q['answer']}")
        print(f"해설: {q['explanation'][:100]}...")
    
    # 일반 샘플
    print("\n[SAMPLE] 첫 3개 문제:")
    for q in questions[:3]:
        print(f"\n--- Q{q['q_no']} ---")
        print(f"문제: {q['question_en'][:80]}...")
        print(f"선택지: {q['choices_en']}")
        print(f"정답: {q['answer']}")


if __name__ == "__main__":
    # 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text_path = os.path.join(base_dir, "cissp_raw.txt")
    output_path = os.path.join(base_dir, "data", "items_cissp.jsonl")
    
    print("=" * 60)
    print("CISSP Question Parser v2")
    print("=" * 60)
    
    # 파싱 실행
    questions = parse_cissp_questions(text_path, output_path)
    
    if questions:
        # 검증
        validate_questions(questions)
        
        print("\n" + "=" * 60)
        print("[DONE] 파싱 완료!")
        print(f"[FILE] 출력 파일: {output_path}")
        print("=" * 60)
