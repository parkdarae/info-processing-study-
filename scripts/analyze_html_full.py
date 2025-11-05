"""
전체 HTML 구조 분석
"""
import requests
from bs4 import BeautifulSoup
import re

url = "https://chobopark.tistory.com/540"

response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# 본문 찾기
content = soup.find('div', class_='entry-content') or \
          soup.find('div', {'itemprop': 'articleBody'}) or \
          soup.find('article')

if content:
    print("="*60)
    print("HTML 구조 분석")
    print("="*60)
    
    # 첫 번째 문제 부분 찾기 (1. 로 시작하는 부분)
    text = content.get_text('\n')
    
    # 1번 문제 찾기
    match = re.search(r'1\.\s+(.+?)(?=\n2\.|$)', text, re.DOTALL)
    if match:
        question_1_text = match.group(0)[:500]
        print("\n첫 번째 문제 텍스트 (처음 500자):")
        print(question_1_text)
    
    # 색상이 있는 모든 요소 찾기
    print("\n" + "="*60)
    print("색상이 있는 요소들:")
    print("="*60)
    
    colored_elements = []
    
    # 모든 요소에서 style 속성 확인
    for tag in content.find_all(style=True):
        style = tag.get('style', '')
        text = tag.get_text(strip=True)[:100]
        
        # 색상 관련 스타일만
        if 'color' in style.lower():
            colored_elements.append({
                'tag': tag.name,
                'style': style,
                'text': text
            })
    
    print(f"\n총 {len(colored_elements)}개 색상 요소 발견")
    print("\n처음 20개:")
    for i, elem in enumerate(colored_elements[:20], 1):
        print(f"\n{i}. <{elem['tag']}>")
        print(f"   style: {elem['style']}")
        print(f"   text: {elem['text']}")
    
    # 초록색 요소
    print("\n" + "="*60)
    print("초록색 요소들:")
    print("="*60)
    green_count = 0
    for elem in colored_elements:
        style_lower = elem['style'].lower()
        if any(g in style_lower for g in ['00b050', '00b04f', 'green', '008000']):
            green_count += 1
            print(f"\n<{elem['tag']}>: {elem['text']}")
    
    print(f"\n총 {green_count}개 초록색 요소")
    
    # 파란색 요소
    print("\n" + "="*60)
    print("파란색 요소들:")
    print("="*60)
    blue_count = 0
    for elem in colored_elements:
        style_lower = elem['style'].lower()
        if any(b in style_lower for b in ['0070c0', '0070c1', 'blue', '0000ff']):
            blue_count += 1
            print(f"\n<{elem['tag']}>: {elem['text']}")
    
    print(f"\n총 {blue_count}개 파란색 요소")

else:
    print("본문을 찾을 수 없습니다.")



