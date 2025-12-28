# 🔧 브라우저 캐시 문제 해결 방법

## 문제 상황
- 햄버거 메뉴가 보이지 않음
- 스타일이 제대로 적용되지 않음

## ✅ 해결 방법

### 방법 1: 강력 새로고침 (Ctrl + Shift + R)
**Windows/Linux:**
```
Ctrl + Shift + R
또는
Ctrl + F5
```

**Mac:**
```
Cmd + Shift + R
```

### 방법 2: 캐시 완전 삭제
1. **F12** 키를 눌러 개발자 도구 열기
2. **Network** (네트워크) 탭 선택
3. **Disable cache** 체크박스 활성화
4. 페이지 새로고침 (F5)

### 방법 3: 브라우저 설정에서 캐시 삭제

**Chrome:**
1. 주소창 옆 🔒 아이콘 클릭
2. "사이트 설정" 클릭
3. "데이터 삭제" 클릭

**Firefox:**
1. Ctrl + Shift + Delete
2. "캐시" 선택
3. "지금 삭제" 클릭

**Edge:**
1. Ctrl + Shift + Delete
2. "캐시된 이미지 및 파일" 선택
3. "지금 지우기" 클릭

### 방법 4: 프라이빗 브라우징 모드로 테스트
- Chrome: Ctrl + Shift + N
- Firefox: Ctrl + Shift + P
- Edge: Ctrl + Shift + N

프라이빗 모드에서 http://localhost:8080 접속하여 확인

## 🚨 여전히 안 된다면?

### 서버 재시작
```bash
# 기존 서버 종료 (Ctrl + C)
# 다시 시작
python -m http.server 8080
```

### 파일 확인
```bash
# CSS 파일이 정상인지 확인
dir css
```

모든 CSS 파일 크기가 0 이상이어야 합니다:
- ✅ common.css (2130 bytes)
- ✅ menu.css (2944 bytes)
- ✅ modal.css (5257 bytes)
- ✅ question.css (7991 bytes)
- ✅ responsive.css (1425 bytes)

## 📞 문제가 계속되면?

개발자 도구(F12)의 Console 탭에서 에러 메시지를 확인하고 알려주세요.




