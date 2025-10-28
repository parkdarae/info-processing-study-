# GitHub → Vercel 배포 가이드

## 1단계: GitHub 저장소 생성

1. **GitHub 웹사이트 접속**
   - https://github.com 접속
   - 로그인

2. **새 저장소 생성**
   - 우측 상단의 `+` 버튼 클릭
   - `New repository` 선택

3. **저장소 설정**
   - Repository name: `info_ver2` (또는 원하는 이름)
   - Description: `문제은행 학습 시스템`
   - **Public** 선택
   - **README, .gitignore, LICENSE 추가하지 않음** (이미 있음)
   - `Create repository` 클릭

## 2단계: 로컬 저장소를 GitHub에 연결

터미널에서 다음 명령어 실행:

```bash
git remote add origin https://github.com/사용자이름/info_ver2.git
git branch -M main
git push -u origin main
```

> **주의**: `사용자이름` 부분을 본인의 GitHub 사용자명으로 변경하세요!

## 3단계: Vercel에 배포

1. **Vercel 웹사이트 접속**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인

2. **프로젝트 추가**
   - `Add New Project` 클릭
   - `info_ver2` 저장소 선택
   - `Import` 클릭

3. **프로젝트 설정**
   - **Framework Preset**: Other
   - **Root Directory**: `.` (기본값)
   - **Build and Output Settings**: 건드리지 않음 (정적 사이트)
   - `Deploy` 클릭

4. **배포 완료**
   - 배포가 완료되면 자동으로 URL이 생성됩니다
   - 예: `https://info-ver2-xxx.vercel.app`

## 4단계: 이미지 경로 수정 (필요시)

Vercel에서 이미지 경로가 제대로 작동하는지 확인하고, 필요하면 `index.html`에서 이미지 경로를 수정하세요.

---

## 빠른 명령어 모음

```bash
# 1. GitHub 저장소 연결 (저장소 URL은 GitHub에서 생성 후 복사)
git remote add origin https://github.com/사용자이름/info_ver2.git

# 2. 메인 브랜치로 변경
git branch -M main

# 3. GitHub에 푸시
git push -u origin main

# 4. 이후 변경사항 푸시
git add .
git commit -m "변경 메시지"
git push
```

## 문제 해결

### 인증 오류가 발생하는 경우
```bash
# GitHub Personal Access Token 생성 필요
# GitHub > Settings > Developer settings > Personal access tokens > Generate new token
```

### 이미 푸시되어 있는 저장소가 있는 경우
```bash
git remote -v  # 현재 원격 저장소 확인
git remote remove origin  # 기존 원격 저장소 제거
git remote add origin https://github.com/사용자이름/info_ver2.git  # 새로 추가
```
