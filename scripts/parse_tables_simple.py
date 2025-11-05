"""
간소화된 표 파싱
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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

tables_dir = Path("data/tables")
parsed_tables_dir = Path("data/parsed_tables")
tables_dir.mkdir(exist_ok=True)
parsed_tables_dir.mkdir(exist_ok=True)

total_tables = 0

for exam_info in EXAM_URLS:
    year = exam_info['year']
    round_num = exam_info['round']
    url = exam_info['url']
    
    print(f"\n[{year}년 {round_num}회] 표 파싱...")
    
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
        
        # 표 찾기
        tables_found = []
        all_tables = article.find_all('table')
        print(f"  [발견] 표 {len(all_tables)}개")
        
        for table in all_tables:
            # 최소 크기 확인
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue
            
            # 문제 번호 찾기
            current = table
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
            
            if not q_no:
                continue
            
            # 표 데이터 파싱
            headers = []
            thead = table.find('thead')
            if thead:
                header_cells = thead.find_all(['th', 'td'])
                headers = [cell.get_text(strip=True) for cell in header_cells]
            elif rows:
                first_row_cells = rows[0].find_all(['th', 'td'])
                headers = [cell.get_text(strip=True) for cell in first_row_cells]
            
            # 데이터 행
            data_rows = []
            start_idx = 1 if not thead and headers else 0
            for row in rows[start_idx:]:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data:
                    data_rows.append(row_data)
            
            if data_rows:
                tables_found.append({
                    "q_no": q_no,
                    "headers": headers,
                    "rows": data_rows,
                    "row_count": len(data_rows),
                    "col_count": len(headers) if headers else (len(data_rows[0]) if data_rows else 0)
                })
                print(f"  [표] Q{q_no:03d} - {len(data_rows)}행 x {len(headers)}열")
        
        if tables_found:
            doc_id = f"{year}_round{round_num}"
            round_dir = tables_dir / doc_id
            round_dir.mkdir(exist_ok=True)
            
            # 문제별 카운터
            q_counters = {}
            saved = []
            
            for table_info in tables_found:
                q_no = table_info['q_no']
                
                if q_no not in q_counters:
                    q_counters[q_no] = 0
                q_counters[q_no] += 1
                
                q_no_str = f"Q{q_no:03d}"
                json_filename = f"{q_no_str}_table{q_counters[q_no]}.json"
                json_filepath = round_dir / json_filename
                
                # JSON 저장
                with open(json_filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        "headers": table_info['headers'],
                        "rows": table_info['rows'],
                        "row_count": table_info['row_count'],
                        "col_count": table_info['col_count']
                    }, f, ensure_ascii=False, indent=2)
                
                saved.append({
                    "q_no": q_no_str,
                    "index": q_counters[q_no],
                    "json_path": f"data/tables/{doc_id}/{json_filename}",
                    "rows": table_info['row_count'],
                    "cols": table_info['col_count']
                })
            
            # 메타데이터 저장
            if saved:
                grouped = {}
                for item in saved:
                    q_no = item['q_no']
                    if q_no not in grouped:
                        grouped[q_no] = {
                            "doc_id": doc_id,
                            "q_no": q_no,
                            "table_refs": []
                        }
                    grouped[q_no]["table_refs"].append({
                        "id": f"table{item['index']}",
                        "json": item['json_path'],
                        "rows": item['rows'],
                        "cols": item['cols']
                    })
                
                json_file = parsed_tables_dir / f"tables_{doc_id}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(list(grouped.values()), f, ensure_ascii=False, indent=2)
                
                print(f"  [완료] {len(saved)}개 표 저장")
                total_tables += len(saved)
        else:
            print(f"  [정보] 표 없음")
    
    except Exception as e:
        print(f"  [ERROR] {e}")

driver.quit()
print(f"\n[총계] {total_tables}개 표 저장 완료")



