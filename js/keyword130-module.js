// 핵심 키워드 130 문제 모듈 - PMP 스타일 적용
class Keyword130Module {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
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
                        <button class="main-mode-card accent" onclick="keyword130Module.showRangeModal()">
                            <div class="mode-icon"><i class="fas fa-sliders-h"></i></div>
                            <div class="mode-title">범위학습</div>
                            <div class="mode-desc">원하는 범위만</div>
                        </button>
                        <button class="main-mode-card bookmarked" onclick="keyword130Module.startBookmarkedStudy()">
                            <div class="mode-icon"><i class="fas fa-star"></i></div>
                            <div class="mode-title">체크문제</div>
                            <div class="mode-desc">${stats.bookmarked}개 문제</div>
                        </button>
                    </div>
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
}

// 전역 인스턴스
const keyword130Module = new Keyword130Module();

// 전역 함수 (HTML에서 호출용)
window.keyword130Module = keyword130Module;

