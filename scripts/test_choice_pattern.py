"""
선택지 패턴 테스트
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re

# 실제 PDF에서 추출한 텍스트 샘플
sample_text = """프로젝트 관리자가 동일 사소에 근무하는 자자의 프로젝트 팀과 함께 하고 있다. 이 팀은
개발과 실행(Performing) 단계에 있을 만큼 오랫동안 함께 일해왔다. 최근에 몇몇한 사건으로 인해
팀이 분산되어 더 이상 동일 사소 근무가 불가능하게 되었고 가상 가능한 최선의 결과로서 성과를
유지하도록 하기 위해 프로젝트 관리자는 무엇을 해야 하는가?
A. 프로젝트 팀원과 경영진 이해관계자에게 최선의 성과를 유지하도록 격려해달고 요청한다.
B. 팀의 최선 성과 중심 관리를 위해 대면 자자의 작업법에서 가상의 작업법으로 전환한다.
C. 일상을 최소화하기 위해 팀에게 가상 작업 플랫폼과 그에 대한 교육을 제공한다.
D. 프로젝트 성과를 평가하고, 성과가 사용 불가능한 사소으로 감소하면 개입한다.
정답: C"""

print("테스트 텍스트:")
print("=" * 80)
print(sample_text)
print("=" * 80)

# 다양한 선택지 패턴 테스트
patterns = [
    (r'([A-E])\.\s+([^\n]+)', 'A. B. C. (점 + 공백)'),
    (r'([A-E])\.\s*([^\n]+)', 'A. B. C. (점 + 공백 선택)'),
    (r'([A-E])\.\s+(.+?)(?=\s*[A-E]\.\s+|\s*정답:|\s*No\.\s*\d+|$)', 'A. B. C. (lookahead)'),
    (r'([A-E])\.\s+([^A-E\n]+?)(?=[A-E]\.|정답:|$)', 'A. B. C. (negative lookahead)'),
]

for pattern, desc in patterns:
    print(f"\n패턴: {desc}")
    print(f"정규식: {pattern}")
    matches = re.findall(pattern, sample_text, re.DOTALL)
    print(f"발견: {len(matches)}개")
    for i, match in enumerate(matches, 1):
        print(f"  {i}. {match[0]}: {match[1][:60]}...")

