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
        
        // 실기 최빈출 모듈인 경우 대시보드 표시
        if (moduleName === 'theory_frequent') {
            theoryFrequent.loadItems().then(() => {
                theoryFrequent.renderDashboard();
            });
        }
        // PMP 모듈인 경우 대시보드 표시
        else if (moduleName === 'pmp') {
            pmpModule.loadItems().then(() => {
                pmpModule.renderDashboard();
            });
        }
        // 핵심 키워드 130 모듈인 경우 대시보드 표시
        else if (moduleName === 'keyword130') {
            renderKeyword130Dashboard();
        }
        // 코드-제어문 모듈인 경우 대시보드 표시
        else if (moduleName === 'code_control') {
            renderCodeControlDashboard();
        }
        // 이론 모듈인 경우 객관식/주관식 선택 화면 표시
        else if (moduleName === 'theory') {
            document.getElementById('questionContainer').innerHTML = `
                <div class="question-card">
                    <div style="text-align: center; padding: 50px;">
                        <i class="fas fa-lightbulb" style="font-size: 4em; color: #667eea; margin-bottom: 20px;"></i>
                        <h2>🎯 정처기 실기 이론 학습</h2>
                        <p style="color: #6c757d; margin: 20px 0;">문제 유형을 선택해주세요</p>
                        <div style="display: flex; gap: 20px; justify-content: center; margin-top: 30px;">
                            <button class="mode-btn" onclick="startTheoryMode('objective')" style="flex: 1; max-width: 300px; padding: 30px; font-size: 1.2em;">
                                <i class="fas fa-list-ul" style="font-size: 2em; margin-bottom: 10px;"></i><br>
                                <strong>객관식</strong><br>
                                <small style="opacity: 0.7;">4지선다 문제</small>
                            </button>
                            <button class="mode-btn" onclick="startTheoryMode('subjective')" style="flex: 1; max-width: 300px; padding: 30px; font-size: 1.2em;">
                                <i class="fas fa-keyboard" style="font-size: 2em; margin-bottom: 10px;"></i><br>
                                <strong>주관식</strong><br>
                                <small style="opacity: 0.7;">직접 입력</small>
                            </button>
                        </div>
                        <p style="color: #666; margin-top: 30px; font-size: 0.9em;">
                            💡 선택 후 기존과 동일한 모든 기능 사용 가능:<br>
                            순차/랜덤/범위설정/오답만풀기/체크한문제/정답확인/답보기/해설보기
                        </p>
                    </div>
                </div>
            `;
        } else {
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
        <div class="theory-category-dashboard">
            <div class="dashboard-header-compact">
                <h2><i class="fas fa-graduation-cap"></i> 핵심 키워드 130 문제</h2>
                <div class="total-count">
                    <span class="count-number">130</span>
                    <span class="count-label">개 문제</span>
                </div>
            </div>
            
            <div class="stats-mini-cards">
                <div class="mini-card">
                    <i class="fas fa-check-circle"></i>
                    <div class="mini-content">
                        <div class="mini-value">${stats.completed}</div>
                        <div class="mini-label">완료</div>
                    </div>
                </div>
                <div class="mini-card">
                    <i class="fas fa-percentage"></i>
                    <div class="mini-content">
                        <div class="mini-value">${stats.accuracy}%</div>
                        <div class="mini-label">정답률</div>
                    </div>
                </div>
                <div class="mini-card">
                    <i class="fas fa-star"></i>
                    <div class="mini-content">
                        <div class="mini-value">${stats.marked}</div>
                        <div class="mini-label">체크</div>
                    </div>
                </div>
            </div>
            
            <div class="main-actions">
                <button class="main-action-card primary" onclick="loadQuestions('sequential')">
                    <div class="action-icon"><i class="fas fa-play-circle"></i></div>
                    <div class="action-content">
                        <div class="action-title">순차 학습</div>
                        <div class="action-desc">1번부터 순서대로</div>
                    </div>
                </button>
                <button class="main-action-card secondary" onclick="loadQuestions('random')">
                    <div class="action-icon"><i class="fas fa-random"></i></div>
                    <div class="action-content">
                        <div class="action-title">랜덤 학습</div>
                        <div class="action-desc">문제를 섞어서</div>
                    </div>
                </button>
                <button class="main-action-card accent" onclick="showRangeModal()">
                    <div class="action-icon"><i class="fas fa-sliders-h"></i></div>
                    <div class="action-content">
                        <div class="action-title">범위 학습</div>
                        <div class="action-desc">원하는 범위만</div>
                    </div>
                </button>
                <button class="main-action-card special" onclick="loadQuestions('wrong')">
                    <div class="action-icon"><i class="fas fa-exclamation-circle"></i></div>
                    <div class="action-content">
                        <div class="action-title">오답 노트</div>
                        <div class="action-desc">틀린 문제만</div>
                    </div>
                </button>
            </div>
            
            <div class="category-section-compact">
                <button class="section-toggle" onclick="toggleKeyword130Section()">
                    <span><i class="fas fa-check"></i> 체크한 문제</span>
                    <i class="fas fa-chevron-down toggle-icon"></i>
                </button>
                <div id="keyword130-section" class="section-content" style="display: none;">
                    <div style="text-align: center; padding: 20px;">
                        <button class="main-action-card special" onclick="loadQuestions('marked')" style="max-width: 400px; margin: 0 auto;">
                            <div class="action-icon"><i class="fas fa-star"></i></div>
                            <div class="action-content">
                                <div class="action-title">체크한 ${stats.marked}개 문제 풀기</div>
                                <div class="action-desc">나중에 다시 풀어볼 문제</div>
                            </div>
                        </button>
                    </div>
                </div>
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

// 키워드 130 섹션 토글
function toggleKeyword130Section() {
    const section = document.getElementById('keyword130-section');
    const toggle = event.target.closest('.section-toggle');
    const icon = toggle.querySelector('.toggle-icon');
    
    if (section.style.display === 'none') {
        section.style.display = 'block';
        icon.style.transform = 'rotate(180deg)';
    } else {
        section.style.display = 'none';
        icon.style.transform = 'rotate(0deg)';
    }
}

// 코드-제어문 14문제 대시보드 렌더링
function renderCodeControlDashboard() {
    const container = document.getElementById('questionContainer');
    const stats = getCodeControlStats();
    
    container.innerHTML = `
        <div class="theory-category-dashboard">
            <div class="dashboard-header-compact">
                <h2><i class="fas fa-code"></i> 코드-제어문 14 문제</h2>
                <div class="total-count">
                    <span class="count-number">14</span>
                    <span class="count-label">개 문제</span>
                </div>
            </div>
            
            <div class="stats-mini-cards">
                <div class="mini-card">
                    <i class="fas fa-check-circle"></i>
                    <div class="mini-content">
                        <div class="mini-value">${stats.completed}</div>
                        <div class="mini-label">완료</div>
                    </div>
                </div>
                <div class="mini-card">
                    <i class="fas fa-percentage"></i>
                    <div class="mini-content">
                        <div class="mini-value">${stats.accuracy}%</div>
                        <div class="mini-label">정답률</div>
                    </div>
                </div>
                <div class="mini-card">
                    <i class="fas fa-star"></i>
                    <div class="mini-content">
                        <div class="mini-value">${stats.marked}</div>
                        <div class="mini-label">체크</div>
                    </div>
                </div>
            </div>
            
            <div class="main-actions">
                <button class="main-action-card primary" onclick="loadQuestions('sequential')">
                    <div class="action-icon"><i class="fas fa-play-circle"></i></div>
                    <div class="action-content">
                        <div class="action-title">순차 학습</div>
                        <div class="action-desc">1번부터 순서대로</div>
                    </div>
                </button>
                <button class="main-action-card secondary" onclick="loadQuestions('random')">
                    <div class="action-icon"><i class="fas fa-random"></i></div>
                    <div class="action-content">
                        <div class="action-title">랜덤 학습</div>
                        <div class="action-desc">문제를 섞어서</div>
                    </div>
                </button>
                <button class="main-action-card accent" onclick="showRangeModal()">
                    <div class="action-icon"><i class="fas fa-sliders-h"></i></div>
                    <div class="action-content">
                        <div class="action-title">범위 학습</div>
                        <div class="action-desc">원하는 범위만</div>
                    </div>
                </button>
                <button class="main-action-card special" onclick="loadQuestions('wrong')">
                    <div class="action-icon"><i class="fas fa-exclamation-circle"></i></div>
                    <div class="action-content">
                        <div class="action-title">오답 노트</div>
                        <div class="action-desc">틀린 문제만</div>
                    </div>
                </button>
            </div>
            
            <div class="category-section-compact">
                <button class="section-toggle" onclick="toggleCodeControlSection()">
                    <span><i class="fas fa-check"></i> 체크한 문제</span>
                    <i class="fas fa-chevron-down toggle-icon"></i>
                </button>
                <div id="codecontrol-section" class="section-content" style="display: none;">
                    <div style="text-align: center; padding: 20px;">
                        <button class="main-action-card special" onclick="loadQuestions('marked')" style="max-width: 400px; margin: 0 auto;">
                            <div class="action-icon"><i class="fas fa-star"></i></div>
                            <div class="action-content">
                                <div class="action-title">체크한 ${stats.marked}개 문제 풀기</div>
                                <div class="action-desc">나중에 다시 풀어볼 문제</div>
                            </div>
                        </button>
                    </div>
                </div>
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

// 코드-제어문 섹션 토글
function toggleCodeControlSection() {
    const section = document.getElementById('codecontrol-section');
    const toggle = event.target.closest('.section-toggle');
    const icon = toggle.querySelector('.toggle-icon');
    
    if (section.style.display === 'none') {
        section.style.display = 'block';
        icon.style.transform = 'rotate(180deg)';
    } else {
        section.style.display = 'none';
        icon.style.transform = 'rotate(0deg)';
    }
}

