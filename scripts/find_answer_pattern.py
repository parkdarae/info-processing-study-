"""
더보기 주변의 텍스트 패턴 분석
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

content = soup.find('div', class_='entry-content') or \
          soup.find('div', {'itemprop': 'articleBody'})

if content:
    # 전체 HTML 저장 (구조 확인용)
    with open('data/content_structure.txt', 'w', encoding='utf-8') as f:
        f.write(content.prettify())
    print("[SAVE] HTML 구조 저장: data/content_structure.txt")
    
    # 전체 텍스트
    full_text = content.get_text('\n', strip=True)
    
    # "더보기" 키워드 찾기
    more_positions = [m.start() for m in re.finditer(r'더보기', full_text)]
    print(f"\n더보기 키워드 발견: {len(more_positions)}개")
    
    # 각 "더보기" 주변 텍스트 분석
    with open('data/more_button_context.txt', 'w', encoding='utf-8') as f:
        for i, pos in enumerate(more_positions[:5], 1):  # 처음 5개만
            # 앞뒤 200자씩
            start = max(0, pos - 200)
            end = min(len(full_text), pos + 200)
            context = full_text[start:end]
            
            f.write("="*60 + "\n")
            f.write(f"더보기 #{i} (위치: {pos})\n")
            f.write("="*60 + "\n")
            f.write(context)
            f.write("\n\n")
    
    print("[SAVE] 더보기 주변 텍스트: data/more_button_context.txt")
    
    # 첫 번째 문제 전체 추출
    match = re.search(r'1\.\s+(.+?)(?=\n2\.|$)', full_text, re.DOTALL)
    if match:
        q1_text = match.group(0)
        with open('data/question_1_full.txt', 'w', encoding='utf-8') as f:
            f.write(q1_text)
        print(f"[SAVE] 첫 번째 문제 전체: data/question_1_full.txt ({len(q1_text)} 글자)")

print("\n[완료] 파일들을 확인하여 실제 패턴을 분석하세요.")


