// PMP 문제집 학습 모듈 (핵심키워드130과 동일한 스타일)
class PMPModule {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
        this.studyMode = 'quiz'; // 'quiz' 또는 'card'
        this.currentLabel = 'all';
        this.studyData = this.loadStudyData();
        this.selectedAnswer = null;
        this.enhancedMode = false; // 학습 모드 (키워드 강조)
        this.cardStep = 1; // 카드 학습 단계 (1: 문제, 2: 답, 3: 해설)
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
                    <div style="display: flex; gap: 6px;">
                        <button class="btn btn-info" onclick="pmpModule.toggleEnhancedMode()">
                            <i class="fas fa-highlighter"></i> ${this.enhancedMode ? 'OFF' : 'ON'}
                        </button>
                        <button class="btn btn-secondary" onclick="pmpModule.toggleBookmarkButton('${item.id}')">
                            <i class="fas fa-star"></i> ${isBookmarked ? '✓' : '☆'}
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
                    <div class="main-controls">
                        <button class="btn btn-primary" onclick="pmpModule.checkAnswer()">
                            <i class="fas fa-check"></i> 제출
                        </button>
                        <button class="btn" onclick="pmpModule.showAnswerOnly()" style="background: #17a2b8; color: white;">
                            <i class="fas fa-eye"></i> 답
                        </button>
                        <button class="btn btn-secondary" onclick="pmpModule.showExplanation()">
                            <i class="fas fa-lightbulb"></i> 해설
                        </button>
                    </div>
                    <div class="navigation-controls">
                        <button class="btn btn-secondary" onclick="pmpModule.previousItem()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="pmpModule.renderDashboard()">
                            <i class="fas fa-home"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="pmpModule.nextItem()" ${this.currentIndex === this.items.length - 1 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
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

    // 카드 학습 모드 렌더링
    renderCardMode(item) {
        const container = document.getElementById('questionContainer');
        const isBookmarked = this.isBookmarked(item.id);
        
        let cardContent = '';
        
        // 단계별 콘텐츠
        if (this.cardStep === 1) {
            // 1단계: 문제만
            const questionText = this.highlightKeywords(item.question);
            cardContent = `
                <div class="card-question">
                    <h3>문제</h3>
                    <p>${questionText}</p>
                </div>
            `;
        } else if (this.cardStep === 2) {
            // 2단계: 답
            const answerText = item.options.find(opt => opt.startsWith(item.answer + '.'))
                ?.replace(/^[A-D]\.\s*/, '') || item.answer_text;
            cardContent = `
                <div class="card-question dimmed">
                    <p>${item.question}</p>
                </div>
                <div class="card-answer">
                    <h3>정답</h3>
                    <div class="answer-key">${item.answer}</div>
                    <p>${answerText}</p>
                </div>
                <div class="card-hint">클릭하여 해설 확인</div>
            `;
        } else if (this.cardStep === 3) {
            // 3단계: 해설 요약
            const answerText = item.options.find(opt => opt.startsWith(item.answer + '.'))
                ?.replace(/^[A-D]\.\s*/, '') || item.answer_text;
            const explanationText = this.highlightKeywords(this.summarizeExplanation(item.explanation));
            cardContent = `
                <div class="card-question dimmed">
                    <p>${item.question}</p>
                </div>
                <div class="card-answer">
                    <div class="answer-key">${item.answer}</div>
                    <p>${answerText}</p>
                </div>
                <div class="card-explanation">
                    <h3>해설 요약</h3>
                    <p>${explanationText}</p>
                </div>
                <div class="card-hint">클릭하여 다음 문제</div>
            `;
        }
        
        container.innerHTML = `
            <div class="question-card card-mode" onclick="pmpModule.nextCardStep()">
                <div class="question-header">
                    <div class="question-no">${item.q_no}</div>
                    <div class="card-step-indicator">${this.cardStep}/3</div>
                    <button class="btn btn-secondary" onclick="event.stopPropagation(); pmpModule.toggleBookmarkButton('${item.id}')">
                        <i class="fas fa-star"></i> ${isBookmarked ? '✓' : '☆'}
                    </button>
                </div>
                
                <div class="card-content">
                    ${cardContent}
                </div>
                
                <div class="action-buttons">
                    <div class="main-controls">
                        <button class="btn btn-primary" onclick="event.stopPropagation(); pmpModule.nextCardStep()">
                            <i class="fas fa-arrow-right"></i> ${this.cardStep === 3 ? '다음문제' : '다음'}
                        </button>
                        <button class="btn" onclick="event.stopPropagation(); pmpModule.jumpToCardStep(2)" style="background: #17a2b8; color: white;">
                            <i class="fas fa-eye"></i> 답
                        </button>
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); pmpModule.jumpToCardStep(3)">
                            <i class="fas fa-lightbulb"></i> 해설
                        </button>
                    </div>
                    <div class="navigation-controls">
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); pmpModule.previousCardItem()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); pmpModule.renderDashboard()">
                            <i class="fas fa-home"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); pmpModule.nextCardItem()" ${this.currentIndex === this.items.length - 1 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // 대시보드 렌더링
    renderDashboard() {
        const container = document.getElementById('questionContainer');
        const stats = this.calculateStats();
        
        container.innerHTML = `
            <div class="pmp-dashboard">
                <div class="dashboard-header">
                    <h2><i class="fas fa-project-diagram"></i> PMP 문제집</h2>
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
                        <button class="main-mode-card primary" onclick="pmpModule.startStudy('all', 'sequential')">
                            <div class="mode-icon"><i class="fas fa-play-circle"></i></div>
                            <div class="mode-title">순차학습</div>
                            <div class="mode-desc">처음부터 순서대로</div>
                        </button>
                        <button class="main-mode-card secondary" onclick="pmpModule.startStudy('all', 'random')">
                            <div class="mode-icon"><i class="fas fa-random"></i></div>
                            <div class="mode-title">랜덤학습</div>
                            <div class="mode-desc">무작위로 섞어서</div>
                        </button>
                        <button class="main-mode-card accent" onclick="pmpModule.startCardStudy('all', 'sequential')">
                            <div class="mode-icon"><i class="fas fa-layer-group"></i></div>
                            <div class="mode-title">카드학습</div>
                            <div class="mode-desc">플립 카드 방식</div>
                        </button>
                        <button class="main-mode-card bookmarked" onclick="pmpModule.startBookmarkedStudy()">
                            <div class="mode-icon"><i class="fas fa-star"></i></div>
                            <div class="mode-title">체크문제</div>
                            <div class="mode-desc">${stats.bookmarked}개 문제</div>
                        </button>
                    </div>
                </div>
                
                <!-- 범위학습 (별도 강조) -->
                <div class="range-study-section">
                    <button class="range-study-btn" onclick="pmpModule.showRangeModal()">
                        <i class="fas fa-sliders-h"></i> 범위를 지정해서 학습하기
                    </button>
                </div>
                
                <!-- 지식영역 드롭다운 -->
                <div class="compact-section">
                    <button class="section-toggle" onclick="pmpModule.toggleSection('knowledge')">
                        <span><i class="fas fa-book"></i> 지식영역별 학습</span>
                        <i class="fas fa-chevron-down toggle-icon"></i>
                    </button>
                    <div id="knowledge-section" class="section-content" style="display: none;">
                        <div class="label-grid-compact">
                            ${this.renderKnowledgeAreaCardsCompact(stats)}
                        </div>
                    </div>
                </div>
                
                <!-- 프로세스 그룹 드롭다운 -->
                <div class="compact-section">
                    <button class="section-toggle" onclick="pmpModule.toggleSection('process')">
                        <span><i class="fas fa-cogs"></i> 프로세스 그룹별 학습</span>
                        <i class="fas fa-chevron-down toggle-icon"></i>
                    </button>
                    <div id="process-section" class="section-content" style="display: none;">
                        <div class="label-grid-compact">
                            ${this.renderProcessGroupCardsCompact(stats)}
                        </div>
                    </div>
                </div>
            </div>
        `;
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
    
    // 컴팩트 지식영역 카드
    renderKnowledgeAreaCardsCompact(stats) {
        const knowledgeAreas = [
            'project_integration', 'project_scope', 'project_schedule', 'project_cost',
            'project_quality', 'project_resource', 'project_communication', 
            'project_risk', 'project_procurement', 'project_stakeholder'
        ];

        return knowledgeAreas.map(area => {
            const count = stats.byLabel[area] || 0;
            if (count === 0) return '';
            
            return `
                <button class="label-btn-compact" onclick="pmpModule.startStudy('${area}', 'sequential')">
                    ${this.getLabelName(area)} (${count})
                </button>
            `;
        }).filter(card => card).join('');
    }
    
    // 컴팩트 프로세스 그룹 카드
    renderProcessGroupCardsCompact(stats) {
        const processGroups = ['initiating', 'planning', 'executing', 'monitoring', 'closing'];

        return processGroups.map(process => {
            const count = stats.byLabel[process] || 0;
            if (count === 0) return '';
            
            return `
                <button class="label-btn-compact" onclick="pmpModule.startStudy('${process}', 'sequential')">
                    ${this.getLabelName(process)} (${count})
                </button>
            `;
        }).filter(card => card).join('');
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
        this.studyMode = 'quiz';
        
        this.renderQuestion(this.currentItem);
    }

    // 카드 학습 모드 시작
    async startCardStudy(label = 'all', mode = 'sequential') {
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
        this.studyMode = 'card';
        this.cardStep = 1;
        
        this.renderCardMode(this.currentItem);
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
    
    // 범위 학습 모달 표시
    showRangeModal() {
        const totalQuestions = this.items.length;
        const rangeStart = prompt(`시작 문제 번호 (1~${totalQuestions}):`, '1');
        
        if (!rangeStart) return; // 취소
        
        const rangeEnd = prompt(`끝 문제 번호 (${rangeStart}~${totalQuestions}):`, totalQuestions.toString());
        
        if (!rangeEnd) return; // 취소
        
        const start = parseInt(rangeStart);
        const end = parseInt(rangeEnd);
        
        // 유효성 검사
        if (isNaN(start) || isNaN(end)) {
            alert('숫자를 입력해주세요.');
            return;
        }
        
        if (start < 1 || start > totalQuestions || end < 1 || end > totalQuestions) {
            alert(`1~${totalQuestions} 사이의 번호를 입력해주세요.`);
            return;
        }
        
        if (start > end) {
            alert('시작 번호가 끝 번호보다 클 수 없습니다.');
            return;
        }
        
        this.startRangeStudy(start, end);
    }
    
    // 범위 학습 시작
    startRangeStudy(start, end) {
        // q_no 기준으로 필터링
        const rangeItems = this.items.filter(item => {
            const qNo = parseInt(item.q_no);
            return qNo >= start && qNo <= end;
        });
        
        if (rangeItems.length === 0) {
            alert(`${start}~${end} 범위에 해당하는 문제가 없습니다.`);
            return;
        }
        
        this.items = rangeItems;
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

    // 카드 학습: 다음 단계로 진행
    nextCardStep() {
        if (this.cardStep < 3) {
            this.cardStep++;
            this.renderCardMode(this.currentItem);
        } else {
            // 3단계에서 다음 문제로
            this.nextCardItem();
        }
    }

    // 카드 학습: 특정 단계로 점프
    jumpToCardStep(step) {
        this.cardStep = step;
        this.renderCardMode(this.currentItem);
    }

    // 카드 학습: 다음 문제
    nextCardItem() {
        if (this.currentIndex < this.items.length - 1) {
            this.currentIndex++;
            this.currentItem = this.items[this.currentIndex];
            this.cardStep = 1; // 1단계로 리셋
            this.renderCardMode(this.currentItem);
        } else {
            // 마지막 문제인 경우 대시보드로
            alert('모든 문제를 완료했습니다!');
            this.renderDashboard();
        }
    }

    // 카드 학습: 이전 문제
    previousCardItem() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.currentItem = this.items[this.currentIndex];
            this.cardStep = 1; // 1단계로 리셋
            this.renderCardMode(this.currentItem);
        }
    }

    // 해설 요약 (첫 2-3 문장 추출)
    summarizeExplanation(explanation) {
        if (!explanation || explanation === '해설이 없습니다.') {
            return '해설이 없습니다.';
        }
        
        // 첫 2-3 문장만 추출 (간단한 요약)
        const sentences = explanation.split(/[.!?]\s+/);
        const summary = sentences.slice(0, 2).join('. ');
        
        return summary + (sentences.length > 2 ? '...' : '');
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