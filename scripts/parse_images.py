"""
Tistory 정보처리기사 실기 기출문제 - 이미지 파싱 스크립트

문제에 포함된 이미지를 다운로드하여 년도-회차별로 저장합니다.
- Selenium을 사용하여 동적 콘텐츠 로드
- 본문 영역의 이미지만 추출 (광고/배너 제외)
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
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
import sys
from urllib.parse import urljoin

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

class ImageParser:
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
        
        self.output_dir = Path("data/parsed_images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 세션 설정 (이미지 다운로드용)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
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
    
    def download_image(self, img_url: str, save_path: Path) -> bool:
        """이미지 다운로드"""
        try:
            response = self.session.get(img_url, timeout=10)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"[ERROR] 이미지 다운로드 실패 ({img_url}): {e}")
            return False
    
    def is_valid_image(self, img_elem) -> bool:
        """유효한 이미지인지 확인 (광고/아이콘 제외)"""
        # src 속성 확인
        src = img_elem.get('src', '')
        if not src:
            return False
        
        # 광고/아이콘 필터링
        exclude_patterns = [
            'ad', 'banner', 'logo', 'icon', 'avatar',
            'badge', 'button', 'emoticon', 'emoji'
        ]
        
        src_lower = src.lower()
        for pattern in exclude_patterns:
            if pattern in src_lower:
                return False
        
        # 크기 확인 (너무 작은 이미지 제외)
        width = img_elem.get('width', '')
        height = img_elem.get('height', '')
        
        try:
            if width and int(width) < 50:
                return False
            if height and int(height) < 50:
                return False
        except:
            pass
        
        return True
    
    def extract_images(self, html: str, year: int, round_num: int, url: str) -> List[Dict[str, Any]]:
        """이미지 추출"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 본문 영역 찾기
        article = soup.find('div', class_='tt_article_useless_p_margin')
        if not article:
            print("[WARNING] 본문 영역을 찾을 수 없습니다.")
            return []
        
        images = []
        current_question_no = None
        question_image_count = {}  # 문제별 이미지 카운터
        
        # 모든 요소를 순회
        all_elements = article.find_all(['p', 'div', 'img', 'figure', 'h2', 'h3', 'h4'])
        
        for elem in all_elements:
            # 문제 번호 감지
            text = elem.get_text(strip=True)
            q_match = re.match(r'^(\d+)\.\s', text)
            if q_match:
                current_question_no = int(q_match.group(1))
                if current_question_no not in question_image_count:
                    question_image_count[current_question_no] = 0
                continue
            
            # 이미지 찾기
            img_elems = []
            if elem.name == 'img':
                img_elems = [elem]
            else:
                img_elems = elem.find_all('img')
            
            for img_elem in img_elems:
                if not self.is_valid_image(img_elem):
                    continue
                
                src = img_elem.get('src', '')
                if not src:
                    continue
                
                # 절대 URL로 변환
                img_url = urljoin(url, src)
                
                # alt 텍스트 (캡션)
                alt = img_elem.get('alt', '')
                
                # 문제 번호 확인
                if current_question_no is None:
                    print(f"[WARNING] 문제 번호 없는 이미지 발견: {img_url}")
                    continue
                
                question_image_count[current_question_no] += 1
                img_index = question_image_count[current_question_no]
                
                images.append({
                    "question_no": current_question_no,
                    "image_url": img_url,
                    "alt": alt,
                    "index": img_index
                })
                
                print(f"[IMAGE] 문제 {current_question_no}-{img_index}: {img_url}")
        
        return images
    
    def save_images(self, images: List[Dict[str, Any]], year: int, round_num: int):
        """이미지 저장"""
        doc_id = f"{year}_round{round_num}"
        
        # 년도-회차별 폴더 생성
        round_dir = self.images_dir / doc_id
        round_dir.mkdir(parents=True, exist_ok=True)
        
        # 각 이미지 다운로드 및 저장
        saved_images = []
        
        for img_info in images:
            q_no = img_info['question_no']
            img_index = img_info['index']
            img_url = img_info['image_url']
            
            q_no_str = f"Q{q_no:03d}"
            
            # 파일 확장자 추출
            ext = '.png'  # 기본값
            if '.' in img_url:
                url_ext = img_url.rsplit('.', 1)[-1].lower()
                if url_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    ext = f'.{url_ext}'
            
            filename = f"{q_no_str}_{img_index}{ext}"
            filepath = round_dir / filename
            
            # 이미지 다운로드
            if self.download_image(img_url, filepath):
                relative_path = f"images/{doc_id}/{filename}"
                saved_images.append({
                    "question_no": q_no,
                    "q_no_str": q_no_str,
                    "image_path": relative_path,
                    "alt": img_info['alt'],
                    "index": img_index,
                    "source_url": img_url
                })
                print(f"[SAVE] {filepath}")
            else:
                print(f"[FAIL] {filepath}")
        
        # JSON 메타데이터 저장
        output_file = self.output_dir / f"images_{doc_id}.json"
        
        # 문제 번호별로 그룹화
        grouped = {}
        for img_info in saved_images:
            q_no_str = img_info['q_no_str']
            if q_no_str not in grouped:
                grouped[q_no_str] = {
                    "doc_id": doc_id,
                    "q_no": q_no_str,
                    "image_refs": []
                }
            
            grouped[q_no_str]["image_refs"].append({
                "path": img_info['image_path'],
                "alt": img_info['alt'],
                "source_url": img_info['source_url']
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(list(grouped.values()), f, ensure_ascii=False, indent=2)
        
        print(f"[JSON] {output_file} (총 {len(grouped)}개 문제, {len(saved_images)}개 이미지)")
    
    def parse_exam(self, exam_info: Dict[str, Any]) -> bool:
        """단일 회차 파싱"""
        year = exam_info['year']
        round_num = exam_info['round']
        url = exam_info['url']
        
        print(f"\n{'='*60}")
        print(f"[START] 이미지 파싱: {year}년 {round_num}회")
        print(f"[URL] {url}")
        print(f"{'='*60}")
        
        # HTML 가져오기
        html = self.fetch_page(url)
        if not html:
            return False
        
        # 이미지 추출
        images = self.extract_images(html, year, round_num, url)
        
        if not images:
            print(f"[INFO] 이미지를 찾을 수 없습니다. (이미지가 없는 회차일 수 있음)")
            return True  # 이미지가 없는 것도 정상
        
        print(f"[SUCCESS] {len(images)}개 이미지 발견")
        
        # 저장
        self.save_images(images, year, round_num)
        
        return True
    
    def parse_all(self):
        """전체 회차 파싱"""
        print("\n" + "="*60)
        print("[START] Tistory 기출문제 이미지 파싱 시작")
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
        print(f"[COMPLETE] 이미지 파싱 완료: {success_count}/{total_count} 회차 성공")
        print(f"[FOLDER] 이미지 파일: {self.images_dir.absolute()}")
        print(f"[FOLDER] JSON 파일: {self.output_dir.absolute()}")
        print("="*60)

def main():
    parser = ImageParser()
    parser.parse_all()

if __name__ == "__main__":
    main()


