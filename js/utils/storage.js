// localStorage 관리 함수들

// 진행 상황 저장
function saveProgress() {
    localStorage.setItem('progress', JSON.stringify({
        correct: App.state.stats.correct,
        wrong: App.state.stats.wrong
    }));
}

// 진행 상황 로드
function loadProgress() {
    const saved = JSON.parse(localStorage.getItem('progress') || '{}');
    App.state.stats.correct = saved.correct || 0;
    App.state.stats.wrong = saved.wrong || 0;
    
    // 하위 호환성
    stats.correct = App.state.stats.correct;
    stats.wrong = App.state.stats.wrong;
}

// 오답 추가
function addWrongQuestion(qNo) {
    const wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    if (!wrongQuestions.includes(qNo)) {
        wrongQuestions.push(qNo);
        localStorage.setItem('wrongQuestions', JSON.stringify(wrongQuestions));
    }
}

// 오답 제거
function removeWrongQuestion(qNo) {
    const wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    const index = wrongQuestions.indexOf(qNo);
    if (index > -1) {
        wrongQuestions.splice(index, 1);
        localStorage.setItem('wrongQuestions', JSON.stringify(wrongQuestions));
    }
}

// 문제 체크
function markQuestion(qNo) {
    const markedQuestions = JSON.parse(localStorage.getItem('markedQuestions') || '[]');
    const btn = event.target.closest('button');
    
    if (!markedQuestions.includes(qNo)) {
        markedQuestions.push(qNo);
        localStorage.setItem('markedQuestions', JSON.stringify(markedQuestions));
        btn.innerHTML = '<i class="fas fa-check"></i> 체크됨';
        btn.style.background = '#28a745';
    } else {
        const index = markedQuestions.indexOf(qNo);
        markedQuestions.splice(index, 1);
        localStorage.setItem('markedQuestions', JSON.stringify(markedQuestions));
        btn.innerHTML = '<i class="fas fa-star"></i> 체크';
        btn.style.background = '';
    }
}

// 진행 초기화
function resetProgress() {
    if (confirm('모든 진행 상황을 초기화하시겠습니까?')) {
        localStorage.clear();
        App.state.stats = { total: 0, correct: 0, wrong: 0, wrongQuestions: [] };
        stats = App.state.stats;
        updateStats();
        location.reload();
    }
}

// 환영 팝업 닫기
function closeWelcomePopup() {
    document.getElementById('welcomePopup').classList.remove('show');
    localStorage.setItem('welcomeShown', 'true');
}

// 폰트 크기 저장 및 로드
function loadFontSize() {
    const savedSize = localStorage.getItem('fontSize') || 'normal';
    document.body.classList.remove('font-smallest', 'font-small', 'font-normal', 'font-large');
    document.body.classList.add('font-' + savedSize);
}

function setFontSize(size) {
    document.body.classList.remove('font-smallest', 'font-small', 'font-normal', 'font-large');
    document.body.classList.add('font-' + size);
    localStorage.setItem('fontSize', size);
}

