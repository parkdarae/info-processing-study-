# Vercel 프로젝트 공개 설정 방법

## 문제
모바일에서 접속 시 Vercel 로그인 화면이 나타남 → 프로젝트가 비공개 설정으로 되어 있음

## 해결 방법

### 1. Vercel 대시보드 접속
- https://vercel.com 접속
- 로그인

### 2. 프로젝트 설정 확인
1. 프로젝트 선택: `info-processing-study`
2. **Settings** 탭 클릭
3. **General** 섹션 확인

### 3. 프로젝트 공개 설정

#### 방법 A: 프로젝트를 Public으로 변경 (추천)
1. Settings → **General** → **Privacy** 섹션 찾기
2. **"Make this project public"** 또는 "Public" 옵션 선택
3. 확인/저장

#### 방법 B: 액세스 제어 확인
1. Settings → **General** → **Vercel for Git** 섹션
2. 배포 URL이 공개적으로 접근 가능한지 확인
3. Deployment Protection이 비활성화되어 있는지 확인

### 4. 배포 URL 확인
배포된 URL은 다음과 같은 형태여야 합니다:
- `https://info-processing-study-xxx.vercel.app`
- 또는 Custom Domain이 설정된 경우 그 도메인

이 URL은 누구나 접근 가능해야 합니다.

### 5. 추가 확인 사항

#### Deployment Protection 해제
1. Settings → **General** → **Deployment Protection**
2. 모든 배포에 대한 보호가 비활성화되어 있는지 확인
3. 필요시 **"Disable Deployment Protection"** 클릭

#### Team 설정 확인
1. 프로젝트가 **Personal Account** 또는 **Public Team**에 있는지 확인
2. Private Team에 있는 경우, 프로젝트를 Personal로 이동하거나 Team을 Public으로 변경

---

## 배포 후 확인

1. 배포 URL을 **시크릿/비공개 모드**에서 열기
2. 로그인 없이 사이트가 표시되는지 확인
3. 모바일에서도 테스트

## 문제가 계속되면

1. Vercel 지원팀 문의
2. 또는 새 프로젝트로 재배포 (Public으로 설정)
