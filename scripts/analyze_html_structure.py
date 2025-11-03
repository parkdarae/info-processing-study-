"""
특정 회차의 HTML 구조 분석 스크립트
2024년 1회를 예시로 코드 블록이 어떻게 표시되는지 확인
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 2024년 1회 URL (문제 1에 Java 코드가 있음)
TEST_URL = "https://chobopark.tistory.com/476"

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

print("[INFO] Chrome 드라이버 초기화...")
driver = webdriver.Chrome(options=chrome_options)

try:
    print(f"[INFO] 페이지 로드: {TEST_URL}")
    driver.get(TEST_URL)
    
    # 페이지 로드 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tt_article_useless_p_margin"))
    )
    print("[INFO] 본문 로드 완료")
    
    # 더보기 버튼 클릭
    time.sleep(2)
    more_clicks = 0
    
    selectors = [
        "//a[contains(text(), '더보기')]",
        "//button[contains(text(), '더보기')]",
        "//span[contains(text(), '더보기')]"
    ]
    
    for selector in selectors:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            for btn in buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    more_clicks += 1
                    time.sleep(0.3)
        except:
            pass
    
    print(f"[INFO] 더보기 버튼 {more_clicks}개 클릭")
    time.sleep(2)
    
    # Alert 처리
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"[INFO] Alert 발견: {alert_text}")
        alert.accept()
        print("[INFO] Alert 처리 완료")
        time.sleep(1)
    except:
        pass  # Alert가 없으면 무시
    
    # HTML 저장
    html = driver.page_source
    with open('data/analysis_2024_round1.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[SAVE] data/analysis_2024_round1.html (길이: {len(html)})")
    
    # BeautifulSoup으로 분석
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='tt_article_useless_p_margin')
    
    if not article:
        print("[ERROR] 본문 영역을 찾을 수 없습니다.")
    else:
        print("\n" + "="*60)
        print("[분석] 문제 1 영역 찾기")
        print("="*60)
        
        # 문제 1 찾기
        all_p = article.find_all('p')
        problem1_found = False
        
        for i, p in enumerate(all_p):
            text = p.get_text(strip=True)
            if text.startswith('1.') and not problem1_found:
                print(f"\n[문제 1 발견] 인덱스: {i}")
                print(f"텍스트: {text[:100]}...")
                problem1_found = True
                
                # 다음 10개 p 태그 검사
                print(f"\n[분석] 문제 1 이후 요소들:")
                for j in range(i+1, min(i+11, len(all_p))):
                    next_p = all_p[j]
                    next_text = next_p.get_text(strip=True)
                    
                    # 다음 문제 번호면 중단
                    if next_text.startswith('2.'):
                        print(f"\n[문제 2 발견] 인덱스: {j}")
                        break
                    
                    print(f"\n--- p[{j}] ---")
                    print(f"텍스트 (처음 80자): {next_text[:80]}")
                    print(f"텍스트 길이: {len(next_text)}")
                    print(f"줄바꿈 수: {next_text.count(chr(10))}")
                    
                    # 하위 요소 확인
                    has_pre = next_p.find('pre')
                    has_code = next_p.find('code')
                    has_colorscripter = next_p.find('div', class_='colorscripter-code')
                    has_img = next_p.find('img')
                    has_codeblock = next_p.find('div', {'data-ke-type': 'codeblock'})
                    
                    print(f"<pre>: {bool(has_pre)}")
                    print(f"<code>: {bool(has_code)}")
                    print(f".colorscripter-code: {bool(has_colorscripter)}")
                    print(f"<img>: {bool(has_img)}")
                    print(f"data-ke-type='codeblock': {bool(has_codeblock)}")
                    
                    # class 속성 확인
                    if next_p.get('class'):
                        print(f"클래스: {next_p.get('class')}")
                    
                    # 코드처럼 보이는지 확인
                    if 'class' in next_text.lower() or '{' in next_text or 'public' in next_text.lower():
                        print("⭐ 코드로 추정됨!")
                        print(f"\n전체 텍스트:\n{next_text[:500]}")
                        
                        # HTML 구조 출력
                        print(f"\nHTML 구조:")
                        print(str(next_p)[:500])
                
                break
        
        if not problem1_found:
            print("[WARNING] 문제 1을 찾을 수 없습니다.")
            print("\n처음 10개 p 태그:")
            for i, p in enumerate(all_p[:10]):
                print(f"{i}: {p.get_text(strip=True)[:80]}")

finally:
    driver.quit()
    print("\n[완료] 분석 완료")

