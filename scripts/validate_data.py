"""
크롤링된 데이터 검증 스크립트
모든 JSONL 파일의 품질을 검증하고 종합 리포트를 생성합니다.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class DataValidator:
    def __init__(self):
        self.data_dir = Path("data")
        self.results = []
        
    def load_jsonl(self, filepath: Path) -> List[Dict[str, Any]]:
        """JSONL 파일 로드"""
        items = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                items.append(json.loads(line))
        return items
    
    def validate_file(self, filepath: Path) -> Dict[str, Any]:
        """개별 파일 검증"""
        items = self.load_jsonl(filepath)
        
        # 통계 계산
        total = len(items)
        with_answers = sum(1 for item in items if item['answer']['keys'])
        with_explanation = sum(1 for item in items if item['explanation'])
        with_choices = sum(1 for item in items if item['choices'])
        
        # 경고 수집
        all_warnings = []
        for item in items:
            if item['meta'].get('warnings'):
                all_warnings.extend(item['meta']['warnings'])
        
        # 문제 번호 중복 확인
        q_nos = [item['q_no'] for item in items]
        duplicates = len(q_nos) - len(set(q_nos))
        
        # 평균 confidence
        avg_confidence = sum(item['meta']['confidence'] for item in items) / total if total > 0 else 0
        
        result = {
            "filename": filepath.name,
            "total_questions": total,
            "with_answers": with_answers,
            "with_explanation": with_explanation,
            "with_choices": with_choices,
            "success_rate": f"{(with_answers / total * 100):.1f}%" if total > 0 else "0%",
            "avg_confidence": f"{avg_confidence:.2f}",
            "duplicates": duplicates,
            "warnings": len(all_warnings),
            "status": "OK" if with_answers >= total * 0.5 else "NEEDS_REVIEW"
        }
        
        return result
    
    def validate_all(self):
        """모든 파일 검증"""
        print("\n" + "="*60)
        print("[VALIDATION] 데이터 검증 시작")
        print("="*60)
        
        # JSONL 파일 목록
        jsonl_files = sorted(self.data_dir.glob("items_*.jsonl"))
        
        for filepath in jsonl_files:
            print(f"\n[CHECK] {filepath.name}")
            result = self.validate_file(filepath)
            self.results.append(result)
            
            # 결과 출력
            print(f"  - 문제 수: {result['total_questions']}")
            print(f"  - 정답 추출률: {result['success_rate']}")
            print(f"  - 평균 신뢰도: {result['avg_confidence']}")
            print(f"  - 상태: {result['status']}")
        
        # 종합 통계
        self.print_summary()
        
        # 종합 리포트 저장
        self.save_summary_report()
    
    def print_summary(self):
        """종합 통계 출력"""
        print("\n" + "="*60)
        print("[SUMMARY] 종합 통계")
        print("="*60)
        
        total_questions = sum(r['total_questions'] for r in self.results)
        total_with_answers = sum(r['with_answers'] for r in self.results)
        total_with_explanation = sum(r['with_explanation'] for r in self.results)
        
        print(f"\n전체 회차: {len(self.results)}개")
        print(f"총 문제 수: {total_questions}개")
        print(f"정답 추출: {total_with_answers}개 ({(total_with_answers/total_questions*100):.1f}%)")
        print(f"해설 포함: {total_with_explanation}개 ({(total_with_explanation/total_questions*100):.1f}%)")
        
        # 상태별 분류
        ok_count = sum(1 for r in self.results if r['status'] == 'OK')
        review_count = len(self.results) - ok_count
        
        print(f"\n상태:")
        print(f"  - OK: {ok_count}개")
        print(f"  - 검토 필요: {review_count}개")
        
        # 회차별 상세 테이블
        print("\n" + "-"*60)
        print(f"{'파일명':<30} {'문제수':>8} {'정답률':>10} {'상태':>10}")
        print("-"*60)
        for r in self.results:
            print(f"{r['filename']:<30} {r['total_questions']:>8} {r['success_rate']:>10} {r['status']:>10}")
        print("-"*60)
    
    def save_summary_report(self):
        """종합 리포트 저장"""
        total_questions = sum(r['total_questions'] for r in self.results)
        total_with_answers = sum(r['with_answers'] for r in self.results)
        total_with_explanation = sum(r['with_explanation'] for r in self.results)
        
        summary = {
            "version": "1.0",
            "validated_at": datetime.now().isoformat(),
            "total_files": len(self.results),
            "total_questions": total_questions,
            "total_with_answers": total_with_answers,
            "total_with_explanation": total_with_explanation,
            "overall_success_rate": f"{(total_with_answers/total_questions*100):.1f}%" if total_questions > 0 else "0%",
            "files": self.results
        }
        
        filepath = self.data_dir / "validation_summary.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n[SAVE] 종합 리포트 저장: {filepath}")
        print("="*60)

def main():
    validator = DataValidator()
    validator.validate_all()

if __name__ == "__main__":
    main()



