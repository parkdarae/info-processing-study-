"""
간소화된 이미지 파싱 - 빠른 실행
한 번에 모든 이미지를 찾아 다운로드
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re
import json
from pathlib import Path
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

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

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print("[INFO] Chrome 초기화...")
driver = webdriver.Chrome(options=chrome_options)

images_dir = Path("images")
parsed_images_dir = Path("data/parsed_images")
images_dir.mkdir(exist_ok=True)
parsed_images_dir.mkdir(exist_ok=True)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

total_images = 0

for exam_info in EXAM_URLS:  # 전체 실행
    year = exam_info['year']
    round_num = exam_info['round']
    url = exam_info['url']
    
    print(f"\n[{year}년 {round_num}회] 이미지 파싱...")
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tt_article_useless_p_margin"))
        )
        time.sleep(1)
        
        # Alert 처리
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', class_='tt_article_useless_p_margin')
        
        if not article:
            print(f"  [ERROR] 본문 없음")
            continue
        
        # 이미지 찾기
        images = []
        all_imgs = article.find_all('img')
        print(f"  [발견] 이미지 {len(all_imgs)}개")
        
        for img in all_imgs:
            src = img.get('src', '')
            if not src or 'ad' in src.lower() or 'banner' in src.lower():
                continue
            
            # 절대 URL
            if not src.startswith('http'):
                src = f"https:{src}" if src.startswith('//') else f"https://chobopark.tistory.com{src}"
            
            # 문제 번호 찾기
            current = img
            q_no = None
            for _ in range(15):
                prev = current.find_previous(['p', 'div', 'h1', 'h2', 'h3'])
                if prev:
                    text = prev.get_text(strip=True)
                    match = re.match(r'^(\d+)\.\s', text)
                    if match:
                        q_no = int(match.group(1))
                        break
                    current = prev
                else:
                    break
            
            if q_no:
                images.append({"q_no": q_no, "src": src})
        
        if images:
            doc_id = f"{year}_round{round_num}"
            round_dir = images_dir / doc_id
            round_dir.mkdir(exist_ok=True)
            
            # 문제별 카운터
            q_counters = {}
            saved = []
            
            for img_info in images:
                q_no = img_info['q_no']
                src = img_info['src']
                
                if q_no not in q_counters:
                    q_counters[q_no] = 0
                q_counters[q_no] += 1
                
                q_no_str = f"Q{q_no:03d}"
                ext = '.png'
                if src.endswith('.jpg') or src.endswith('.jpeg'):
                    ext = '.jpg'
                
                filename = f"{q_no_str}_{q_counters[q_no]}{ext}"
                filepath = round_dir / filename
                
                # 다운로드
                try:
                    resp = session.get(src, timeout=10)
                    resp.raise_for_status()
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    
                    saved.append({
                        "q_no": q_no_str,
                        "path": f"images/{doc_id}/{filename}",
                        "src": src
                    })
                    print(f"  [이미지] {q_no_str}_{q_counters[q_no]}")
                except Exception as e:
                    print(f"  [ERROR] {src}: {e}")
            
            # JSON 저장
            if saved:
                grouped = {}
                for item in saved:
                    q_no = item['q_no']
                    if q_no not in grouped:
                        grouped[q_no] = {
                            "doc_id": doc_id,
                            "q_no": q_no,
                            "image_refs": []
                        }
                    grouped[q_no]["image_refs"].append({
                        "path": item['path'],
                        "source_url": item['src']
                    })
                
                json_file = parsed_images_dir / f"images_{doc_id}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(list(grouped.values()), f, ensure_ascii=False, indent=2)
                
                print(f"  [완료] {len(saved)}개 이미지 저장")
                total_images += len(saved)
        else:
            print(f"  [정보] 이미지 없음")
    
    except Exception as e:
        print(f"  [ERROR] {e}")
        import traceback
        traceback.print_exc()

driver.quit()
print(f"\n[총계] {total_images}개 이미지 다운로드 완료")

