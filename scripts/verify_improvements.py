#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선사항 검증 스크립트
1. 가독성 개선 확인
2. 프로그래밍 언어별 문제 수 확인
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def verify_readability_improvements():
    """가독성 개선 검증"""
    print("=" * 60)
    print("1. 가독성 개선 검증")
    print("=" * 60)
    
    jsonl_path = Path("data/items_2021_round1.jsonl")
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    # Q002 검증 (DB 설계 절차 문제)
    q002 = next((q for q in questions if q['q_no'] == 'Q002'), None)
    if q002:
        text = q002['question_text']
        print("\n📝 Q002 가독성 샘플:")
        print("-" * 60)
        print(text[:300] + "...")
        print("-" * 60)
        
        # 개선사항 체크
        improvements = []
        if '\n\n[보기]' in text or '[보기]\n\n' in text:
            improvements.append("✅ [보기] 섹션 구분")
        if '\n\n- (' in text:
            improvements.append("✅ 리스트 항목 줄바꿈")
        if 'DB\n설' not in text and 'DB 설' in text:
            improvements.append("✅ 단어 중간 줄바꿈 제거")
        
        print("\n개선사항 적용 여부:")
        for imp in improvements:
            print(f"  {imp}")
    
    print("\n")

def verify_programming_subcategories():
    """프로그래밍 하위 카테고리 검증"""
    print("=" * 60)
    print("2. 프로그래밍 하위 카테고리 검증")
    print("=" * 60)
    
    jsonl_path = Path("data/items_all.jsonl")
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        questions = [json.loads(line) for line in f if line.strip()]
    
    # 프로그래밍 문제 필터링
    prog_questions = [q for q in questions if q.get('primary_category') == '프로그래밍']
    
    # 언어별 카운트
    lang_counts = {'java': 0, 'c': 0, 'python': 0, 'other': 0}
    
    for q in prog_questions:
        tags = q.get('tags', [])
        code_blocks = q.get('code_blocks', [])
        
        has_lang = False
        for lang in ['java', 'c', 'python']:
            if lang in tags or any(cb.get('language') == lang for cb in code_blocks):
                lang_counts[lang] += 1
                has_lang = True
                break
        
        if not has_lang:
            lang_counts['other'] += 1
    
    print(f"\n총 프로그래밍 문제: {len(prog_questions)}개")
    print("-" * 60)
    print(f"☕ Java:   {lang_counts['java']}개")
    print(f"🔧 C언어:  {lang_counts['c']}개")
    print(f"🐍 Python: {lang_counts['python']}개")
    print(f"❓ 기타:   {lang_counts['other']}개")
    print("-" * 60)
    print(f"합계:      {sum(lang_counts.values())}개")
    
    # 샘플 문제 출력
    print("\n📋 언어별 샘플 문제:")
    for lang in ['java', 'c', 'python']:
        sample = next((q for q in prog_questions 
                      if lang in q.get('tags', []) or 
                      any(cb.get('language') == lang for cb in q.get('code_blocks', []))), 
                     None)
        if sample:
            print(f"  {lang.upper()}: {sample['q_no']} - {sample['question_text'][:40]}...")
    
    print("\n")

def verify_index_html():
    """index.html 변경사항 검증"""
    print("=" * 60)
    print("3. index.html 변경사항 검증")
    print("=" * 60)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('category_programming_java', '☕ Java 하위 카테고리 설정'),
        ('category_programming_c', '🔧 C언어 하위 카테고리 설정'),
        ('category_programming_python', '🐍 Python 하위 카테고리 설정'),
        ('subcategory:', 'subcategory 필드 존재'),
        ('optgroup label="💻 프로그래밍"', '프로그래밍 optgroup 메뉴'),
        ('config.subcategory', 'subcategory 필터링 로직')
    ]
    
    print("\n변경사항 체크:")
    all_passed = True
    for keyword, description in checks:
        if keyword in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False
    
    if all_passed:
        print("\n✅ 모든 변경사항이 정상적으로 적용되었습니다!")
    else:
        print("\n⚠️ 일부 변경사항이 누락되었습니다.")
    
    print("\n")

def main():
    """메인 실행"""
    print("\n" + "🎯 개선사항 검증 시작".center(60, "="))
    print()
    
    verify_readability_improvements()
    verify_programming_subcategories()
    verify_index_html()
    
    print("=" * 60)
    print("✅ 검증 완료")
    print("=" * 60)
    print("\n📌 다음 단계:")
    print("  1. 브라우저에서 http://localhost:8000 접속")
    print("  2. Ctrl+Shift+Delete로 캐시 완전 삭제")
    print("  3. 문제패턴별 기출문제 > 프로그래밍 > Java/C/Python 선택 테스트")
    print("  4. 문제 본문 가독성 확인 (줄바꿈, [보기] 구분)")
    print()

if __name__ == "__main__":
    main()



