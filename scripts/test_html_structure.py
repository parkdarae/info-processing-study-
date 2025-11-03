"""
HTML 구조 분석 스크립트
실제 HTML에서 색상 정보와 구조를 확인합니다.
"""
import requests
from bs4 import BeautifulSoup

url = "https://chobopark.tistory.com/540"

response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# 본문 찾기
content = soup.find('div', class_='entry-content') or \
          soup.find('div', {'itemprop': 'articleBody'})

if content:
    # details 요소 찾기
    details_list = content.find_all('details')
    print(f"총 details 요소: {len(details_list)}개\n")
    
    # 첫 3개 details 내용 분석
    for i, details in enumerate(details_list[:3], 1):
        print(f"="*60)
        print(f"Details {i}:")
        print(f"="*60)
        
        # 모든 span 태그 확인
        spans = details.find_all('span')
        print(f"\n총 {len(spans)}개 span 태그:")
        for j, span in enumerate(spans[:10], 1):  # 처음 10개만
            style = span.get('style', '')
            text = span.get_text(strip=True)[:50]  # 처음 50자만
            print(f"  {j}. style='{style}'")
            print(f"     text='{text}'")
        
        # 모든 p 태그 확인
        ps = details.find_all('p')
        print(f"\n총 {len(ps)}개 p 태그:")
        for j, p in enumerate(ps[:5], 1):  # 처음 5개만
            style = p.get('style', '')
            text = p.get_text(strip=True)[:50]
            print(f"  {j}. style='{style}'")
            print(f"     text='{text}'")
        
        print()
else:
    print("본문을 찾을 수 없습니다.")


