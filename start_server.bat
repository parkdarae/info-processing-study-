@echo off
echo ====================================
echo 로컬 서버 시작 중...
echo ====================================
echo.

cd /d "%~dp0"

echo 현재 디렉토리: %CD%
echo.

echo Python 버전 확인:
python --version
echo.

echo 서버 시작 (포트 8080)...
echo.
echo 브라우저에서 다음 주소로 접속하세요:
echo http://localhost:8080
echo.
echo 서버 중지: Ctrl+C
echo ====================================
echo.

python -m http.server 8080
pause
