"""
Tistory 정보처리기사 실기 기출문제 - 코드 블록 파싱 스크립트

코드 블록을 추출하여 년도-회차별로 저장합니다.
- Selenium을 사용하여 동적 콘텐츠 로드
- <pre>, <code>, <div class="colorscripter-code"> 등에서 코드 추출
- 문제 번호와 매칭하여 저장

Zero Tolerance 정책:
- 실제 데이터만 사용
- 추정/가상 데이터 완전 차단
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
import sys

# 크롤링 대상 URL 목록
EXAM_URLS = [
    {"year": 2025, "round": 1, "url": "https://chobopark.tistory.com/540"},
    {"year": 2025, "round": 2, "url": "https://chobopark.tistory.com/554"},
    {"year": 2024, "round": 3, "url": "https://chobopark.tistory.com/495"},
    {"year": 2024, "round": 2, "url": "https://chobopark.tistory.com/483"},
    {"year": 2024, "round": 1, "url": "https://chobopark.tistory.com/476"},
    {"year": 2023, "round": 3, "url": "https://chobopark.tistory.com/453"},
    {"year": 2023, "round": 2, "url": "https://chobopark.tistory.com/420"},
    {"year": 2023, "round": 1, "url": "https://chobopark.tistory.com/372"},
    {"year": 2022, "round": 3, "url": "https://chobopark.tistory.com/424"},
    {"year": 2022, "round": 2, "url": "https://chobopark.tistory.com/423"},
    {"year": 2022, "round": 1, "url": "https://chobopark.tistory.com/271"},
    {"year": 2021, "round": 1, "url": "https://chobopark.tistory.com/191"},
]

class CodeBlockParser:
    def __init__(self):
        sys.stdout.reconfigure(encoding='utf-8')
        
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            print("[INFO] Chrome 드라이버 초기화 중...")
            self.driver = webdriver.Chrome(options=chrome_options)
            print("[INFO] Chrome 드라이버 초기화 성공")
        except Exception as e:
            print(f"[ERROR] Chrome 드라이버 초기화 실패: {e}")
            print("[INFO] Edge 드라이버로 재시도...")
            try:
                self.driver = webdriver.Edge()
                print("[INFO] Edge 드라이버 초기화 성공")
            except Exception as e2:
                print(f"[ERROR] Edge 드라이버도 실패: {e2}")
                raise
        
        # 출력 디렉토리 설정
        self.codes_dir = Path("data/codes")
        self.codes_dir.mkdir(parents=True, exist_ok=True)
        
        self.output_dir = Path("data/parsed_codes")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def __del__(self):
        """드라이버 종료"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def fetch_page(self, url: str) -> Optional[str]:
        """페이지 HTML 가져오기 (더보기 버튼 클릭)"""
        try:
            print(f"[DEBUG] 페이지 로드 중: {url}")
            self.driver.get(url)
            
            # 페이지 로드 대기
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tt_article_useless_p_margin"))
            )
            print("[DEBUG] 본문 영역 로드 완료")
            
            # "더보기" 버튼 찾기 및 클릭
            time.sleep(2)
            more_button_clicked = 0
            
            try:
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
                            except:
                                pass
                    except:
                        pass
            except Exception as e:
                print(f"[DEBUG] 더보기 버튼 처리 중 오류 (무시 가능): {e}")
            
            print(f"[DEBUG] 총 {more_button_clicked}개 더보기 버튼 클릭")
            time.sleep(2)
            
            html = self.driver.page_source
            print(f"[DEBUG] HTML 소스 가져오기 완료 (길이: {len(html)})")
            return html
            
        except Exception as e:
            print(f"[ERROR] 페이지 로드 실패 ({url}): {e}")
            return None
    
    def detect_language(self, code: str) -> str:
        """코드 언어 감지"""
        code_lower = code.lower()
        
        # Java
        if 'public class' in code_lower or 'public static void main' in code_lower:
            return 'java'
        # C/C++
        elif '#include' in code_lower or 'printf' in code_lower or 'scanf' in code_lower:
            return 'c'
        # Python
        elif 'def ' in code_lower or 'import ' in code_lower or 'print(' in code_lower:
            return 'python'
        # JavaScript
        elif 'function' in code_lower or 'const ' in code_lower or 'let ' in code_lower or 'var ' in code_lower:
            return 'javascript'
        # SQL
        elif 'select ' in code_lower or 'from ' in code_lower or 'where ' in code_lower:
            return 'sql'
        else:
            return 'unknown'
    
    def extract_code_blocks(self, html: str, year: int, round_num: int, url: str) -> List[Dict[str, Any]]:
        """코드 블록 추출"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 본문 영역 찾기
        article = soup.find('div', class_='tt_article_useless_p_margin')
        if not article:
            print("[WARNING] 본문 영역을 찾을 수 없습니다.")
            return []
        
        code_blocks = []
        
        # 모든 colorscripter 코드 블록 찾기
        colorscripters = article.find_all('div', class_='colorscripter-code')
        
        print(f"[DEBUG] colorscripter 블록 {len(colorscripters)}개 발견")
        
        for colorscripter in colorscripters:
            # 이 colorscripter 앞에 있는 문제 번호 찾기
            current_elem = colorscripter
            question_no = None
            
            # 최대 10개 이전 형제/부모 요소 검사
            for _ in range(10):
                prev = current_elem.find_previous(['p', 'h1', 'h2', 'h3', 'h4', 'div'])
                if prev:
                    text = prev.get_text(strip=True)
                    q_match = re.match(r'^(\d+)\.\s', text)
                    if q_match:
                        question_no = int(q_match.group(1))
                        break
                    current_elem = prev
                else:
                    break
            
            if not question_no:
                print(f"[WARNING] colorscripter 블록의 문제 번호를 찾을 수 없음")
                continue
            
            # colorscripter-code-table의 두 번째 td에서 코드 추출
            table = colorscripter.find('table', class_='colorscripter-code-table')
            code_text = None
            
            if table:
                tds = table.find_all('td')
                if len(tds) >= 2:
                    # 두 번째 td에 실제 코드가 있음
                    code_td = tds[1]
                    # 최상위 div 찾기
                    top_div = code_td.find('div', recursive=False)
                    if top_div:
                        # 모든 하위 div에서 텍스트 추출 (줄 단위)
                        line_divs = top_div.find_all('div', recursive=False)
                        code_lines = []
                        for line_div in line_divs:
                            line_text = line_div.get_text()
                            # 빈 줄도 포함
                            code_lines.append(line_text)
                        code_text = '\n'.join(code_lines)
            
            # 실패하면 전체 텍스트 추출
            if not code_text:
                code_text = colorscripter.get_text()
            
            if code_text and len(code_text.strip()) > 20:
                # 줄 번호 제거
                lines = code_text.split('\n')
                cleaned_lines = []
                for line in lines:
                    line_stripped = line.strip()
                    # 숫자만 있는 줄 제거
                    if line_stripped and not line_stripped.isdigit():
                        cleaned_lines.append(line)
                
                code_text = '\n'.join(cleaned_lines).strip()
                
                if len(code_text) > 20:
                    language = self.detect_language(code_text)
                    line_count = len([l for l in code_text.split('\n') if l.strip()])
                    
                    code_blocks.append({
                        "question_no": question_no,
                        "language": language,
                        "code": code_text,
                        "line_numbers": [1, line_count]
                    })
                    
                    print(f"[CODE] 문제 {question_no}: {language} 코드 ({line_count}줄)")
        
        return code_blocks
    
    def save_code_blocks(self, code_blocks: List[Dict[str, Any]], year: int, round_num: int):
        """코드 블록 저장"""
        doc_id = f"{year}_round{round_num}"
        
        # 년도-회차별 폴더 생성
        round_dir = self.codes_dir / doc_id
        round_dir.mkdir(parents=True, exist_ok=True)
        
        # 각 코드 블록을 개별 파일로 저장
        for block in code_blocks:
            q_no = block['question_no']
            if q_no is None:
                continue
            
            q_no_str = f"Q{q_no:03d}"
            filename = f"{q_no_str}_code.txt"
            filepath = round_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(block['code'])
            
            print(f"[SAVE] {filepath}")
        
        # JSON 메타데이터 저장
        output_file = self.output_dir / f"codes_{doc_id}.json"
        
        # 문제 번호별로 그룹화
        grouped = {}
        for block in code_blocks:
            q_no = block['question_no']
            if q_no is None:
                continue
            
            q_no_str = f"Q{q_no:03d}"
            if q_no_str not in grouped:
                grouped[q_no_str] = {
                    "doc_id": doc_id,
                    "q_no": q_no_str,
                    "code_blocks": []
                }
            
            grouped[q_no_str]["code_blocks"].append({
                "language": block['language'],
                "code": block['code'],
                "line_numbers": block['line_numbers'],
                "file": f"data/codes/{doc_id}/{q_no_str}_code.txt"
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(list(grouped.values()), f, ensure_ascii=False, indent=2)
        
        print(f"[JSON] {output_file} (총 {len(grouped)}개 문제)")
    
    def parse_exam(self, exam_info: Dict[str, Any]) -> bool:
        """단일 회차 파싱"""
        year = exam_info['year']
        round_num = exam_info['round']
        url = exam_info['url']
        
        print(f"\n{'='*60}")
        print(f"[START] 코드 블록 파싱: {year}년 {round_num}회")
        print(f"[URL] {url}")
        print(f"{'='*60}")
        
        # HTML 가져오기
        html = self.fetch_page(url)
        if not html:
            return False
        
        # 코드 블록 추출
        code_blocks = self.extract_code_blocks(html, year, round_num, url)
        
        if not code_blocks:
            print(f"[WARNING] 코드 블록을 찾을 수 없습니다.")
            return False
        
        print(f"[SUCCESS] {len(code_blocks)}개 코드 블록 추출 완료")
        
        # 저장
        self.save_code_blocks(code_blocks, year, round_num)
        
        return True
    
    def parse_all(self):
        """전체 회차 파싱"""
        print("\n" + "="*60)
        print("[START] Tistory 기출문제 코드 블록 파싱 시작")
        print("="*60)
        
        success_count = 0
        total_count = len(EXAM_URLS)
        
        for exam_info in EXAM_URLS:
            try:
                success = self.parse_exam(exam_info)
                if success:
                    success_count += 1
            except Exception as e:
                print(f"[ERROR] 파싱 실패: {e}")
            
            # 서버 부하 방지
            time.sleep(2)
        
        print("\n" + "="*60)
        print(f"[COMPLETE] 코드 블록 파싱 완료: {success_count}/{total_count} 회차 성공")
        print(f"[FOLDER] 코드 파일: {self.codes_dir.absolute()}")
        print(f"[FOLDER] JSON 파일: {self.output_dir.absolute()}")
        print("="*60)

def main():
    parser = CodeBlockParser()
    parser.parse_all()

if __name__ == "__main__":
    main()

