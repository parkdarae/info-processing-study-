# -*- coding: utf-8 -*-
"""파싱 로직 디버깅"""
from bs4 import BeautifulSoup
import re

html = open('data/selenium_page.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

content = soup.find('div', class_='tt_article_useless_p_margin')
paragraphs = content.find_all('p', recursive=False)

print(f"총 단락 수 (recursive=False): {len(paragraphs)}")

# 2번 문제 찾기
for i, p in enumerate(paragraphs):
    text = p.get_text(separator='\n', strip=True)
    
    # 문제 번호 감지
    q_num_match = re.match(r'^(\d+)\.\s+(.{20,})', text, re.DOTALL)
    
    if q_num_match and q_num_match.group(1) == '2':
        print(f"\n=== 2번 문제 발견 (인덱스 {i}) ===")
        print(f"문제 텍스트: {text[:150]}")
        print(f"\n=== 다음 10개 단락 분석 ===")
        
        for j in range(i+1, min(i+11, len(paragraphs))):
            p_text = paragraphs[j].get_text(strip=True)
            if p_text and len(p_text) < 200:
                print(f"\n[{j}] {p_text[:100]}")
                
                # 초록색 텍스트 찾기
                green_spans = paragraphs[j].find_all('span')
                for span in green_spans:
                    style = span.get('style', '')
                    if '#009a87' in style:
                        print(f"  ✓ 초록색 답안: {span.get_text()}")
                
                # 파란색 텍스트 찾기
                blue_spans = paragraphs[j].find_all('span')
                for span in blue_spans:
                    style = span.get('style', '')
                    if '#006dd7' in style:
                        print(f"  ✓ 파란색 해설: {span.get_text()}")
        
        break

print("\n\n=== recursive=True로 다시 시도 ===")
paragraphs_all = content.find_all('p')
print(f"총 단락 수 (recursive=True): {len(paragraphs_all)}")



