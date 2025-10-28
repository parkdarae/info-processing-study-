# 🚀 GitHub Pages 배포 가이드

이 문서는 정보처리기사 실기 학습 시스템 v3.0을 GitHub Pages에 배포하는 방법을 설명합니다.

## 📋 사전 준비

- GitHub 계정
- Git 설치
- 프로젝트 파일

## 🔧 배포 단계

### 1. GitHub 저장소 생성

1. GitHub에 로그인
2. 우측 상단 `+` 버튼 클릭 > `New repository`
3. 저장소 정보 입력:
   - **Repository name**: `info-processing-study` (원하는 이름)
   - **Description**: `정보처리기사 실기 학습 시스템 v3.0`
   - **Public** 선택 (GitHub Pages는 Public 저장소에서 무료)
   - **Add a README file**: 체크 해제 (이미 있음)
4. `Create repository` 클릭

### 2. 로컬 저장소 초기화 및 푸시

```bash
# 프로젝트 폴더로 이동
cd C:\Users\darae\Desktop\info_ver3

# Git 초기화 (이미 되어있지 않다면)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: 정보처리기사 실기 학습 시스템 v3.0"

# 원격 저장소 연결 (YOUR_USERNAME을 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/YOUR_USERNAME/info-processing-study.git

# 푸시
git branch -M main
git push -u origin main
```

### 3. GitHub Pages 활성화

1. GitHub 저장소 페이지로 이동
2. `Settings` 탭 클릭
3. 좌측 메뉴에서 `Pages` 클릭
4. **Source** 섹션에서:
   - Branch: `main` 선택
   - Folder: `/ (root)` 선택
5. `Save` 버튼 클릭
6. 몇 분 후 페이지 상단에 배포 URL 표시
   - 예: `https://YOUR_USERNAME.github.io/info-processing-study/`

### 4. 배포 확인

1. 생성된 URL로 접속
2. `index.html`이 자동으로 로드됨
3. 햄버거 메뉴에서 문제집 선택 가능 확인
4. 학습 모드 동작 확인

## 📁 배포 파일 목록

다음 파일들이 GitHub Pages에 배포됩니다:

### 필수 파일
- ✅ `index.html` - 메인 학습 시스템
- ✅ `items.jsonl` - 핵심 키워드 130문제
- ✅ `tables.jsonl` - 핵심 키워드 표 데이터
- ✅ `items_code_control.jsonl` - 코드-제어문 14문제
- ✅ `tables_code_control.jsonl` - 코드-제어문 표 데이터
- ✅ `images/` - 핵심 키워드 이미지 폴더
- ✅ `images2/` - 코드-제어문 이미지 폴더
- ✅ `README.md` - 프로젝트 설명

### 선택 파일 (배포 불필요)
- ❌ `*.py` - Python 스크립트 (개발용)
- ❌ `*.pdf` - 원본 PDF 파일
- ❌ `*.txt` - 임시 텍스트 파일
- ❌ `info_ver2 - 복사본/` - 이전 버전 폴더

## 🗂️ .gitignore 설정

불필요한 파일이 업로드되지 않도록 `.gitignore` 파일을 생성합니다:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv

# 개발 파일
*.pdf
*.txt
*.pyc
.env
.env.local

# 임시 파일
*.tmp
*.bak
*.swp
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.sublime-*

# 이전 버전
info_ver2 - 복사본/

# Python 스크립트 (선택)
extract.py
parse_code_control_manual.py
fix_*.py
update_*.py
```

## 🔄 업데이트 방법

코드를 수정한 후 다시 배포하려면:

```bash
# 변경사항 추가
git add .

# 커밋
git commit -m "Update: 설명"

# 푸시
git push origin main
```

GitHub Pages는 자동으로 업데이트됩니다 (1-2분 소요).

## 🌐 커스텀 도메인 설정 (선택)

자신의 도메인을 사용하려면:

1. 도메인 구입 (예: Namecheap, GoDaddy)
2. DNS 설정:
   ```
   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io
   ```
3. GitHub Settings > Pages > Custom domain에 도메인 입력
4. `Enforce HTTPS` 체크

## 🐛 문제 해결

### 페이지가 로드되지 않음
- GitHub Pages 활성화 확인
- 브라우저 캐시 삭제 (Ctrl+F5)
- 몇 분 후 재시도

### 이미지가 표시되지 않음
- 이미지 파일이 `images/`, `images2/` 폴더에 있는지 확인
- 파일명 대소문자 확인 (GitHub는 대소문자 구분)
- 경로가 상대 경로인지 확인 (`images/1.png`)

### JSONL 파일을 읽을 수 없음
- 파일 인코딩이 UTF-8인지 확인
- JSON 형식이 올바른지 확인
- 브라우저 콘솔(F12)에서 에러 메시지 확인

### 로컬에서는 되는데 GitHub Pages에서 안됨
- 절대 경로 대신 상대 경로 사용
- 파일명 대소문자 정확히 일치
- CORS 문제 확인

## 📊 배포 상태 확인

GitHub Actions를 통해 배포 상태를 확인할 수 있습니다:

1. 저장소 페이지 > `Actions` 탭
2. 최근 워크플로우 확인
3. 녹색 체크: 배포 성공
4. 빨간 X: 배포 실패 (로그 확인)

## 🔒 보안 고려사항

- **API 키**: `.env` 파일은 절대 커밋하지 마세요
- **개인정보**: 민감한 정보는 제거
- **Public 저장소**: 모든 코드가 공개됨

## 📈 트래픽 분석 (선택)

Google Analytics를 추가하려면:

1. Google Analytics 계정 생성
2. 추적 ID 받기
3. `index.html`의 `<head>` 섹션에 추가:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

## 🎉 완료!

이제 전 세계 어디서나 학습 시스템에 접속할 수 있습니다!

배포 URL: `https://YOUR_USERNAME.github.io/info-processing-study/`

---

**문제가 있으면 GitHub Issues에 등록해주세요!**

