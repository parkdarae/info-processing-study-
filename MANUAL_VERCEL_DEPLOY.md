# Vercel 수동 재배포 가이드

## 문제
GitHub에는 `config.js`가 최신 버전으로 올라가 있지만, Vercel 배포 버전에는 반영되지 않았습니다.

## 해결 방법

### 방법 1: Vercel 대시보드에서 수동 재배포 (권장)

1. https://vercel.com/dashboard 접속
2. 프로젝트 선택: `info-processing-study-`
3. "Deployments" 탭 클릭
4. 최신 배포 항목의 "..." 메뉴 클릭
5. **"Redeploy"** 선택
6. 배포 완료 대기 (약 1-2분)

### 방법 2: Vercel CLI 사용

```bash
# Vercel CLI 설치 (없는 경우)
npm install -g vercel

# 프로젝트 디렉토리에서
cd C:\Users\darae\Desktop\info_ver5
vercel --prod --force
```

### 방법 3: 빌드 캐시 클리어

Vercel 대시보드에서:
1. 프로젝트 설정 → "General" 탭
2. "Clear Build Cache" 버튼 클릭
3. 재배포 트리거

## 확인 방법

배포 완료 후:
```bash
node verify_vercel_config.js
```

또는 브라우저에서:
1. https://info-processing-study-daryong2.agency/js/config.js 접속
2. `App.configVersion = '20251221_cissp_force_deploy'` 확인
3. `'cissp': { ... }` 모듈 확인

## 참고

- GitHub의 최신 `config.js`: https://github.com/parkdarae/info-processing-study-/blob/main/js/config.js
- Vercel 배포 URL: https://info-processing-study-daryong2.agency

