# -*- coding: utf-8 -*-
"""
전체 답안 및 해설 종합 검증 및 개선 스크립트
모든 회차의 답안과 해설을 재확인하고 개선사항을 제시합니다.
"""
import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict

class AnswerReviewer:
    def __init__(self):
        self.data_dir = Path("data")
        self.manual_dir = Path("data/manual_input")
        self.issues = defaultdict(list)
        self.stats = {
            'total_files': 0,
            'total_questions': 0,
            'with_answers': 0,
            'with_explanations': 0,
            'empty_answers': 0,
            'empty_explanations': 0,
            'quality_issues': 0,
            'format_issues': 0
        }
    
    def load_jsonl(self, filepath: Path) -> List[Dict[str, Any]]:
        """JSONL 파일 로드"""
        items = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        items.append(json.loads(line))
        except Exception as e:
            print(f"[ERROR] {filepath.name} 로드 실패: {e}")
        return items
    
    def validate_answer_format(self, answer: Dict[str, Any], q_no: str) -> List[str]:
        """답안 형식 검증"""
        issues = []
        
        # keys 필드 확인
        if not answer.get('keys'):
            issues.append("answer.keys가 비어있음")
            return issues
        
        keys = answer['keys']
        if not isinstance(keys, list):
            issues.append(f"answer.keys가 리스트가 아님: {type(keys)}")
            return issues
        
        if len(keys) == 0:
            issues.append("answer.keys가 빈 배열")
            return issues
        
        # raw_text 확인
        raw_text = answer.get('raw_text', '')
        if not raw_text:
            issues.append("answer.raw_text가 비어있음")
        else:
            # raw_text가 keys의 조합과 일치하는지 확인
            expected_raw = '\n'.join(keys)
            if raw_text.strip() != expected_raw.strip():
                # 경고만 (다소 다를 수 있음)
                pass
        
        # 각 답안 품질 체크
        for i, key in enumerate(keys):
            if not key or not key.strip():
                issues.append(f"답안 {i+1}이 비어있음")
            elif len(key.strip()) < 1:
                issues.append(f"답안 {i+1}이 너무 짧음")
            elif len(key.strip()) > 500:
                issues.append(f"답안 {i+1}이 너무 김 ({len(key)}자)")
            
            # 특수 문자나 불필요한 공백 확인
            if key.strip() != key:
                issues.append(f"답안 {i+1}에 앞뒤 공백 있음")
        
        return issues
    
    def validate_explanation(self, explanation: Any, q_no: str, question_text: str = "") -> List[str]:
        """해설 품질 검증"""
        issues = []
        
        if explanation is None:
            issues.append("해설이 null")
            return issues
        
        if not explanation:
            issues.append("해설이 비어있음")
            return issues
        
        explanation_str = str(explanation).strip()
        
        # 길이 체크
        if len(explanation_str) < 20:
            issues.append(f"해설이 너무 짧음 ({len(explanation_str)}자, 권장: 50자 이상)")
        elif len(explanation_str) < 50:
            issues.append(f"해설이 다소 짧음 ({len(explanation_str)}자, 권장: 50자 이상)")
        
        # 구체적인 설명이 있는지 체크
        explanation_words = ['은', '는', '이', '가', '을', '를', '한다', '합니다', '이다', '입니다', 
                          '에서', '의', '따라서', '때문에', '설명', '의미', '기능', '역할']
        has_explanation_words = any(word in explanation_str for word in explanation_words)
        
        if not has_explanation_words:
            issues.append("구체적인 설명 문장이 부족함 (단순 키워드나 약자만 있을 가능성)")
        
        # 단순 키워드만 있는지 체크
        if len(explanation_str.split()) <= 3 and not any(word in explanation_str for word in explanation_words):
            issues.append("단순 키워드나 약자만 있음")
        
        # 반복적인 패턴 확인
        if explanation_str.count('\n') > 10:
            issues.append("해설이 너무 길게 나뉘어져 있음 (형식 정리 필요)")
        
        return issues
    
    def check_answer_consistency(self, q: Dict[str, Any]) -> List[str]:
        """답안 일관성 체크 (question_text와의 연관성)"""
        issues = []
        
        answer_keys = q.get('answer', {}).get('keys', [])
        question_text = q.get('question_text', '')
        choices = q.get('choices', [])
        
        if not answer_keys:
            return issues
        
        # 서술형 문제인 경우 (choices가 없음)
        if not choices or len(choices) == 0:
            # 서술형 답안은 특별 검증 없음 (다양할 수 있음)
            pass
        else:
            # 객관식 문제인 경우 - 답안이 선택지와 일치하는지 확인
            for ans in answer_keys:
                # 답안이 숫자나 기호인 경우 (1, 2, 3, ①, ② 등)
                if ans.strip() in ['1', '2', '3', '4', '①', '②', '③', '④', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ']:
                    # 정상적인 형식
                    pass
                else:
                    # 텍스트 답안인 경우 - 선택지와 비교 필요할 수 있음
                    # 일단 경고만
                    pass
        
        return issues
    
    def validate_question(self, q: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """개별 문제 검증"""
        result = {
            'q_no': q.get('q_no', 'UNKNOWN'),
            'filename': filename,
            'answer_issues': [],
            'explanation_issues': [],
            'consistency_issues': [],
            'has_answer': bool(q.get('answer', {}).get('keys')),
            'has_explanation': bool(q.get('explanation')),
            'confidence': q.get('meta', {}).get('confidence', 0.0),
            'warnings': q.get('meta', {}).get('warnings', [])
        }
        
        # 답안 검증
        answer = q.get('answer', {})
        result['answer_issues'] = self.validate_answer_format(answer, result['q_no'])
        
        # 해설 검증
        explanation = q.get('explanation')
        question_text = q.get('question_text', '')
        result['explanation_issues'] = self.validate_explanation(explanation, result['q_no'], question_text)
        
        # 일관성 체크
        result['consistency_issues'] = self.check_answer_consistency(q)
        
        return result
    
    def review_file(self, filepath: Path) -> Dict[str, Any]:
        """파일 단위 검증"""
        questions = self.load_jsonl(filepath)
        
        if not questions:
            return {
                'filename': filepath.name,
                'total': 0,
                'results': []
            }
        
        results = []
        for q in questions:
            result = self.validate_question(q, filepath.name)
            results.append(result)
        
        return {
            'filename': filepath.name,
            'total': len(questions),
            'results': results
        }
    
    def compare_with_manual_input(self, filepath: Path) -> Dict[str, Any]:
        """수동 입력 CSV와 비교"""
        # 파일명에서 회차 추출
        # items_2021_round1.jsonl -> manual_2021_round1.csv
        match = re.match(r'items_(\d{4})_round(\d+)\.jsonl', filepath.name)
        if not match:
            return {}
        
        year, round_num = match.groups()
        csv_file = self.manual_dir / f"manual_{year}_round{round_num}.csv"
        
        if not csv_file.exists():
            return {'csv_exists': False}
        
        # CSV 읽기
        manual_data = {}
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    q_no = row.get('문제번호', '').strip()
                    if q_no:
                        manual_data[q_no] = {
                            'ans1': row.get('답안1', '').strip(),
                            'ans2': row.get('답안2', '').strip(),
                            'ans3': row.get('답안3', '').strip(),
                            'explanation': row.get('해설', '').strip()
                        }
        except Exception as e:
            return {'csv_error': str(e)}
        
        # JSONL 읽기
        questions = self.load_jsonl(filepath)
        jsonl_data = {q['q_no']: q for q in questions}
        
        # 비교
        comparison = {
            'csv_exists': True,
            'csv_entries': len(manual_data),
            'jsonl_entries': len(jsonl_data),
            'matches': 0,
            'mismatches': [],
            'csv_only': [],
            'jsonl_only': []
        }
        
        all_q_nos = set(manual_data.keys()) | set(jsonl_data.keys())
        
        for q_no in all_q_nos:
            csv_entry = manual_data.get(q_no)
            jsonl_entry = jsonl_data.get(q_no)
            
            if csv_entry and jsonl_entry:
                # 답안 비교
                csv_answers = [csv_entry['ans1'], csv_entry['ans2'], csv_entry['ans3']]
                csv_answers = [a for a in csv_answers if a]
                jsonl_answers = jsonl_entry.get('answer', {}).get('keys', [])
                
                if csv_answers == jsonl_answers:
                    comparison['matches'] += 1
                else:
                    comparison['mismatches'].append({
                        'q_no': q_no,
                        'csv_answers': csv_answers,
                        'jsonl_answers': jsonl_answers,
                        'csv_explanation': csv_entry['explanation'],
                        'jsonl_explanation': jsonl_entry.get('explanation')
                    })
            elif csv_entry:
                comparison['csv_only'].append(q_no)
            elif jsonl_entry:
                comparison['jsonl_only'].append(q_no)
        
        return comparison
    
    def review_all(self):
        """전체 검증 실행"""
        print("=" * 80)
        print("전체 답안 및 해설 종합 검증")
        print("=" * 80)
        print()
        
        # 모든 JSONL 파일 검증
        jsonl_files = sorted(self.data_dir.glob("items_*.jsonl"))
        
        # 백업 파일 제외
        jsonl_files = [f for f in jsonl_files if 'backup' not in f.name and 'improved' not in f.name 
                      and 'detailed' not in f.name and 'specific' not in f.name]
        
        all_reviews = []
        
        for filepath in jsonl_files:
            print(f"[검증 중] {filepath.name}")
            review = self.review_file(filepath)
            comparison = self.compare_with_manual_input(filepath)
            review['comparison'] = comparison
            
            all_reviews.append(review)
            
            # 통계 업데이트
            self.stats['total_files'] += 1
            self.stats['total_questions'] += review['total']
            for result in review['results']:
                if result['has_answer']:
                    self.stats['with_answers'] += 1
                else:
                    self.stats['empty_answers'] += 1
                
                if result['has_explanation']:
                    self.stats['with_explanations'] += 1
                else:
                    self.stats['empty_explanations'] += 1
                
                if result['answer_issues'] or result['explanation_issues']:
                    self.stats['quality_issues'] += 1
        
        # 리포트 생성
        self.generate_report(all_reviews)
        
        return all_reviews
    
    def generate_report(self, reviews: List[Dict[str, Any]]):
        """종합 리포트 생성"""
        print("\n" + "=" * 80)
        print("검증 결과 요약")
        print("=" * 80)
        
        # 전체 통계
        print(f"\n전체 파일: {self.stats['total_files']}개")
        print(f"총 문제 수: {self.stats['total_questions']}개")
        print(f"\n답안 상태:")
        print(f"  ✓ 답안 있음: {self.stats['with_answers']}개 ({self.stats['with_answers']/self.stats['total_questions']*100:.1f}%)")
        print(f"  ✗ 답안 없음: {self.stats['empty_answers']}개 ({self.stats['empty_answers']/self.stats['total_questions']*100:.1f}%)")
        print(f"\n해설 상태:")
        print(f"  ✓ 해설 있음: {self.stats['with_explanations']}개 ({self.stats['with_explanations']/self.stats['total_questions']*100:.1f}%)")
        print(f"  ✗ 해설 없음: {self.stats['empty_explanations']}개 ({self.stats['empty_explanations']/self.stats['total_questions']*100:.1f}%)")
        print(f"\n품질 이슈: {self.stats['quality_issues']}개")
        
        # 파일별 상세
        print("\n" + "-" * 80)
        print("파일별 상세 정보")
        print("-" * 80)
        print(f"{'파일명':<30} {'문제수':>6} {'답안률':>8} {'해설률':>8} {'이슈':>6}")
        print("-" * 80)
        
        for review in reviews:
            filename = review['filename']
            total = review['total']
            
            with_answers = sum(1 for r in review['results'] if r['has_answer'])
            with_explanations = sum(1 for r in review['results'] if r['has_explanation'])
            issues_count = sum(1 for r in review['results'] if r['answer_issues'] or r['explanation_issues'])
            
            answer_rate = (with_answers / total * 100) if total > 0 else 0
            explanation_rate = (with_explanations / total * 100) if total > 0 else 0
            
            print(f"{filename:<30} {total:>6} {answer_rate:>6.1f}% {explanation_rate:>6.1f}% {issues_count:>6}")
        
        # 수동 입력 CSV 비교
        print("\n" + "-" * 80)
        print("수동 입력 CSV 비교")
        print("-" * 80)
        
        for review in reviews:
            comp = review.get('comparison', {})
            if comp.get('csv_exists'):
                matches = comp.get('matches', 0)
                mismatches = len(comp.get('mismatches', []))
                print(f"\n{review['filename']}:")
                print(f"  CSV 항목: {comp['csv_entries']}개")
                print(f"  일치: {matches}개")
                print(f"  불일치: {mismatches}개")
                
                if mismatches > 0:
                    print(f"  ⚠️  불일치 항목:")
                    for mm in comp['mismatches'][:3]:
                        print(f"    - {mm['q_no']}: CSV={mm['csv_answers']}, JSONL={mm['jsonl_answers']}")
            elif not comp.get('csv_error'):
                print(f"{review['filename']}: CSV 파일 없음")
        
        # 주요 이슈 요약
        print("\n" + "-" * 80)
        print("주요 이슈 요약")
        print("-" * 80)
        
        all_issues = defaultdict(int)
        for review in reviews:
            for result in review['results']:
                for issue in result['answer_issues']:
                    all_issues[issue] += 1
                for issue in result['explanation_issues']:
                    all_issues[issue] += 1
        
        for issue, count in sorted(all_issues.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {issue}: {count}회")
        
        # 리포트 파일 저장
        report = {
            'version': '1.0',
            'reviewed_at': datetime.now().isoformat(),
            'stats': self.stats,
            'reviews': reviews
        }
        
        report_path = self.data_dir / 'answer_review_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n[저장] 상세 리포트: {report_path}")
        print("=" * 80)

def main():
    reviewer = AnswerReviewer()
    reviewer.review_all()

if __name__ == "__main__":
    main()


