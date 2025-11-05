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
        usedQuestions: new Set()
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
        
        // 이론 데이터를 기존 문제 형식으로 변환
        const convertedQuestions = convertTheoryItemsToQuestions(theoryItems, App.theory.questionType);
        console.log('🔄 변환된 문제 수:', convertedQuestions.length);
        
        // App.state에 저장 (기존 시스템과 호환)
        App.state.allQuestions = convertedQuestions;
        allQuestions = App.state.allQuestions; // 하위 호환성
        
        // 기본 모드로 시작 (순차 풀기)
        App.state.currentMode = 'sequential';
        currentMode = 'sequential'; // 하위 호환성
        
        // 기존 모드 필터링 시스템 사용
        App.state.currentQuestions = filterQuestionsByMode('sequential');
        currentQuestions = App.state.currentQuestions; // 하위 호환성
        
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

