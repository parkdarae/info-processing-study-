# 배포 체크리스트

## ✅ 배포 전 확인사항

### 1. 파일 확인
- [x] `data/items_pmp.jsonl` - 798개 문제
- [x] `js/pmp-module.js` - 키워드 강조 기능
- [x] `css/pmp-module.css` - 스타일
- [x] `scripts/extract_pmp_v3.py` - 파싱 스크립트
- [x] `scripts/validate_pmp_quality.py` - 품질 점검
- [x] `scripts/improve_pmp_readability.py` - 가독성 개선

### 2. 데이터 품질
- [x] 총 문제 수: 798개
- [x] 추출 비율: 99.9%
- [x] 해설 완성도: 100%
- [x] 가독성 개선: 797개

### 3. 기능 테스트
- [ ] 로컬에서 정상 동작 확인
- [ ] 키워드 강조 ON/OFF 동작 확인
- [ ] 문제 풀이 정상 동작
- [ ] 해설 표시 정상 동작
- [ ] 모바일 반응형 확인

## 📦 배포 단계

### Step 1: 로컬 테스트
```bash
# Python 서버 실행
py -m http.server 8000

# 브라우저에서 테스트
# http://localhost:8000
```

**테스트 항목:**
1. PMP 메뉴 접근
2. 798개 문제 로드
3. 키워드 강조 기능
4. 문제 풀이 흐름
5. 대시보드 통계

### Step 2: Git 커밋
```bash
# 상태 확인
git status

# 변경사항 추가
git add data/items_pmp.jsonl
git add js/pmp-module.js
git add scripts/extract_pmp_v3.py
git add scripts/validate_pmp_quality.py
git add scripts/improve_pmp_readability.py
git add PMP_COMPLETION_REPORT.md
git add TEST_GUIDE.md
git add DEPLOYMENT_CHECKLIST.md

# 커밋
git commit -m "feat: PMP 문제집 798개 추출 및 키워드 강조 학습 모드 추가

- PDF 파싱 개선: 544개 → 798개 (99.9%)
- 데이터 품질 개선: 가독성 797개 문제 개선
- 키워드 강조 기능: 40+ PMP 핵심 키워드 자동 강조
- 품질 점검 스크립트: 자동 검증 시스템 구축
- 학습 경험 개선: 토글 버튼으로 강조 ON/OFF"

# 푸시
git push origin main
```

### Step 3: Vercel 배포 확인
1. Vercel 대시보드 접속
2. 자동 배포 트리거 확인
3. 빌드 로그 확인
4. 배포 완료 대기 (약 2-3분)

### Step 4: 프로덕션 테스트
```
배포 URL: https://your-app.vercel.app
```

**재테스트 항목:**
1. [ ] PMP 메뉴 접근
2. [ ] 문제 로딩 속도
3. [ ] 키워드 강조 동작
4. [ ] 모바일 환경 테스트
5. [ ] 브라우저 호환성 (Chrome, Safari, Edge)

## 🐛 배포 후 이슈 대응

### 이슈 1: 데이터 로드 실패
**원인**: JSONL 파일 경로 문제
**해결**: 
```javascript
// js/pmp-module.js 확인
fetch('data/items_pmp.jsonl')
```

### 이슈 2: 한글 깨짐
**원인**: UTF-8 인코딩
**해결**: 
- Vercel은 자동으로 UTF-8 처리
- 로컬에서만 발생 시 Python 서버 사용

### 이슈 3: 캐시 문제
**원인**: 브라우저 캐시
**해결**:
```html
<!-- index.html에서 버전 업데이트 -->
<link rel="stylesheet" href="css/pmp-module.css?v=20251106">
<script src="js/pmp-module.js?v=20251106"></script>
```

## 📊 배포 후 모니터링

### 1주일 후 확인사항
- [ ] 사용자 피드백 수집
- [ ] 에러 로그 확인
- [ ] 성능 지표 확인
- [ ] 추가 개선사항 도출

### 성능 지표
- 페이지 로딩: < 3초
- 문제 전환: < 0.5초
- 메모리 사용: < 100MB

## 🎯 다음 단계 (선택사항)

### 단기 (1-2주)
- [ ] 이미지 문제 13개 수동 캡처 및 병합
- [ ] 불완전한 문장 44개 수동 보정
- [ ] 사용자 피드백 반영

### 중기 (1개월)
- [ ] 학습 통계 기능 강화
- [ ] 오답노트 기능 추가
- [ ] 모의고사 모드 추가

### 장기 (3개월)
- [ ] AI 기반 문제 추천
- [ ] 학습 진도 추적
- [ ] 소셜 학습 기능

## 📝 배포 완료 보고

### 배포 정보
- 배포 일시: _______________
- 배포자: _______________
- Git 커밋 해시: _______________
- Vercel 배포 URL: _______________

### 배포 결과
- [ ] 성공
- [ ] 실패 (사유: _______________)

### 테스트 결과
- [ ] 모든 기능 정상 동작
- [ ] 일부 이슈 있음 (내용: _______________)

---

**참고 문서:**
- `PMP_COMPLETION_REPORT.md` - 완료 보고서
- `TEST_GUIDE.md` - 테스트 가이드
- `pmp_quality_report.txt` - 품질 리포트

