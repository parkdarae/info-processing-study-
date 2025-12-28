# 📦 백업 정보

## 최신 백업
- **백업 시간**: 2025-11-03 14:15:04
- **백업 폴더**: `C:\Users\darae\Desktop\info_ver4_backup_20251103_141504`
- **상태**: ✅ 완료

## 백업 내용
- ✅ 전체 소스 코드 (HTML, CSS, JavaScript)
- ✅ 모든 데이터 파일 (259개 문제, 12개 회차)
- ✅ 이미지 파일
- ✅ 설정 파일 및 스크립트

## 백업 이유
CSS 파일 복구 후 안전한 상태 보존

## 복원 방법
문제가 생기면 백업 폴더를 `info_ver4`로 복사하세요:
```powershell
cd C:\Users\darae\Desktop
Remove-Item -Path info_ver4 -Recurse -Force
Copy-Item -Path info_ver4_backup_20251103_141504 -Destination info_ver4 -Recurse
```

## 주의사항
- 백업 폴더는 삭제하지 마세요
- 새 백업을 만들기 전에 이전 백업 확인
- 정기적으로 백업 권장 (중요한 변경 전후)




