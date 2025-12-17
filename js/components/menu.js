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
    
    // App.moduleConfig가 초기화되지 않은 경우
    if (!App || !App.moduleConfig) {
        console.error('App.moduleConfig가 초기화되지 않았습니다. config.js가 로드되었는지 확인하세요.');
        console.error('App 객체:', App);
        showMessage('모듈 설정을 불러올 수 없습니다. 페이지를 새로고침해주세요.');
        return;
    }
    
    // 디버깅: 모듈 설정 확인
    console.log('switchModule 호출:', moduleName);
    console.log('App.moduleConfig:', App.moduleConfig);
    console.log('모듈 존재 여부:', App.moduleConfig[moduleName]);
    console.log('사용 가능한 모듈:', Object.keys(App.moduleConfig));
    
    // CISSP 모듈 특별 처리
    if (moduleName === 'cissp') {
        console.log('CISSP 모듈 전환 시도');
        if (App.moduleConfig['cissp']) {
            console.log('✅ CISSP 모듈 설정 발견:', App.moduleConfig['cissp']);
        } else {
            console.error('❌ CISSP 모듈 설정을 찾을 수 없습니다!');
            console.error('전체 모듈 목록:', Object.keys(App.moduleConfig));
        }
    }
    
    if (!App.moduleConfig[moduleName]) {
        console.error('알 수 없는 모듈:', moduleName);
        console.error('사용 가능한 모듈:', Object.keys(App.moduleConfig));
        const availableModules = Object.keys(App.moduleConfig).join(', ');
        showMessage(`알 수 없는 모듈입니다: ${moduleName}\n사용 가능한 모듈: ${availableModules}`);
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
    
    // 모듈별로 대시보드 표시 또는 문제 로드
    App.state.currentQuestions = [];
    currentQuestions = []; // 하위 호환성
    App.state.currentIndex = 0;
    currentIndex = 0; // 하위 호환성
    
    // 실기 최빈출 모듈인 경우 대시보드 표시
    if (moduleName === 'theory_frequent') {
        App.state.currentMode = null; // 대시보드 표시를 위해 모드 초기화
        theoryFrequent.loadItems().then(() => {
            theoryFrequent.renderDashboard();
        });
    }
    // PMP 모듈인 경우 대시보드 표시
    else if (moduleName === 'pmp') {
        App.state.currentMode = null; // 대시보드 표시를 위해 모드 초기화
        pmpModule.loadItems().then(() => {
            pmpModule.renderDashboard();
        });
    }
    // CISSP 모듈인 경우 대시보드 표시
    else if (moduleName === 'cissp') {
        App.state.currentMode = null; // 대시보드 표시를 위해 모드 초기화
        if (typeof window.cisspModule !== 'undefined' && window.cisspModule) {
            window.cisspModule.loadItems().then(() => {
                window.cisspModule.renderDashboard();
            });
        } else {
            console.error('CISSP 모듈이 로드되지 않았습니다. 페이지를 새로고침해주세요.');
            alert('CISSP 모듈을 불러올 수 없습니다. 페이지를 새로고침해주세요.');
        }
    }
    // 핵심 키워드 130 모듈인 경우 대시보드 표시
    else if (moduleName === 'keyword130') {
        App.state.currentMode = null; // 대시보드 표시를 위해 모드 초기화
        currentMode = null; // 하위 호환성
        keyword130Module.loadItems().then(() => {
            keyword130Module.renderDashboard();
        });
    }
    // 코드-제어문 모듈인 경우 대시보드 표시
    else if (moduleName === 'code_control') {
        App.state.currentMode = null; // 대시보드 표시를 위해 모드 초기화
        currentMode = null; // 하위 호환성
        codeControlModule.loadItems().then(() => {
            codeControlModule.renderDashboard();
        });
    }
    // 이론 모듈인 경우 카테고리 대시보드 표시
    else if (moduleName === 'theory') {
        App.state.currentMode = null; // 대시보드 표시를 위해 모드 초기화
        currentMode = null; // 하위 호환성
        // theory 데이터 로드 후 대시보드 렌더링
        loadTheoryData().then(() => {
            renderTheoryCategoryDashboard();
        }).catch(error => {
            console.error('Theory 데이터 로드 실패:', error);
            document.getElementById('questionContainer').innerHTML = `
                <div class="question-card">
                    <div style="text-align: center; padding: 50px;">
                        <i class="fas fa-exclamation-triangle" style="font-size: 4em; color: #dc3545; margin-bottom: 20px;"></i>
                        <h2>데이터 로드 실패</h2>
                        <p style="color: #6c757d; margin: 20px 0;">이론 문제 데이터를 불러오지 못했습니다.</p>
                        <button class="btn-primary" onclick="location.reload()">새로고침</button>
                    </div>
                </div>
            `;
        });
    } 
    // 기출문제 모듈인 경우 기본 메시지 표시
    else {
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

// 핵심 키워드 130 대시보드 렌더링
function renderKeyword130Dashboard() {
    const container = document.getElementById('questionContainer');
    const stats = getKeyword130Stats();
    
    container.innerHTML = `
        <div class="simple-dashboard">
            <div class="dash-header">
                <h2>핵심 키워드 130</h2>
                <div class="dash-stats">
                    <span>완료 ${stats.completed}</span>
                    <span>정답률 ${stats.accuracy}%</span>
                    <span>체크 ${stats.marked}</span>
                </div>
            </div>
            
            <div class="dash-actions">
                <button class="dash-btn primary" onclick="loadQuestions('sequential')">
                    <i class="fas fa-play-circle"></i> 순차 풀기
                </button>
                <button class="dash-btn secondary" onclick="loadQuestions('random')">
                    <i class="fas fa-random"></i> 랜덤 풀기
                </button>
                <button class="dash-btn accent" onclick="showRangeModal()">
                    <i class="fas fa-sliders-h"></i> 범위 설정
                </button>
                <button class="dash-btn special" onclick="loadQuestions('wrong')">
                    <i class="fas fa-times-circle"></i> 오답 노트
                </button>
                ${stats.marked > 0 ? `
                <button class="dash-btn marked" onclick="loadQuestions('marked')">
                    <i class="fas fa-star"></i> 체크 문제 (${stats.marked})
                </button>
                ` : ''}
            </div>
        </div>
    `;
}

// 핵심 키워드 130 통계 가져오기
function getKeyword130Stats() {
    const wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    const correctQuestions = JSON.parse(localStorage.getItem('correctQuestions') || '[]');
    const markedQuestions = JSON.parse(localStorage.getItem('markedQuestions') || '[]');
    
    const total = wrongQuestions.length + correctQuestions.length;
    const accuracy = total > 0 ? Math.round((correctQuestions.length / total) * 100) : 0;
    
    return {
        completed: total,
        accuracy: accuracy,
        marked: markedQuestions.length
    };
}

// 코드-제어문 14문제 대시보드 렌더링
function renderCodeControlDashboard() {
    const container = document.getElementById('questionContainer');
    const stats = getCodeControlStats();
    
    container.innerHTML = `
        <div class="simple-dashboard">
            <div class="dash-header">
                <h2>코드-제어문 14</h2>
                <div class="dash-stats">
                    <span>완료 ${stats.completed}</span>
                    <span>정답률 ${stats.accuracy}%</span>
                    <span>체크 ${stats.marked}</span>
                </div>
            </div>
            
            <div class="dash-actions">
                <button class="dash-btn primary" onclick="loadQuestions('sequential')">
                    <i class="fas fa-play-circle"></i> 순차 풀기
                </button>
                <button class="dash-btn secondary" onclick="loadQuestions('random')">
                    <i class="fas fa-random"></i> 랜덤 풀기
                </button>
                <button class="dash-btn accent" onclick="showRangeModal()">
                    <i class="fas fa-sliders-h"></i> 범위 설정
                </button>
                <button class="dash-btn special" onclick="loadQuestions('wrong')">
                    <i class="fas fa-times-circle"></i> 오답 노트
                </button>
                ${stats.marked > 0 ? `
                <button class="dash-btn marked" onclick="loadQuestions('marked')">
                    <i class="fas fa-star"></i> 체크 문제 (${stats.marked})
                </button>
                ` : ''}
            </div>
        </div>
    `;
}

// 코드-제어문 통계 가져오기
function getCodeControlStats() {
    const wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    const correctQuestions = JSON.parse(localStorage.getItem('correctQuestions') || '[]');
    const markedQuestions = JSON.parse(localStorage.getItem('markedQuestions') || '[]');
    
    const total = wrongQuestions.length + correctQuestions.length;
    const accuracy = total > 0 ? Math.round((correctQuestions.length / total) * 100) : 0;
    
    return {
        completed: total,
        accuracy: accuracy,
        marked: markedQuestions.length
    };
}

