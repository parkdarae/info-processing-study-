"""
2022년 회차만 코드 블록 파싱
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
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 2022년 회차만
EXAM_URLS = [
    {"year": 2022, "round": 1, "url": "https://chobopark.tistory.com/271"},
    {"year": 2022, "round": 2, "url": "https://chobopark.tistory.com/423"},
    {"year": 2022, "round": 3, "url": "https://chobopark.tistory.com/424"},
]

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print("[INFO] Chrome 초기화...")
driver = webdriver.Chrome(options=chrome_options)

codes_dir = Path("data/codes")
parsed_codes_dir = Path("data/parsed_codes")
codes_dir.mkdir(parents=True, exist_ok=True)
parsed_codes_dir.mkdir(parents=True, exist_ok=True)

total_codes = 0

for exam_info in EXAM_URLS:
    year = exam_info['year']
    round_num = exam_info['round']
    url = exam_info['url']
    
    print(f"\n[{year}년 {round_num}회] 파싱 시작...")
    
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tt_article_useless_p_margin"))
    )
    time.sleep(2)
    
    # 더보기 클릭
    for _ in range(3):
        try:
            buttons = driver.find_elements(By.XPATH, "//a[contains(text(), '더보기')]")
            for btn in buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.3)
        except:
            pass
    
    # Alert 처리
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
    
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='tt_article_useless_p_margin')
    
    if not article:
        print(f"  [ERROR] 본문 없음")
        continue
    
    # colorscripter 찾기
    colorscripters = article.find_all('div', class_='colorscripter-code')
    print(f"  [발견] colorscripter {len(colorscripters)}개")
    
    code_blocks = []
    
    for cs in colorscripters:
        # 문제 번호 찾기
        current = cs
        q_no = None
        for _ in range(10):
            prev = current.find_previous(['p', 'div'])
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
        
        # 코드 추출
        table = cs.find('table', class_='colorscripter-code-table')
        if table:
            tds = table.find_all('td')
            if len(tds) >= 2:
                code_td = tds[1]
                top_div = code_td.find('div', recursive=False)
                if top_div:
                    line_divs = top_div.find_all('div', recursive=False)
                    code_lines = [div.get_text() for div in line_divs]
                    code_text = '\n'.join(code_lines)
                    
                    # 줄 번호 제거
                    lines = [l for l in code_text.split('\n') if l.strip() and not l.strip().isdigit()]
                    code_text = '\n'.join(lines).strip()
                    
                    if len(code_text) > 20:
                        # 언어 감지
                        lang = 'unknown'
                        if 'public class' in code_text or 'public static' in code_text:
                            lang = 'java'
                        elif '#include' in code_text or 'printf' in code_text:
                            lang = 'c'
                        elif 'def ' in code_text or 'print(' in code_text:
                            lang = 'python'
                        
                        code_blocks.append({
                            "question_no": q_no,
                            "language": lang,
                            "code": code_text,
                            "line_numbers": [1, len([l for l in code_text.split('\n') if l.strip()])]
                        })
                        
                        print(f"  [코드] Q{q_no:03d} - {lang}")
    
    if code_blocks:
        # 파일 저장
        doc_id = f"{year}_round{round_num}"
        round_dir = codes_dir / doc_id
        round_dir.mkdir(exist_ok=True)
        
        # 문제별 그룹화
        grouped = {}
        for block in code_blocks:
            q_no = block['question_no']
            q_no_str = f"Q{q_no:03d}"
            
            # txt 파일 저장
            txt_file = round_dir / f"{q_no_str}_code.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(block['code'])
            
            # JSON 메타데이터
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
        
        # JSON 저장
        json_file = parsed_codes_dir / f"codes_{doc_id}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(list(grouped.values()), f, ensure_ascii=False, indent=2)
        
        print(f"  [완료] {len(grouped)}개 문제 저장")
        total_codes += len(grouped)
    else:
        print(f"  [경고] 코드 없음")

driver.quit()
print(f"\n[총계] {total_codes}개 코드 블록 추가 완료")


