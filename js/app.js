// 메인 앱 로직

// 템플릿 로더
async function loadTemplate(templatePath, targetId) {
    try {
        const response = await fetch(templatePath);
        const html = await response.text();
        const target = document.getElementById(targetId);
        if (target) {
            target.innerHTML = html;
        }
    } catch (error) {
        console.error(`템플릿 로드 실패: ${templatePath}`, error);
    }
}

// 배열 섞기
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// 학습 모드 설정
function setMode(mode) {
    App.state.currentMode = mode;
    currentMode = mode; // 하위 호환성
    
    // 버튼 활성화
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // 문제 로드
    loadQuestions(mode);
}

// 문제 로드
async function loadQuestions(mode) {
    try {
        const config = App.moduleConfig[App.state.currentModule];
        
        // items.jsonl 로드
        const response = await fetch(config.itemsFile);
        const text = await response.text();
        let questions = text.trim().split('\n').map(line => JSON.parse(line));
        
        // 카테고리 모드인 경우 필터링
        if (config.isCategoryMode && config.category) {
            questions = questions.filter(q => q.primary_category === config.category);
            console.log(`카테고리 필터링: ${config.category} - ${questions.length}개 문제`);
        }
        
        App.state.allQuestions = questions;
        allQuestions = App.state.allQuestions; // 하위 호환성
        
        // tables.jsonl 로드
        if (config.tablesFile) {
            try {
                const tablesResponse = await fetch(config.tablesFile);
                const tablesText = await tablesResponse.text();
                const tables = tablesText.trim().split('\n').map(line => JSON.parse(line));
                
                // 표를 ID로 인덱싱
                App.state.allTables = {};
                for (const table of tables) {
                    App.state.allTables[table.table_id] = table;
                }
                allTables = App.state.allTables; // 하위 호환성
                console.log(`${tables.length}개 표 로드 완료`);
            } catch (e) {
                console.log('표 데이터 없음:', e);
            }
        }
        
        // 모드별 필터링
        App.state.currentQuestions = filterQuestionsByMode(mode);
        currentQuestions = App.state.currentQuestions; // 하위 호환성
        
        if (App.state.currentQuestions.length === 0) {
            showMessage('해당 모드에 문제가 없습니다.');
            return;
        }
        
        App.state.currentIndex = 0;
        currentIndex = 0; // 하위 호환성
        displayQuestion(App.state.currentQuestions[0]);
        updateStats();
        
    } catch (error) {
        console.error('문제 로드 오류:', error);
        showMessage('문제를 불러올 수 없습니다.');
    }
}

// 모드별 필터링
function filterQuestionsByMode(mode) {
    const savedProgress = JSON.parse(localStorage.getItem('progress') || '{}');
    const wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    const markedQuestions = JSON.parse(localStorage.getItem('markedQuestions') || '[]');
    
    switch(mode) {
        case 'sequential':
            return App.state.allQuestions;
            
        case 'random':
            return shuffleArray([...App.state.allQuestions]);
            
        case 'range':
            // 모달 창 표시
            showRangeModal();
            return [];
            
        case 'wrong':
            return App.state.allQuestions.filter(q => wrongQuestions.includes(q.q_no));
            
        case 'marked':
            return App.state.allQuestions.filter(q => markedQuestions.includes(q.q_no));
            
        default:
            return App.state.allQuestions;
    }
}

// 통계 업데이트
function updateStats() {
    App.state.stats.total = App.state.allQuestions.length;
    stats.total = App.state.stats.total; // 하위 호환성
    
    const progress = ((App.state.stats.correct + App.state.stats.wrong) / App.state.stats.total * 100).toFixed(1);
    const accuracy = App.state.stats.correct > 0 ? (App.state.stats.correct / (App.state.stats.correct + App.state.stats.wrong) * 100).toFixed(1) : 0;
    
    // 애니메이션과 함께 업데이트
    updateStatWithAnimation('progress', progress + '%');
    updateStatWithAnimation('accuracy', accuracy + '%');
    updateStatWithAnimation('remaining', App.state.allQuestions.length - (App.state.stats.correct + App.state.stats.wrong));
    updateStatWithAnimation('wrongCount', App.state.stats.wrong);
}

// 애니메이션과 함께 통계 업데이트
function updateStatWithAnimation(id, newValue) {
    const element = document.getElementById(id);
    if (element && element.textContent !== newValue.toString()) {
        element.classList.add('updating');
        setTimeout(() => {
            element.textContent = newValue;
            element.classList.remove('updating');
        }, 100);
    }
}

// 메시지 표시
function showMessage(msg) {
    alert(msg);
}

// 초기화
document.addEventListener('DOMContentLoaded', async function() {
    console.log('앱 초기화 시작...');
    
    // 템플릿 로드
    await loadTemplate('templates/welcome.html', 'welcomePopup');
    await loadTemplate('templates/menu.html', 'sidebarMenu');
    await loadTemplate('templates/modal-font.html', 'fontSizeModal');
    await loadTemplate('templates/modal-stats.html', 'statsModal');
    await loadTemplate('templates/modal-range.html', 'rangeModal');
    
    console.log('템플릿 로드 완료');
    
    // 진행 상황 로드
    loadProgress();
    loadFontSize();
    updateStats();
    
    // 기본 모듈 활성화
    const menuItem = document.getElementById(`menu_${App.state.currentModule}`);
    if (menuItem) {
        menuItem.style.background = '#667eea';
        menuItem.style.color = 'white';
    }
    
    // 환영 팝업 표시 (첫 방문 시)
    if (!localStorage.getItem('welcomeShown')) {
        const welcomePopup = document.getElementById('welcomePopup');
        if (welcomePopup) {
            welcomePopup.classList.add('show');
        }
    }
    
    console.log('앱 초기화 완료');
});

