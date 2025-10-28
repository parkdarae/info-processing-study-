"""
PDF 문제은행 추출 프로그램 v1.0
keyword130.pdf에서 문제, 선택지, 정답, 해설, 표를 추출합니다.
"""
import os
import json
import hashlib
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import pdfplumber
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") or os.getenv("CURSOR_API_KEY")
)

# 스키마 정의
class Choice(BaseModel):
    key: str
    raw_key: str
    text: str

class Answer(BaseModel):
    keys: List[str]
    raw_text: str

class QuestionMeta(BaseModel):
    layout: str = "single"
    anchors: List[str] = []
    page_anchors: List[int] = []
    bbox: Optional[Dict[str, float]] = None
    confidence: float = 1.0
    warnings: List[str] = []

class TableSpan(BaseModel):
    r: int
    c: int
    rowspan: int
    colspan: int

class Question(BaseModel):
    doc_id: str
    page_range: List[int]
    q_no: str
    question_text: str
    choices: List[Choice] = []
    answer: Answer
    explanation: Optional[str] = None
    table_refs: List[str] = []
    image_refs: List[str] = []
    meta: QuestionMeta

class Table(BaseModel):
    table_id: str
    doc_id: str
    page: int
    caption: str
    header: List[str]
    rows: List[List[str]]
    span: List[TableSpan] = []

