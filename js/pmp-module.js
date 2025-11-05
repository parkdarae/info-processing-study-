// PMP 문제집 학습 모듈
class PMPModule {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
        this.isFlipped = false;
        this.studyMode = 'card'; // card, quiz
        this.currentLabel = 'all';
        this.studyData = this.loadStudyData();
        this.spacedRepetition = new PMPSpacedRepetition();
    }

    // 학습 데이터 로드
    loadStudyData() {
        const saved = localStorage.getItem('pmp_study_data');
        if (saved) {
            return JSON.parse(saved);
        }
        return {
            completedItems: [],
            reviewSchedule: {},
            studyTime: {},
            streak: 0,
            lastStudyDate: null,
            bookmarkedItems: []
        };
    }

    // 학습 데이터 저장
    saveStudyData() {
        localStorage.setItem('pmp_study_data', JSON.stringify(this.studyData));
    }

    // 북마크 관리
    toggleBookmark(itemId) {
        const index = this.studyData.bookmarkedItems.indexOf(itemId);
        if (index === -1) {
            this.studyData.bookmarkedItems.push(itemId);
        } else {
            this.studyData.bookmarkedItems.splice(index, 1);
        }
        this.saveStudyData();
        return this.studyData.bookmarkedItems.includes(itemId);
    }

    // 북마크 상태 확인
    isBookmarked(itemId) {
        return this.studyData.bookmarkedItems.includes(itemId);
    }

    // 데이터 로드
    async loadItems() {
        try {
            const response = await fetch('data/items_pmp.jsonl');
            const text = await response.text();
            
            this.items = text.trim().split('\n').map(line => {
                const item = JSON.parse(line);
                item.studyState = this.getItemStudyState(item.id);
                return item;
            });
            
            console.log(`PMP ${this.items.length}개 문제 로드 완료`);
            return this.items;
        } catch (error) {
            console.error('PMP 데이터 로드 실패:', error);
            return [];
        }
    }

    // 항목별 학습 상태 조회
    getItemStudyState(itemId) {
        return this.studyData.studyTime[itemId] || {
            attempts: 0,
            correct: 0,
            lastReview: null,
            nextReview: null,
            difficulty: 1,
            interval: 1
        };
    }

    // 라벨별 필터링
    filterByLabel(label = 'all') {
        this.currentLabel = label;
        if (label === 'all') {
            return this.items;
        }
        return this.items.filter(item => item.labels.includes(label));
    }

    // 체크한 문제만 필터링
    filterBookmarkedItems() {
        return this.items.filter(item => this.isBookmarked(item.id));
    }

    // 카드 모드 렌더링
    renderCard(item) {
        const container = document.getElementById('questionContainer');
        const isBookmarked = this.isBookmarked(item.id);
        
        container.innerHTML = `
            <div class="pmp-card-container">
                <div class="pmp-card ${this.isFlipped ? 'flipped' : ''}" onclick="pmpModule.flipCard()">
                    <div class="pmp-card-front">
                        <div class="card-header">
                            <span class="card-number">${this.currentIndex + 1} / ${this.items.length}</span>
                            <div class="card-actions">
                                <button class="bookmark-btn ${isBookmarked ? 'bookmarked' : ''}" 
                                        onclick="pmpModule.toggleBookmark('${item.id}'); event.stopPropagation();">
                                    <i class="fas fa-star"></i>
                                </button>
                            </div>
                        </div>
                        <div class="card-labels">
                            ${item.labels.map(label => `<span class="label label-${label}">${this.getLabelName(label)}</span>`).join('')}
                        </div>
                        <div class="card-content">
                            <div class="question-text">${item.question}</div>
                            <div class="options-list">
                                ${item.options.map(option => `<div class="option-item">${option}</div>`).join('')}
                            </div>
                            <div class="flip-hint">
                                <i class="fas fa-hand-pointer"></i>
                                클릭하여 정답 확인
                            </div>
                        </div>
                    </div>
                    <div class="pmp-card-back">
                        <div class="card-header">
                            <span class="card-number">${this.currentIndex + 1} / ${this.items.length}</span>
                            <div class="card-actions">
                                <button class="bookmark-btn ${isBookmarked ? 'bookmarked' : ''}" 
                                        onclick="pmpModule.toggleBookmark('${item.id}'); event.stopPropagation();">
                                    <i class="fas fa-star"></i>
                                </button>
                            </div>
                        </div>
                        <div class="card-labels">
                            ${item.labels.map(label => `<span class="label label-${label}">${this.getLabelName(label)}</span>`).join('')}
                        </div>
                        <div class="card-content">
                            <div class="answer-section">
                                <div class="correct-answer">
                                    <strong>정답: ${item.answer}</strong>
                                    <p>${item.answer_text}</p>
                                </div>
                                <div class="explanation">
                                    <h4>해설</h4>
                                    <p>${item.explanation}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="pmp-controls">
                    <div class="top-controls">
                        <button class="back-to-dashboard-btn" onclick="pmpModule.renderDashboard()">
                            <i class="fas fa-home"></i> 대시보드로 돌아가기
                        </button>
                    </div>
                    <div class="navigation-controls">
                        <button class="control-btn" onclick="pmpModule.previousItem()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전
                        </button>
                        <button class="control-btn" onclick="pmpModule.nextItem()" ${this.currentIndex === this.items.length - 1 ? 'disabled' : ''}>
                            다음 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                    
                    ${this.isFlipped ? `
                        <div class="self-assessment">
                            <p>이 문제를 얼마나 잘 알고 있나요?</p>
                            <div class="assessment-buttons">
                                <button class="assessment-btn difficulty-hard" onclick="pmpModule.recordAssessment(3)">
                                    <i class="fas fa-times"></i> 모르겠음
                                </button>
                                <button class="assessment-btn difficulty-medium" onclick="pmpModule.recordAssessment(2)">
                                    <i class="fas fa-question"></i> 애매함
                                </button>
                                <button class="assessment-btn difficulty-easy" onclick="pmpModule.recordAssessment(1)">
                                    <i class="fas fa-check"></i> 알았음
                                </button>
                            </div>
                        </div>
                    ` : ''}
                </div>
                
                <div class="study-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${((this.currentIndex + 1) / this.items.length) * 100}%"></div>
                    </div>
                    <div class="progress-text">
                        진도: ${this.currentIndex + 1} / ${this.items.length} 
                        (${Math.round(((this.currentIndex + 1) / this.items.length) * 100)}%)
                    </div>
                </div>
            </div>
        `;
    }

    // 라벨명 변환
    getLabelName(label) {
        const labelMap = {
            'project_integration': '통합관리',
            'project_scope': '범위관리',
            'project_schedule': '일정관리',
            'project_cost': '원가관리',
            'project_quality': '품질관리',
            'project_resource': '자원관리',
            'project_communication': '의사소통',
            'project_risk': '위험관리',
            'project_procurement': '조달관리',
            'project_stakeholder': '이해관계자',
            'initiating': '착수',
            'planning': '기획',
            'executing': '실행',
            'monitoring': '감시통제',
            'closing': '종료'
        };
        return labelMap[label] || label;
    }

    // 카드 뒤집기
    flipCard() {
        this.isFlipped = !this.isFlipped;
        this.renderCard(this.currentItem);
    }

    // 이전 항목
    previousItem() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.currentItem = this.items[this.currentIndex];
            this.isFlipped = false;
            this.renderCard(this.currentItem);
        }
    }

    // 다음 항목
    nextItem() {
        if (this.currentIndex < this.items.length - 1) {
            this.currentIndex++;
            this.currentItem = this.items[this.currentIndex];
            this.isFlipped = false;
            this.renderCard(this.currentItem);
        }
    }

    // 자가평가 기록
    recordAssessment(difficulty) {
        const itemId = this.currentItem.id;
        const now = new Date();
        
        if (!this.studyData.studyTime[itemId]) {
            this.studyData.studyTime[itemId] = {
                attempts: 0,
                correct: 0,
                lastReview: null,
                nextReview: null,
                difficulty: 1,
                interval: 1
            };
        }
        
        const itemData = this.studyData.studyTime[itemId];
        itemData.attempts++;
        itemData.lastReview = now.toISOString();
        itemData.difficulty = difficulty;
        
        const nextInterval = this.spacedRepetition.calculateNextInterval(difficulty, itemData.interval);
        itemData.interval = nextInterval;
        
        const nextReview = new Date(now.getTime() + nextInterval * 24 * 60 * 60 * 1000);
        itemData.nextReview = nextReview.toISOString();
        
        if (difficulty === 1) {
            itemData.correct++;
        }
        
        if (!this.studyData.completedItems.includes(itemId)) {
            this.studyData.completedItems.push(itemId);
        }
        
        this.saveStudyData();
        
        setTimeout(() => {
            this.nextItem();
        }, 1000);
    }

    // 대시보드 렌더링
    renderDashboard() {
        const container = document.getElementById('questionContainer');
        const stats = this.calculateStats();
        
        container.innerHTML = `
            <div class="pmp-dashboard">
                <div class="dashboard-header">
                    <h2><i class="fas fa-project-diagram"></i> PMP 문제집</h2>
                    <p>Project Management Professional 자격증 대비 학습</p>
                    <div class="total-count">
                        <span class="count-number">${stats.total}</span>
                        <span class="count-label">개 문제</span>
                    </div>
                </div>
                
                <div class="study-modes">
                    <div class="mode-selector">
                        <button class="mode-btn active" onclick="pmpModule.setStudyMode('card')">
                            <i class="fas fa-id-card"></i>
                            <span>카드 모드</span>
                        </button>
                        <button class="mode-btn" onclick="pmpModule.setStudyMode('quiz')">
                            <i class="fas fa-list-ul"></i>
                            <span>객관식 모드</span>
                        </button>
                    </div>
                    
                    <div class="filter-options">
                        <button class="filter-btn" onclick="pmpModule.startStudy('all', 'sequential')">
                            <i class="fas fa-play"></i> 전체 순차 학습
                        </button>
                        <button class="filter-btn" onclick="pmpModule.startStudy('all', 'random')">
                            <i class="fas fa-random"></i> 전체 랜덤 학습
                        </button>
                        <button class="filter-btn" onclick="pmpModule.showRangeModal()">
                            <i class="fas fa-sliders-h"></i> 범위 설정
                        </button>
                        <button class="filter-btn" onclick="pmpModule.startBookmarkedStudy()">
                            <i class="fas fa-star"></i> 체크한 문제 (${stats.bookmarked}개)
                        </button>
                    </div>
                </div>
                
                <div class="knowledge-areas">
                    <h3>📚 지식 영역별 학습</h3>
                    <div class="label-grid">
                        ${this.renderKnowledgeAreaCards(stats)}
                    </div>
                </div>
                
                <div class="process-groups">
                    <h3>🔄 프로세스 그룹별 학습</h3>
                    <div class="label-grid">
                        ${this.renderProcessGroupCards(stats)}
                    </div>
                </div>
                
                <div class="study-stats">
                    <h3>📊 학습 통계</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <i class="fas fa-check-circle"></i>
                            <div class="stat-number">${stats.completed}</div>
                            <div class="stat-label">완료한 문제</div>
                        </div>
                        <div class="stat-card">
                            <i class="fas fa-star"></i>
                            <div class="stat-number">${stats.bookmarked}</div>
                            <div class="stat-label">체크한 문제</div>
                        </div>
                        <div class="stat-card">
                            <i class="fas fa-percentage"></i>
                            <div class="stat-number">${stats.accuracy}%</div>
                            <div class="stat-label">정답률</div>
                        </div>
                        <div class="stat-card">
                            <i class="fas fa-fire"></i>
                            <div class="stat-number">${stats.streak}</div>
                            <div class="stat-label">연속 학습일</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // 지식 영역 카드 렌더링
    renderKnowledgeAreaCards(stats) {
        const knowledgeAreas = [
            'project_integration', 'project_scope', 'project_schedule', 'project_cost',
            'project_quality', 'project_resource', 'project_communication', 
            'project_risk', 'project_procurement', 'project_stakeholder'
        ];

        return knowledgeAreas.map(area => {
            const count = stats.byLabel[area] || 0;
            const icon = this.getKnowledgeAreaIcon(area);
            const color = this.getKnowledgeAreaColor(area);
            
            return `
                <button class="label-card" onclick="pmpModule.startStudy('${area}', 'sequential')" 
                        style="border-left-color: ${color}">
                    <div class="label-icon" style="color: ${color}">
                        <i class="${icon}"></i>
                    </div>
                    <div class="label-info">
                        <div class="label-name">${this.getLabelName(area)}</div>
                        <div class="label-count">${count}개 문제</div>
                    </div>
                </button>
            `;
        }).join('');
    }

    // 프로세스 그룹 카드 렌더링
    renderProcessGroupCards(stats) {
        const processGroups = ['initiating', 'planning', 'executing', 'monitoring', 'closing'];

        return processGroups.map(process => {
            const count = stats.byLabel[process] || 0;
            const icon = this.getProcessGroupIcon(process);
            const color = this.getProcessGroupColor(process);
            
            return `
                <button class="label-card" onclick="pmpModule.startStudy('${process}', 'sequential')" 
                        style="border-left-color: ${color}">
                    <div class="label-icon" style="color: ${color}">
                        <i class="${icon}"></i>
                    </div>
                    <div class="label-info">
                        <div class="label-name">${this.getLabelName(process)}</div>
                        <div class="label-count">${count}개 문제</div>
                    </div>
                </button>
            `;
        }).join('');
    }

    // 지식 영역 아이콘
    getKnowledgeAreaIcon(area) {
        const icons = {
            'project_integration': 'fas fa-puzzle-piece',
            'project_scope': 'fas fa-expand-arrows-alt',
            'project_schedule': 'fas fa-calendar-alt',
            'project_cost': 'fas fa-dollar-sign',
            'project_quality': 'fas fa-award',
            'project_resource': 'fas fa-users',
            'project_communication': 'fas fa-comments',
            'project_risk': 'fas fa-exclamation-triangle',
            'project_procurement': 'fas fa-handshake',
            'project_stakeholder': 'fas fa-user-friends'
        };
        return icons[area] || 'fas fa-circle';
    }

    // 지식 영역 색상
    getKnowledgeAreaColor(area) {
        const colors = {
            'project_integration': '#6f42c1',
            'project_scope': '#20c997',
            'project_schedule': '#fd7e14',
            'project_cost': '#28a745',
            'project_quality': '#ffc107',
            'project_resource': '#dc3545',
            'project_communication': '#17a2b8',
            'project_risk': '#e83e8c',
            'project_procurement': '#6610f2',
            'project_stakeholder': '#007bff'
        };
        return colors[area] || '#6c757d';
    }

    // 프로세스 그룹 아이콘
    getProcessGroupIcon(process) {
        const icons = {
            'initiating': 'fas fa-play',
            'planning': 'fas fa-clipboard-list',
            'executing': 'fas fa-cogs',
            'monitoring': 'fas fa-chart-line',
            'closing': 'fas fa-flag-checkered'
        };
        return icons[process] || 'fas fa-circle';
    }

    // 프로세스 그룹 색상
    getProcessGroupColor(process) {
        const colors = {
            'initiating': '#28a745',
            'planning': '#17a2b8',
            'executing': '#ffc107',
            'monitoring': '#fd7e14',
            'closing': '#dc3545'
        };
        return colors[process] || '#6c757d';
    }

    // 학습 시작
    async startStudy(label = 'all', mode = 'sequential') {
        if (this.items.length === 0) {
            await this.loadItems();
        }
        
        let studyItems = this.filterByLabel(label);
        
        if (mode === 'random') {
            studyItems = this.shuffleArray([...studyItems]);
        }
        
        if (studyItems.length === 0) {
            alert('선택한 조건에 해당하는 문제가 없습니다.');
            return;
        }
        
        this.items = studyItems;
        this.currentIndex = 0;
        this.currentItem = this.items[0];
        this.isFlipped = false;
        
        this.renderCard(this.currentItem);
    }

    // 체크한 문제 학습 시작
    startBookmarkedStudy() {
        const bookmarkedItems = this.filterBookmarkedItems();
        
        if (bookmarkedItems.length === 0) {
            alert('체크한 문제가 없습니다.');
            return;
        }
        
        this.items = bookmarkedItems;
        this.currentIndex = 0;
        this.currentItem = this.items[0];
        this.isFlipped = false;
        
        this.renderCard(this.currentItem);
    }

    // 범위 설정 모달 표시
    showRangeModal() {
        // 범위 설정 모달 구현 (기존 시스템과 유사)
        alert('범위 설정 기능은 곧 구현됩니다.');
    }

    // 학습 모드 설정
    setStudyMode(mode) {
        this.studyMode = mode;
        document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
        event.currentTarget.classList.add('active');
    }

    // 배열 셔플
    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    // 통계 계산
    calculateStats() {
        const stats = {
            total: this.items.length,
            completed: this.studyData.completedItems.length,
            bookmarked: this.studyData.bookmarkedItems.length,
            streak: this.studyData.streak,
            accuracy: 0,
            byLabel: {}
        };

        // 라벨별 통계
        this.items.forEach(item => {
            item.labels.forEach(label => {
                stats.byLabel[label] = (stats.byLabel[label] || 0) + 1;
            });
        });

        // 정답률 계산
        let totalAttempts = 0;
        let totalCorrect = 0;

        Object.values(this.studyData.studyTime).forEach(data => {
            totalAttempts += data.attempts;
            totalCorrect += data.correct;
        });

        stats.accuracy = totalAttempts > 0 ? Math.round((totalCorrect / totalAttempts) * 100) : 0;

        return stats;
    }
}

// PMP 간격 반복 학습 클래스
class PMPSpacedRepetition {
    calculateNextInterval(difficulty, currentInterval) {
        const multipliers = {
            1: 2.5, // 알았음
            2: 1.3, // 애매함  
            3: 0.5  // 모르겠음
        };
        
        const multiplier = multipliers[difficulty] || 1;
        let nextInterval = Math.round(currentInterval * multiplier);
        
        return Math.max(1, Math.min(30, nextInterval));
    }
}

// 전역 인스턴스
const pmpModule = new PMPModule();

// 전역 함수들
window.pmpModule = pmpModule;
