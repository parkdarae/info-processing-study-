"""
Tistory 정보처리기사 실기 기출문제 - 표 파싱 스크립트

문제에 포함된 표를 추출하여 이미지와 JSON으로 저장합니다.
- Selenium을 사용하여 동적 콘텐츠 로드
- HTML <table> 태그 추출 및 JSON 변환
- 표를 이미지로도 스크린샷 저장

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
from PIL import Image
import io

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

class TableParser:
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
            print(f"[WARNING] Chrome 드라이버 초기화 실패: {e}")
            print("[INFO] Edge 드라이버로 재시도...")
            try:
                self.driver = webdriver.Edge()
                print("[INFO] Edge 드라이버 초기화 성공")
            except Exception as e2:
                print(f"[ERROR] Edge 드라이버도 실패: {e2}")
                raise
        
        # 출력 디렉토리 설정
        self.images_dir = Path("images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        self.tables_dir = Path("data/tables")
        self.tables_dir.mkdir(parents=True, exist_ok=True)
        
        self.output_dir = Path("data/parsed_tables")
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
    
    def parse_table_to_json(self, table_elem) -> Dict[str, Any]:
        """HTML 표를 JSON으로 변환"""
        rows_data = []
        
        # 헤더 찾기
        headers = []
        thead = table_elem.find('thead')
        if thead:
            header_cells = thead.find_all(['th', 'td'])
            headers = [cell.get_text(strip=True) for cell in header_cells]
        else:
            # 첫 번째 행을 헤더로 사용
            first_row = table_elem.find('tr')
            if first_row:
                header_cells = first_row.find_all(['th', 'td'])
                headers = [cell.get_text(strip=True) for cell in header_cells]
        
        # 데이터 행 추출
        tbody = table_elem.find('tbody')
        rows = tbody.find_all('tr') if tbody else table_elem.find_all('tr')
        
        # 첫 행이 헤더였다면 스킵
        start_idx = 1 if not thead and headers else 0
        
        for row in rows[start_idx:]:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data:  # 빈 행 제외
                rows_data.append(row_data)
        
        return {
            "headers": headers,
            "rows": rows_data,
            "row_count": len(rows_data),
            "col_count": len(headers) if headers else (len(rows_data[0]) if rows_data else 0)
        }
    
    def screenshot_table(self, table_elem_selenium, save_path: Path) -> bool:
        """표를 스크린샷으로 저장"""
        try:
            # 요소로 스크롤
            self.driver.execute_script("arguments[0].scrollIntoView(true);", table_elem_selenium)
            time.sleep(0.5)
            
            # 스크린샷
            png_data = table_elem_selenium.screenshot_as_png
            
            # 이미지 저장
            image = Image.open(io.BytesIO(png_data))
            image.save(save_path)
            
            return True
        except Exception as e:
            print(f"[ERROR] 표 스크린샷 실패: {e}")
            return False
    
    def extract_tables(self, html: str, year: int, round_num: int, url: str) -> List[Dict[str, Any]]:
        """표 추출"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 본문 영역 찾기
        article = soup.find('div', class_='tt_article_useless_p_margin')
        if not article:
            print("[WARNING] 본문 영역을 찾을 수 없습니다.")
            return []
        
        tables = []
        current_question_no = None
        question_table_count = {}  # 문제별 표 카운터
        
        # 모든 요소를 순회
        all_elements = article.find_all(['p', 'div', 'table', 'h2', 'h3', 'h4'])
        
        for elem in all_elements:
            # 문제 번호 감지
            text = elem.get_text(strip=True)
            q_match = re.match(r'^(\d+)\.\s', text)
            if q_match:
                current_question_no = int(q_match.group(1))
                if current_question_no not in question_table_count:
                    question_table_count[current_question_no] = 0
                continue
            
            # 표 찾기
            table_elems = []
            if elem.name == 'table':
                table_elems = [elem]
            else:
                table_elems = elem.find_all('table')
            
            for table_elem in table_elems:
                # 표 크기 확인 (너무 작은 표 제외)
                rows = table_elem.find_all('tr')
                if len(rows) < 2:  # 최소 2행 (헤더 + 데이터)
                    continue
                
                # 문제 번호 확인
                if current_question_no is None:
                    print(f"[WARNING] 문제 번호 없는 표 발견")
                    continue
                
                question_table_count[current_question_no] += 1
                table_index = question_table_count[current_question_no]
                
                # 표 데이터 파싱
                table_data = self.parse_table_to_json(table_elem)
                
                tables.append({
                    "question_no": current_question_no,
                    "index": table_index,
                    "data": table_data,
                    "html": str(table_elem)
                })
                
                print(f"[TABLE] 문제 {current_question_no}-{table_index}: {table_data['row_count']}행 x {table_data['col_count']}열")
        
        return tables
    
    def save_tables(self, tables: List[Dict[str, Any]], year: int, round_num: int):
        """표 저장"""
        doc_id = f"{year}_round{round_num}"
        
        # 년도-회차별 폴더 생성
        round_tables_dir = self.tables_dir / doc_id
        round_tables_dir.mkdir(parents=True, exist_ok=True)
        
        round_images_dir = self.images_dir / doc_id
        round_images_dir.mkdir(parents=True, exist_ok=True)
        
        # 각 표를 JSON과 이미지로 저장
        saved_tables = []
        
        for table_info in tables:
            q_no = table_info['question_no']
            table_index = table_info['index']
            table_data = table_info['data']
            
            q_no_str = f"Q{q_no:03d}"
            
            # JSON 파일명
            json_filename = f"{q_no_str}_table{table_index}.json"
            json_filepath = round_tables_dir / json_filename
            
            # JSON 저장
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(table_data, f, ensure_ascii=False, indent=2)
            
            print(f"[SAVE JSON] {json_filepath}")
            
            # 이미지는 Selenium을 통해 스크린샷 (별도로 처리 필요)
            # 현재는 JSON만 저장하고, 이미지는 parse_images.py에서 처리
            img_filename = f"{q_no_str}_table{table_index}.png"
            
            saved_tables.append({
                "question_no": q_no,
                "q_no_str": q_no_str,
                "index": table_index,
                "json_path": f"data/tables/{doc_id}/{json_filename}",
                "image_path": f"images/{doc_id}/{img_filename}",
                "rows": table_data['row_count'],
                "cols": table_data['col_count']
            })
        
        # 메타데이터 저장
        output_file = self.output_dir / f"tables_{doc_id}.json"
        
        # 문제 번호별로 그룹화
        grouped = {}
        for table_info in saved_tables:
            q_no_str = table_info['q_no_str']
            if q_no_str not in grouped:
                grouped[q_no_str] = {
                    "doc_id": doc_id,
                    "q_no": q_no_str,
                    "table_refs": []
                }
            
            grouped[q_no_str]["table_refs"].append({
                "id": f"table{table_info['index']}",
                "json": table_info['json_path'],
                "image": table_info['image_path'],
                "rows": table_info['rows'],
                "cols": table_info['cols']
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(list(grouped.values()), f, ensure_ascii=False, indent=2)
        
        print(f"[JSON] {output_file} (총 {len(grouped)}개 문제, {len(saved_tables)}개 표)")
    
    def parse_exam(self, exam_info: Dict[str, Any]) -> bool:
        """단일 회차 파싱"""
        year = exam_info['year']
        round_num = exam_info['round']
        url = exam_info['url']
        
        print(f"\n{'='*60}")
        print(f"[START] 표 파싱: {year}년 {round_num}회")
        print(f"[URL] {url}")
        print(f"{'='*60}")
        
        # HTML 가져오기
        html = self.fetch_page(url)
        if not html:
            return False
        
        # 표 추출
        tables = self.extract_tables(html, year, round_num, url)
        
        if not tables:
            print(f"[INFO] 표를 찾을 수 없습니다. (표가 없는 회차일 수 있음)")
            return True  # 표가 없는 것도 정상
        
        print(f"[SUCCESS] {len(tables)}개 표 발견")
        
        # 저장
        self.save_tables(tables, year, round_num)
        
        return True
    
    def parse_all(self):
        """전체 회차 파싱"""
        print("\n" + "="*60)
        print("[START] Tistory 기출문제 표 파싱 시작")
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
                import traceback
                traceback.print_exc()
            
            # 서버 부하 방지
            time.sleep(2)
        
        print("\n" + "="*60)
        print(f"[COMPLETE] 표 파싱 완료: {success_count}/{total_count} 회차 성공")
        print(f"[FOLDER] 표 JSON: {self.tables_dir.absolute()}")
        print(f"[FOLDER] 메타데이터: {self.output_dir.absolute()}")
        print("="*60)

def main():
    parser = TableParser()
    parser.parse_all()

if __name__ == "__main__":
    main()



