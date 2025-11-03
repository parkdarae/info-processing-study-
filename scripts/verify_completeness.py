"""
데이터 완성도 검증 스크립트

병합 후 모든 데이터가 올바르게 추가되었는지 확인합니다.
- 코드 블록이 있어야 할 문제 확인
- 이미지가 있어야 할 문제 확인
- 표가 있어야 할 문제 확인
- 파일 존재 여부 확인

Zero Tolerance 정책:
- 실제 데이터만 사용
- 추정/가상 데이터 완전 차단
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

class DataVerifier:
    def __init__(self):
        sys.stdout.reconfigure(encoding='utf-8')
        self.data_dir = Path("data")
    
    def check_code_keywords(self, question_text: str) -> bool:
        """코드가 있어야 할 문제인지 키워드로 확인"""
        keywords = [
            '코드', 'code', 'java', 'c언어', 'python', 'javascript',
            'class', 'public', 'void', 'int main', '#include',
            '출력값', '출력 값', '출력되는 값', '실행 결과'
        ]
        text_lower = question_text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def check_image_keywords(self, question_text: str) -> bool:
        """이미지가 있어야 할 문제인지 키워드로 확인"""
        keywords = [
            '그림', '도표', '다이어그램', '아래 그림', '다음 그림',
            '다음 도표', '아래 도표', '네트워크 구성도', 'erd',
            '아래의', '다음의'
        ]
        text_lower = question_text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def check_table_keywords(self, question_text: str) -> bool:
        """표가 있어야 할 문제인지 키워드로 확인"""
        keywords = [
            '표', 'table', '테이블', '다음 표', '아래 표',
            '릴레이션', 'relation', '아래 테이블'
        ]
        text_lower = question_text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def verify_file_exists(self, filepath: str) -> bool:
        """파일 존재 여부 확인"""
        path = Path(filepath)
        return path.exists()
    
    def verify_jsonl_file(self, jsonl_path: Path) -> Dict[str, Any]:
        """JSONL 파일 검증"""
        print(f"\n{'='*60}")
        print(f"[검증] {jsonl_path.name}")
        print(f"{'='*60}")
        
        # 데이터 로드
        questions = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        stats = {
            'total': len(questions),
            'with_codes': 0,
            'with_images': 0,
            'with_tables': 0,
            'should_have_codes': 0,
            'should_have_images': 0,
            'should_have_tables': 0,
            'missing_codes': [],
            'missing_images': [],
            'missing_tables': [],
            'invalid_files': []
        }
        
        for q in questions:
            q_no = q['q_no']
            question_text = q['question_text']
            
            # 현재 상태
            has_codes = bool(q.get('code_blocks'))
            has_images = bool(q.get('image_refs'))
            has_tables = bool(q.get('table_refs'))
            
            if has_codes:
                stats['with_codes'] += 1
            if has_images:
                stats['with_images'] += 1
            if has_tables:
                stats['with_tables'] += 1
            
            # 예상 여부
            should_have_code = self.check_code_keywords(question_text)
            should_have_image = self.check_image_keywords(question_text)
            should_have_table = self.check_table_keywords(question_text)
            
            if should_have_code:
                stats['should_have_codes'] += 1
                if not has_codes:
                    stats['missing_codes'].append({
                        'q_no': q_no,
                        'text': question_text[:80] + '...'
                    })
            
            if should_have_image:
                stats['should_have_images'] += 1
                if not has_images:
                    stats['missing_images'].append({
                        'q_no': q_no,
                        'text': question_text[:80] + '...'
                    })
            
            if should_have_table:
                stats['should_have_tables'] += 1
                if not has_tables:
                    stats['missing_tables'].append({
                        'q_no': q_no,
                        'text': question_text[:80] + '...'
                    })
            
            # 파일 존재 여부 확인
            for img_path in q.get('image_refs', []):
                if not self.verify_file_exists(img_path):
                    stats['invalid_files'].append({
                        'q_no': q_no,
                        'type': 'image',
                        'path': img_path
                    })
            
            for table_ref in q.get('table_refs', []):
                if isinstance(table_ref, dict):
                    json_path = table_ref.get('json', '')
                    if json_path and not self.verify_file_exists(json_path):
                        stats['invalid_files'].append({
                            'q_no': q_no,
                            'type': 'table_json',
                            'path': json_path
                        })
        
        # 결과 출력
        print(f"\n총 문제 수: {stats['total']}개")
        print(f"\n[현재 상태]")
        print(f"  코드 블록: {stats['with_codes']}개 ({stats['with_codes']/stats['total']*100:.1f}%)")
        print(f"  이미지: {stats['with_images']}개 ({stats['with_images']/stats['total']*100:.1f}%)")
        print(f"  표: {stats['with_tables']}개 ({stats['with_tables']/stats['total']*100:.1f}%)")
        
        print(f"\n[예상 필요]")
        print(f"  코드 블록: {stats['should_have_codes']}개")
        print(f"  이미지: {stats['should_have_images']}개")
        print(f"  표: {stats['should_have_tables']}개")
        
        # 누락 항목 출력
        if stats['missing_codes']:
            print(f"\n⚠ 코드 블록 누락 가능성: {len(stats['missing_codes'])}개")
            for item in stats['missing_codes'][:5]:  # 최대 5개만 표시
                print(f"  - {item['q_no']}: {item['text']}")
            if len(stats['missing_codes']) > 5:
                print(f"  ... 외 {len(stats['missing_codes'])-5}개")
        
        if stats['missing_images']:
            print(f"\n⚠ 이미지 누락 가능성: {len(stats['missing_images'])}개")
            for item in stats['missing_images'][:5]:
                print(f"  - {item['q_no']}: {item['text']}")
            if len(stats['missing_images']) > 5:
                print(f"  ... 외 {len(stats['missing_images'])-5}개")
        
        if stats['missing_tables']:
            print(f"\n⚠ 표 누락 가능성: {len(stats['missing_tables'])}개")
            for item in stats['missing_tables'][:5]:
                print(f"  - {item['q_no']}: {item['text']}")
            if len(stats['missing_tables']) > 5:
                print(f"  ... 외 {len(stats['missing_tables'])-5}개")
        
        if stats['invalid_files']:
            print(f"\n❌ 파일 없음: {len(stats['invalid_files'])}개")
            for item in stats['invalid_files'][:5]:
                print(f"  - {item['q_no']} ({item['type']}): {item['path']}")
            if len(stats['invalid_files']) > 5:
                print(f"  ... 외 {len(stats['invalid_files'])-5}개")
        
        # 완성도 평가
        if not stats['missing_codes'] and not stats['missing_images'] and not stats['missing_tables'] and not stats['invalid_files']:
            print(f"\n✅ 완벽! 모든 데이터가 정상입니다.")
        elif len(stats['missing_codes']) + len(stats['missing_images']) + len(stats['missing_tables']) < 5:
            print(f"\n✓ 양호! 대부분의 데이터가 정상입니다.")
        else:
            print(f"\n⚠ 주의! 일부 데이터가 누락되었을 수 있습니다.")
        
        return stats
    
    def verify_all(self):
        """전체 JSONL 파일 검증"""
        print("\n" + "="*60)
        print("[START] 데이터 완성도 검증")
        print("="*60)
        
        # 모든 items_*.jsonl 파일 찾기
        jsonl_files = sorted(list(self.data_dir.glob("items_*.jsonl")))
        
        if not jsonl_files:
            print("[ERROR] items_*.jsonl 파일을 찾을 수 없습니다.")
            return
        
        print(f"\n{len(jsonl_files)}개 파일 검증 중...")
        
        # 전체 통계
        total_stats = {
            'total': 0,
            'with_codes': 0,
            'with_images': 0,
            'with_tables': 0,
            'should_have_codes': 0,
            'should_have_images': 0,
            'should_have_tables': 0,
            'missing_codes_count': 0,
            'missing_images_count': 0,
            'missing_tables_count': 0,
            'invalid_files_count': 0
        }
        
        # 각 파일 검증
        for jsonl_path in jsonl_files:
            stats = self.verify_jsonl_file(jsonl_path)
            total_stats['total'] += stats['total']
            total_stats['with_codes'] += stats['with_codes']
            total_stats['with_images'] += stats['with_images']
            total_stats['with_tables'] += stats['with_tables']
            total_stats['should_have_codes'] += stats['should_have_codes']
            total_stats['should_have_images'] += stats['should_have_images']
            total_stats['should_have_tables'] += stats['should_have_tables']
            total_stats['missing_codes_count'] += len(stats['missing_codes'])
            total_stats['missing_images_count'] += len(stats['missing_images'])
            total_stats['missing_tables_count'] += len(stats['missing_tables'])
            total_stats['invalid_files_count'] += len(stats['invalid_files'])
        
        # 최종 통계
        print("\n" + "="*60)
        print("[전체 통계]")
        print("="*60)
        print(f"총 문제 수: {total_stats['total']}개")
        print(f"\n[현재 상태]")
        print(f"  코드 블록: {total_stats['with_codes']}개 ({total_stats['with_codes']/total_stats['total']*100:.1f}%)")
        print(f"  이미지: {total_stats['with_images']}개 ({total_stats['with_images']/total_stats['total']*100:.1f}%)")
        print(f"  표: {total_stats['with_tables']}개 ({total_stats['with_tables']/total_stats['total']*100:.1f}%)")
        
        print(f"\n[예상 필요]")
        print(f"  코드 블록: {total_stats['should_have_codes']}개")
        print(f"  이미지: {total_stats['should_have_images']}개")
        print(f"  표: {total_stats['should_have_tables']}개")
        
        print(f"\n[누락/오류]")
        print(f"  코드 블록 누락 가능: {total_stats['missing_codes_count']}개")
        print(f"  이미지 누락 가능: {total_stats['missing_images_count']}개")
        print(f"  표 누락 가능: {total_stats['missing_tables_count']}개")
        print(f"  파일 없음: {total_stats['invalid_files_count']}개")
        
        # 전체 완성도 평가
        total_issues = (total_stats['missing_codes_count'] + 
                       total_stats['missing_images_count'] + 
                       total_stats['missing_tables_count'] + 
                       total_stats['invalid_files_count'])
        
        print(f"\n{'='*60}")
        if total_issues == 0:
            print("✅ 검증 완료! 모든 데이터가 정상입니다.")
        elif total_issues < 10:
            print("✓ 검증 완료! 대부분의 데이터가 정상입니다.")
        else:
            print("⚠ 검증 완료! 일부 데이터 확인이 필요합니다.")
        print("="*60)

def main():
    verifier = DataVerifier()
    verifier.verify_all()

if __name__ == "__main__":
    main()


