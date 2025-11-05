// 모달 관련 함수들

// 통계 모달 토글
function toggleStats() {
    closeMenu();
    const modal = document.getElementById('statsModal');
    modal.style.display = 'flex';
    
    // 모달에 통계 업데이트
    const progress = document.getElementById('progress');
    const accuracy = document.getElementById('accuracy');
    const remaining = document.getElementById('remaining');
    const wrongCount = document.getElementById('wrongCount');
    
    if (progress) document.getElementById('modalProgress').textContent = progress.textContent;
    if (accuracy) document.getElementById('modalAccuracy').textContent = accuracy.textContent;
    if (remaining) document.getElementById('modalRemaining').textContent = remaining.textContent;
    if (wrongCount) document.getElementById('modalWrongCount').textContent = wrongCount.textContent;
}

// 통계 모달 닫기
function closeStats() {
    const modal = document.getElementById('statsModal');
    modal.style.display = 'none';
}

// 폰트 크기 모달 열기
function openFontModal() {
    closeMenu();
    const modal = document.getElementById('fontSizeModal');
    modal.classList.add('show');
    
    // 현재 선택된 폰트 크기 표시
    const currentSize = localStorage.getItem('fontSize') || 'normal';
    document.querySelectorAll('.font-size-option').forEach(opt => opt.classList.remove('active'));
    document.querySelectorAll('.font-size-option').forEach(opt => {
        if (opt.onclick.toString().includes(currentSize)) {
            opt.classList.add('active');
        }
    });
}

// 폰트 크기 모달 닫기
function closeFontModal() {
    const modal = document.getElementById('fontSizeModal');
    modal.classList.remove('show');
}

// 폰트 크기 선택
function selectFontSize(size) {
    setFontSize(size);
    
    // active 클래스 업데이트
    document.querySelectorAll('.font-size-option').forEach(opt => opt.classList.remove('active'));
    event.target.closest('.font-size-option').classList.add('active');
}

// 사용 방법 보기
function showWelcome() {
    closeMenu();
    document.getElementById('welcomePopup').classList.add('show');
}

// 범위 설정 모달 표시
function showRangeModal() {
    const modal = document.getElementById('rangeModal');
    modal.style.display = 'flex';
    
    // 입력값 변경 이벤트 리스너
    const startInput = document.getElementById('rangeStart');
    const endInput = document.getElementById('rangeEnd');
    
    startInput.addEventListener('input', updateRangePreview);
    endInput.addEventListener('input', updateRangePreview);
    
    updateRangePreview();
}

// 범위 설정 모달 닫기
function closeRangeModal() {
    const modal = document.getElementById('rangeModal');
    modal.style.display = 'none';
}

// 범위 미리보기 업데이트
function updateRangePreview() {
    const config = App.moduleConfig[App.state.currentModule];
    const start = parseInt(document.getElementById('rangeStart').value) || 1;
    const end = parseInt(document.getElementById('rangeEnd').value) || config.maxRange;
    
    // 유효성 검사
    const validStart = Math.max(1, Math.min(start, config.maxRange));
    const validEnd = Math.max(validStart, Math.min(end, config.maxRange));
    
    const count = validEnd - validStart + 1;
    const preview = document.getElementById('rangePreview');
    preview.textContent = `선택된 범위: ${validStart}번 ~ ${validEnd}번 (총 ${count}문제)`;
}

