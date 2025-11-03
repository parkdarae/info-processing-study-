"""
HTML을 파일로 저장하여 분석
"""
import requests
from bs4 import BeautifulSoup

url = "https://chobopark.tistory.com/540"

response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
response.encoding = 'utf-8'

# HTML 파일로 저장
with open('data/test_page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("[SAVE] HTML 저장 완료: data/test_page.html")

# 색상 요소 분석
soup = BeautifulSoup(response.text, 'html.parser')
content = soup.find('div', class_='entry-content') or \
          soup.find('div', {'itemprop': 'articleBody'})

if content:
    # 색상이 있는 모든 span 요소
    colored_spans = []
    for span in content.find_all('span', style=True):
        style = span.get('style', '')
        if 'color' in style.lower():
            text = span.get_text(strip=True)
            colored_spans.append({
                'style': style,
                'text': text
            })
    
    # 결과를 파일로 저장
    with open('data/colored_elements.txt', 'w', encoding='utf-8') as f:
        f.write(f"총 {len(colored_spans)}개 색상 span 요소\n\n")
        
        for i, elem in enumerate(colored_spans, 1):
            f.write(f"{i}. style: {elem['style']}\n")
            f.write(f"   text: {elem['text']}\n\n")
    
    print(f"[SAVE] 색상 요소 분석 완료: data/colored_elements.txt ({len(colored_spans)}개)")
    
    # 초록색과 파란색 분류
    green_texts = []
    blue_texts = []
    
    for elem in colored_spans:
        style_lower = elem['style'].lower()
        text = elem['text']
        
        # 초록색 판별
        if any(g in style_lower for g in ['00b050', '00b04f', '00b051', 'green', '008000', 'rgb(0, 176, 80)', 'rgb(0,176,80)']):
            green_texts.append(text)
        
        # 파란색 판별
        if any(b in style_lower for b in ['0070c0', '0070c1', '0070bf', 'blue', '0000ff', 'rgb(0, 112, 192)', 'rgb(0,112,192)']):
            blue_texts.append(text)
    
    # 결과 저장
    with open('data/answers_explanations.txt', 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write(f"초록색 텍스트 (정답): {len(green_texts)}개\n")
        f.write("="*60 + "\n\n")
        for i, text in enumerate(green_texts, 1):
            f.write(f"{i}. {text}\n\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write(f"파란색 텍스트 (해설): {len(blue_texts)}개\n")
        f.write("="*60 + "\n\n")
        for i, text in enumerate(blue_texts, 1):
            f.write(f"{i}. {text}\n\n")
    
    print(f"[SAVE] 정답/해설 분류 완료: data/answers_explanations.txt")
    print(f"  - 초록색 (정답): {len(green_texts)}개")
    print(f"  - 파란색 (해설): {len(blue_texts)}개")

print("\n[완료] 파일들을 확인하여 HTML 구조를 분석하세요.")