class ExtractionReport(BaseModel):
    version: str
    doc_id: str
    total_pages: int
    total_questions: int
    total_tables: int
    failures: int
    warnings: int
    items: List[str] = []
    tables: List[str] = []
    validation_results: Dict[str, Any] = {}

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc_id = "keyword130"
        self.images_dir = Path("images")
        self.items = []
        self.tables = []
        self.warnings = []
        self.failures = []
        
    def extract_text(self) -> Dict[int, str]:
        """PDF에서 페이지별 텍스트 추출"""
        text_by_page = {}
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text_by_page[i] = page.extract_text() or ""
        return text_by_page
    
    def extract_questions(self, text_by_page: Dict[int, str]) -> List[Question]:
        """Cursor AI를 사용하여 문제 추출"""
        print("문제 추출 시작...")
        
        # 전체 텍스트 결합 (페이지별로 구분)
        combined_text = "\n".join([f"[PAGE {i}]\n{text}" for i, text in text_by_page.items()])
        
        # 프롬프트 구성
        prompt = f"""
당신은 PDF 원문 보존 추출기입니다. 추측/보정/요약 금지.

[INPUT]
PDF 원문 텍스트 (개행과 공백을 정확히 보존):
{combined_text[:75000]}

[STRICT RULES]
1. 문항 인식: Q번호, 문제 번호, (보기), 정답: 패턴으로 문항 추출
2. 선지 키 변환:
   - ①,②,③,④ → key: "1","2","3","4"
   - ㄱ,ㄴ,ㄷ,ㄹ → key: "1","2","3","4"
   - a,b,c,d → key: "1","2","3","4"
   - 원본 표기는 raw_key에 보존
3. 원문 보존: 공백, 개행(\\n), 특수기호 그대로 유지
4. 불확실한 항목은 해당 필드를 null로 설정하고 meta.warnings에 사유 기록
5. 스키마 준수 필수

[OUTPUT FORMAT]
{{
  "items": [
    {{
      "doc_id": "keyword130",
      "page_range": [시작페이지, 끝페이지],
      "q_no": "Q001",
      "question_text": "원문 그대로(공백·개행 보존)",
      "choices": [
        {{"key": "1", "raw_key": "①", "text": "원문"}},
        {{"key": "2", "raw_key": "②", "text": "원문"}}
      ],
      "answer": {{"keys": ["2"], "raw_text": "정답 ②"}},
      "explanation": null,
      "table_refs": [],
      "image_refs": ["파일명.png"],
      "meta": {{
        "layout": "single",
        "anchors": ["Q1.", "(보기)", "정답"],
        "page_anchors": [1, 2],
        "confidence": 1.0,
        "warnings": []
      }}
    }}
  ]
}}

[IMPORTANT]
- 머리말/바닥글/워터마크/페이지번호 제외
- 모든 텍스트 원문 그대로 (의미 변환 금지)
- JSON 형식으로 정확히 출력
"""

        try:
            # OpenAI API 호출 (온도 0, JSON 모드)
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "당신은 PDF 원문 보존 추출기입니다. 추측/보정/요약 금지. JSON 형식으로 정확히 출력하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                top_p=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            questions = []
            
            # JSON 객체에서 items 배열 추출
            if "items" in result:
                items = result["items"]
                for item in items:
                    try:
                        q = Question(**item)
                        questions.append(q)
                    except Exception as e:
                        self.warnings.append(f"문항 파싱 오류: {e}")
                        print(f"오류: {item.get('q_no', 'unknown')} - {e}")
            
            print(f"추출 완료: {len(questions)}개 문항")
            return questions
            
        except Exception as e:
            print(f"API 오류: {e}")
            self.failures.append(f"문제 추출 실패: {e}")
            return []
    
    def extract_tables(self, text_by_page: Dict[int, str]) -> List[Table]:
        """표 추출"""
        print("표 추출 시작...")
        
        combined_text = "\n".join([f"[PAGE {i}]\n{text}" for i, text in text_by_page.items()])
        
        prompt = f"""
당신은 표 구조 보존 추출기입니다. 원문 그대로 보존.

[INPUT]
PDF 원문 (줄바꿈과 공백 정확히 보존):
{combined_text[:75000]}

[STRICT RULES]
1. 표 인식: 테두리 있는 표와 없는 표 모두 추출
2. 캡션: 표 상단 또는 하단의 설명 텍스트
3. 헤더: 첫 번째 행을 header 배열로
4. 셀: 줄바꿈은 \\n으로 보존
5. 병합: rowspan, colspan으로 기록
6. 숫자/단위: 변환 금지, 원문 그대로

[OUTPUT FORMAT]
{{
  "tables": [
    {{
      "table_id": "table_페이지_번호",
      "doc_id": "keyword130",
      "page": 페이지번호,
      "caption": "원문 캡션",
      "header": ["컬럼1", "컬럼2", "컬럼3"],
      "rows": [
        ["셀1", "셀2", "셀3"],
        ["셀4", "셀5", "셀6"]
      ],
      "span": [
        {{"r": 0, "c": 0, "rowspan": 1, "colspan": 1}}
      ]
    }}
  ]
}}

[IMPORTANT]
- 모든 텍스트 원문 그대로
- 줄바꿈은 \\n으로 표현
- 병합 정보 정확히 기록
- JSON 형식으로 출력
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "당신은 표 구조 보존 추출기입니다. JSON 형식으로 정확히 출력하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                top_p=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            tables = []
            
            if "tables" in result:
                for item in result["tables"]:
                    try:
                        t = Table(**item)
                        tables.append(t)
                    except Exception as e:
                        self.warnings.append(f"표 파싱 오류: {e}")
            
            print(f"추출 완료: {len(tables)}개 표")
            return tables
            
        except Exception as e:
            print(f"API 오류: {e}")
            return []
    
    def match_images(self, questions: List[Question]):
        """이미지 파일 매칭"""
        print("이미지 매칭 시작...")
        
        # 이미지 파일 목록
        image_files = list(self.images_dir.glob("*.png"))
        
        for q in questions:
            # 파일명에서 숫자 추출: (?<=^|_)Q?(\d{1,3})[-_]?.*\.png
            q_num = re.search(r'\d+', q.q_no)
            if not q_num:
                continue
                
            q_num = int(q_num.group())
            
            # 매칭되는 이미지 찾기
            for img_file in image_files:
                img_num = re.search(r'\d+', img_file.stem)
                if img_num and int(img_num.group()) == q_num:
                    q.image_refs.append(img_file.name)
    
    def validate(self, questions: List[Question], tables: List[Table]) -> Dict[str, Any]:
        """검증 수행"""
        print("검증 시작...")
        
        validation_results = {
            "text_hash_check": [],
            "table_structure_check": [],
            "forbidden_pattern_check": [],
            "meta_integrity_check": []
        }
        
        # 금지 패턴 검사
        forbidden_patterns = ["아마도", "즉", "의미", "추정"]
        for q in questions:
            text = q.question_text + " ".join([c.text for c in q.choices])
            for pattern in forbidden_patterns:
                if pattern in text:
                    validation_results["forbidden_pattern_check"].append({
                        "q_no": q.q_no,
                        "pattern": pattern,
                        "status": "FAIL"
                    })
                    self.failures.append(f"{q.q_no}: 금지 패턴 발견 - {pattern}")
        
        # 메타 무결성 검사
        for q in questions:
            if q.answer.keys:
                for key in q.answer.keys:
                    if not any(c.key == key for c in q.choices):
                        validation_results["meta_integrity_check"].append({
                            "q_no": q.q_no,
                            "issue": f"정답 키 '{key}'가 choices에 없음",
                            "status": "FAIL"
                        })
                        self.failures.append(f"{q.q_no}: 정답 키 불일치")
        
        return validation_results
    
    def run(self):
        """전체 추출 프로세스 실행"""
        print("=" * 50)
        print("PDF 추출 시작")
        print("=" * 50)
        
        # 텍스트 추출
        text_by_page = self.extract_text()
        print(f"총 {len(text_by_page)} 페이지 추출됨")
        
        # 문제 추출
        questions = self.extract_questions(text_by_page)
        
        # 표 추출
        tables = self.extract_tables(text_by_page)
        
        # 이미지 매칭
        self.match_images(questions)
        
        # 검증
        validation_results = self.validate(questions, tables)
        
        # items.jsonl 저장
        with open("items.jsonl", "w", encoding="utf-8") as f:
            for q in questions:
                f.write(json.dumps(q.model_dump(), ensure_ascii=False) + "\n")
        
        # tables.jsonl 저장
        with open("tables.jsonl", "w", encoding="utf-8") as f:
            for t in tables:
                f.write(json.dumps(t.model_dump(), ensure_ascii=False) + "\n")
        
        # report.json 생성
        report = ExtractionReport(
            version="1.0",
            doc_id=self.doc_id,
            total_pages=len(text_by_page),
            total_questions=len(questions),
            total_tables=len(tables),
            failures=len(self.failures),
            warnings=len(self.warnings),
            validation_results=validation_results
        )
        
        with open("report.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(report.model_dump(), ensure_ascii=False, indent=2))
        
        print("=" * 50)
        print("추출 완료!")
        print(f"문항: {len(questions)}개")
        print(f"표: {len(tables)}개")
        print(f"실패: {len(self.failures)}개")
        print(f"경고: {len(self.warnings)}개")
        print("=" * 50)
        
        return report

if __name__ == "__main__":
    extractor = PDFExtractor("keyword130.pdf")
    extractor.run()

