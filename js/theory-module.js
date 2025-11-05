// 정처기 실기 이론 모듈 - 객관식/주관식 문제 생성 및 검증

// 이론 모듈 상태
App.theory = {
    questionType: 'objective', // 'objective' or 'subjective'
    currentQuestion: null,
    questionPool: [],
    usedQuestions: new Set()
};

// 이론 모듈 시작
function startTheoryMode(questionType) {
    initTheoryModule(questionType);
    
    // 문제 로드
    loadTheoryQuestions();
}

// 이론 문제 로드
async function loadTheoryQuestions() {
    try {
        const config = App.moduleConfig['theory'];
        
        // items.jsonl 로드
        const response = await fetch(config.itemsFile);
        const text = await response.text();
        const questions = text.trim().split('\n').map(line => JSON.parse(line));
        
        App.state.allQuestions = questions;
        allQuestions = App.state.allQuestions; // 하위 호환성
        
        // 랜덤 섞기
        App.state.currentQuestions = shuffleArray([...questions]);
        currentQuestions = App.state.currentQuestions; // 하위 호환성
        
        App.state.currentIndex = 0;
        currentIndex = 0; // 하위 호환성
        
        // 첫 문제 표시
        displayTheoryQuestion(App.state.currentQuestions[0]);
        updateStats();
        
        console.log(`이론 문제 ${questions.length}개 로드 완료`);
        
    } catch (error) {
        console.error('이론 문제 로드 오류:', error);
        showMessage('문제를 불러올 수 없습니다.');
    }
}

// 문제 생성 (객관식 또는 주관식)
function generateTheoryQuestion(item) {
    // 50% 확률로 설명→용어 or 용어→설명 결정
    const isDescriptionToTerm = Math.random() > 0.5;
    
    const question = {
        item: item,
        isDescriptionToTerm: isDescriptionToTerm,
        questionText: isDescriptionToTerm ? item.description : item.term,
        correctAnswer: isDescriptionToTerm ? item.term : item.description,
        acceptAnswers: item.accept_answers || [item.term],
        category: item.category,
        subcategory: item.subcategory
    };
    
    // 객관식인 경우 오답 생성
    if (App.theory.questionType === 'objective') {
        question.choices = generateChoices(item, isDescriptionToTerm);
    }
    
    return question;
}

// 객관식 선택지 생성
function generateChoices(item, isDescriptionToTerm) {
    const allItems = App.state.allQuestions;
    const correctAnswer = isDescriptionToTerm ? item.term : item.description;
    
    // 같은 subcategory 내에서 오답 3개 선택
    let wrongItems = allItems.filter(q => 
        q.doc_id !== item.doc_id && 
        q.subcategory === item.subcategory
    );
    
    // subcategory 내 항목이 부족하면 같은 category에서 선택
    if (wrongItems.length < 3) {
        wrongItems = allItems.filter(q => 
            q.doc_id !== item.doc_id && 
            q.category === item.category
        );
    }
    
    // 그래도 부족하면 전체에서 선택
    if (wrongItems.length < 3) {
        wrongItems = allItems.filter(q => q.doc_id !== item.doc_id);
    }
    
    // 랜덤하게 3개 선택
    const shuffled = shuffleArray(wrongItems);
    const selectedWrong = shuffled.slice(0, 3);
    
    // 선택지 배열 생성
    const choices = [
        { text: correctAnswer, isCorrect: true }
    ];
    
    selectedWrong.forEach(wrongItem => {
        const wrongText = isDescriptionToTerm ? wrongItem.term : wrongItem.description;
        choices.push({ text: wrongText, isCorrect: false });
    });
    
    // 선택지 순서 섞기
    return shuffleArray(choices);
}

// 주관식 답안 검증
function validateSubjectiveAnswer(userInput, correctAnswers) {
    // 공백 제거 및 소문자 변환
    const normalized = userInput.trim().toLowerCase().replace(/\s+/g, '');
    
    // 정답 배열과 비교
    return correctAnswers.some(ans => {
        const normalizedAns = ans.toLowerCase().replace(/\s+/g, '');
        return normalizedAns === normalized;
    });
}

