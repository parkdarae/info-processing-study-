import json
import re

# JSONL 파일 읽기
items = []
with open('data/items_pmp.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        items.append(json.loads(line))

print(f'총 문제 수: {len(items)}개\n')

# 선택지 개수가 적은 문제 찾기
missing_options = []
for item in items:
    q_no = item['q_no']
    options_count = len(item['options'])
    explanation = item.get('explanation', '')
    
    # explanation에서 언급된 선택지 찾기
    mentioned_options = set(re.findall(r'\b([A-F])\s*[,:는]', explanation))
    
    # options에서 실제 선택지 추출
    actual_options = set()
    for opt in item['options']:
        match = re.match(r'^([A-F])\.', opt)
        if match:
            actual_options.add(match.group(1))
    
    # 누락된 선택지 확인
    missing = mentioned_options - actual_options
    
    if missing or options_count < 4:
        missing_options.append({
            'q_no': q_no,
            'actual_count': options_count,
            'actual_options': sorted(actual_options),
            'mentioned_options': sorted(mentioned_options),
            'missing': sorted(missing),
            'explanation_preview': explanation[:200] if explanation else 'No explanation'
        })

print(f'선택지 누락 의심 문제: {len(missing_options)}개\n')

# 결과를 파일로 저장
with open('data/pmp_missing_options_report.txt', 'w', encoding='utf-8') as f:
    f.write(f'총 문제 수: {len(items)}개\n')
    f.write(f'선택지 누락 의심 문제: {len(missing_options)}개\n\n')
    f.write('=' * 80 + '\n')
    
    for item in missing_options:
        f.write(f"\nQ{item['q_no']}:\n")
        f.write(f"  실제 선택지: {item['actual_options']} ({item['actual_count']}개)\n")
        f.write(f"  언급된 선택지: {item['mentioned_options']}\n")
        if item['missing']:
            f.write(f"  [누락] {item['missing']}\n")
        f.write(f"  설명: {item['explanation_preview']}...\n")

print(f'결과가 data/pmp_missing_options_report.txt 파일에 저장되었습니다.')

# 누락이 명확한 케이스만 출력
critical_missing = [item for item in missing_options if item['missing']]
print(f'\n명확하게 누락된 선택지가 있는 문제: {len(critical_missing)}개')
for item in critical_missing[:10]:
    print(f"  Q{item['q_no']}: 누락 {item['missing']}")

