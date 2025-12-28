# -*- coding: utf-8 -*-
"""색상 텍스트 추출 함수 테스트"""
from bs4 import BeautifulSoup
import re

html = open('data/selenium_page.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
content = soup.find('div', class_='tt_article_useless_p_margin')
paragraphs = content.find_all('p', recursive=False)

output = open('data/color_test.txt', 'w', encoding='utf-8')

def log(text):
    output.write(text + '\n')
    output.flush()

def extract_colored_text(element, color: str):
    """특정 색상의 텍스트 추출"""
    color_codes = {
        'green': ['#009a87'],
        'blue': ['#006dd7']
    }
    
    spans = element.find_all('span', recursive=True)
    texts = []
    
    for span in spans:
        style = span.get('style', '')
        if not style:
            continue
        
        style_lower = style.lower()
        if 'color' in style_lower:
            color_match = re.search(r'color:\s*([^;]+)', style_lower)
            if color_match:
                color_value = color_match.group(1).strip()
                
                for code in color_codes.get(color, []):
                    if code.lower() in color_value:
                        text = span.get_text(strip=True)
                        if text and len(text) > 1:
                            texts.append(text)
                        break
    
    return '\n'.join(texts) if texts else None

# 2번 문제 찾기
for i, p in enumerate(paragraphs):
    text = p.get_text()
    if text.startswith('2. ') and 'DB' in text[:50]:
        log(f"2번 문제 발견 at P{i}\n")
        
        # 다음 20개 단락에서 색상 텍스트 추출
        for j in range(i+1, min(i+21, len(paragraphs))):
            green = extract_colored_text(paragraphs[j], 'green')
            blue = extract_colored_text(paragraphs[j], 'blue')
            
            if green or blue:
                log(f"\n[P{j}]")
                if green:
                    log(f"  초록색: {green}")
                if blue:
                    log(f"  파란색: {blue}")
        
        break

# 전체 초록색/파란색 텍스트 통계
log("\n\n=== 전체 통계 ===")
green_count = 0
blue_count = 0

for p in paragraphs:
    green = extract_colored_text(p, 'green')
    blue = extract_colored_text(p, 'blue')
    if green:
        green_count += 1
    if blue:
        blue_count += 1

log(f"초록색 텍스트가 있는 단락: {green_count}개")
log(f"파란색 텍스트가 있는 단락: {blue_count}개")

output.close()
print("테스트 완료! data/color_test.txt 확인")




