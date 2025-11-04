# -*- coding: utf-8 -*-
"""
해설의 마크다운 형식을 HTML 친화적인 형식으로 개선
"""
import json
from pathlib import Path
import re
import sys
import io

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def improve_explanation_formatting(explanation: str) -> str:
    """
    해설의 마크다운 형식을 개선합니다.
    **제목:** 형식을 [제목] 형식으로 변경
    과도한 **강조** 제거
    """
    if not explanation:
        return explanation
    
    # 1. **섹션 제목:** 형식을 [섹션 제목] 형식으로 변경
    # 예: **TCP 세션 하이재킹:** → [TCP 세션 하이재킹]
    explanation = re.sub(r'\*\*([^*]+):\*\*', r'[\1]', explanation)
    
    # 2. **숫자. **제목**: 형식을 처리
    # 예: **1. **기본 정의**: → • 기본 정의:
    explanation = re.sub(r'\*\*\d+\.\s*\*\*([^*]+)\*\*:', r'• \1:', explanation)
    
    # 3. 남은 **제목**: 형식 (콜론 포함)
    # 예: **기본 정의**: → • 기본 정의:
    explanation = re.sub(r'\*\*([^*]+):\*\*', r'• \1:', explanation)
    
    # 4. 줄 시작 부분의 **제목** (콜론 없음)
    # 예: \n**TCP 세션 하이재킹** → \n[TCP 세션 하이재킹]
    explanation = re.sub(r'\n\*\*([^*]+)\*\*\n', r'\n[\1]\n', explanation)
    
    # 5. 남은 **강조** 형식은 유지 (중요한 키워드)
    # 하지만 너무 길거나 문장 전체를 강조하는 것은 제거
    # 예: **이 문제는 ... 문제입니다.** → 이 문제는 ... 문제입니다.
    def reduce_long_bold(match):
        text = match.group(1)
        # 20자 이상이거나 마침표가 포함된 경우 강조 제거
        if len(text) > 20 or '.' in text or '입니다' in text:
            return text
        return f'**{text}**'
    
    explanation = re.sub(r'\*\*([^*]+)\*\*', reduce_long_bold, explanation)
    
    # 6. 다중 공백 정리
    explanation = re.sub(r'\n\n\n+', '\n\n', explanation)
    
    return explanation

def process_file(filepath: Path):
    """JSONL 파일을 읽고 해설 형식을 개선하여 저장합니다."""
    print(f"\n처리 중: {filepath.name}")
    
    # 백업 생성
    backup_path = filepath.with_suffix('.jsonl.formatting_bak')
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    # 파일 읽기
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    questions.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"  경고: {line_num}번째 라인 JSON 오류: {e}")
                    continue
    
    # 해설 형식 개선
    improved_count = 0
    for item in questions:
        if 'explanation' in item and item['explanation']:
            original = item['explanation']
            improved = improve_explanation_formatting(original)
            if improved != original:
                item['explanation'] = improved
                improved_count += 1
    
    # 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in questions:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"  ✓ {improved_count}/{len(questions)}개 해설 형식 개선 완료")

def main():
    data_dir = Path(__file__).parent.parent / "data"
    jsonl_files = sorted(list(data_dir.glob('items_*.jsonl')))
    
    print("=" * 80)
    print("해설 가독성 개선: 마크다운 형식 → HTML 친화적 형식")
    print("=" * 80)
    
    for jsonl_file in jsonl_files:
        if jsonl_file.name == 'items_all.jsonl':
            continue  # items_all.jsonl은 나중에 업데이트
        process_file(jsonl_file)
    
    print("\n" + "=" * 80)
    print("✓ 모든 파일 가독성 개선 완료!")
    print("=" * 80)

if __name__ == "__main__":
    main()

