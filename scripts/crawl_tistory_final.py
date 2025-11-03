"""
Tistory 정보처리기사 실기 기출문제 크롤링 스크립트 (Selenium 버전)
더보기 버튼을 자동 클릭하여 동적 컨텐츠를 로드하고 정답과 해설을 정확히 추출합니다.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
    {"year": 2023, "round": 3, "url": "https://chobopark.tistory.com/453"},
    {"year": 2023, "round": 2, "url": "https://chobopark.tistory.com/420"},
    {"year": 2022, "round": 3, "url": "https://chobopark.tistory.com/424"},
    {"year": 2022, "round": 2, "url": "https://chobopark.tistory.com/423"},
    {"year": 2022, "round": 1, "url": "https://chobopark.tistory.com/271"},
    {"year": 2021, "round": 1, "url": "https://chobopark.tistory.com/191"},
]

class FinalTistoryCrawler:
    def __init__(self):
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # 백그라운드 실행
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            print("[INFO] Chrome 드라이버 초기화 중...")
            self.driver = webdriver.Chrome(options=chrome_options)
            print("[INFO] Chrome 드라이버 초기화 성공")
        except Exception as e:
            print(f"[WARNING] Chrome 드라이버 초기화 실패: {e}")
            print("[INFO] Edge 드라이버 시도 중...")
            try:
                self.driver = webdriver.Edge(options=chrome_options)
                print("[INFO] Edge 드라이버 초기화 성공")
            except Exception as e2:
                print(f"[ERROR] 브라우저 드라이버를 초기화할 수 없습니다: {e2}")
                raise
        
        # 출력 디렉토리 생성
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
    def __del__(self):
        """드라이버 정리"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except:
                pass
        
    def fetch_page(self, url: str) -> Optional[str]:
        """페이지 HTML 가져오기 (Selenium 사용, 더보기 버튼 자동 클릭)"""
        try:
            print(f"[DEBUG] 페이지 로드 중: {url}")
            self.driver.get(url)
            
            # 페이지 로드 대기
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tt_article_useless_p_margin"))
            )
            print("[DEBUG] 본문 영역 로드 완료")
            
            # "더보기" 버튼 찾기 및 클릭
            time.sleep(2)  # 페이지 완전 로드 대기
            
            more_button_clicked = 0
            try:
                # 여러 가지 "더보기" 버튼 셀렉터 시도
                selectors = [
                    "//a[contains(text(), '더보기')]",
                    "//button[contains(text(), '더보기')]",
                    "//span[contains(text(), '더보기')]",
                    "//*[@class='btn_open']",
                    "//*[contains(@class, 'more')]"
                ]
                
                for selector in selectors:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, selector)
                        for btn in buttons:
                            try:
                                if btn.is_displayed():
                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                                    time.sleep(0.5)
                                    self.driver.execute_script("arguments[0].click();", btn)
                                    more_button_clicked += 1
                                    print(f"[DEBUG] 더보기 버튼 클릭 완료 ({more_button_clicked})")
                                    time.sleep(1)
                            except Exception as e:
                                pass
                    except:
                        pass
            except Exception as e:
                print(f"[DEBUG] 더보기 버튼 처리 중 오류 (무시 가능): {e}")
            
            print(f"[DEBUG] 총 {more_button_clicked}개 더보기 버튼 클릭")
            
            # 페이지 완전 로드 대기
            time.sleep(2)
            
            html = self.driver.page_source
            print(f"[DEBUG] HTML 소스 가져오기 완료 (길이: {len(html)})")
            return html
            
        except Exception as e:
            print(f"[ERROR] 페이지 로드 실패 ({url}): {e}")
            return None
    
    def extract_questions(self, html: str, year: int, round_num: int, url: str) -> List[Dict[str, Any]]:
        """HTML에서 문제 추출 (완전 개선 버전 - 답안 추출 강화)"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 본문 추출
        content_area = soup.find('div', class_='tt_article_useless_p_margin') or \
                      soup.find('div', class_='entry-content') or \
                      soup.find('div', class_='article')
        
        if not content_area:
            print(f"[WARNING] 본문 영역을 찾을 수 없습니다: {url}")
            return []
        
        questions = []
        doc_id = f"{year}_round{round_num}"
        
        # 모든 <p> 태그 순회
        paragraphs = content_area.find_all('p', recursive=False)
        current_question = None
        after_question_count = 0  # 문제 번호 이후 수집한 단락 수
        max_paragraphs_per_question = 20  # 문제당 최대 단락 수
        
        for p_idx, p in enumerate(paragraphs):
            text = p.get_text(separator='\n', strip=True)
            
            # 빈 태그나 광고 건너뛰기
            if not text or '반응형' in text or len(text) < 3:
                continue
            
            # 문제 번호 감지 (라인 시작, 최소 20자 이상의 문장이 따라옴)
            q_num_match = re.match(r'^(\d+)\.\s+(.{20,})', text, re.DOTALL)
            
            if q_num_match:
                # 이전 문제 저장
                if current_question:
                    questions.append(current_question)
                
                q_num = int(q_num_match.group(1))
                question_text = q_num_match.group(2).strip()
                
                current_question = {
                    "doc_id": doc_id,
                    "page_range": [1, 1],
                    "q_no": f"Q{q_num:03d}",
                    "question_text": question_text,
                    "choices": [],
                    "answer": {"keys": [], "raw_text": ""},
                    "explanation": None,
                    "table_refs": [],
                    "image_refs": [],
                    "meta": {
                        "layout": "single",
                        "anchors": [f"{q_num}."],
                        "page_anchors": [1],
                        "confidence": 1.0,
                        "warnings": [],
                        "source_url": url,
                        "crawled_at": datetime.now().isoformat()
                    }
                }
                after_question_count = 0
                continue
            
            if not current_question:
                continue
            
            # 문제 번호 이후 단락만 처리 (다음 문제 번호 전까지)
            after_question_count += 1
            if after_question_count > max_paragraphs_per_question:
                continue
            
            # 초록색 답안 추출 (모든 span 확인)
            green_text = self.extract_colored_text(p, 'green')
            if green_text:
                # 다중 답안 파싱
                answers = self.parse_multiple_answers(green_text)
                if answers:
                    current_question['answer']['keys'].extend(answers)
                else:
                    current_question['answer']['keys'].append(green_text)
            
            # 파란색 해설 추출
            blue_text = self.extract_colored_text(p, 'blue')
            if blue_text:
                if current_question['explanation']:
                    current_question['explanation'] += "\n" + blue_text
                else:
                    current_question['explanation'] = blue_text
            
            # 문제 본문에 추가 (녹색/파란색이 아니고 의미있는 텍스트)
            if not green_text and not blue_text and '더보기' not in text and len(text) > 10:
                current_question['question_text'] += "\n" + text
        
        # 마지막 문제 저장
        if current_question:
            questions.append(current_question)
        
        # 답안 정리 및 중복 제거
        for q in questions:
            if q['answer']['keys']:
                # 중복 제거
                unique_answers = []
                for ans in q['answer']['keys']:
                    if ans not in unique_answers:
                        unique_answers.append(ans)
                q['answer']['keys'] = unique_answers
                q['answer']['raw_text'] = '\n'.join(unique_answers)
            else:
                q['meta']['warnings'].append("정답을 찾을 수 없음")
                q['meta']['confidence'] = 0.7
        
        print(f"[DEBUG] {len(questions)}개 문제 추출 완료")
        return questions
    
    def extract_colored_text(self, element, color: str) -> Optional[str]:
        """특정 색상의 텍스트 추출"""
        # 실제 Tistory에서 사용하는 색상 코드 (분석 결과 기반)
        color_codes = {
            'green': ['#009a87'],  # 답안 색상
            'blue': ['#006dd7']    # 해설 색상
        }
        
        spans = element.find_all('span', recursive=True)
        texts = []
        
        for span in spans:
            style = span.get('style', '')
            if not style:
                continue
            
            style_lower = style.lower()
            if 'color' in style_lower:
                # 스타일에서 color 값 추출
                color_match = re.search(r'color:\s*([^;]+)', style_lower)
                if color_match:
                    color_value = color_match.group(1).strip()
                    
                    # 색상 코드 매칭
                    for code in color_codes.get(color, []):
                        if code.lower() in color_value:
                            text = span.get_text(strip=True)
                            if text and len(text) > 1:
                                texts.append(text)
                            break
        
        return '\n'.join(texts) if texts else None
    
    def parse_multiple_answers(self, answer_text: str) -> List[str]:
        """다중 답안 파싱 (1. 답1 2. 답2 3. 답3 형식)"""
        # "1. ", "2. ", "3. " 패턴으로 분리
        pattern = r'(\d+)\.\s*([^\d]+?)(?=\d+\.\s*|$)'
        matches = re.findall(pattern, answer_text)
        
        if matches and len(matches) > 1:
            # 다중 답안
            return [f"{num}. {ans.strip()}" for num, ans in matches]
        
        return []
    
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
            "version": "3.0",
            "exam_info": exam_info,
            "total_questions": total,
            "questions_with_answers": with_answers,
            "questions_with_explanations": with_explanations,
            "total_warnings": warnings,
            "crawled_at": datetime.now().isoformat(),
            "success_rate": f"{(with_answers / total * 100):.1f}%" if total > 0 else "0%"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"[REPORT] {report['success_rate']} 정답 추출 성공 (총 {total}문제)")
    
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
        print("[START] Tistory 기출문제 크롤링 시작 (최종 버전)")
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
    crawler = FinalTistoryCrawler()
    crawler.crawl_all()

if __name__ == "__main__":
    main()

