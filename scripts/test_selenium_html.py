"""Selenium으로 로드한 HTML을 파일로 저장하여 분석"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Chrome 옵션
opts = Options()
opts.add_argument('--headless=new')

# 드라이버 시작
driver = webdriver.Chrome(options=opts)

try:
    # 페이지 로드
    driver.get('https://chobopark.tistory.com/191')
    time.sleep(3)
    
    # 더보기 버튼 클릭
    buttons = driver.find_elements(By.XPATH, "//a[text()='더보기']")
    print(f"찾은 더보기 버튼: {len(buttons)}개")
    
    for i, btn in enumerate(buttons[:10]):  # 처음 10개만
        try:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                print(f"버튼 {i+1} 클릭 완료")
                time.sleep(0.5)
        except:
            pass
    
    time.sleep(2)
    
    # HTML 저장
    html = driver.page_source
    with open('data/selenium_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML 저장 완료: {len(html)} bytes")
    
    # 답안 영역 분석
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_='tt_article_useless_p_margin')
    
    # 2번 문제 찾기
    paragraphs = content.find_all('p')
    for i, p in enumerate(paragraphs):
        text = p.get_text()
        if '2. 다음은 DB 설계' in text:
            print(f"\n=== 2번 문제 발견 (P{i}) ===")
            print(text[:200])
            
            # 다음 10개 단락 확인
            for j in range(i+1, min(i+11, len(paragraphs))):
                p_text = paragraphs[j].get_text(strip=True)
                if p_text:
                    print(f"\nP{j}: {p_text[:100]}")
                    
                    # 색상 span 찾기
                    spans = paragraphs[j].find_all('span')
                    for span in spans:
                        style = span.get('style', '')
                        if 'color' in style:
                            print(f"  색상 span: style='{style}' text='{span.get_text()[:50]}'")
            break
    
finally:
    driver.quit()



