# Vercel 프로젝트 삭제 및 재생성 가이드

## 현재 상황
- Git 저장소는 정상 (최신 `config.js` 포함)
- Vercel 배포 버전이 오래된 파일을 캐시하고 있음
- Fallback 로직이 있지만, 근본적인 해결을 위해 프로젝트 재생성 필요

## 절차

### 1단계: Vercel 프로젝트 삭제

1. **Vercel 대시보드 접속**
   - https://vercel.com/dashboard
   - 로그인

2. **프로젝트 선택**
   - `info-processing-study-` 프로젝트 클릭

3. **프로젝트 설정**
   - 상단 "Settings" 탭 클릭
   - 스크롤하여 맨 아래로 이동

4. **프로젝트 삭제**
   - "Delete Project" 섹션 찾기
   - "Delete" 버튼 클릭
   - 프로젝트 이름 입력하여 확인
   - "Delete" 최종 확인

### 2단계: Vercel 프로젝트 재생성

1. **새 프로젝트 생성**
   - Vercel 대시보드에서 "Add New..." → "Project" 클릭
   - 또는 https://vercel.com/new 접속

2. **Git 저장소 연결**
   - GitHub 저장소 선택: `parkdarae/info-processing-study-`
   - "Import" 클릭

3. **프로젝트 설정**
   - **Project Name**: `info-processing-study` (또는 원하는 이름)
   - **Framework Preset**: "Other" 또는 "Vite" (프레임워크 없음)
   - **Root Directory**: `./` (기본값)
   - **Build Command**: `echo 'Build complete'` (또는 비워두기)
   - **Output Directory**: `./` (기본값)
   - **Install Command**: 비워두기 (필요 없음)

4. **Environment Variables**
   - 현재는 필요 없음 (필요시 나중에 추가)

5. **Deploy**
   - "Deploy" 버튼 클릭
   - 배포 완료 대기 (약 1-2분)

### 3단계: 배포 확인

1. **배포 완료 확인**
   - Vercel 대시보드에서 배포 상태 확인
   - "Ready" 상태가 되면 완료

2. **config.js 확인**
   ```bash
   node verify_vercel_config.js
   ```
   
   또는 브라우저에서:
   - https://[새-도메인]/js/config.js 접속
   - `App.configVersion = '20251221_cissp_force_deploy_v2'` 확인
   - `'cissp': { ... }` 모듈 확인

3. **CISSP 모듈 테스트**
   - https://[새-도메인]/ 접속
   - CISSP 메뉴 클릭
   - 오류가 발생하지 않는지 확인

### 4단계: 도메인 설정 (선택사항)

기존 도메인을 사용하려면:

1. **Vercel 프로젝트 설정**
   - "Settings" → "Domains" 탭
   - 기존 도메인 추가: `info-processing-study-daryong2.agency`
   - DNS 설정 확인 (기존과 동일)

2. **DNS 확인**
   - 도메인 제공업체에서 DNS 레코드 확인
   - Vercel이 제공하는 DNS 값과 일치하는지 확인

## 주의사항

1. **Git 저장소는 변경하지 않음**
   - Git 저장소는 그대로 유지
   - 기존 커밋 히스토리 유지

2. **로컬 파일 확인**
   - 로컬 `config.js`에 CISSP 모듈이 있는지 확인
   - `git status`로 변경사항 확인

3. **배포 후 캐시 클리어**
   - 브라우저 강력 새로고침 (Ctrl+Shift+R)
   - 개발자 도구에서 "Disable cache" 체크

## 문제 해결

### 배포 후에도 오래된 파일이 보이는 경우

1. **Vercel 빌드 캐시 클리어**
   - 프로젝트 설정 → "General" → "Clear Build Cache"

2. **브라우저 캐시 클리어**
   - 개발자 도구 → Network 탭 → "Disable cache" 체크
   - 강력 새로고침 (Ctrl+Shift+R)

3. **CDN 캐시 무효화**
   - Vercel 대시보드 → "Deployments" → 최신 배포 → "Redeploy"

## 확인 체크리스트

- [ ] Vercel 프로젝트 삭제 완료
- [ ] 새 프로젝트 생성 완료
- [ ] Git 저장소 연결 완료
- [ ] 배포 완료 (Ready 상태)
- [ ] `config.js`에 CISSP 모듈 확인
- [ ] CISSP 메뉴 클릭 시 오류 없음
- [ ] 도메인 설정 완료 (선택사항)

