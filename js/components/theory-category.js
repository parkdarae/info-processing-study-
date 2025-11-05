// 정처기 실기 이론 - 카테고리별 학습 컴포넌트

// 카테고리 대시보드 렌더링
function renderTheoryCategoryDashboard() {
    console.log('🎨 카테고리 대시보드 렌더링');
    
    const container = document.getElementById('questionContainer');
    
    // 통계 정보 가져오기
    const totalCount = App.theory.categoryStats?.totalCount || 0;
    const categoryStats = App.theory.categoryStats?.stats || {};
    
    container.innerHTML = `
        <div class="theory-category-dashboard">
            <div class="dashboard-header">
                <h2><i class="fas fa-graduation-cap"></i> 정처기 실기 이론</h2>
                <p>카테고리별로 체계적인 학습을 시작하세요</p>
                <div class="total-count">
                    <span class="count-number">${totalCount}</span>
                    <span class="count-label">개 문제</span>
                </div>
            </div>
            
            <div class="study-mode-selector">
                <h3>📚 학습 모드 선택</h3>
                <div class="mode-buttons">
                    <button class="mode-btn active" onclick="setTheoryStudyMode('sequential')">
                        <i class="fas fa-list-ol"></i>
                        <span>순차 풀기</span>
                    </button>
                    <button class="mode-btn" onclick="setTheoryStudyMode('random')">
                        <i class="fas fa-random"></i>
                        <span>랜덤 풀기</span>
                    </button>
                    <button class="mode-btn" onclick="setTheoryStudyMode('range')">
                        <i class="fas fa-sliders-h"></i>
                        <span>범위 설정</span>
                    </button>
                </div>
            </div>
            
            <div class="category-grid-section">
                <div class="section-header">
                    <h3>🏷️ 카테고리별 학습</h3>
                    <button class="all-study-btn" onclick="startCategoryStudy('all', getTheoryStudyMode())">
                        <i class="fas fa-play"></i>
                        전체 학습 시작 (${totalCount}개)
                    </button>
                </div>
                
                <div class="category-grid">
                    ${renderCategoryCards(categoryStats)}
                </div>
            </div>
            
            <div class="study-progress-section">
                <h3>📊 학습 현황</h3>
                <div class="progress-overview">
                    <div class="progress-item">
                        <div class="progress-icon">
                            <i class="fas fa-check-circle"></i>
                        </div>
                        <div class="progress-info">
                            <div class="progress-value" id="completedCount">0</div>
                            <div class="progress-label">완료한 문제</div>
                        </div>
                    </div>
                    <div class="progress-item">
                        <div class="progress-icon">
                            <i class="fas fa-percentage"></i>
                        </div>
                        <div class="progress-info">
                            <div class="progress-value" id="accuracyRate">0%</div>
                            <div class="progress-label">정답률</div>
                        </div>
                    </div>
                    <div class="progress-item">
                        <div class="progress-icon">
                            <i class="fas fa-clock"></i>
                        </div>
                        <div class="progress-info">
                            <div class="progress-value" id="studyTime">0분</div>
                            <div class="progress-label">학습 시간</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 학습 현황 업데이트
    updateTheoryProgress();
}

// 카테고리 카드 렌더링
function renderCategoryCards(categoryStats) {
    const sortedCategories = Object.entries(THEORY_CATEGORY_CONFIG)
        .sort((a, b) => b[1].count - a[1].count)
        .filter(([category, config]) => config.count > 0);
    
    return sortedCategories.map(([category, config]) => {
        const count = config.count;
        const percentage = App.theory.categoryStats?.totalCount > 0 
            ? Math.round((count / App.theory.categoryStats.totalCount) * 100) 
            : 0;
        
        return `
            <div class="category-card" onclick="startCategoryStudy('${category}', getTheoryStudyMode())" 
                 style="border-left-color: ${config.color}">
                <div class="category-header">
                    <div class="category-icon" style="color: ${config.color}">
                        <i class="${config.icon}"></i>
                    </div>
                    <div class="category-info">
                        <div class="category-name">${config.name}</div>
                        <div class="category-count">${count}개 문제</div>
                    </div>
                </div>
                <div class="category-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${percentage}%; background: ${config.color}"></div>
                    </div>
                    <div class="progress-text">${percentage}%</div>
                </div>
                <div class="category-action">
                    <i class="fas fa-play"></i>
                    학습 시작
                </div>
            </div>
        `;
    }).join('');
}

// 현재 학습 모드 가져오기
function getTheoryStudyMode() {
    const activeBtn = document.querySelector('.mode-btn.active');
    return activeBtn ? activeBtn.onclick.toString().match(/'([^']+)'/)[1] : 'sequential';
}

// 학습 모드 설정
function setTheoryStudyMode(mode) {
    console.log(`🎯 학습 모드 변경: ${mode}`);
    
    // 버튼 활성화 상태 업데이트
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    event.currentTarget.classList.add('active');
    
    // 전체 학습 버튼 텍스트 업데이트
    const allStudyBtn = document.querySelector('.all-study-btn');
    if (allStudyBtn) {
        const totalCount = App.theory.categoryStats?.totalCount || 0;
        const modeText = {
            'sequential': '순차',
            'random': '랜덤',
            'range': '범위'
        };
        
        allStudyBtn.innerHTML = `
            <i class="fas fa-play"></i>
            전체 ${modeText[mode]} 학습 (${totalCount}개)
        `;
    }
}

// 이론 학습 진도 업데이트
function updateTheoryProgress() {
    const savedProgress = JSON.parse(localStorage.getItem('theory_progress') || '{}');
    const savedStats = JSON.parse(localStorage.getItem('theory_stats') || '{"correct": 0, "wrong": 0, "total": 0}');
    
    // 완료한 문제 수
    const completedCount = Object.keys(savedProgress).length;
    const completedElement = document.getElementById('completedCount');
    if (completedElement) {
        completedElement.textContent = completedCount;
    }
    
    // 정답률
    const totalAttempts = savedStats.correct + savedStats.wrong;
    const accuracy = totalAttempts > 0 ? Math.round((savedStats.correct / totalAttempts) * 100) : 0;
    const accuracyElement = document.getElementById('accuracyRate');
    if (accuracyElement) {
        accuracyElement.textContent = `${accuracy}%`;
    }
    
    // 학습 시간 (추정치)
    const studyTime = Math.round(completedCount * 0.5); // 문제당 평균 30초 추정
    const studyTimeElement = document.getElementById('studyTime');
    if (studyTimeElement) {
        studyTimeElement.textContent = `${studyTime}분`;
    }
}

// 범위 설정 모달 표시
function showTheoryRangeModal(questionsData, category) {
    const totalCount = questionsData.length;
    const categoryName = THEORY_CATEGORY_CONFIG[category]?.name || category;
    
    const modal = document.createElement('div');
    modal.className = 'theory-range-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeTheoryRangeModal()"></div>
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-sliders-h"></i> 범위 설정</h3>
                <button class="close-btn" onclick="closeTheoryRangeModal()">×</button>
            </div>
            <div class="modal-body">
                <p><strong>${categoryName}</strong> 카테고리에서 학습할 범위를 설정하세요.</p>
                <div class="range-inputs">
                    <div class="input-group">
                        <label for="theoryRangeStart">시작 문제</label>
                        <input type="number" id="theoryRangeStart" min="1" max="${totalCount}" value="1">
                    </div>
                    <div class="range-separator">~</div>
                    <div class="input-group">
                        <label for="theoryRangeEnd">끝 문제</label>
                        <input type="number" id="theoryRangeEnd" min="1" max="${totalCount}" value="${totalCount}">
                    </div>
                </div>
                <div class="range-info">
                    전체 <strong>${totalCount}개</strong> 문제 중 
                    <span id="selectedCount">${totalCount}개</span> 선택됨
                </div>
            </div>
            <div class="modal-footer">
                <button class="modal-btn secondary" onclick="closeTheoryRangeModal()">취소</button>
                <button class="modal-btn primary" onclick="applyTheoryRange('${category}')">학습 시작</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 범위 변경 이벤트 리스너
    const startInput = document.getElementById('theoryRangeStart');
    const endInput = document.getElementById('theoryRangeEnd');
    const selectedCountSpan = document.getElementById('selectedCount');
    
    function updateSelectedCount() {
        const start = parseInt(startInput.value) || 1;
        const end = parseInt(endInput.value) || totalCount;
        const count = Math.max(0, end - start + 1);
        selectedCountSpan.textContent = `${count}개`;
    }
    
    startInput.addEventListener('input', updateSelectedCount);
    endInput.addEventListener('input', updateSelectedCount);
}

// 범위 설정 모달 닫기
function closeTheoryRangeModal() {
    const modal = document.querySelector('.theory-range-modal');
    if (modal) {
        modal.remove();
    }
}

// 범위 적용 및 학습 시작
function applyTheoryRange(category) {
    const startInput = document.getElementById('theoryRangeStart');
    const endInput = document.getElementById('theoryRangeEnd');
    
    const start = parseInt(startInput.value) || 1;
    const end = parseInt(endInput.value) || 1;
    
    if (start > end) {
        alert('시작 문제 번호가 끝 문제 번호보다 클 수 없습니다.');
        return;
    }
    
    closeTheoryRangeModal();
    
    // 범위별 필터링 및 학습 시작
    const filteredData = filterQuestionsByCategory(App.theory.allTheoryData, category);
    const rangedData = filterQuestionsByRange(filteredData, start - 1, end - 1);
    
    startTheoryQuestions(rangedData);
}

// 전역 함수로 노출 (HTML에서 호출용)
window.renderTheoryCategoryDashboard = renderTheoryCategoryDashboard;
window.setTheoryStudyMode = setTheoryStudyMode;
window.showTheoryRangeModal = showTheoryRangeModal;
window.closeTheoryRangeModal = closeTheoryRangeModal;
window.applyTheoryRange = applyTheoryRange;