// 이론 모듈 초기화
function initTheoryModule(questionType) {
    App.theory.questionType = questionType;
    App.theory.usedQuestions.clear();
    
    console.log(`이론 모듈 초기화: ${questionType === 'objective' ? '객관식' : '주관식'}`);
}

// 이론 문제 표시
function displayTheoryQuestion(item) {
    const question = generateTheoryQuestion(item);
    App.theory.currentQuestion = question;
    
    const container = document.getElementById('questionContainer');
    if (!container) return;
    
    // 문제 번호 및 카테고리 표시
    const headerHTML = `
        <div class="question-header">
            <div class="question-meta">
                <span class="question-category">${question.category}</span>
                ${question.subcategory !== question.category ? `<span class="question-subcategory">${question.subcategory}</span>` : ''}
            </div>
            <div class="question-no">${item.doc_id}</div>
        </div>
    `;
    
    // 문제 텍스트
    const questionPrompt = question.isDescriptionToTerm ? 
        '다음 설명에 해당하는 용어를 고르시오 (또는 작성하시오):' : 
        '다음 용어의 설명을 고르시오 (또는 작성하시오):';
    
    const questionTextHTML = `
        <div class="question-text">
            <p style="font-weight: bold; color: #667eea; margin-bottom: 15px;">${questionPrompt}</p>
            <p>${question.questionText}</p>
        </div>
    `;
    
    // 객관식/주관식에 따른 답안 입력 영역
    let answerHTML = '';
    
    if (App.theory.questionType === 'objective') {
        // 객관식 선택지
        answerHTML = '<div class="choices-list">';
        question.choices.forEach((choice, index) => {
            const choiceKey = String.fromCharCode(65 + index); // A, B, C, D
            answerHTML += `
                <div class="choice-item" onclick="selectTheoryChoice(${index})">
                    <span class="choice-key">${choiceKey}</span>
                    <span class="choice-text">${choice.text}</span>
                </div>
            `;
        });
        answerHTML += '</div>';
    } else {
        // 주관식 입력 필드
        answerHTML = `
            <div class="subjective-answer">
                <input type="text" id="subjectiveInput" placeholder="정답을 입력하세요" 
                       class="subjective-input" onkeypress="if(event.key==='Enter') checkTheorySubjective()">
                <p class="subjective-hint">💡 힌트: 여러 답안 가능 (용어/약어 모두 인정, 대소문자 무관)</p>
                <button class="submit-btn" onclick="checkTheorySubjective()" style="margin-top: 15px;">
                    <i class="fas fa-check"></i> 정답 확인
                </button>
            </div>
        `;
    }
    
    container.innerHTML = `<div class="question-card">${headerHTML}${questionTextHTML}${answerHTML}</div>`;
}

// 객관식 선택
function selectTheoryChoice(choiceIndex) {
    const choices = document.querySelectorAll('.choice-item');
    choices.forEach((choice, idx) => {
        choice.classList.remove('selected');
        if (idx === choiceIndex) {
            choice.classList.add('selected');
        }
    });
    
    // 정답 확인
    checkTheoryObjective(choiceIndex);
}

// 객관식 정답 확인
function checkTheoryObjective(selectedIndex) {
    const question = App.theory.currentQuestion;
    if (!question) return;
    
    const isCorrect = question.choices[selectedIndex].isCorrect;
    
    // 결과 표시
    showTheoryResult(isCorrect, question);
    
    // 통계 업데이트
    if (isCorrect) {
        App.state.stats.correct++;
    } else {
        App.state.stats.wrong++;
        App.state.stats.wrongQuestions.push(question.item.doc_id);
    }
    
    updateStats();
}

