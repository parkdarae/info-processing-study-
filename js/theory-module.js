// 정처기 실기 이론 모듈 - 객관식/주관식 문제 생성 및 검증

// 이론 모듈 상태 초기화
if (typeof App === 'undefined') {
    console.error('❌ App 객체가 정의되지 않았습니다!');
} else {
    console.log('✅ App 객체 사용 가능');
    App.theory = {
        questionType: 'objective', // 'objective' or 'subjective'
        currentQuestion: null,
        questionPool: [],
        usedQuestions: new Set(),
        allTheoryData: [],
        categoryStats: {},
        currentCategory: 'all',
        studyMode: 'sequential' // 'sequential', 'random', 'range'
    };
}

// 이론 모듈 시작
function startTheoryMode(questionType) {
    console.log('🎯 이론 모듈 시작:', questionType);
    
    if (!App || !App.theory) {
        console.error('❌ App.theory가 초기화되지 않았습니다!');
        alert('이론 모듈을 초기화할 수 없습니다. 페이지를 새로고침해주세요.');
        return;
    }
    
    initTheoryModule(questionType);
    
    // 기존 모드 시스템 사용하여 문제 로드
    loadTheoryQuestions();
}

// 이론 데이터 로드 (대시보드용)
async function loadTheoryData() {
    try {
        console.log('📥 이론 데이터 로드 시작 (대시보드용)...');
        
        const config = App.moduleConfig['theory'];
        if (!config) {
            throw new Error('theory 모듈 설정을 찾을 수 없습니다.');
        }
        
        console.log('📂 파일 로드:', config.itemsFile);
        
        const response = await fetch(config.itemsFile);
        if (!response.ok) {
            throw new Error(`파일 로드 실패: ${response.statusText}`);
        }
        
        const text = await response.text();
        const theoryItems = text.trim().split('\n').map(line => JSON.parse(line));
        
        console.log('✅ 로드된 이론 항목 수:', theoryItems.length);
        
        // App.theory에 저장
        App.theory.allTheoryData = theoryItems;
        
        // 카테고리별 통계 계산
        App.theory.categoryStats = calculateCategoryStats(theoryItems);
        
        console.log('✅ 이론 데이터 로드 완료');
        return theoryItems;
    } catch (error) {
        console.error('❌ 이론 데이터 로드 실패:', error);
        throw error;
    }
}

