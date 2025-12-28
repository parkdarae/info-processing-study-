"""
HTML에서 코드가 어떻게 표시되는지 찾기
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# HTML 파일 읽기
with open('data/analysis_2024_round1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# "1. " 문자열 찾기
search_str = "1.  다음 Java"
pos = html.find(search_str)

if pos == -1:
    search_str = "1. 다음 Java"
    pos = html.find(search_str)

if pos == -1:
    print("[ERROR] 문제 1을 찾을 수 없습니다.")
    # 대체 검색
    search_str = "Java 코드"
    pos = html.find(search_str)
    if pos != -1:
        print(f"[INFO] 'Java 코드' 발견: 위치 {pos}")

if pos != -1:
    print(f"[FOUND] 문제 1 발견: 위치 {pos}")
    print(f"\n[컨텍스트] 이전 500자:")
    print("="*60)
    print(html[max(0, pos-500):pos])
    
    print(f"\n[컨텍스트] 해당 부분:")
    print("="*60)
    print(html[pos:pos+200])
    
    print(f"\n[컨텍스트] 이후 3000자 (코드가 있을 것으로 예상):")
    print("="*60)
    excerpt = html[pos:pos+3000]
    print(excerpt)
    
    # 특정 태그 찾기
    print(f"\n[분석] 태그 존재 여부:")
    print(f"  <pre>: {'<pre' in excerpt}")
    print(f"  <code>: {'<code' in excerpt}")
    print(f"  <img: {'<img' in excerpt}")
    print(f"  colorscripter: {'colorscripter' in excerpt}")
    print(f"  data-ke-type: {'data-ke-type' in excerpt}")
    
    # img 태그 위치 찾기
    if '<img' in excerpt:
        img_pos = excerpt.find('<img')
        print(f"\n[IMG] 이미지 태그 발견: 위치 {img_pos} (문제 시작 기준)")
        img_excerpt = excerpt[img_pos:img_pos+500]
        print(img_excerpt)
        
        # src 추출
        src_start = img_excerpt.find('src="')
        if src_start != -1:
            src_end = img_excerpt.find('"', src_start + 5)
            src = img_excerpt[src_start+5:src_end]
            print(f"\n[SRC] 이미지 소스: {src}")
else:
    print("[ERROR] 문제 1을 찾을 수 없습니다.")