// 주관식 정답 확인
function checkTheorySubjective() {
    const input = document.getElementById('subjectiveInput');
    if (!input) return;
    
    const userAnswer = input.value.trim();
    if (!userAnswer) {
        alert('답을 입력해주세요.');
        return;
    }
    
    const question = App.theory.currentQuestion;
    if (!question) return;
    
    const isCorrect = validateSubjectiveAnswer(userAnswer, question.acceptAnswers);
    
    // 결과 표시
    showTheoryResult(isCorrect, question, userAnswer);
    
    // 통계 업데이트
    if (isCorrect) {
        App.state.stats.correct++;
    } else {
        App.state.stats.wrong++;
        App.state.stats.wrongQuestions.push(question.item.doc_id);
    }
    
    updateStats();
}

// 결과 표시
function showTheoryResult(isCorrect, question, userAnswer = null) {
    const resultSection = document.createElement('div');
    resultSection.className = isCorrect ? 'result-section result-correct' : 'result-section result-incorrect';
    
    let resultHTML = `
        <div class="result-badge">
            ${isCorrect ? '✅ 정답입니다!' : '❌ 오답입니다'}
        </div>
    `;
    
    if (!isCorrect && userAnswer) {
        resultHTML += `
            <div class="user-answer">
                <strong>입력한 답:</strong> ${userAnswer}
            </div>
        `;
    }
    
    if (!isCorrect) {
        resultHTML += `
            <div class="correct-answer">
                <strong>정답:</strong> ${question.correctAnswer}
                ${question.acceptAnswers.length > 1 ? `<br><small>(인정 답안: ${question.acceptAnswers.join(', ')})</small>` : ''}
            </div>
        `;
    }
    
    // 해설 (항상 표시)
    const item = question.item;
    resultHTML += `
        <div class="explanation">
            <h4>📖 상세 정보</h4>
            <div class="explanation-content">
                <p><strong>용어:</strong> ${item.term}</p>
                ${item.abbreviations && item.abbreviations.length > 0 ? `<p><strong>약어:</strong> ${item.abbreviations.join(', ')}</p>` : ''}
                <p><strong>설명:</strong> ${item.description}</p>
                <p><strong>카테고리:</strong> ${item.category} > ${item.subcategory}</p>
            </div>
        </div>
        <div style="text-align: center; margin-top: 25px;">
            <button class="nav-btn" onclick="nextTheoryQuestion()">
                <i class="fas fa-arrow-right"></i> 다음 문제
            </button>
        </div>
    `;
    
    resultSection.innerHTML = resultHTML;
    
    const questionCard = document.querySelector('.question-card');
    if (questionCard) {
        questionCard.appendChild(resultSection);
    }
}


// 다음 문제로 이동
function nextTheoryQuestion() {
    App.state.currentIndex++;
    
    if (App.state.currentIndex >= App.state.currentQuestions.length) {
        // 모든 문제 완료
        showTheoryComplete();
        return;
    }
    
    const nextItem = App.state.currentQuestions[App.state.currentIndex];
    displayTheoryQuestion(nextItem);
}

// 이론 학습 완료 화면
function showTheoryComplete() {
    const questionCard = document.querySelector('.question-card');
    if (!questionCard) return;
    
    const total = App.state.stats.correct + App.state.stats.wrong;
    const accuracy = total > 0 ? (App.state.stats.correct / total * 100).toFixed(1) : 0;
    
    questionCard.innerHTML = `
        <div class="complete-screen">
            <div class="complete-icon">🎉</div>
            <h2>학습 완료!</h2>
            <div class="complete-stats">
                <div class="stat-item">
                    <div class="stat-value">${total}</div>
                    <div class="stat-label">풀이한 문제</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${App.state.stats.correct}</div>
                    <div class="stat-label">맞힌 문제</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${accuracy}%</div>
                    <div class="stat-label">정답률</div>
                </div>
            </div>
            <button class="restart-btn" onclick="restartTheory()">
                <i class="fas fa-redo"></i> 다시 시작
            </button>
        </div>
    `;
}

// 이론 학습 다시 시작
function restartTheory() {
    App.state.currentIndex = 0;
    App.state.stats.correct = 0;
    App.state.stats.wrong = 0;
    App.state.stats.wrongQuestions = [];
    
    // 모드 선택 화면으로 돌아가기
    showModeSelection();
}

