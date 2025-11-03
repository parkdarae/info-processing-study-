# -*- coding: utf-8 -*-
"""
전체 답안/해설 동기화 및 검증 통합 스크립트
1. 수동 입력 CSV 적용
2. 답안/해설 개선
3. 종합 검증
4. 리포트 생성
"""
import sys
import io
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 스크립트 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from apply_manual_input import apply_manual_input
from comprehensive_answer_review import AnswerReviewer
from improve_answers_explanations import AnswerImprover
from check_answer_rate import check_answer_rate

def main():
    print("=" * 80)
    print("전체 답안/해설 동기화 및 검증 통합 프로세스")
    print("=" * 80)
    
    # 1단계: 수동 입력 CSV 적용
    print("\n[1단계] 수동 입력 CSV 적용")
    print("-" * 80)
    try:
        apply_manual_input()
        print("[완료] 수동 입력 CSV 적용 완료")
    except Exception as e:
        print(f"[오류] {e}")
    
    # 2단계: 답안/해설 자동 개선
    print("\n[2단계] 답안/해설 자동 개선")
    print("-" * 80)
    try:
        improver = AnswerImprover()
        improver.improve_all(create_backup=True)
        print("[완료] 답안/해설 개선 완료")
    except Exception as e:
        print(f"[오류] {e}")
    
    # 3단계: 종합 검증
    print("\n[3단계] 종합 검증")
    print("-" * 80)
    try:
        reviewer = AnswerReviewer()
        reviewer.review_all()
        print("[완료] 종합 검증 완료")
    except Exception as e:
        print(f"[오류] {e}")
    
    # 4단계: 답안 입력률 확인
    print("\n[4단계] 답안 입력률 확인")
    print("-" * 80)
    try:
        check_answer_rate()
        print("[완료] 답안 입력률 확인 완료")
    except Exception as e:
        print(f"[오류] {e}")
    
    print("\n" + "=" * 80)
    print("전체 프로세스 완료")
    print("=" * 80)
    print("\n다음 파일들을 확인하세요:")
    print("  - data/answer_review_report.json: 상세 검증 리포트")
    print("  - data/validation_summary.json: 검증 요약")
    print("  - data/backups/: 백업 파일들")
    print("=" * 80)

if __name__ == "__main__":
    main()

