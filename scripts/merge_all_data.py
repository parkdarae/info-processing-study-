"""
모든 파싱 데이터를 기존 JSONL 파일에 병합

코드 블록, 이미지, 표 데이터를 기존 items_*.jsonl 파일에 통합합니다.
- data/parsed_codes/*.json 읽기
- data/parsed_images/*.json 읽기
- data/parsed_tables/*.json 읽기
- data/items_*.jsonl 업데이트

Zero Tolerance 정책:
- 실제 데이터만 사용
- 추정/가상 데이터 완전 차단
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

class DataMerger:
    def __init__(self):
        sys.stdout.reconfigure(encoding='utf-8')
        
        self.data_dir = Path("data")
        self.parsed_codes_dir = self.data_dir / "parsed_codes"
        self.parsed_images_dir = self.data_dir / "parsed_images"
        self.parsed_tables_dir = self.data_dir / "parsed_tables"
        
        # 파싱된 데이터 캐시
        self.codes_cache = {}
        self.images_cache = {}
        self.tables_cache = {}
    
    def load_parsed_data(self):
        """파싱된 데이터 로드"""
        print("\n[LOAD] 파싱된 데이터 로드 중...")
        
        # 코드 블록 로드
        if self.parsed_codes_dir.exists():
            for json_file in self.parsed_codes_dir.glob("codes_*.json"):
                doc_id = json_file.stem.replace("codes_", "")
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.codes_cache[doc_id] = {item['q_no']: item for item in data}
                print(f"  - 코드: {doc_id} ({len(data)}개 문제)")
        
        # 이미지 로드
        if self.parsed_images_dir.exists():
            for json_file in self.parsed_images_dir.glob("images_*.json"):
                doc_id = json_file.stem.replace("images_", "")
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.images_cache[doc_id] = {item['q_no']: item for item in data}
                print(f"  - 이미지: {doc_id} ({len(data)}개 문제)")
        
        # 표 로드
        if self.parsed_tables_dir.exists():
            for json_file in self.parsed_tables_dir.glob("tables_*.json"):
                doc_id = json_file.stem.replace("tables_", "")
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tables_cache[doc_id] = {item['q_no']: item for item in data}
                print(f"  - 표: {doc_id} ({len(data)}개 문제)")
        
        print(f"\n[SUMMARY] 로드 완료:")
        print(f"  - 코드 블록: {len(self.codes_cache)}개 회차")
        print(f"  - 이미지: {len(self.images_cache)}개 회차")
        print(f"  - 표: {len(self.tables_cache)}개 회차")
    
    def merge_question(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """단일 문제 데이터 병합"""
        doc_id = question['doc_id']
        q_no = question['q_no']
        
        updated = False
        
        # 코드 블록 병합
        if doc_id in self.codes_cache and q_no in self.codes_cache[doc_id]:
            code_data = self.codes_cache[doc_id][q_no]
            question['code_blocks'] = code_data['code_blocks']
            updated = True
        else:
            # 기존 필드가 없으면 빈 배열로 초기화
            if 'code_blocks' not in question:
                question['code_blocks'] = []
        
        # 이미지 병합
        if doc_id in self.images_cache and q_no in self.images_cache[doc_id]:
            image_data = self.images_cache[doc_id][q_no]
            # image_refs를 경로 문자열 배열로 변환
            question['image_refs'] = [img['path'] for img in image_data['image_refs']]
            updated = True
        else:
            # 기존 필드가 없으면 빈 배열로 초기화
            if 'image_refs' not in question or not question['image_refs']:
                question['image_refs'] = []
        
        # 표 병합
        if doc_id in self.tables_cache and q_no in self.tables_cache[doc_id]:
            table_data = self.tables_cache[doc_id][q_no]
            question['table_refs'] = table_data['table_refs']
            updated = True
        else:
            # 기존 필드가 없으면 빈 배열로 초기화
            if 'table_refs' not in question:
                question['table_refs'] = []
        
        return question, updated
    
    def merge_jsonl_file(self, jsonl_path: Path) -> Dict[str, int]:
        """JSONL 파일 병합"""
        print(f"\n[MERGE] {jsonl_path.name}")
        
        # 기존 데이터 로드
        questions = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        print(f"  - 총 {len(questions)}개 문제")
        
        # 각 문제 병합
        stats = {
            'total': len(questions),
            'updated': 0,
            'codes': 0,
            'images': 0,
            'tables': 0
        }
        
        merged_questions = []
        for question in questions:
            merged_q, updated = self.merge_question(question)
            merged_questions.append(merged_q)
            
            if updated:
                stats['updated'] += 1
            
            # 통계
            if merged_q.get('code_blocks'):
                stats['codes'] += 1
            if merged_q.get('image_refs'):
                stats['images'] += 1
            if merged_q.get('table_refs'):
                stats['tables'] += 1
        
        # 업데이트된 데이터 저장
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for q in merged_questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"  - 업데이트: {stats['updated']}개 문제")
        print(f"  - 코드 블록: {stats['codes']}개")
        print(f"  - 이미지: {stats['images']}개")
        print(f"  - 표: {stats['tables']}개")
        
        return stats
    
    def merge_all(self):
        """전체 JSONL 파일 병합"""
        print("\n" + "="*60)
        print("[START] 데이터 병합 시작")
        print("="*60)
        
        # 파싱된 데이터 로드
        self.load_parsed_data()
        
        # 모든 items_*.jsonl 파일 찾기
        jsonl_files = sorted(list(self.data_dir.glob("items_*.jsonl")))
        
        if not jsonl_files:
            print("[ERROR] items_*.jsonl 파일을 찾을 수 없습니다.")
            return
        
        print(f"\n[INFO] {len(jsonl_files)}개 JSONL 파일 발견")
        
        # 전체 통계
        total_stats = {
            'files': len(jsonl_files),
            'total': 0,
            'updated': 0,
            'codes': 0,
            'images': 0,
            'tables': 0
        }
        
        # 각 파일 병합
        for jsonl_path in jsonl_files:
            stats = self.merge_jsonl_file(jsonl_path)
            total_stats['total'] += stats['total']
            total_stats['updated'] += stats['updated']
            total_stats['codes'] += stats['codes']
            total_stats['images'] += stats['images']
            total_stats['tables'] += stats['tables']
        
        # 최종 통계
        print("\n" + "="*60)
        print("[COMPLETE] 데이터 병합 완료")
        print("="*60)
        print(f"파일 수: {total_stats['files']}개")
        print(f"총 문제: {total_stats['total']}개")
        print(f"업데이트: {total_stats['updated']}개")
        print(f"\n[추가된 데이터]")
        print(f"  - 코드 블록: {total_stats['codes']}개 문제")
        print(f"  - 이미지: {total_stats['images']}개 문제")
        print(f"  - 표: {total_stats['tables']}개 문제")
        print("="*60)
        
        # 비율 계산
        if total_stats['total'] > 0:
            code_rate = (total_stats['codes'] / total_stats['total']) * 100
            image_rate = (total_stats['images'] / total_stats['total']) * 100
            table_rate = (total_stats['tables'] / total_stats['total']) * 100
            
            print(f"\n[비율]")
            print(f"  - 코드 블록: {code_rate:.1f}%")
            print(f"  - 이미지: {image_rate:.1f}%")
            print(f"  - 표: {table_rate:.1f}%")

def main():
    merger = DataMerger()
    merger.merge_all()

if __name__ == "__main__":
    main()


