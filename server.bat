@echo off
echo ========================================
echo 문제은행 학습 시스템 서버 시작
echo ========================================
echo.
echo 서버 주소: http://localhost:8080
echo.
echo 학습 시스템: http://localhost:8080/index.html
echo Admin 페이지: http://localhost:8080/admin.html
echo.
echo 서버를 종료하려면 Ctrl+C를 누르세요.
echo ========================================
echo.

python -m http.server 8080

