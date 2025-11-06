// 핵심 키워드 130 문제 모듈 - PMP 스타일 적용
class Keyword130Module {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
        this.cardStep = 1; // 카드 학습 단계 (1: 문제, 2: 답, 3: 다음)
        this.studyData = this.loadStudyData();
        this.bookmarkedItems = this.loadBookmarkedItems();
    }

    // 학습 데이터 로드
    loadStudyData() {
        const saved = localStorage.getItem('keyword130_study_data');
        if (saved) {
            return JSON.parse(saved);
        }
        return {
            completedItems: [],
            stats: {
                total: 0,
                correct: 0,
                wrong: 0
            },
            streak: 0,
            lastStudyDate: null
        };
    }

    // 학습 데이터 저장
    saveStudyData() {
        localStorage.setItem('keyword130_study_data', JSON.stringify(this.studyData));
    }

    // 북마크 데이터 로드
    loadBookmarkedItems() {
        const saved = localStorage.getItem('keyword130_bookmarks');
        return saved ? JSON.parse(saved) : [];
    }

    // 북마크 데이터 저장
    saveBookmarkedItems() {
        localStorage.setItem('keyword130_bookmarks', JSON.stringify(this.bookmarkedItems));
    }

    // 문제 북마크 토글
    toggleBookmark(itemId) {
        const index = this.bookmarkedItems.indexOf(itemId);
        if (index > -1) {
            this.bookmarkedItems.splice(index, 1);
        } else {
            this.bookmarkedItems.push(itemId);
        }
        this.saveBookmarkedItems();
        this.updateBookmarkButtonStyle(itemId);
    }

    // 북마크 버튼 스타일 업데이트
    updateBookmarkButtonStyle(itemId) {
        const btn = document.getElementById('keyword130BookmarkBtn');
        if (btn) {
            if (this.bookmarkedItems.includes(itemId)) {
                btn.style.background = '#ffc107';
                btn.style.color = 'white';
                btn.innerHTML = '<i class="fas fa-star"></i> 체크됨';
            } else {
                btn.style.background = '#f8f9fa';
                btn.style.color = '#495057';
                btn.innerHTML = '<i class="far fa-star"></i> 체크';
            }
        }
    }

    // 데이터 로드
    async loadItems() {
        try {
            const config = App.moduleConfig['keyword130'];
            const response = await fetch(config.itemsFile);
            const text = await response.text();
            this.items = text.trim().split('\n').map(line => JSON.parse(line));
            console.log('✅ Keyword130 데이터 로드 완료:', this.items.length);
        } catch (error) {
            console.error('❌ Keyword130 데이터 로드 실패:', error);
        }
    }

    // 통계 계산
    calculateStats() {
        const total = this.items.length;
        const completed = this.studyData.completedItems.length;
        const bookmarked = this.bookmarkedItems.length;
        const totalAttempts = this.studyData.stats.total;
        const accuracy = totalAttempts > 0 
            ? Math.round((this.studyData.stats.correct / totalAttempts) * 100) 
            : 0;
        const streak = this.studyData.streak || 0;

        return { total, completed, bookmarked, accuracy, streak };
    }

    // 대시보드 렌더링
    renderDashboard() {
        const container = document.getElementById('questionContainer');
        const stats = this.calculateStats();
        
        container.innerHTML = `
            <div class="module-dashboard">
                <div class="dashboard-header-compact">
                    <h2><i class="fas fa-key"></i> 핵심 키워드 130 문제</h2>
                    <div class="total-count">
                        <span class="count-number">${stats.total}</span>
                        <span class="count-label">개 문제</span>
                    </div>
                </div>
                
                <!-- 학습 통계 -->
                <div class="study-stats-top">
                    <div class="stats-grid-horizontal">
                        <div class="stat-card-mini">
                            <i class="fas fa-check-circle" style="color: #28a745;"></i>
                            <div class="stat-content">
                                <div class="stat-number">${stats.completed}</div>
                                <div class="stat-label">완료</div>
                            </div>
                        </div>
                        <div class="stat-card-mini">
                            <i class="fas fa-star" style="color: #ffc107;"></i>
                            <div class="stat-content">
                                <div class="stat-number">${stats.bookmarked}</div>
                                <div class="stat-label">체크</div>
                            </div>
                        </div>
                        <div class="stat-card-mini">
                            <i class="fas fa-percentage" style="color: #17a2b8;"></i>
                            <div class="stat-content">
                                <div class="stat-number">${stats.accuracy}%</div>
                                <div class="stat-label">정답률</div>
                            </div>
                        </div>
                        <div class="stat-card-mini">
                            <i class="fas fa-fire" style="color: #fd7e14;"></i>
                            <div class="stat-content">
                                <div class="stat-number">${stats.streak}</div>
                                <div class="stat-label">연속일</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 주요 학습 모드 -->
                <div class="main-study-modes">
                    <h3 class="section-title"><i class="fas fa-graduation-cap"></i> 학습 시작하기</h3>
                    <div class="main-mode-grid">
                        <button class="main-mode-card primary" onclick="keyword130Module.startStudy('sequential')">
                            <div class="mode-icon"><i class="fas fa-play-circle"></i></div>
                            <div class="mode-title">순차학습</div>
                            <div class="mode-desc">처음부터 순서대로</div>
                        </button>
                        <button class="main-mode-card secondary" onclick="keyword130Module.startStudy('random')">
                            <div class="mode-icon"><i class="fas fa-random"></i></div>
                            <div class="mode-title">랜덤학습</div>
                            <div class="mode-desc">무작위로 섞어서</div>
                        </button>
                        <button class="main-mode-card accent" onclick="keyword130Module.startCardStudy()">
                            <div class="mode-icon"><i class="fas fa-layer-group"></i></div>
                            <div class="mode-title">카드학습</div>
                            <div class="mode-desc">플립 카드 방식</div>
                        </button>
                        <button class="main-mode-card bookmarked" onclick="keyword130Module.startBookmarkedStudy()">
                            <div class="mode-icon"><i class="fas fa-star"></i></div>
                            <div class="mode-title">체크문제</div>
                            <div class="mode-desc">${stats.bookmarked}개 문제</div>
                        </button>
                    </div>
                </div>
                
                <!-- 범위학습 섹션 -->
                <div class="range-study-section">
                    <button class="range-study-btn" onclick="keyword130Module.showRangeModal()">
                        <i class="fas fa-sliders-h"></i> 범위를 지정해서 학습하기
                    </button>
                </div>
            </div>
        `;
    }

    // 범위 모달 표시
    showRangeModal() {
        // 기존 범위 모달 사용
        App.state.currentModule = 'keyword130';
        currentModule = 'keyword130';
        showRangeModal();
    }

    // 학습 시작
    async startStudy(mode) {
        if (this.items.length === 0) {
            await this.loadItems();
        }

        App.state.currentModule = 'keyword130';
        currentModule = 'keyword130';
        
        // 기존 시스템 사용
        App.state.allQuestions = this.items;
        allQuestions = this.items;
        App.state.currentMode = mode;
        currentMode = mode;

        if (mode === 'random') {
            startRandomMode();
        } else {
            startSequentialMode();
        }
    }

    // 체크한 문제만 풀기
    async startBookmarkedStudy() {
        if (this.bookmarkedItems.length === 0) {
            alert('체크한 문제가 없습니다.');
            return;
        }

        if (this.items.length === 0) {
            await this.loadItems();
        }

        const bookmarkedQuestions = this.items.filter(item => 
            this.bookmarkedItems.includes(item.q_no)
        );

        App.state.currentModule = 'keyword130';
        currentModule = 'keyword130';
        App.state.allQuestions = bookmarkedQuestions;
        allQuestions = bookmarkedQuestions;
        App.state.currentMode = 'bookmarked';
        currentMode = 'bookmarked';

        startSequentialMode();
    }

    // 카드 학습 시작
    async startCardStudy() {
        if (this.items.length === 0) {
            await this.loadItems();
        }

        this.currentIndex = 0;
        this.currentItem = this.items[0];
        this.cardStep = 1;
        this.renderCardMode(this.currentItem);
    }

    // 카드 모드 렌더링
    renderCardMode(item) {
        const container = document.getElementById('questionContainer');
        const isBookmarked = this.bookmarkedItems.includes(item.q_no);
        
        let cardContent = '';
        
        // 단계별 콘텐츠
        if (this.cardStep === 1) {
            // 1단계: 문제만
            cardContent = `
                <div class="card-question">
                    <h3>문제</h3>
                    <p>${item.question_text}</p>
                </div>
            `;
        } else if (this.cardStep === 2) {
            // 2단계: 답
            const answerText = item.answer?.raw_text || item.answer?.keys?.[0] || '답안 없음';
            cardContent = `
                <div class="card-question dimmed">
                    <p>${item.question_text}</p>
                </div>
                <div class="card-answer">
                    <h3>정답</h3>
                    <p>${answerText}</p>
                </div>
            `;
        }
        
        container.innerHTML = `
            <div class="question-card card-mode" onclick="keyword130Module.nextCardStep()">
                <div class="question-header">
                    <div class="question-no">${item.q_no}</div>
                    <div class="card-step-indicator">${this.cardStep}/2</div>
                    <button class="btn btn-secondary" onclick="event.stopPropagation(); keyword130Module.toggleBookmark('${item.q_no}')">
                        <i class="fas fa-star"></i> ${isBookmarked ? '✓' : '☆'}
                    </button>
                </div>
                
                <div class="card-content">
                    ${cardContent}
                </div>
                
                <div class="action-buttons">
                    <div class="main-controls">
                        <button class="btn btn-primary" onclick="event.stopPropagation(); keyword130Module.nextCardStep()">
                            <i class="fas fa-arrow-right"></i> ${this.cardStep === 2 ? '다음문제' : '답보기'}
                        </button>
                        <button class="btn" onclick="event.stopPropagation(); keyword130Module.jumpToCardStep(2)" style="background: #17a2b8; color: white;">
                            <i class="fas fa-eye"></i> 답
                        </button>
                    </div>
                    <div class="navigation-controls">
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); keyword130Module.previousCardItem()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); keyword130Module.renderDashboard()">
                            <i class="fas fa-home"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); keyword130Module.nextCardItem()" ${this.currentIndex === this.items.length - 1 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
                
                <div class="progress-indicator">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${((this.currentIndex + 1) / this.items.length) * 100}%"></div>
                    </div>
                    <div class="progress-text">${this.currentIndex + 1} / ${this.items.length}</div>
                </div>
            </div>
        `;
    }

    // 다음 카드 단계
    nextCardStep() {
        if (this.cardStep === 1) {
            this.cardStep = 2;
            this.renderCardMode(this.currentItem);
        } else {
            // 다음 문제로
            this.nextCardItem();
        }
    }

    // 특정 카드 단계로 이동
    jumpToCardStep(step) {
        this.cardStep = step;
        this.renderCardMode(this.currentItem);
    }

    // 이전 카드 항목
    previousCardItem() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.currentItem = this.items[this.currentIndex];
            this.cardStep = 1;
            this.renderCardMode(this.currentItem);
        }
    }

    // 다음 카드 항목
    nextCardItem() {
        if (this.currentIndex < this.items.length - 1) {
            this.currentIndex++;
            this.currentItem = this.items[this.currentIndex];
            this.cardStep = 1;
            this.renderCardMode(this.currentItem);
        } else {
            alert('학습을 완료했습니다! 🎉');
            this.renderDashboard();
        }
    }
}

// 전역 인스턴스
const keyword130Module = new Keyword130Module();

// 전역 함수 (HTML에서 호출용)
window.keyword130Module = keyword130Module;

