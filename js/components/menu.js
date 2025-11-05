// 메뉴 관련 함수들

// 햄버거 메뉴 토글
function toggleMenu() {
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('menuOverlay');
    
    sidebar.classList.toggle('show');
    overlay.classList.toggle('show');
}

// 메뉴 닫기
function closeMenu() {
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('menuOverlay');
    
    sidebar.classList.remove('show');
    overlay.classList.remove('show');
}

// 모듈 전환
function switchModule(moduleName) {
    closeMenu();
    
    if (!App.moduleConfig[moduleName]) {
        showMessage('알 수 없는 모듈입니다.');
        return;
    }
    
    App.state.currentModule = moduleName;
    currentModule = moduleName; // 하위 호환성
    const config = App.moduleConfig[moduleName];
    
    // 제목 업데이트
    document.querySelector('.header h1').innerHTML = `<i class="fas fa-book-reader"></i> ${config.title}`;
    
    // 메뉴 활성화 상태 업데이트
    document.querySelectorAll('.menu-item').forEach(item => {
        item.style.background = 'white';
        item.style.color = '';
    });
    const menuItem = document.getElementById(`menu_${moduleName}`);
    if (menuItem) {
        menuItem.style.background = '#667eea';
        menuItem.style.color = 'white';
    }
    
    // 범위 모달 max 값 업데이트
    document.getElementById('rangeStart').max = config.maxRange;
    document.getElementById('rangeEnd').max = config.maxRange;
    document.getElementById('rangeEnd').value = config.maxRange;
    
    // 문제 로드
    if (App.state.currentMode) {
        loadQuestions(App.state.currentMode);
    } else {
        App.state.currentQuestions = [];
        currentQuestions = []; // 하위 호환성
        App.state.currentIndex = 0;
        currentIndex = 0; // 하위 호환성
        document.getElementById('questionContainer').innerHTML = `
            <div class="question-card">
                <div style="text-align: center; padding: 50px;">
                    <i class="fas fa-book" style="font-size: 4em; color: #667eea; margin-bottom: 20px;"></i>
                    <h2>학습 모드를 선택해주세요</h2>
                    <p style="color: #6c757d; margin-top: 10px;">위 버튼 중 하나를 클릭하여 시작하세요</p>
                </div>
            </div>
        `;
    }
    
    updateStats();
}

// 기출문제 회차 선택
function switchPastExam() {
    const selector = document.getElementById('pastExamSelector');
    const examId = selector.value;
    
    if (!examId) {
        return;
    }
    
    // switchModule 호출
    switchModule(examId);
    
    // 정보 업데이트
    const config = App.moduleConfig[examId];
    const infoDiv = document.getElementById('pastExamInfo');
    infoDiv.innerHTML = `
        <i class="fas fa-check-circle" style="color: #667eea;"></i> 
        선택됨: ${config.maxRange}개 문제
    `;
    
    // 기존 메뉴 아이템 비활성화
    document.querySelectorAll('.menu-item').forEach(item => {
        item.style.background = 'white';
        item.style.color = '';
    });
}

// 카테고리별 문제 선택
function switchCategory() {
    const selector = document.getElementById('categorySelector');
    const categoryId = selector.value;
    
    if (!categoryId) {
        return;
    }
    
    closeMenu();
    
    // switchModule 호출
    switchModule(categoryId);
    
    // 정보 업데이트
    const config = App.moduleConfig[categoryId];
    const infoDiv = document.getElementById('categoryInfo');
    infoDiv.innerHTML = `
        <i class="fas fa-check-circle" style="color: #667eea;"></i> 
        선택됨: ${config.title}
    `;
    
    // 기존 메뉴 아이템 및 기출문제 선택 초기화
    document.querySelectorAll('.menu-item').forEach(item => {
        item.style.background = 'white';
        item.style.color = '';
    });
    document.getElementById('pastExamSelector').value = '';
}

