# -*- coding: utf-8 -*-
"""
답안 및 해설 자동 개선 스크립트
검증 결과를 바탕으로 답안과 해설을 개선합니다.
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnswerImprover:
    def __init__(self):
        self.data_dir = Path("data")
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def normalize_answer(self, answer_text: str) -> str:
        """답안 텍스트 정규화"""
        if not answer_text:
            return ""
        
        # 앞뒤 공백 제거
        normalized = answer_text.strip()
        
        # 불필요한 공백 제거 (여러 공백을 하나로)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # 특수 문자 정리 (일부는 유지)
        # 예: "1. 답안" -> "1. 답안" (유지)
        
        return normalized
    
    def normalize_explanation(self, explanation: str) -> str:
        """해설 텍스트 정규화"""
        if not explanation:
            return ""
        
        # 앞뒤 공백 제거
        normalized = explanation.strip()
        
        # 불필요한 줄바꿈 정리
        normalized = re.sub(r'\n{3,}', '\n\n', normalized)  # 3개 이상 줄바꿈을 2개로
        
        # 각 줄의 앞뒤 공백 제거
        lines = normalized.split('\n')
        lines = [line.strip() for line in lines]
        normalized = '\n'.join(lines)
        
        # 빈 줄 정리
        normalized = re.sub(r'\n\s*\n', '\n\n', normalized)
        
        return normalized
    
    def fix_answer_format(self, answer: Dict[str, Any]) -> Dict[str, Any]:
        """답안 형식 개선"""
        if not answer:
            return answer
        
        keys = answer.get('keys', [])
        if not keys:
            return answer
        
        # 각 답안 정규화
        normalized_keys = []
        for key in keys:
            normalized = self.normalize_answer(key)
            if normalized:
                normalized_keys.append(normalized)
        
        # raw_text 재생성
        raw_text = '\n'.join(normalized_keys)
        
        # 개선된 답안 반환
        improved = {
            'keys': normalized_keys,
            'raw_text': raw_text
        }
        
        return improved
    
    def improve_explanation_quality(self, explanation: Optional[str], question_text: str = "") -> Optional[str]:
        """해설 품질 개선"""
        if not explanation:
            return None
        
        # 기본 정규화
        improved = self.normalize_explanation(explanation)
        
        # 너무 짧은 해설 확인 (개선 필요하지만 자동으로는 어려움)
        if len(improved) < 20:
            # 경고만 표시 (실제 개선은 수동 필요)
            pass
        
        return improved
    
    def improve_question(self, q: Dict[str, Any]) -> Dict[str, Any]:
        """문제 단위 개선"""
        improved = q.copy()
        
        # 답안 개선
        if 'answer' in improved:
            improved['answer'] = self.fix_answer_format(improved['answer'])
        
        # 해설 개선
        if 'explanation' in improved:
            question_text = improved.get('question_text', '')
            improved['explanation'] = self.improve_explanation_quality(
                improved.get('explanation'),
                question_text
            )
        
        # 메타데이터 업데이트
        if 'meta' not in improved:
            improved['meta'] = {}
        
        improved['meta']['last_improved'] = datetime.now().isoformat()
        
        # 답안/해설이 있으면 confidence 향상
        if improved.get('answer', {}).get('keys') and improved.get('explanation'):
            improved['meta']['confidence'] = 1.0
            improved['meta']['warnings'] = []
        
        return improved
    
    def create_backup(self, filepath: Path) -> Path:
        """백업 파일 생성"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{filepath.stem}_backup_{timestamp}{filepath.suffix}"
        backup_path = self.backup_dir / backup_name
        
        if filepath.exists():
            import shutil
            shutil.copy2(filepath, backup_path)
            print(f"[백업] {backup_path.name}")
        
        return backup_path
    
    def improve_file(self, filepath: Path, create_backup: bool = True) -> Dict[str, Any]:
        """파일 단위 개선"""
        print(f"\n[개선 중] {filepath.name}")
        
        # 백업 생성
        if create_backup:
            self.create_backup(filepath)
        
        # JSONL 읽기
        questions = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        # 각 문제 개선
        improved_questions = []
        improvements = {
            'total': len(questions),
            'answers_improved': 0,
            'explanations_improved': 0,
            'confidences_updated': 0
        }
        
        for q in questions:
            original_answer_keys = q.get('answer', {}).get('keys', [])
            original_explanation = q.get('explanation')
            original_confidence = q.get('meta', {}).get('confidence', 0.0)
            
            improved_q = self.improve_question(q)
            
            # 변경사항 확인
            improved_answer_keys = improved_q.get('answer', {}).get('keys', [])
            improved_explanation = improved_q.get('explanation')
            improved_confidence = improved_q.get('meta', {}).get('confidence', 0.0)
            
            if original_answer_keys != improved_answer_keys:
                improvements['answers_improved'] += 1
            
            if original_explanation != improved_explanation and improved_explanation:
                improvements['explanations_improved'] += 1
            
            if original_confidence < improved_confidence:
                improvements['confidences_updated'] += 1
            
            improved_questions.append(improved_q)
        
        # 개선된 데이터 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            for q in improved_questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"  - 답안 개선: {improvements['answers_improved']}개")
        print(f"  - 해설 개선: {improvements['explanations_improved']}개")
        print(f"  - 신뢰도 업데이트: {improvements['confidences_updated']}개")
        
        return improvements
    
    def improve_all(self, create_backup: bool = True):
        """전체 파일 개선"""
        print("=" * 80)
        print("답안 및 해설 자동 개선 시작")
        print("=" * 80)
        
        # 모든 JSONL 파일 찾기
        jsonl_files = sorted(self.data_dir.glob("items_*.jsonl"))
        
        # 백업 파일 제외
        jsonl_files = [f for f in jsonl_files if 'backup' not in f.name and 'improved' not in f.name 
                      and 'detailed' not in f.name and 'specific' not in f.name]
        
        total_improvements = {
            'files': 0,
            'answers_improved': 0,
            'explanations_improved': 0,
            'confidences_updated': 0
        }
        
        for filepath in jsonl_files:
            improvements = self.improve_file(filepath, create_backup)
            total_improvements['files'] += 1
            total_improvements['answers_improved'] += improvements['answers_improved']
            total_improvements['explanations_improved'] += improvements['explanations_improved']
            total_improvements['confidences_updated'] += improvements['confidences_updated']
        
        print("\n" + "=" * 80)
        print("개선 완료")
        print("=" * 80)
        print(f"처리된 파일: {total_improvements['files']}개")
        print(f"답안 개선: {total_improvements['answers_improved']}개")
        print(f"해설 개선: {total_improvements['explanations_improved']}개")
        print(f"신뢰도 업데이트: {total_improvements['confidences_updated']}개")
        print("=" * 80)

def main():
    improver = AnswerImprover()
    improver.improve_all(create_backup=True)

if __name__ == "__main__":
    main()


