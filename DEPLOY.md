# GitHub 배포 가이드

## 1. 기존 저장소 삭제 (선택사항)
GitHub 웹사이트에서 https://github.com/parkdarae/info-processing-study 저장소로 이동하여:
1. Settings 탭 클릭
2. 맨 아래 "Danger Zone" 섹션
3. "Delete this repository" 클릭
4. 저장소 이름 입력하여 확인

## 2. Git 초기화 및 커밋

```bash
# Git 저장소 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "feat: 정보처리기사 실기 학습 시스템 v2.0

- 130개 문제 완벽 추출
- 5가지 학습 모드 (순차/랜덤/범위/오답/체크)
- 스마트 정답 시스템 (다양한 입력 형식 지원)
- 복수 답안 지원
- 표 및 이미지 렌더링
- 학습 통계 및 진행률 추적
- LocalStorage 기반 진행 상황 저장"
```

## 3. GitHub 저장소 생성 및 푸시

### 방법 1: GitHub CLI 사용
```bash
# GitHub CLI로 저장소 생성 및 푸시
gh repo create info-processing-study --public --source=. --push
```

### 방법 2: 수동 방법
```bash
# 원격 저장소 연결
git remote add origin https://github.com/parkdarae/info-processing-study.git

# 기본 브랜치 설정
git branch -M main

# 푸시
git push -u origin main
```

## 4. GitHub Pages 설정 (선택사항)

저장소 Settings > Pages에서:
1. Source: Deploy from a branch
2. Branch: main
3. Folder: / (root)
4. Save

배포 후 `https://parkdarae.github.io/info-processing-study/` 에서 접속 가능

## 5. 저장소 설명 추가

GitHub 저장소 페이지에서:
- **Description**: 정보처리기사 실기 학습 시스템 - 130문제 완벽 지원
- **Website**: https://parkdarae.github.io/info-processing-study/
- **Topics**: `정보처리기사`, `실기`, `학습시스템`, `pdf-parser`, `javascript`, `html5`

## 6. README 배지 추가 (선택사항)

README.md 상단에 다음 배지들이 자동으로 추가됩니다:
- License 배지
- Python 버전 배지
- HTML5 배지

## 주의사항

- `.env` 파일은 `.gitignore`에 포함되어 있어 업로드되지 않습니다
- API 키는 절대 커밋하지 마세요
- `keyword130.pdf`는 저작권 문제가 있을 수 있으니 확인 필요

