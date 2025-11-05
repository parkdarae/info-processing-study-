// 정답 검증 함수들

// 정규화 함수
function normalizeAnswer(answer) {
    // 대소문자 무시
    answer = answer.toLowerCase().trim();
    
    // 띄어쓰기 제거
    answer = answer.replace(/\s/g, '');
    
    // 동의어 변환
    for (let [key, values] of Object.entries(App.synonyms)) {
        if (values.includes(answer)) {
            answer = key;
            break;
        }
    }
    
    return answer;
}

// 키 매핑
function mapAnswerKey(input, choices) {
    // 숫자 변환
    const numMap = {'1': '1', '2': '2', '3': '3', '4': '4', 
                   '①': '1', '②': '2', '③': '3', '④': '4',
                   'ㄱ': '1', 'ㄴ': '2', 'ㄷ': '3', 'ㄹ': '4',
                   'a': '1', 'b': '2', 'c': '3', 'd': '4'};
    
    const lowerInput = input.toLowerCase().trim();
    if (numMap[lowerInput]) {
        return numMap[lowerInput];
    }
    
    // 복수 정답 처리
    const matches = input.match(/[1-4①②③④ㄱㄴㄷㄹabcd]/g);
    if (matches && matches.length > 1) {
        return matches.map(m => numMap[m.toLowerCase()]).filter(Boolean);
    }
    
    return lowerInput;
}

// 정답 체크 (단일 답안)
function checkAnswer(userAnswer, correctAnswer, choices) {
    if (!userAnswer) return false;
    
    // 서술형 답인 경우 (choices가 없거나 0개인 경우)
    if (!choices || choices.length === 0) {
        // 답안 배열 처리
        if (correctAnswer.keys && correctAnswer.keys.length > 0) {
            // 첫 번째 답안으로 비교
            const correctText = normalizeAnswerText(correctAnswer.keys[0]);
            const userText = normalizeAnswerText(userAnswer);
            return checkAnswerMatch(userText, correctText);
        } else {
            // raw_text로 비교
            const correctText = normalizeAnswerText(correctAnswer.raw_text);
            const userText = normalizeAnswerText(userAnswer);
            return checkAnswerMatch(userText, correctText);
        }
    }
    
    // 객관식 답 체크
    const user = mapAnswerKey(userAnswer, choices);
    const correct = correctAnswer.keys;
    
    // 복수 정답
    if (Array.isArray(user)) {
        return JSON.stringify(user.sort()) === JSON.stringify(correct.sort());
    }
    
    // 단일 정답
    return correct.includes(user);
}

// 문자열 유사도 계산
function calculateSimilarity(str1, str2) {
    const longer = str1.length > str2.length ? str1 : str2;
    const shorter = str1.length > str2.length ? str2 : str1;
    
    if (longer.length === 0) return 1.0;
    
    const editDistance = levenshteinDistance(longer, shorter);
    return (longer.length - editDistance) / longer.length;
}

