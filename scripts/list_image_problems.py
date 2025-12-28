# -*- coding: utf-8 -*-
"""
이미지가 있는 품질 낮은 해설 문제를 점수 낮은 순서로 정렬
"""
import json
from pathlib import Path
import sys
import io

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def list_image_problems():
    """이미지가 있는 문제를 점수 낮은 순서로 정렬"""
    report_path = Path(__file__).parent.parent / "data" / "poor_quality_explanations_all.json"
    
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 이미지가 있는 문제만 필터링
    items_with_images = [item for item in data['items'] if item.get('image_refs')]
    
    # 점수 낮은 순서로 정렬
    sorted_items = sorted(items_with_images, key=lambda x: x['quality']['score'])
    
    print("=" * 80)
    print(f"이미지가 있는 품질 낮은 해설 문제: {len(items_with_images)}개")
    print(f"점수 범위: {sorted_items[0]['quality']['score']} ~ {sorted_items[-1]['quality']['score']}")
    print("=" * 80)
    
    print("\n[상위 30개 문제 - 점수 낮은 순]")
    for i, item in enumerate(sorted_items[:30], 1):
        print(f"{i:2d}. {item['file']:30s} {item['q_no']:5s} "
              f"(점수: {item['quality']['score']:2d}, 이미지: {len(item['image_refs'])}개, "
              f"코드: {len(item.get('code_blocks', []))}개)")
        if i <= 10:
            print(f"    - 이슈: {', '.join(item['quality']['issues'])}")
            if item.get('image_refs'):
                print(f"    - 이미지: {item['image_refs'][0]}")
    
    # JSON으로 저장
    output_path = Path(__file__).parent.parent / "data" / "image_priority_list.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(sorted_items),
            "items": sorted_items[:30]  # 상위 30개만 저장
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장] 우선순위 리스트: {output_path}")
    print("=" * 80)

if __name__ == "__main__":
    list_image_problems()



