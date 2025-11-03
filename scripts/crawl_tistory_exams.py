"""
Tistory 정보처리기사 실기 기출문제 크롤링 스크립트
9개 회차의 기출문제를 크롤링하여 JSONL 형식으로 변환합니다.

Zero Tolerance 정책:
- 실제 데이터만 사용
- 추정/가상 데이터 완전 차단
- 모든 데이터 소스 추적 가능
"""
import requests
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
from datetime import datetime

# 크롤링 대상 URL 목록
EXAM_URLS = [
    {"year": 2025, "round": 1, "url": "https://chobopark.tistory.com/540"},
    {"year": 2025, "round": 2, "url": "https://chobopark.tistory.com/554"},
    {"year": 2024, "round": 3, "url": "https://chobopark.tistory.com/495"},
    {"year": 2024, "round": 2, "url": "https://chobopark.tistory.com/483"},
    {"year": 2024, "round": 1, "url": "https://chobopark.tistory.com/476"},
    {"year": 2023, "round": 2, "url": "https://chobopark.tistory.com/420"},
    {"year": 2022, "round": 3, "url": "https://chobopark.tistory.com/424"},
    {"year": 2022, "round": 2, "url": "https://chobopark.tistory.com/423"},
    {"year": 2021, "round": 1, "url": "https://chobopark.tistory.com/191"},
]

class TistoryCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 출력 디렉토리 생성
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.images_dir = Path("images_past_exams")
        self.images_dir.mkdir(exist_ok=True)
        
    def fetch_page(self, url: str) -> Optional[str]:
        """페이지 HTML 가져오기"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"[ERROR] 페이지 로드 실패 ({url}): {e}")
            return None
    
    def normalize_choice_key(self, raw_key: str) -> str:
        """선택지 키를 정규화 (①②③④ -> 1234)"""
        mapping = {
            '①': '1', '②': '2', '③': '3', '④': '4',
            '1': '1', '2': '2', '3': '3', '4': '4',
            'ㄱ': '1', 'ㄴ': '2', 'ㄷ': '3', 'ㄹ': '4',
            'a': '1', 'b': '2', 'c': '3', 'd': '4',
            'A': '1', 'B': '2', 'C': '3', 'D': '4',
        }
        return mapping.get(raw_key.strip(), raw_key)
    
    def extract_questions(self, html: str, year: int, round_num: int, url: str) -> List[Dict[str, Any]]:
        """HTML에서 문제 추출"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 본문 추출 (Tistory 구조에 따라)
        content_area = soup.find('div', class_='entry-content') or \
                      soup.find('div', class_='article') or \
                      soup.find('div', class_='tt_article_useless_p_margin') or \
                      soup.find('div', {'itemprop': 'articleBody'})
        
        if not content_area:
            print(f"[WARNING] 본문 영역을 찾을 수 없습니다: {url}")
            return []
        
        # "더보기" 접기 영역도 모두 펼치기
        for details in content_area.find_all('details'):
            details.attrs.pop('style', None)
        
        # 전체 텍스트 추출 (separator를 사용하여 구조 보존)
        text = content_area.get_text('\n', strip=True)
        
        # 문제 단위로 분리
        # 패턴: 숫자. 로 시작하는 문제
        question_pattern = r'(?m)^(\d+)\.\s+'
        splits = re.split(question_pattern, text)
        
        questions = []
        doc_id = f"{year}_round{round_num}"
        
        # splits: ['', '1', '문제내용1', '2', '문제내용2', ...]
        for i in range(1, len(splits), 2):
            if i + 1 >= len(splits):
                break
                
            q_num = splits[i].strip()
            q_content = splits[i + 1].strip()
            
            if len(q_content) < 10:  # 너무 짧은 내용은 스킵
                continue
            
            # 문제 파싱
            question_data = self.parse_question(q_num, q_content, doc_id, url)
            if question_data:
                questions.append(question_data)
        
        return questions
    
    def parse_question(self, q_num: str, content: str, doc_id: str, url: str) -> Optional[Dict[str, Any]]:
        """개별 문제 파싱"""
        
        # 선택지 추출 (①②③④ 또는 1) 2) 3) 4))
        choice_pattern = r'(?m)^([①②③④]|[1-4]\))\s*(.+?)(?=^[①②③④]|^[1-4]\)|정답|해설|풀이|$)'
        choices_matches = re.findall(r'(?m)^([①②③④])\s*(.+)', content)
        
        choices = []
        for raw_key, choice_text in choices_matches:
            key = self.normalize_choice_key(raw_key)
            choices.append({
                "key": key,
                "raw_key": raw_key,
                "text": choice_text.strip()
            })
        
        # 정답 추출 (여러 패턴 시도)
        answer_patterns = [
            r'(?i)더보기\s*\n+\s*([^\n]+)',  # 더보기 다음 줄
            r'(?i)(정답|답)\s*[:：]?\s*([^\n]+)',  # 정답: 패턴
            r'(?i)답안\s*[:：]?\s*([^\n]+)',  # 답안: 패턴
        ]
        
        answer_keys = []
        raw_answer_text = ""
        
        for pattern in answer_patterns:
            answer_match = re.search(pattern, content)
            if answer_match:
                if '더보기' in pattern:
                    raw_answer_text = answer_match.group(1).strip()
                    answer_str = answer_match.group(1).strip()
                else:
                    raw_answer_text = answer_match.group(0).strip()
                    answer_str = answer_match.group(2).strip()
                
                # 복수 정답 처리
                for char in answer_str:
                    if char in '①②③④1234ㄱㄴㄷㄹabcdABCD':
                        normalized = self.normalize_choice_key(char)
                        if normalized and normalized not in answer_keys:
                            answer_keys.append(normalized)
                
                # 정답을 찾았으면 루프 종료
                if answer_keys or len(answer_str) > 0:
                    # 서술형 답안 처리
                    if not answer_keys and len(answer_str.strip()) > 0:
                        answer_keys = [answer_str.strip()]
                    break
        
        # 문제 본문 추출 (선택지, 정답, 더보기 제거)
        question_text = content
        
        # "더보기" 이전까지만 추출
        more_pos = content.find('더보기')
        if more_pos > 0:
            question_text = content[:more_pos].strip()
        
        # 선택지 이전까지만 추출
        if choices_matches:
            first_choice_pos = content.find(choices_matches[0][0])
            if first_choice_pos > 0:
                question_text = content[:first_choice_pos].strip()
        
        # 해설 추출
        explanation = None
        explanation_pattern = r'(?i)(해설|풀이|설명)\s*[:：]?\s*(.+?)(?=\n\d+\.|$)'
        explanation_match = re.search(explanation_pattern, content, re.DOTALL)
        
        if explanation_match:
            explanation = explanation_match.group(2).strip()
            # 문제 본문에서 해설 제거
            explanation_pos = content.find(explanation_match.group(0))
            if explanation_pos > 0:
                question_text = content[:explanation_pos].strip()
                if choices_matches:
                    first_choice_pos = question_text.find(choices_matches[0][0])
                    if first_choice_pos > 0:
                        question_text = question_text[:first_choice_pos].strip()
        
        # 빈 정답 키 처리: 선택지가 없으면 서술형 문제
        if not answer_keys and answer_match:
            # 서술형 답안은 원문 그대로
            answer_keys = [answer_match.group(2).strip()]
        
        # 데이터 구조 생성
        question_data = {
            "doc_id": doc_id,
            "page_range": [1, 1],
            "q_no": f"Q{int(q_num):03d}",
            "question_text": question_text,
            "choices": choices,
            "answer": {
                "keys": answer_keys if answer_keys else [],
                "raw_text": raw_answer_text if raw_answer_text else ""
            },
            "explanation": explanation,
            "table_refs": [],
            "image_refs": [],
            "meta": {
                "layout": "single",
                "anchors": [f"{q_num}."],
                "page_anchors": [1],
                "confidence": 0.9 if answer_keys else 0.7,
                "warnings": [] if answer_keys else ["정답을 찾을 수 없음"],
                "source_url": url,
                "crawled_at": datetime.now().isoformat()
            }
        }
        
        return question_data
    
    def save_jsonl(self, questions: List[Dict[str, Any]], filename: str):
        """JSONL 형식으로 저장"""
        filepath = self.data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"[SAVE] 저장 완료: {filepath} ({len(questions)}개 문제)")
    
    def save_report(self, exam_info: Dict[str, Any], questions: List[Dict[str, Any]], filename: str):
        """검증 리포트 저장"""
        filepath = self.data_dir / filename
        
        # 통계 계산
        total = len(questions)
        with_choices = sum(1 for q in questions if q['choices'])
        with_answers = sum(1 for q in questions if q['answer']['keys'])
        with_explanations = sum(1 for q in questions if q['explanation'])
        warnings = sum(len(q['meta']['warnings']) for q in questions)
        
        report = {
            "version": "1.0",
            "exam_info": exam_info,
            "total_questions": total,
            "questions_with_choices": with_choices,
            "questions_with_answers": with_answers,
            "questions_with_explanations": with_explanations,
            "total_warnings": warnings,
            "crawled_at": datetime.now().isoformat(),
            "success_rate": f"{(with_answers / total * 100):.1f}%" if total > 0 else "0%"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"[REPORT] {report['success_rate']} 성공률 (정답 추출: {with_answers}/{total})")
    
    def crawl_exam(self, exam_info: Dict[str, Any]) -> bool:
        """단일 회차 크롤링"""
        year = exam_info['year']
        round_num = exam_info['round']
        url = exam_info['url']
        
        print(f"\n{'='*60}")
        print(f"[START] 크롤링 시작: {year}년 {round_num}회")
        print(f"[URL] {url}")
        print(f"{'='*60}")
        
        # HTML 가져오기
        html = self.fetch_page(url)
        if not html:
            return False
        
        # 문제 추출
        questions = self.extract_questions(html, year, round_num, url)
        
        if not questions:
            print(f"[WARNING] 문제를 추출하지 못했습니다.")
            return False
        
        print(f"[SUCCESS] {len(questions)}개 문제 추출 완료")
        
        # JSONL 저장
        filename = f"items_{year}_round{round_num}.jsonl"
        self.save_jsonl(questions, filename)
        
        # 리포트 저장
        report_filename = f"report_{year}_round{round_num}.json"
        self.save_report(exam_info, questions, report_filename)
        
        return True
    
    def crawl_all(self):
        """전체 회차 크롤링"""
        print("\n" + "="*60)
        print("[START] Tistory 기출문제 크롤링 시작")
        print("="*60)
        
        success_count = 0
        total_count = len(EXAM_URLS)
        
        for exam_info in EXAM_URLS:
            success = self.crawl_exam(exam_info)
            if success:
                success_count += 1
            
            # 서버 부하 방지를 위한 딜레이
            time.sleep(2)
        
        print("\n" + "="*60)
        print(f"[COMPLETE] 크롤링 완료: {success_count}/{total_count} 회차 성공")
        print(f"[FOLDER] 출력 폴더: {self.data_dir.absolute()}")
        print("="*60)

def main():
    crawler = TistoryCrawler()
    crawler.crawl_all()

if __name__ == "__main__":
    main()

