// PMP 문제집 학습 모듈 (핵심키워드130과 동일한 스타일)
class PMPModule {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
        this.studyMode = 'quiz'; // quiz 모드 (핵심키워드130과 동일)
        this.currentLabel = 'all';
        this.studyData = this.loadStudyData();
        this.selectedAnswer = null;
        this.enhancedMode = false; // 학습 모드 (키워드 강조)
    }

    // 학습 데이터 로드
    loadStudyData() {
        const saved = localStorage.getItem('pmp_study_data');
        if (saved) {
            return JSON.parse(saved);
        }
        return {
            completedItems: [],
            studyTime: {},
            streak: 0,
            lastStudyDate: null,
            bookmarkedItems: [],
            stats: { correct: 0, wrong: 0, total: 0 }
        };
    }

    // 학습 데이터 저장
    saveStudyData() {
        localStorage.setItem('pmp_study_data', JSON.stringify(this.studyData));
    }

    // 학습 모드 토글 (키워드 강조)
    toggleEnhancedMode() {
        this.enhancedMode = !this.enhancedMode;
        if (this.currentItem) {
            this.renderQuestion(this.currentItem);
        }
    }

    // 북마크 토글
    toggleBookmarkButton(itemId) {
        const index = this.studyData.bookmarkedItems.indexOf(itemId);
        const btn = event.target.closest('button');
        
        if (index === -1) {
            this.studyData.bookmarkedItems.push(itemId);
            btn.innerHTML = '<i class="fas fa-star"></i> 체크됨';
            btn.style.background = '#28a745';
        } else {
            this.studyData.bookmarkedItems.splice(index, 1);
            btn.innerHTML = '<i class="fas fa-star"></i> 체크';
            btn.style.background = '';
        }
        
        this.saveStudyData();
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
            
            this.items = text.trim().split('\n').map(line => JSON.parse(line));
            
            console.log(`PMP ${this.items.length}개 문제 로드 완료`);
            return this.items;
        } catch (error) {
            console.error('PMP 데이터 로드 실패:', error);
            return [];
        }
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

    // 주요 키워드 강조
    highlightKeywords(text) {
        if (!this.enhancedMode) return text;
        
        // PMP 주요 키워드 목록
        const keywords = [
            // 프로세스 그룹
            '착수', '기획', '계획', '실행', '수행', '감시', '통제', '종료',
            // 지식 영역
            '통합', '범위', '일정', '원가', '품질', '자원', '의사소통', '위험', '조달', '이해관계자',
            // 주요 개념
            'WBS', 'EVM', 'CPM', 'PERT', 'QA', 'QC', '헌장', '변경', '리스크', '계약',
            '애자일', '스프린트', '백로그', '스크럼', '칸반',
            '프로젝트 관리자', '후원자', '팀원', '고객',
            '베이스라인', '마일스톤', '인도물', '요구사항',
            // 영문 키워드
            'Agile', 'Sprint', 'Scrum', 'Kanban', 'Backlog',
            'Stakeholder', 'Sponsor', 'Charter', 'Baseline',
            'Milestone', 'Deliverable', 'Requirement'
        ];
        
        let highlightedText = text;
        keywords.forEach(keyword => {
            const regex = new RegExp(`(${keyword})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<strong style="color: #6f42c1; font-weight: 700;">$1</strong>');
        });
        
        return highlightedText;
    }

    // 문제 표시 (핵심키워드130과 동일한 스타일)
    renderQuestion(item) {
        const container = document.getElementById('questionContainer');
        const isBookmarked = this.isBookmarked(item.id);
        
        // 학습 모드에 따라 텍스트 처리
        const questionText = this.highlightKeywords(item.question);
        const explanationText = this.highlightKeywords(item.explanation || '');
        
        container.innerHTML = `
            <div class="question-card">
                <div class="question-header">
                    <div class="question-no">${item.q_no}</div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn btn-info" onclick="pmpModule.toggleEnhancedMode()" style="font-size: 0.9em;">
                            <i class="fas fa-highlighter"></i> ${this.enhancedMode ? '강조 OFF' : '강조 ON'}
                        </button>
                        <button class="btn btn-secondary" onclick="pmpModule.toggleBookmarkButton('${item.id}')">
                            <i class="fas fa-star"></i> ${isBookmarked ? '체크됨' : '체크'}
                        </button>
                    </div>
                </div>
                
                <div class="question-labels" style="margin-bottom: 20px;">
                    ${item.labels.map(label => `<span class="label label-${label}" style="background: ${this.getLabelColor(label)}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em; margin-right: 8px;">${this.getLabelName(label)}</span>`).join('')}
                </div>
                
                <div class="question-text">
                    ${questionText}
                </div>
                
                <div class="choices">
                    ${item.options.map((option, index) => {
                        const key = String.fromCharCode(65 + index); // A, B, C, D
                        const text = option.replace(/^[A-D]\)\s*/, ''); // A) 제거
                        return `
                            <div class="choice-item" onclick="pmpModule.selectChoice(this, '${key}')">
                                <span class="choice-key">${key}</span>
                                <span class="choice-text">${text}</span>
                            </div>
                        `;
                    }).join('')}
                </div>
                
                <input type="text" class="answer-input" id="pmpAnswerInput" 
                       placeholder="정답을 입력하세요 (A, B, C, D)" style="display: none;">
                
                <div class="action-buttons">
                    <button class="btn btn-primary" onclick="pmpModule.checkAnswer()">
                        <i class="fas fa-check"></i> 정답 확인
                    </button>
                    <button class="btn" onclick="pmpModule.showAnswerOnly()" style="background: #17a2b8; color: white;">
                        <i class="fas fa-eye"></i> 답 보기
                    </button>
                    <button class="btn btn-secondary" onclick="pmpModule.previousItem()">
                        <i class="fas fa-arrow-left"></i> 이전 문제
                    </button>
                    <button class="btn btn-secondary" onclick="pmpModule.nextItem()">
                        <i class="fas fa-arrow-right"></i> 다음 문제
                    </button>
                    <button class="btn btn-secondary" onclick="pmpModule.showExplanation()">
                        <i class="fas fa-lightbulb"></i> 해설 보기
                    </button>
                    <button class="btn btn-secondary" onclick="pmpModule.renderDashboard()">
                        <i class="fas fa-home"></i> 대시보드
                    </button>
                </div>
                
                <div class="result-section" id="pmpResultSection" style="display: none;"></div>
                <div class="explanation" id="pmpExplanationDiv"></div>
            </div>
        `;
        
        // 북마크 버튼 스타일 업데이트
        this.updateBookmarkButtonStyle(item.id);
    }

    // 선택지 클릭
    selectChoice(element, key) {
        // 모든 선택지 스타일 초기화
        document.querySelectorAll('.choice-item').forEach(item => {
            item.style.background = '#f8f9fa';
            item.style.color = '';
        });
        
        // 선택된 선택지 하이라이트
        element.style.background = '#667eea';
        element.style.color = 'white';
        
        // 선택된 답안 저장
        this.selectedAnswer = key;
        
        // 숨겨진 입력창에 값 설정
        const answerInput = document.getElementById('pmpAnswerInput');
        if (answerInput) {
            answerInput.value = key;
        }
    }

    // 정답 확인
    checkAnswer() {
        if (!this.selectedAnswer) {
            alert('답안을 선택해주세요.');
            return;
        }
        
        const item = this.currentItem;
        const isCorrect = this.selectedAnswer === item.answer;
        const resultSection = document.getElementById('pmpResultSection');
        
        // 통계 업데이트
        this.studyData.stats.total++;
        if (isCorrect) {
            this.studyData.stats.correct++;
        } else {
            this.studyData.stats.wrong++;
        }
        
        // 완료 항목에 추가
        if (!this.studyData.completedItems.includes(item.id)) {
            this.studyData.completedItems.push(item.id);
        }
        
        this.saveStudyData();
        
        // 결과 표시
        resultSection.style.display = 'block';
        if (isCorrect) {
            resultSection.className = 'result-section correct';
            resultSection.style.background = '#d4edda';
            resultSection.style.border = '2px solid #155724';
            resultSection.style.color = '#155724';
            resultSection.innerHTML = `
                <i class="fas fa-check-circle"></i> <strong>정답입니다!</strong> ${item.answer_text}
            `;
        } else {
            resultSection.className = 'result-section wrong';
            resultSection.style.background = '#f8d7da';
            resultSection.style.border = '2px solid #721c24';
            resultSection.style.color = '#721c24';
            resultSection.innerHTML = `
                <i class="fas fa-times-circle"></i> <strong>오답입니다.</strong> 정답: ${item.answer} - ${item.answer_text}
            `;
        }
    }

    // 답 보기 (정답만 표시, 통계 반영 안함)
    showAnswerOnly() {
        const item = this.currentItem;
        const resultSection = document.getElementById('pmpResultSection');
        
        resultSection.style.display = 'block';
        resultSection.className = 'result-section';
        resultSection.style.background = '#d1ecf1';
        resultSection.style.border = '2px solid #0c5460';
        resultSection.style.color = '#0c5460';
        resultSection.innerHTML = `
            <i class="fas fa-eye"></i> <strong>정답:</strong> ${item.answer} - ${item.answer_text}
        `;
    }

    // 해설 보기
    showExplanation() {
        const explanationDiv = document.getElementById('pmpExplanationDiv');
        const item = this.currentItem;
        
        if (item.explanation) {
            const explanationText = this.highlightKeywords(item.explanation);
            explanationDiv.innerHTML = `
                <div class="explanation-content">
                    <h4><i class="fas fa-lightbulb"></i> 해설</h4>
                    <p style="white-space: pre-line;">${explanationText}</p>
                </div>
            `;
            explanationDiv.classList.toggle('show');
        } else {
            explanationDiv.innerHTML = '<div class="explanation-content"><p>해설이 없습니다.</p></div>';
            explanationDiv.classList.add('show');
        }
    }

    // 이전 문제
    previousItem() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.currentItem = this.items[this.currentIndex];
            this.selectedAnswer = null;
            this.renderQuestion(this.currentItem);
        }
    }

    // 다음 문제
    nextItem() {
        if (this.currentIndex < this.items.length - 1) {
            this.currentIndex++;
            this.currentItem = this.items[this.currentIndex];
            this.selectedAnswer = null;
            this.renderQuestion(this.currentItem);
        }
    }

    // 북마크 버튼 스타일 업데이트
    updateBookmarkButtonStyle(itemId) {
        const btn = document.querySelector(`button[onclick*="${itemId}"]`);
        if (btn) {
            const isBookmarked = this.isBookmarked(itemId);
            btn.innerHTML = `<i class="fas fa-star"></i> ${isBookmarked ? '체크됨' : '체크'}`;
            btn.style.background = isBookmarked ? '#28a745' : '';
        }
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
                    <div class="filter-options">
                        <button class="filter-btn" onclick="pmpModule.startStudy('all', 'sequential')">
                            <i class="fas fa-play"></i> 전체 순차 학습 (${stats.total}개)
                        </button>
                        <button class="filter-btn" onclick="pmpModule.startStudy('all', 'random')">
                            <i class="fas fa-random"></i> 전체 랜덤 학습 (${stats.total}개)
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
            if (count === 0) return '';
            
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
        }).filter(card => card).join('');
    }

    // 프로세스 그룹 카드 렌더링
    renderProcessGroupCards(stats) {
        const processGroups = ['initiating', 'planning', 'executing', 'monitoring', 'closing'];

        return processGroups.map(process => {
            const count = stats.byLabel[process] || 0;
            if (count === 0) return '';
            
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
        }).filter(card => card).join('');
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

    // 라벨 색상
    getLabelColor(label) {
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
            'project_stakeholder': '#007bff',
            'initiating': '#28a745',
            'planning': '#17a2b8',
            'executing': '#ffc107',
            'monitoring': '#fd7e14',
            'closing': '#dc3545'
        };
        return colors[label] || '#6c757d';
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
        this.selectedAnswer = null;
        
        this.renderQuestion(this.currentItem);
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
        this.selectedAnswer = null;
        
        this.renderQuestion(this.currentItem);
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
        const totalAttempts = this.studyData.stats.correct + this.studyData.stats.wrong;
        stats.accuracy = totalAttempts > 0 ? Math.round((this.studyData.stats.correct / totalAttempts) * 100) : 0;

        return stats;
    }
}

// 전역 인스턴스
const pmpModule = new PMPModule();

// 전역 함수들
window.pmpModule = pmpModule;