// 이론 데이터를 기존 문제 형식으로 변환하는 어댑터

// 이론 문제 변환 함수
function convertTheoryToQuestion(theoryItem, questionType, allTheoryItems) {
    const isDescriptionToTerm = Math.random() > 0.5;
    
    const questionText = generateQuestionText(theoryItem, isDescriptionToTerm);
    const choices = questionType === 'objective' ? generateChoices(theoryItem, isDescriptionToTerm, allTheoryItems) : [];
    const correctAnswer = isDescriptionToTerm ? theoryItem.term : theoryItem.description;
    
    // 디버깅 로그
    console.log('문제 변환:', {
        doc_id: theoryItem.doc_id,
        questionType: questionType,
        correctAnswer: correctAnswer,
        choices: choices,
        acceptAnswers: theoryItem.accept_answers
    });
    
    return {
        q_no: theoryItem.doc_id,
        question_text: questionText,
        choices: choices,
        answer: {
            keys: theoryItem.accept_answers || [correctAnswer],
            raw_text: theoryItem.accept_answers ? theoryItem.accept_answers.join(', ') : correctAnswer
        },
        explanation: generateExplanation(theoryItem),
        image_refs: [],
        table_refs: [],
        code_blocks: [],
        meta: {
            isTheoryQuestion: true,
            originalItem: theoryItem,
            questionType: questionType,
            isDescriptionToTerm: isDescriptionToTerm,
            acceptAnswers: theoryItem.accept_answers || [correctAnswer]
        }
    };
}

// 문제 텍스트 생성
function generateQuestionText(theoryItem, isDescriptionToTerm) {
    if (isDescriptionToTerm) {
        return `다음 설명에 해당하는 용어를 고르시오 (또는 작성하시오):\n\n${theoryItem.description}`;
    } else {
        return `다음 용어의 설명을 고르시오 (또는 작성하시오):\n\n${theoryItem.term}`;
    }
}

// 객관식 선택지 생성
function generateChoices(theoryItem, isDescriptionToTerm, allTheoryItems) {
    const correctAnswer = isDescriptionToTerm ? theoryItem.term : theoryItem.description;
    
    // 디버깅 로그
    console.log('선택지 생성:', {
        item: theoryItem.doc_id,
        correct: correctAnswer,
        isDescToTerm: isDescriptionToTerm
    });
    
    // 같은 subcategory 내에서 오답 3개 선택
    let wrongItems = allTheoryItems.filter(item => 
        item.doc_id !== theoryItem.doc_id && 
        item.subcategory === theoryItem.subcategory
    );
    
    // subcategory 내 항목이 부족하면 같은 category에서 선택
    if (wrongItems.length < 3) {
        wrongItems = allTheoryItems.filter(item => 
            item.doc_id !== theoryItem.doc_id && 
            item.category === theoryItem.category
        );
    }
    
    // 그래도 부족하면 전체에서 선택
    if (wrongItems.length < 3) {
        wrongItems = allTheoryItems.filter(item => item.doc_id !== theoryItem.doc_id);
    }
    
    // 랜덤하게 3개 선택
    const shuffled = shuffleArray(wrongItems);
    const selectedWrong = shuffled.slice(0, Math.min(3, wrongItems.length));
    
    // 선택지 배열 생성 (기존 형식과 동일 - 객체 배열)
    const choices = [];
    
    // 정답 추가
    choices.push({
        raw_key: 'A',
        text: correctAnswer
    });
    
    // 오답 추가
    selectedWrong.forEach((wrongItem, index) => {
        const wrongText = isDescriptionToTerm ? wrongItem.term : wrongItem.description;
        if (wrongText && wrongText.trim()) {
            choices.push({
                raw_key: String.fromCharCode(66 + index), // B, C, D
                text: wrongText
            });
        }
    });
    
    // 부족한 선택지는 기본값으로 채우기
    while (choices.length < 4) {
        choices.push({
            raw_key: String.fromCharCode(65 + choices.length), // A, B, C, D
            text: `선택지 ${choices.length + 1}`
        });
    }
    
    console.log('생성된 선택지:', choices);
    
    // 선택지 순서 섞기 (키는 다시 할당)
    const shuffledTexts = shuffleArray(choices.map(c => c.text));
    return shuffledTexts.map((text, index) => ({
        raw_key: String.fromCharCode(65 + index), // A, B, C, D
        text: text
    }));
}

// 해설 생성
function generateExplanation(theoryItem) {
    let explanation = `📖 상세 정보\n\n`;
    explanation += `용어: ${theoryItem.term}\n`;
    
    if (theoryItem.abbreviations && theoryItem.abbreviations.length > 0) {
        explanation += `약어: ${theoryItem.abbreviations.join(', ')}\n`;
    }
    
    explanation += `설명: ${theoryItem.description}\n`;
    explanation += `카테고리: ${theoryItem.category} > ${theoryItem.subcategory}`;
    
    return explanation;
}

// 이론 모듈용 답안 검증
function checkTheoryAnswer(userAnswers, question) {
    if (!question.meta || !question.meta.isTheoryQuestion) {
        // 기존 문제는 기존 검증 방식 사용
        return checkMultipleAnswer(userAnswers, question);
    }
    
    const acceptAnswers = question.meta.acceptAnswers || [];
    const userAnswer = Array.isArray(userAnswers) ? userAnswers[0] : userAnswers;
    
    if (!userAnswer || !userAnswer.trim()) {
        return false;
    }
    
    // 정규화하여 비교
    const normalizedUser = normalizeTheoryAnswer(userAnswer);
    
    return acceptAnswers.some(answer => {
        const normalizedAnswer = normalizeTheoryAnswer(answer);
        return normalizedUser === normalizedAnswer;
    });
}

// 이론 답안 정규화
function normalizeTheoryAnswer(answer) {
    if (!answer) return '';
    
    // 공백 제거 및 소문자 변환
    return answer.toString().toLowerCase().replace(/\s+/g, '').trim();
}

// 이론 문제 목록을 기존 형식으로 변환
function convertTheoryItemsToQuestions(theoryItems, questionType) {
    return theoryItems.map(item => convertTheoryToQuestion(item, questionType, theoryItems));
}

// 전역 함수로 노출
window.convertTheoryToQuestion = convertTheoryToQuestion;
window.convertTheoryItemsToQuestions = convertTheoryItemsToQuestions;
window.generateQuestionText = generateQuestionText;
window.generateChoices = generateChoices;
window.generateExplanation = generateExplanation;