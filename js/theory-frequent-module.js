// 실기 최빈출 50개 학습 모듈
class TheoryFrequentModule {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
        this.isFlipped = false;
        this.studyMode = 'flashcard'; // flashcard, quiz, fill-blank
        this.currentLabel = 'all'; // all, database, os, network, security, etc.
        this.studyData = this.loadStudyData();
        this.spacedRepetition = new SpacedRepetitionManager();
        this.bookmarkedItems = this.loadBookmarkedItems();
    }

    // 학습 데이터 로드
    loadStudyData() {
        const saved = localStorage.getItem('theory_frequent_study_data');
        if (saved) {
            return JSON.parse(saved);
        }
        return {
            completedItems: [],
            reviewSchedule: {},
            studyTime: {},
            streak: 0,
            lastStudyDate: null
        };
    }

    // 학습 데이터 저장
    saveStudyData() {
        localStorage.setItem('theory_frequent_study_data', JSON.stringify(this.studyData));
    }

    // 북마크 데이터 로드
    loadBookmarkedItems() {
        const saved = localStorage.getItem('theory_frequent_bookmarks');
        return saved ? JSON.parse(saved) : [];
    }

    // 북마크 데이터 저장
    saveBookmarkedItems() {
        localStorage.setItem('theory_frequent_bookmarks', JSON.stringify(this.bookmarkedItems));
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
        return this.bookmarkedItems.includes(itemId);
    }

    // 체크한 문제들 복사
    copyBookmarkedItems() {
        if (this.bookmarkedItems.length === 0) {
            alert('체크한 문제가 없습니다.');
            return;
        }

        const bookmarkedQuestions = this.items.filter(item => 
            this.bookmarkedItems.includes(item.id)
        );

        let copyText = `📚 실기 최빈출 - 체크한 문제 목록 (${bookmarkedQuestions.length}개)\n`;
        copyText += `생성일: ${new Date().toLocaleDateString()}\n\n`;

        bookmarkedQuestions.forEach((item, index) => {
            copyText += `${index + 1}. ${item.title}\n`;
            copyText += `Q: ${item.question}\n`;
            copyText += `A: ${item.content.replace(/\n/g, ' ')}\n`;
            copyText += `라벨: ${item.labels.map(label => this.getLabelName(label)).join(', ')}\n\n`;
        });

        // 클립보드에 복사
        navigator.clipboard.writeText(copyText).then(() => {
            alert(`체크한 ${bookmarkedQuestions.length}개 문제가 클립보드에 복사되었습니다!`);
        }).catch(() => {
            // 클립보드 API가 지원되지 않는 경우 텍스트 영역 사용
            const textArea = document.createElement('textarea');
            textArea.value = copyText;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert(`체크한 ${bookmarkedQuestions.length}개 문제가 클립보드에 복사되었습니다!`);
        });
    }

    // 데이터 로드
    async loadItems() {
        try {
            const response = await fetch('data/items_theory_frequent.jsonl');
            const text = await response.text();
            
            this.items = text.trim().split('\n').map(line => {
                const item = JSON.parse(line);
                // 학습 상태 추가
                item.studyState = this.getItemStudyState(item.id);
                return item;
            });
            
            console.log(`실기 최빈출 ${this.items.length}개 항목 로드 완료`);
            return this.items;
        } catch (error) {
            console.error('데이터 로드 실패:', error);
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
            difficulty: 1, // 1: 쉬움, 2: 보통, 3: 어려움
            interval: 1 // 다음 복습까지 일수
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

    // 학습 모드별 항목 준비
    prepareStudyItems(mode = 'flashcard', label = 'all') {
        this.studyMode = mode;
        let filteredItems = this.filterByLabel(label);
        
            // 각 항목에 학습 상태 추가
        filteredItems = filteredItems.map(item => ({
            ...item,
            studyState: this.getItemStudyState(item.id)
        }));
        
        // 간격 반복 학습 적용
        filteredItems = this.spacedRepetition.prioritizeItems(filteredItems);
        
        return filteredItems;
    }

    // 플래시카드 UI 렌더링
    renderFlashcard(item) {
        const container = document.getElementById('questionContainer');
        
        // 디버깅: 아이템 데이터 확인
        console.log('현재 플래시카드 데이터:', item);
        console.log('답안 내용:', item.content);
        console.log('뒤집힘 상태:', this.isFlipped);
        
        container.innerHTML = `
            <div class="flashcard-container">
                <div class="flashcard ${this.isFlipped ? 'flipped' : ''}" onclick="flipCard()">
                    <div class="flashcard-front">
                        <div class="card-header">
                            <span class="card-number">${this.currentIndex + 1} / ${this.items.length}</span>
                            <div class="card-labels">
                                ${item.labels.map(label => `<span class="label label-${label}">${this.getLabelName(label)}</span>`).join('')}
                            </div>
                        </div>
                        <div class="card-content">
                            <h3>${item.title}</h3>
                            <p class="question">${item.question}</p>
                            <div class="flip-hint">
                                <i class="fas fa-hand-pointer"></i>
                                클릭하여 답 확인
                            </div>
                        </div>
                    </div>
                    <div class="flashcard-back">
                        <div class="card-header">
                            <span class="card-number">${this.currentIndex + 1} / ${this.items.length}</span>
                            <div class="card-labels">
                                ${item.labels.map(label => `<span class="label label-${label}">${this.getLabelName(label)}</span>`).join('')}
                            </div>
                        </div>
                        <div class="card-content">
                            <h3>${item.title}</h3>
                            <div class="answer-content">
                                ${item.content ? item.content.split('\n').filter(line => line.trim() !== '').map(line => `<p>${line}</p>`).join('') : '<p>답안 내용이 없습니다.</p>'}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="flashcard-controls">
                    <div class="top-controls">
                        <button class="back-to-dashboard-btn" onclick="theoryFrequent.renderDashboard()">
                            <i class="fas fa-home"></i> 대시보드로 돌아가기
                        </button>
                    </div>
                    <div class="navigation-controls">
                        <button class="control-btn" onclick="theoryFrequent.previousItem()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전
                        </button>
                        <button class="control-btn" onclick="theoryFrequent.nextItem()" ${this.currentIndex === this.items.length - 1 ? 'disabled' : ''}>
                            다음 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                    
                    ${this.isFlipped ? `
                        <div class="self-assessment">
                            <p>이 문제를 얼마나 잘 알고 있나요?</p>
                            <div class="assessment-buttons">
                                <button class="assessment-btn difficulty-hard" onclick="theoryFrequent.recordAssessment(3)">
                                    <i class="fas fa-times"></i> 모르겠음
                                </button>
                                <button class="assessment-btn difficulty-medium" onclick="theoryFrequent.recordAssessment(2)">
                                    <i class="fas fa-question"></i> 애매함
                                </button>
                                <button class="assessment-btn difficulty-easy" onclick="theoryFrequent.recordAssessment(1)">
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
            'database': 'DB',
            'sql': 'SQL', 
            'os': 'OS',
            'network': '네트워크',
            'security': '보안',
            'software_engineering': 'SW공학',
            'programming': '프로그래밍',
            'data_structure': '자료구조',
            'algorithm': '알고리즘',
            'other': '기타'
        };
        return labelMap[label] || label;
    }

    // 카드 뒤집기
    flipCard() {
        this.isFlipped = !this.isFlipped;
        this.renderFlashcard(this.currentItem);
    }

    // 이전 항목
    previousItem() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.currentItem = this.items[this.currentIndex];
            this.isFlipped = false;
            this.renderFlashcard(this.currentItem);
        }
    }

    // 다음 항목
    nextItem() {
        if (this.currentIndex < this.items.length - 1) {
            this.currentIndex++;
            this.currentItem = this.items[this.currentIndex];
            this.isFlipped = false;
            this.renderFlashcard(this.currentItem);
        }
    }

    // 자가평가 기록
    recordAssessment(difficulty) {
        const itemId = this.currentItem.id;
        const now = new Date();
        
        // 학습 데이터 업데이트
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
        
        // 간격 반복 학습 스케줄 계산
        const nextInterval = this.spacedRepetition.calculateNextInterval(difficulty, itemData.interval);
        itemData.interval = nextInterval;
        
        const nextReview = new Date(now.getTime() + nextInterval * 24 * 60 * 60 * 1000);
        itemData.nextReview = nextReview.toISOString();
        
        if (difficulty === 1) { // "알았음"인 경우
            itemData.correct++;
        }
        
        // 완료 항목에 추가 (중복 제거)
        if (!this.studyData.completedItems.includes(itemId)) {
            this.studyData.completedItems.push(itemId);
        }
        
        // 학습 스트릭 업데이트
        this.updateStudyStreak();
        
        this.saveStudyData();
        
        // 다음 항목으로 자동 이동
        setTimeout(() => {
            this.nextItem();
        }, 1000);
    }

    // 학습 시작
    async startStudy(mode = 'flashcard', label = 'all') {
        if (this.items.length === 0) {
            await this.loadItems();
        }
        
        const studyItems = this.prepareStudyItems(mode, label);
        
        if (studyItems.length === 0) {
            document.getElementById('questionContainer').innerHTML = `
                <div class="question-card">
                    <div style="text-align: center; padding: 50px;">
                        <i class="fas fa-info-circle" style="font-size: 4em; color: #667eea; margin-bottom: 20px;"></i>
                        <h2>학습할 항목이 없습니다</h2>
                        <p style="color: #6c757d; margin-top: 10px;">선택한 라벨에 해당하는 항목이 없습니다.</p>
                    </div>
                </div>
            `;
            return;
        }
        
        this.items = studyItems;
        this.currentIndex = 0;
        this.currentItem = this.items[0];
        this.isFlipped = false;
        
        if (mode === 'flashcard') {
            this.renderFlashcard(this.currentItem);
        }
    }

    // 라벨별 학습 시작
    startLabelStudy(label) {
        this.startStudy('flashcard', label);
    }

    // 학습 스트릭 업데이트
    updateStudyStreak() {
        const today = new Date().toDateString();
        const lastStudyDate = this.studyData.lastStudyDate;
        
        if (lastStudyDate === today) {
            // 오늘 이미 학습함 - 스트릭 유지
            return;
        }
        
        if (lastStudyDate) {
            const lastDate = new Date(lastStudyDate);
            const todayDate = new Date(today);
            const diffTime = todayDate - lastDate;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (diffDays === 1) {
                // 연속 학습
                this.studyData.streak++;
            } else {
                // 연속 학습 중단
                this.studyData.streak = 1;
            }
        } else {
            // 첫 학습
            this.studyData.streak = 1;
        }
        
        this.studyData.lastStudyDate = today;
    }

    // 섹션 토글
    toggleSection(sectionId) {
        const section = document.getElementById(`${sectionId}-section`);
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

    // 대시보드 렌더링
    renderDashboard() {
        const container = document.getElementById('questionContainer');
        const stats = this.calculateStats();
        
        container.innerHTML = `
            <div class="theory-frequent-dashboard">
                <div class="dashboard-header-compact">
                    <h2><i class="fas fa-star"></i> 실기 최빈출 50개</h2>
                    <div class="total-count">
                        <span class="count-number">${stats.total}</span>
                        <span class="count-label">개 문제</span>
                    </div>
                </div>
                
                <!-- 학습 통계 (상단으로 이동) -->
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
                            <i class="fas fa-fire" style="color: #fd7e14;"></i>
                            <div class="stat-content">
                                <div class="stat-number">${stats.streak}</div>
                                <div class="stat-label">연속일</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 주요 학습 버튼 -->
                <div class="main-study-section">
                    <button class="main-study-btn" onclick="theoryFrequent.startLabelStudy('all')">
                        <div class="btn-icon"><i class="fas fa-play-circle"></i></div>
                        <div class="btn-content">
                            <div class="btn-title">전체 학습 시작</div>
                            <div class="btn-desc">${stats.total}개 항목 • 플래시카드 방식</div>
                        </div>
                    </button>
                </div>
                
                <!-- 라벨별 학습 드롭다운 -->
                <div class="compact-section">
                    <button class="section-toggle" onclick="theoryFrequent.toggleSection('labels')">
                        <span><i class="fas fa-folder-open"></i> 라벨별 학습</span>
                        <i class="fas fa-chevron-down toggle-icon"></i>
                    </button>
                    <div id="labels-section" class="section-content" style="display: none;">
                        <div class="label-grid-compact">
                            <button class="label-btn-compact" onclick="theoryFrequent.startLabelStudy('database')">
                                <i class="fas fa-database"></i> 데이터베이스<br><small>${stats.byLabel.database || 0}개</small>
                            </button>
                            <button class="label-btn-compact" onclick="theoryFrequent.startLabelStudy('os')">
                                <i class="fas fa-desktop"></i> 운영체제<br><small>${stats.byLabel.os || 0}개</small>
                            </button>
                            <button class="label-btn-compact" onclick="theoryFrequent.startLabelStudy('network')">
                                <i class="fas fa-network-wired"></i> 네트워크<br><small>${stats.byLabel.network || 0}개</small>
                            </button>
                            <button class="label-btn-compact" onclick="theoryFrequent.startLabelStudy('security')">
                                <i class="fas fa-shield-alt"></i> 정보보안<br><small>${stats.byLabel.security || 0}개</small>
                            </button>
                            <button class="label-btn-compact" onclick="theoryFrequent.startLabelStudy('software_engineering')">
                                <i class="fas fa-cogs"></i> SW공학<br><small>${stats.byLabel.software_engineering || 0}개</small>
                            </button>
                            <button class="label-btn-compact" onclick="theoryFrequent.startLabelStudy('programming')">
                                <i class="fas fa-code"></i> 프로그래밍<br><small>${stats.byLabel.programming || 0}개</small>
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- 체크한 문제 복사 -->
                ${stats.bookmarked > 0 ? `
                <div class="bookmark-section">
                    <button class="bookmark-copy-btn" onclick="theoryFrequent.copyBookmarkedItems()">
                        <i class="fas fa-copy"></i> 체크한 ${stats.bookmarked}개 문제 복사하기
                    </button>
                </div>
                ` : ''}
                
                <!-- 라벨별 진도 드롭다운 -->
                <div class="compact-section">
                    <button class="section-toggle" onclick="theoryFrequent.toggleSection('progress')">
                        <span><i class="fas fa-chart-line"></i> 라벨별 진도</span>
                        <i class="fas fa-chevron-down toggle-icon"></i>
                    </button>
                    <div id="progress-section" class="section-content" style="display: none;">
                        <div class="label-progress">
                            ${Object.entries(stats.byLabel).map(([label, count]) => {
                                const completedInLabel = this.studyData.completedItems.filter(id => {
                                    const item = this.items.find(i => i.id === id);
                                    return item && item.labels.includes(label);
                                }).length;
                                const percentage = count > 0 ? Math.round(completedInLabel / count * 100) : 0;
                                
                                return `
                                    <div class="label-progress-item">
                                        <span class="label-name">${this.getLabelName(label)}</span>
                                        <div class="mini-progress">
                                            <div class="mini-progress-bar">
                                                <div class="mini-progress-fill label-${label}" style="width: ${percentage}%"></div>
                                            </div>
                                            <span class="mini-progress-text">${percentage}%</span>
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // 통계 계산
    calculateStats() {
        const stats = {
            total: this.items.length,
            completed: this.studyData.completedItems.length,
            streak: this.studyData.streak,
            totalTime: 0,
            accuracy: 0,
            byLabel: {}
        };

        // 라벨별 통계
        this.items.forEach(item => {
            item.labels.forEach(label => {
                stats.byLabel[label] = (stats.byLabel[label] || 0) + 1;
            });
        });

        // 총 학습시간 및 정답률 계산
        let totalAttempts = 0;
        let totalCorrect = 0;
        let totalTime = 0;

        Object.values(this.studyData.studyTime).forEach(data => {
            totalAttempts += data.attempts;
            totalCorrect += data.correct;
            totalTime += data.attempts * 0.5; // 평균 30초 per attempt
        });

        stats.accuracy = totalAttempts > 0 ? Math.round((totalCorrect / totalAttempts) * 100) : 0;
        stats.totalTime = Math.round(totalTime);

        return stats;
    }
}

// 간격 반복 학습 관리자
class SpacedRepetitionManager {
    // 다음 복습 간격 계산 (에빙하우스 망각 곡선 기반)
    calculateNextInterval(difficulty, currentInterval) {
        const difficultyMultiplier = {
            1: 2.5, // 알았음: 간격을 2.5배로 늘림
            2: 1.3, // 애매함: 간격을 1.3배로 늘림
            3: 0.5  // 모르겠음: 간격을 절반으로 줄임
        };
        
        const multiplier = difficultyMultiplier[difficulty] || 1;
        let nextInterval = Math.round(currentInterval * multiplier);
        
        // 최소 1일, 최대 30일로 제한
        nextInterval = Math.max(1, Math.min(30, nextInterval));
        
        return nextInterval;
    }

    // 복습이 필요한 항목들을 우선순위로 정렬
    prioritizeItems(items) {
        const now = new Date();
        
        return items.sort((a, b) => {
            const aState = a.studyState;
            const bState = b.studyState;
            
            // 복습 예정일이 지난 항목들 우선
            if (aState.nextReview && new Date(aState.nextReview) <= now) {
                if (!bState.nextReview || new Date(bState.nextReview) > now) {
                    return -1;
                }
            }
            
            // 어려운 항목들 우선
            if (aState.difficulty !== bState.difficulty) {
                return bState.difficulty - aState.difficulty;
            }
            
            // 학습 횟수가 적은 항목들 우선
            return aState.attempts - bState.attempts;
        });
    }
}

// 전역 인스턴스
const theoryFrequent = new TheoryFrequentModule();

// 전역 함수들 (HTML에서 호출용)
function flipCard() {
    theoryFrequent.flipCard();
}

function startTheoryFrequent() {
    theoryFrequent.renderDashboard();
}