// 이론 문제 로드 (기존 시스템 활용)
async function loadTheoryQuestions() {
    try {
        console.log('📥 이론 문제 로드 시작...');
        
        const config = App.moduleConfig['theory'];
        if (!config) {
            throw new Error('theory 모듈 설정을 찾을 수 없습니다.');
        }
        
        console.log('📂 파일 로드:', config.itemsFile);
        
        // 원본 이론 데이터 로드
        const response = await fetch(config.itemsFile);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${config.itemsFile} 파일을 불러올 수 없습니다.`);
        }
        
        const text = await response.text();
        const theoryItems = text.trim().split('\n').map(line => JSON.parse(line));
        console.log('✅ 파싱된 이론 항목 수:', theoryItems.length);
        
        // 전체 이론 데이터 저장
        App.theory.allTheoryData = theoryItems;
        
        // 카테고리별 통계 계산
        App.theory.categoryStats = calculateCategoryStats(theoryItems);
        
        // 이론 데이터를 기존 문제 형식으로 변환
        const convertedQuestions = convertTheoryItemsToQuestions(theoryItems, App.theory.questionType);
        console.log('🔄 변환된 문제 수:', convertedQuestions.length);
        
        // App.state에 저장 (기존 시스템과 호환)
        App.state.allQuestions = convertedQuestions;
        allQuestions = App.state.allQuestions; // 하위 호환성
        
        // 기본 모드로 시작 (순차 풀기)
        App.state.currentMode = 'sequential';
        currentMode = 'sequential'; // 하위 호환성
        
        // 카테고리 대시보드 표시
        renderTheoryCategoryDashboard();
        
        App.state.currentIndex = 0;
        currentIndex = 0; // 하위 호환성
        
        // 기존 문제 표시 시스템 사용
        displayQuestion(App.state.currentQuestions[0]);
        updateStats();
        
        console.log(`✅ 이론 문제 ${convertedQuestions.length}개 로드 완료`);
        
    } catch (error) {
        console.error('❌ 이론 문제 로드 오류:', error);
        alert(`문제를 불러올 수 없습니다: ${error.message}`);
    }
}

// 기존 함수들은 theory-adapter.js로 이동됨

// 이론 모듈 초기화
function initTheoryModule(questionType) {
    App.theory.questionType = questionType;
    App.theory.usedQuestions.clear();
    
    console.log(`이론 모듈 초기화: ${questionType === 'objective' ? '객관식' : '주관식'}`);
}

// 이론 모듈은 이제 기존 displayQuestion 시스템을 사용함
// 기존 checkCurrentAnswer, showAnswerOnly, prevQuestion, nextQuestion, showExplanation 함수들을 그대로 사용

// 모든 기능은 기존 시스템 사용:
// - 정답 확인: checkCurrentAnswer()
// - 답 보기: showAnswerOnly() 
// - 이전/다음 문제: prevQuestion(), nextQuestion()
// - 해설 보기: showExplanation()
// - 문제 체크: markQuestion()
// - 학습 통계: updateStats()
// - 오답 관리: addWrongQuestion(), removeWrongQuestion()

// ===== 카테고리별 필터링 기능 =====

// 카테고리 설정 정보
const THEORY_CATEGORY_CONFIG = {
    '소프트웨어공학': {
        icon: 'fas fa-cogs',
        color: '#607D8B',
        name: '소프트웨어공학',
        count: 0
    },
    '데이터베이스': {
        icon: 'fas fa-database',
        color: '#2196F3',
        name: '데이터베이스',
        count: 0
    },
    '네트워크': {
        icon: 'fas fa-network-wired',
        color: '#9C27B0',
        name: '네트워크',
        count: 0
    },
    '운영체제': {
        icon: 'fas fa-desktop',
        color: '#FF9800',
        name: '운영체제',
        count: 0
    },
    '알고리즘': {
        icon: 'fas fa-project-diagram',
        color: '#FFC107',
        name: '알고리즘',
        count: 0
    },
    '자료구조': {
        icon: 'fas fa-sitemap',
        color: '#8BC34A',
        name: '자료구조',
        count: 0
    },
    '프로그래밍': {
        icon: 'fas fa-code',
        color: '#3F51B5',
        name: '프로그래밍',
        count: 0
    },
    '정보보안': {
        icon: 'fas fa-shield-alt',
        color: '#F44336',
        name: '정보보안',
        count: 0
    },
    '기타': {
        icon: 'fas fa-ellipsis-h',
        color: '#9E9E9E',
        name: '기타',
        count: 0
    }
};

// 카테고리별 문제 수 계산
function calculateCategoryStats(theoryData) {
    console.log('📊 카테고리별 통계 계산 중...');
    
    const stats = {};
    let totalCount = 0;
    
    // 각 카테고리별 문제 수 계산
    theoryData.forEach(item => {
        const category = item.category || '기타';
        stats[category] = (stats[category] || 0) + 1;
        totalCount++;
    });
    
    // THEORY_CATEGORY_CONFIG에 실제 개수 업데이트
    Object.keys(THEORY_CATEGORY_CONFIG).forEach(category => {
        THEORY_CATEGORY_CONFIG[category].count = stats[category] || 0;
    });
    
    console.log(`📋 전체 문제 수: ${totalCount}개`);
    console.log('📊 카테고리별 분포:', stats);
    
    return { stats, totalCount };
}

// 카테고리별 문제 필터링
function filterQuestionsByCategory(theoryData, category) {
    console.log(`🔍 카테고리 필터링: ${category}`);
    
    if (category === 'all') {
        return theoryData;
    }
    
    const filtered = theoryData.filter(item => item.category === category);
    console.log(`✅ 필터링 결과: ${filtered.length}개 문제`);
    
    return filtered;
}

// 랜덤 셔플 함수 (Fisher-Yates 알고리즘)
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// 범위별 문제 필터링
function filterQuestionsByRange(theoryData, startIndex, endIndex) {
    console.log(`📏 범위 필터링: ${startIndex + 1} ~ ${endIndex + 1}`);
    
    if (startIndex < 0) startIndex = 0;
    if (endIndex >= theoryData.length) endIndex = theoryData.length - 1;
    
    const filtered = theoryData.slice(startIndex, endIndex + 1);
    console.log(`✅ 범위 필터링 결과: ${filtered.length}개 문제`);
    
    return filtered;
}

// 카테고리별 학습 시작
function startCategoryStudy(category, mode = 'sequential') {
    console.log(`🎯 카테고리별 학습 시작: ${category} (${mode} 모드)`);
    
    if (!App.theory.allTheoryData || App.theory.allTheoryData.length === 0) {
        console.error('❌ 이론 데이터가 로드되지 않았습니다!');
        alert('데이터를 먼저 로드해주세요.');
        return;
    }
    
    // 카테고리별 필터링
    let filteredData = filterQuestionsByCategory(App.theory.allTheoryData, category);
    
    if (filteredData.length === 0) {
        alert('선택한 카테고리에 문제가 없습니다.');
        return;
    }
    
    // 모드별 처리
    switch (mode) {
        case 'random':
            filteredData = shuffleArray(filteredData);
            console.log('🔀 랜덤 모드 적용');
            break;
        case 'range':
            // 범위 설정 모달 표시
            showTheoryRangeModal(filteredData, category);
            return;
        default:
            console.log('📚 순차 모드 적용');
            break;
    }
    
    // 상태 업데이트
    App.theory.currentCategory = category;
    App.theory.studyMode = mode;
    App.theory.questionPool = filteredData;
    
    // 학습 시작
    startTheoryQuestions(filteredData);
}

// 이론 문제 학습 시작 (기존 함수 개선)
function startTheoryQuestions(questionsData) {
    console.log(`🚀 이론 문제 학습 시작: ${questionsData.length}개 문제`);
    
    // 기존 이론 모듈 시스템과 연동
    App.state.allQuestions = questionsData.map((item, index) => ({
        ...item,
        id: item.doc_id || `theory_${index + 1}`,
        question: `${item.term}의 의미는?`,
        answer: item.accept_answers[0] || item.term,
        explanation: item.description,
        category: item.category,
        subcategory: item.subcategory
    }));
    
    App.state.currentQuestions = App.state.allQuestions;
    App.state.currentIndex = 0;
    App.state.currentMode = 'theory_category';
    
    // 하위 호환성
    allQuestions = App.state.allQuestions;
    currentQuestions = App.state.currentQuestions;
    currentIndex = App.state.currentIndex;
    currentMode = App.state.currentMode;
    
    // 첫 번째 문제 표시
    if (App.state.currentQuestions.length > 0) {
        displayQuestion(App.state.currentQuestions[0]);
        updateStats();
    }
}

// 전역 함수로 노출 (HTML 및 menu.js에서 호출용)
window.loadTheoryData = loadTheoryData;
window.startTheoryMode = startTheoryMode;
window.startCategoryStudy = startCategoryStudy;
window.startTheoryQuestions = startTheoryQuestions;