// 레벤슈타인 거리 계산
function levenshteinDistance(str1, str2) {
    const matrix = [];
    
    for (let i = 0; i <= str2.length; i++) {
        matrix[i] = [i];
    }
    
    for (let j = 0; j <= str1.length; j++) {
        matrix[0][j] = j;
    }
    
    for (let i = 1; i <= str2.length; i++) {
        for (let j = 1; j <= str1.length; j++) {
            if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }
    
    return matrix[str2.length][str1.length];
}

// 복수 답안 체크 (스마트 매칭)
function checkMultipleAnswer(userAnswers, question) {
    const correctAnswers = question.answer.keys || [];
    
    console.log('=== 복수 답안 체크 ===');
    console.log('문제:', question.q_no);
    console.log('입력:', userAnswers);
    console.log('정답:', correctAnswers);
    
    if (userAnswers.length !== correctAnswers.length) {
        console.log('❌ 답안 개수 불일치');
        return false;
    }
    
    // Q060 특별 처리: 숫자만 비교
    if (question.q_no === 'Q060') {
        console.log('🔢 Q060 숫자 전용 매칭');
        for (let i = 0; i < userAnswers.length; i++) {
            const userDigits = (userAnswers[i] || '').toString().replace(/[^0-9]/g, '');
            const correctDigits = (correctAnswers[i] || '').toString().replace(/[^0-9]/g, '');
            console.log(`  [${i+1}] "${userDigits}" === "${correctDigits}" ?`, userDigits === correctDigits);
            if (userDigits !== correctDigits) {
                console.log('❌ 불일치');
                return false;
            }
        }
        console.log('✅ Q060 정답!');
        return true;
    }
    
    // 각 답안 비교 (순서 중요)
    for (let i = 0; i < userAnswers.length; i++) {
        const user = normalizeAnswerText(userAnswers[i]);
        const correct = normalizeAnswerText(correctAnswers[i]);
        
        console.log(`답안 ${i+1}:`);
        console.log('  입력:', user);
        console.log('  정답:', correct);
        
        // 키워드 기반 매칭
        const match = checkAnswerMatch(user, correct);
        console.log('  결과:', match ? '✅' : '❌');
        
        if (!match) {
            return false;
        }
    }
    
    console.log('✅ 정답!');
    return true;
}

// 답안 텍스트 정규화
function normalizeAnswerText(text) {
    if (!text) return '';
    
    // 소문자로 변환
    text = text.toLowerCase();
    
    // 원문자를 한글 자음으로 변환 (㉠→ㄱ, ㉡→ㄴ, ㉢→ㄷ, ㉣→ㄹ, ㉤→ㅁ, ㉥→ㅂ, ㉦→ㅅ, ㉧→ㅇ, ㉨→ㅈ)
    const circledToJamo = {
        '㉠': 'ㄱ', '㉡': 'ㄴ', '㉢': 'ㄷ', '㉣': 'ㄹ', '㉤': 'ㅁ',
        '㉥': 'ㅂ', '㉦': 'ㅅ', '㉧': 'ㅇ', '㉨': 'ㅈ', '㉩': 'ㅊ'
    };
    text = text.replace(/[㉠-㉩]/g, match => circledToJamo[match] || match);
    
    // 괄호 안 내용 제거: 관계(Relationship) -> 관계
    text = text.replace(/\([^)]*\)/g, '');
    
    // 띄어쓰기 제거
    text = text.replace(/\s+/g, '');
    
    // 기타 특수문자 정리 (쉼표, 화살표, 하이픈, 점 등)
    text = text.replace(/[•·,→\-\.]/g, '');
    
    return text.trim();
}

// 답안 매칭 체크 (스마트 매칭)
function checkAnswerMatch(user, correct) {
    // 정확 일치
    if (user === correct) {
        return true;
    }
    
    // 숫자만 있는 경우 (60번 문제 등)
    const userDigits = user.replace(/[^0-9]/g, '');
    const correctDigits = correct.replace(/[^0-9]/g, '');
    
    if (userDigits && correctDigits && userDigits === correctDigits) {
        return true;
    }
    
    // 키워드 추출 (한글/영문 단어)
    const getKeywords = (text) => {
        return text.match(/[가-힣]+|[a-z]+/gi) || [];
    };
    
    const userKeywords = getKeywords(user);
    const correctKeywords = getKeywords(correct);
    
    // 하나라도 키워드가 없으면 단순 비교
    if (userKeywords.length === 0 || correctKeywords.length === 0) {
        return user === correct;
    }
    
    // 키워드 매칭 수
    let matches = 0;
    for (const keyword of userKeywords) {
        if (correctKeywords.some(ck => ck.includes(keyword) || keyword.includes(ck))) {
            matches++;
        }
    }
    
    // 50% 이상 매칭
    const matchRate = matches / Math.max(userKeywords.length, correctKeywords.length);
    return matchRate >= 0.5;
}

