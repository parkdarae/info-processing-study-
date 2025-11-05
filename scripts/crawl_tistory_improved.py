"""
Tistory 정보처리기사 실기 기출문제 크롤링 스크립트 (개선 버전)
색상 기반으로 정답(초록색)과 해설(파란색)을 정확하게 추출합니다.

Zero Tolerance 정책:
- 실제 데이터만 사용
- 추정/가상 데이터 완전 차단
- 모든 데이터 소스 추적 가능
"""
import requests
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
from datetime import datetime

# 크롤링 대상 URL 목록
EXAM_URLS = [
    {"year": 2025, "round": 1, "url": "https://chobopark.tistory.com/540"},
    {"year": 2025, "round": 2, "url": "https://chobopark.tistory.com/554"},
    {"year": 2024, "round": 3, "url": "https://chobopark.tistory.com/495"},
    {"year": 2024, "round": 2, "url": "https://chobopark.tistory.com/483"},
    {"year": 2024, "round": 1, "url": "https://chobopark.tistory.com/476"},
    {"year": 2023, "round": 2, "url": "https://chobopark.tistory.com/420"},
    {"year": 2022, "round": 3, "url": "https://chobopark.tistory.com/424"},
    {"year": 2022, "round": 2, "url": "https://chobopark.tistory.com/423"},
    {"year": 2021, "round": 1, "url": "https://chobopark.tistory.com/191"},
]

class ImprovedTistoryCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 출력 디렉토리 생성
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
    def fetch_page(self, url: str) -> Optional[str]:
        """페이지 HTML 가져오기"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"[ERROR] 페이지 로드 실패 ({url}): {e}")
            return None
    
    def is_green_text(self, element) -> bool:
        """초록색 텍스트인지 확인"""
        if not element:
            return False
        style = element.get('style', '')
        # 초록색 계열 확인
        green_patterns = [
            '#00b050', '#00b04f', '#00b051', 
            'rgb(0, 176, 80)', 'rgb(0,176,80)',
            '#0f0', 'green', '#008000'
        ]
        return any(pattern.lower() in style.lower() for pattern in green_patterns)
    
    def is_blue_text(self, element) -> bool:
        """파란색 텍스트인지 확인"""
        if not element:
            return False
        style = element.get('style', '')
        # 파란색 계열 확인
        blue_patterns = [
            '#0070c0', '#0070c1', '#0070bf',
            'rgb(0, 112, 192)', 'rgb(0,112,192)',
            '#00f', 'blue', '#0000ff'
        ]
        return any(pattern.lower() in style.lower() for pattern in blue_patterns)
    
    def extract_answer_from_details(self, details_element) -> str:
        """더보기(details) 요소에서 초록색 텍스트(정답) 추출"""
        if not details_element:
            return ""
        
        # 모든 span 태그 확인
        for span in details_element.find_all('span'):
            if self.is_green_text(span):
                text = span.get_text(strip=True)
                if text:
                    return text
        
        # p 태그도 확인
        for p in details_element.find_all('p'):
            if self.is_green_text(p):
                text = p.get_text(strip=True)
                if text:
                    return text
        
        return ""
    
    def extract_explanation_from_details(self, details_element) -> str:
        """더보기(details) 요소에서 파란색 텍스트(해설) 추출"""
        if not details_element:
            return ""
        
        explanations = []
        
        # 모든 span 태그 확인
        for span in details_element.find_all('span'):
            if self.is_blue_text(span):
                text = span.get_text(strip=True)
                if text:
                    explanations.append(text)
        
        # p 태그도 확인
        for p in details_element.find_all('p'):
            if self.is_blue_text(p):
                text = p.get_text(strip=True)
                if text:
                    explanations.append(text)
        
        return '\n'.join(explanations)
    
    def extract_questions(self, html: str, year: int, round_num: int, url: str) -> List[Dict[str, Any]]:
        """HTML에서 문제 추출 (개선된 버전)"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 본문 추출
        content_area = soup.find('div', class_='entry-content') or \
                      soup.find('div', class_='article') or \
                      soup.find('div', class_='tt_article_useless_p_margin') or \
                      soup.find('div', {'itemprop': 'articleBody'})
        
        if not content_area:
            print(f"[WARNING] 본문 영역을 찾을 수 없습니다: {url}")
            return []
        
        questions = []
        doc_id = f"{year}_round{round_num}"
        
        # 전체 텍스트를 한 번에 분석
        full_text = content_area.get_text('\n', strip=True)
        
        # 문제 번호로 분리 (1., 2., 3. ... 패턴)
        question_pattern = r'(?m)^(\d+)\.\s*'
        question_parts = re.split(question_pattern, full_text)
        
        # HTML에서 details(더보기) 요소들 추출
        details_elements = content_area.find_all('details')
        
        # 문제 파싱
        for i in range(1, len(question_parts), 2):
            if i + 1 >= len(question_parts):
                break
            
            q_num = question_parts[i].strip()
            q_content = question_parts[i + 1].strip()
            
            if len(q_content) < 5:
                continue
            
            # 해당 문제와 연관된 details 요소 찾기
            q_num_int = int(q_num)
            details_elem = None
            if q_num_int - 1 < len(details_elements):
                details_elem = details_elements[q_num_int - 1]
            
            # 정답과 해설 추출
            answer_text = ""
            explanation_text = ""
            
            if details_elem:
                answer_text = self.extract_answer_from_details(details_elem)
                explanation_text = self.extract_explanation_from_details(details_elem)
            
            # "더보기" 이전까지를 문제 본문으로
            question_text = q_content
            more_pos = q_content.find('더보기')
            if more_pos > 0:
                question_text = q_content[:more_pos].strip()
            
            # 정답 키 추출
            answer_keys = []
            if answer_text:
                answer_keys = [answer_text]
            
            # 데이터 구조 생성
            question_data = {
                "doc_id": doc_id,
                "page_range": [1, 1],
                "q_no": f"Q{int(q_num):03d}",
                "question_text": question_text,
                "choices": [],
                "answer": {
                    "keys": answer_keys,
                    "raw_text": answer_text
                },
                "explanation": explanation_text if explanation_text else None,
                "table_refs": [],
                "image_refs": [],
                "meta": {
                    "layout": "single",
                    "anchors": [f"{q_num}."],
                    "page_anchors": [1],
                    "confidence": 1.0 if answer_text else 0.7,
                    "warnings": [] if answer_text else ["정답을 찾을 수 없음"],
                    "source_url": url,
                    "crawled_at": datetime.now().isoformat()
                }
            }
            
            questions.append(question_data)
        
        return questions
    
    def save_jsonl(self, questions: List[Dict[str, Any]], filename: str):
        """JSONL 형식으로 저장"""
        filepath = self.data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"[SAVE] 저장 완료: {filepath} ({len(questions)}개 문제)")
    
    def save_report(self, exam_info: Dict[str, Any], questions: List[Dict[str, Any]], filename: str):
        """검증 리포트 저장"""
        filepath = self.data_dir / filename
        
        # 통계 계산
        total = len(questions)
        with_answers = sum(1 for q in questions if q['answer']['keys'])
        with_explanations = sum(1 for q in questions if q['explanation'])
        warnings = sum(len(q['meta']['warnings']) for q in questions)
        
        report = {
            "version": "2.0",
            "exam_info": exam_info,
            "total_questions": total,
            "questions_with_answers": with_answers,
            "questions_with_explanations": with_explanations,
            "total_warnings": warnings,
            "crawled_at": datetime.now().isoformat(),
            "success_rate": f"{(with_answers / total * 100):.1f}%" if total > 0 else "0%",
            "explanation_rate": f"{(with_explanations / total * 100):.1f}%" if total > 0 else "0%"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"[REPORT] {report['success_rate']} 정답, {report['explanation_rate']} 해설 (총 {total}문제)")
    
    def crawl_exam(self, exam_info: Dict[str, Any]) -> bool:
        """단일 회차 크롤링"""
        year = exam_info['year']
        round_num = exam_info['round']
        url = exam_info['url']
        
        print(f"\n{'='*60}")
        print(f"[START] 크롤링 시작: {year}년 {round_num}회")
        print(f"[URL] {url}")
        print(f"{'='*60}")
        
        # HTML 가져오기
        html = self.fetch_page(url)
        if not html:
            return False
        
        # 문제 추출
        questions = self.extract_questions(html, year, round_num, url)
        
        if not questions:
            print(f"[WARNING] 문제를 추출하지 못했습니다.")
            return False
        
        print(f"[SUCCESS] {len(questions)}개 문제 추출 완료")
        
        # JSONL 저장
        filename = f"items_{year}_round{round_num}.jsonl"
        self.save_jsonl(questions, filename)
        
        # 리포트 저장
        report_filename = f"report_{year}_round{round_num}.json"
        self.save_report(exam_info, questions, report_filename)
        
        return True
    
    def crawl_all(self):
        """전체 회차 크롤링"""
        print("\n" + "="*60)
        print("[START] Tistory 기출문제 크롤링 시작 (개선 버전)")
        print("="*60)
        
        success_count = 0
        total_count = len(EXAM_URLS)
        
        for exam_info in EXAM_URLS:
            success = self.crawl_exam(exam_info)
            if success:
                success_count += 1
            
            # 서버 부하 방지를 위한 딜레이
            time.sleep(2)
        
        print("\n" + "="*60)
        print(f"[COMPLETE] 크롤링 완료: {success_count}/{total_count} 회차 성공")
        print(f"[FOLDER] 출력 폴더: {self.data_dir.absolute()}")
        print("="*60)

def main():
    crawler = ImprovedTistoryCrawler()
    crawler.crawl_all()

if __name__ == "__main__":
    main()



