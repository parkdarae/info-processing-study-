"""
단일 URL 테스트 크롤링 스크립트
첫 번째 URL만 크롤링하여 결과를 확인합니다.
"""
import sys
from pathlib import Path

# scripts 폴더에서 실행되므로 상위 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.crawl_tistory_exams import TistoryCrawler, EXAM_URLS

def test_single_crawl():
    """첫 번째 URL만 테스트"""
    crawler = TistoryCrawler()
    
    # 첫 번째 회차만 테스트
    test_exam = EXAM_URLS[0]
    
    print("\n" + "="*60)
    print("[TEST] 단일 URL 테스트 크롤링")
    print("="*60)
    
    success = crawler.crawl_exam(test_exam)
    
    if success:
        print("\n[SUCCESS] 테스트 성공!")
        print(f"[FILE] 출력 파일: data/items_{test_exam['year']}_round{test_exam['round']}.jsonl")
        print(f"[REPORT] 리포트: data/report_{test_exam['year']}_round{test_exam['round']}.json")
    else:
        print("\n[FAIL] 테스트 실패!")
    
    return success

if __name__ == "__main__":
    test_single_crawl()

