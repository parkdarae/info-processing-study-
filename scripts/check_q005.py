import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/items_2025_round1.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(l) for l in f if l.strip()]

q005 = questions[4]  # Q005는 5번째 (인덱스 4)

print("="*60)
print("2025년 1회 Q005 확인")
print("="*60)
print(f"문제번호: {q005['q_no']}")
print(f"문제내용: {q005['question_text'][:50]}...")
print(f"\n코드 블록:")
if q005['code_blocks']:
    cb = q005['code_blocks'][0]
    print(f"  언어: {cb['language']} ✅")
    print(f"  파일: {cb['file']}")
    print(f"  코드 미리보기:")
    print("  " + "\n  ".join(cb['code'].split('\n')[:5]))
    print("  ...")
else:
    print("  ❌ 코드 없음")



