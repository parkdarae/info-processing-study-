# -*- coding: utf-8 -*-
"""
Tistory URL 매핑 유틸리티
요구사항정의서 기반 doc_id → URL 매핑
"""

URL_MAPPING = {
    # 2020년
    "2020_round1": "https://chobopark.tistory.com/401",
    "2020_round2": "https://chobopark.tistory.com/403",
    "2020_round3": "https://chobopark.tistory.com/404",
    
    # 2021년
    "2021_round1": "https://chobopark.tistory.com/420",
    "2021_round2": "https://chobopark.tistory.com/422",
    "2021_round3": "https://chobopark.tistory.com/425",
    
    # 2022년
    "2022_round1": "https://chobopark.tistory.com/463",
    "2022_round2": "https://chobopark.tistory.com/482",
    "2022_round3": "https://chobopark.tistory.com/494",
    
    # 2023년
    "2023_round1": "https://chobopark.tistory.com/516",
    "2023_round2": "https://chobopark.tistory.com/528",
    "2023_round3": "https://chobopark.tistory.com/538",
    
    # 2024년
    "2024_round1": "https://chobopark.tistory.com/546",
    "2024_round2": "https://chobopark.tistory.com/552",
    "2024_round3": "https://chobopark.tistory.com/553",
    
    # 2025년
    "2025_round1": "https://chobopark.tistory.com/554",
    "2025_round2": "https://chobopark.tistory.com/555"
}

def get_tistory_url(doc_id):
    """doc_id에 해당하는 Tistory URL 반환"""
    return URL_MAPPING.get(doc_id, None)

def get_all_urls():
    """모든 Tistory URL 목록 반환"""
    return URL_MAPPING

if __name__ == "__main__":
    # 테스트
    print("=== Tistory URL 매핑 테스트 ===")
    print(f"2024_round1: {get_tistory_url('2024_round1')}")
    print(f"2025_round2: {get_tistory_url('2025_round2')}")
    print(f"\n총 {len(URL_MAPPING)}개 회차 매핑 완료")

