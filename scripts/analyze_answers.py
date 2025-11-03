# -*- coding: utf-8 -*-
"""저장된 HTML에서 답안 구조 분석"""
from bs4 import BeautifulSoup
import sys

# 결과를 파일로 저장
output = open('data/answer_analysis.txt', 'w', encoding='utf-8')

def log(text):
    output.write(text + '\n')
    output.flush()

html = open('data/selenium_page.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

content = soup.find('div', class_='tt_article_useless_p_margin')
ps = content.find_all('p')

log(f"총 {len(ps)}개 단락 발견\n")

# 2번 문제 찾기
for i, p in enumerate(ps):
    text = p.get_text()
    
    # 2번 문제 찾기
    if text.startswith('2. ') and 'DB' in text[:50]:
        log(f"=== 2번 문제 발견 (P{i}) ===")
        log(f"내용: {text[:150]}\n")
        
        # 다음 20개 단락 확인
        log("=== 다음 단락들 ===")
        for j in range(i+1, min(i+21, len(ps))):
            ptext = ps[j].get_text(strip=True)
            if ptext and len(ptext) < 200:  # 너무 긴 단락 제외
                log(f"\n[P{j}] {ptext}")
                
                # 색상 span 확인
                spans = ps[j].find_all('span')
                for span in spans:
                    style = span.get('style', '')
                    if 'color' in style.lower():
                        span_text = span.get_text(strip=True)
                        log(f"   → 색상: {style[:50]} | 텍스트: {span_text[:50]}")
        
        break

# 색상별 span 통계
log("\n\n=== 전체 색상 span 통계 ===")
all_spans = content.find_all('span')
color_counts = {}

for span in all_spans:
    style = span.get('style', '')
    if 'color' in style.lower():
        # color 값 추출
        import re
        match = re.search(r'color:\s*([^;]+)', style)
        if match:
            color = match.group(1).strip()
            text = span.get_text(strip=True)
            if len(text) > 5:  # 의미있는 텍스트만
                if color not in color_counts:
                    color_counts[color] = []
                if len(color_counts[color]) < 3:  # 각 색상당 3개 예시만
                    color_counts[color].append(text[:50])

for color, examples in sorted(color_counts.items()):
    log(f"\n색상 {color}:")
    for ex in examples:
        log(f"  - {ex}")

output.close()
print("분석 완료! data/answer_analysis.txt 파일을 확인하세요.")

