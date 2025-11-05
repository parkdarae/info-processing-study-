// 문제 표시 및 답안 체크 관련 함수들

// 문제 표시
function displayQuestion(question) {
    console.log('[displayQuestion] 호출됨:', question.q_no);
    console.log('[displayQuestion] image_refs:', question.image_refs);
    console.log('[displayQuestion] code_blocks:', question.code_blocks);
    
    const container = document.getElementById('questionContainer');
    
    let html = `
        <div class="question-card">
            <div class="question-header">
                <div class="question-no">${question.q_no}</div>
                <button class="btn btn-secondary" onclick="markQuestion('${question.q_no}')">
                    <i class="fas fa-star"></i> 체크
                </button>
            </div>
            <div class="question-text">${formatCodeBlocks(question.question_text)}</div>
    `;
    
    // 코드 블록 표시
    if (question.code_blocks && question.code_blocks.length > 0) {
        for (let codeBlock of question.code_blocks) {
            const language = codeBlock.language || 'text';
            const code = escapeHtml(codeBlock.code);
            html += `
                <div class="code-block-container">
                    <div class="code-header">
                        <span class="code-language">${language.toUpperCase()}</span>
                    </div>
                    <pre class="code-block"><code class="language-${language}">${code}</code></pre>
                </div>
            `;
        }
    }
    
    // 이미지 표시
    if (question.image_refs && question.image_refs.length > 0) {
        console.log('[이미지] image_refs:', question.image_refs);
        for (let img of question.image_refs) {
            // JSONL에 이미 전체 경로가 있으므로 그대로 사용
            const imgPath = img;
            console.log('[이미지] 렌더링:', imgPath);
            html += `
                <div class="image-container">
                    <img src="${imgPath}" class="image-preview" alt="문제 이미지" 
                         onerror="console.error('❌ 이미지 로딩 실패:', this.src); this.style.border='3px solid red';"
                         onload="console.log('✅ 이미지 로딩 성공:', this.src);">
                </div>
            `;
        }
    }
    
    // 표 표시
    if (question.table_refs && question.table_refs.length > 0) {
        for (let tableRef of question.table_refs) {
            const table = App.state.allTables[tableRef];
            if (table) {
                html += '<div class="table-container">';
                if (table.caption && table.caption.trim() !== '') {
                    html += `<div class="table-caption">${escapeHtml(table.caption)}</div>`;
                }
                html += '<table class="question-table">';
                
                // 헤더 (header 또는 headers 필드 모두 지원)
                const headerData = table.headers || table.header;
                if (headerData && headerData.length > 0) {
                    html += '<thead><tr>';
                    for (let cell of headerData) {
                        html += `<th>${escapeHtml(cell)}</th>`;
                    }
                    html += '</tr></thead>';
                }
                
                // 바디
                html += '<tbody>';
                if (table.rows && table.rows.length > 0) {
                    for (let row of table.rows) {
                        html += '<tr>';
                        for (let cell of row) {
                            // 셀 내용이 이미지 파일명인지 확인
                            if (cell && typeof cell === 'string' && (cell.endsWith('.png') || cell.endsWith('.jpg') || cell.endsWith('.jpeg') || cell.endsWith('.gif'))) {
                                html += `<td><img src="images/${cell}" class="table-image" alt=""></td>`;
                            } else if (cell && typeof cell === 'string' && cell.includes('<strong>')) {
                                // HTML 태그가 포함된 경우 이스케이프하지 않음
                                html += `<td>${cell}</td>`;
                            } else {
                                // 일반 텍스트는 이스케이프
                                html += `<td>${escapeHtml(cell).replace(/\n/g, '<br>')}</td>`;
                            }
                        }
                        html += '</tr>';
                    }
                }
                html += '</tbody></table></div>';
                
                // 표 뒤에 추가 텍스트가 있으면 표시
                if (table.after_text) {
                    html += `<div class="table-after-text">${escapeHtml(table.after_text).replace(/\n/g, '<br>')}</div>`;
                }
            }
        }
    }
    
    // Q062 보기 (테이블 뒤)
    if (question.q_no === 'Q062') {
        html += `
            <div class="choices-section" style="margin-top: 20px;">
                <strong>&lt;보기&gt;</strong><br>
                • Equivalence Partition<br>
                • Boundary Value Analysis<br>
                • Condition Test<br>
                • Cause-Effect Graph<br>
                • Error Guess<br>
                • Comparison Test<br>
                • Base Path Test<br>
                • Loop Test<br>
                • Data Flow Test
            </div>
        `;
    }
    
    // 선택지 표시
    if (question.choices && question.choices.length > 0) {
        html += '<div class="choices">';
        for (let choice of question.choices) {
            html += `
                <div class="choice-item" onclick="selectChoice(this)">
                    <span class="choice-key">${choice.raw_key}</span>
                    <span class="choice-text">${escapeHtml(choice.text)}</span>
                </div>
            `;
        }
        html += '</div>';
    }
    
    // 복수 답안 개수 확인
    let numAnswers = 1;
    
    // 1. 괄호 안 번호 범위 추출: (①~⑤)
    const rangeMatch = question.question_text.match(/\([\s]*([①-⑳])[\s]*~[\s]*([①-⑳])[\s]*\)/);
    if (rangeMatch) {
        const startNum = rangeMatch[1].charCodeAt(0) - 0x2460 + 1;
        const endNum = rangeMatch[2].charCodeAt(0) - 0x2460 + 1;
        numAnswers = endNum - startNum + 1;
    }
    
    // 2. 괄호 안 번호 개수 추출: (①, ②) 또는 (① ② ③)
    if (numAnswers === 1) {
        const bracketNumbers = question.question_text.match(/\([\s]*([①-⑳][\s,]*[\s①-⑳]*)+\s*\)/);
        if (bracketNumbers) {
            const matches = bracketNumbers[0].match(/[①-⑳]/g);
            if (matches && matches.length > 1) {
                numAnswers = matches.length;
            }
        }
    }
    
    // 3. 정답 배열 길이로 확인
    if (numAnswers === 1 && question.answer && question.answer.keys && question.answer.keys.length > 1) {
        numAnswers = question.answer.keys.length;
    }
    
    // 16번, 17번은 특수: 순차 입력 모드 (1개 입력창)
    if (question.q_no === 'Q016' || question.q_no === 'Q017') {
        numAnswers = 1;
    }
    
    // 입력 필드 생성
    if (numAnswers > 1) {
        // 복수 답안 입력창
        html += `<div class="multiple-answers">`;
        
        // 특정 문제는 커스텀 라벨
        const customLabels = {
            'Q013': ['카디널리티:', '디그리:'],
            'Q008': ['계산식:', '답:'],
            'Q122': ['LEVEL:']
        };
        
        for (let i = 0; i < numAnswers; i++) {
            let label;
            
            if (customLabels[question.q_no] && customLabels[question.q_no][i]) {
                label = customLabels[question.q_no][i];
            } else {
                const num = String.fromCharCode(0x2460 + i); // ①, ②, ...
                label = `${num}:`;
            }
            
            html += `
                <div class="answer-item">
                    <label>${label}</label>
                    <input type="text" class="answer-input-small" id="answerInput_${i}" 
                           placeholder="답 입력">
                </div>
            `;
        }
        html += `</div>`;
        
        // 특수문자가 필요한지 확인 (정답에 특수문자가 포함되어 있는 경우만)
        const hasSymbols = question.answer && question.answer.keys && 
            question.answer.keys.some(ans => /[∪―×π▷◁∩÷Δ]/.test(ans));
        
        if (hasSymbols) {
            html += `
                <div class="symbol-buttons">
                    <strong>자주 사용하는 기호:</strong>
                    <button class="symbol-btn" onclick="insertSymbol('∪')">∪</button>
                    <button class="symbol-btn" onclick="insertSymbol('―')">―</button>
                    <button class="symbol-btn" onclick="insertSymbol('×')">×</button>
                    <button class="symbol-btn" onclick="insertSymbol('π')">π</button>
                    <button class="symbol-btn" onclick="insertSymbol('▷◁')">▷◁</button>
                    <button class="symbol-btn" onclick="insertSymbol('∩')">∩</button>
                    <button class="symbol-btn" onclick="insertSymbol('÷')">÷</button>
                    <button class="symbol-btn" onclick="insertSymbol('Δ')">Δ</button>
                </div>
            `;
        }
    } else {
        // 단일 답안 입력창
        const placeholder = (question.q_no === 'Q016' || question.q_no === 'Q017') ? '특수문자 버튼을 클릭하여 입력하세요' : '정답을 입력하세요 (예: 1, 2, a, b, ㄱ, ①)';
        const isReadonly = question.q_no === 'Q016' || question.q_no === 'Q017';
        html += `
            <input type="text" class="answer-input" id="answerInput_0" 
                   placeholder="${placeholder}" ${isReadonly ? 'readonly' : ''}>
        `;
    }
    
    // 16번, 17번은 특수문자 버튼 표시
    if (question.q_no === 'Q016' || question.q_no === 'Q017') {
        html += `
            <div class="symbol-buttons">
                <strong>기호를 순서대로 클릭하세요 (다시 클릭하면 제거):</strong>
                <button class="symbol-btn" onclick="insertSymbol('∪')">∪</button>
                <button class="symbol-btn" onclick="insertSymbol('―')">―</button>
                <button class="symbol-btn" onclick="insertSymbol('×')">×</button>
                <button class="symbol-btn" onclick="insertSymbol('π')">π</button>
                <button class="symbol-btn" onclick="insertSymbol('▷◁')">▷◁</button>
                <button class="symbol-btn" onclick="insertSymbol('∩')">∩</button>
                <button class="symbol-btn" onclick="insertSymbol('÷')">÷</button>
                <button class="symbol-btn" onclick="insertSymbol('Δ')">Δ</button>
            </div>
        `;
    }
    
    html += `
            <div class="action-buttons">
                <button class="btn btn-primary" onclick="checkCurrentAnswer()">
                    <i class="fas fa-check"></i> 정답 확인
                </button>
                <button class="btn" onclick="showAnswerOnly()" style="background: #17a2b8; color: white;">
                    <i class="fas fa-eye"></i> 답 보기
                </button>
                <button class="btn btn-secondary" onclick="prevQuestion()">
                    <i class="fas fa-arrow-left"></i> 이전 문제
                </button>
                <button class="btn btn-secondary" onclick="nextQuestion()">
                    <i class="fas fa-arrow-right"></i> 다음 문제
                </button>
                <button class="btn btn-secondary" onclick="showExplanation()">
                    <i class="fas fa-lightbulb"></i> 해설 보기
                </button>
                <button class="btn btn-video" onclick="openVideo()" id="videoBtn" style="display: none;">
                    <i class="fab fa-youtube"></i> 동영상 설명
                </button>
            </div>
            <div class="result-section" id="resultSection" style="display: none;"></div>
            <div class="explanation" id="explanationDiv"></div>
    </div>
    `;
    
    container.innerHTML = html;
    
    // 동영상 버튼 표시 업데이트
    setTimeout(() => {
        updateVideoButton();
    }, 0);
}

// 정답 확인
function checkCurrentAnswer() {
    const question = App.state.currentQuestions[App.state.currentIndex];
    const questionId = question.q_no;
    
    // 이미 답변했으면 무시
    if (App.state.answeredQuestions.has(questionId)) {
        console.log('이미 답변한 문제입니다.');
        return;
    }
    
    // 복수 답안인지 확인
    let userAnswers = [];
    const answerInput0 = document.getElementById('answerInput_0');
    
    if (answerInput0) {
        // 모든 입력창 확인 (0부터 시작)
        for (let i = 0; i < 10; i++) {
            const input = document.getElementById(`answerInput_${i}`);
            if (input) {
                userAnswers.push(input.value);
            }
        }
    }
    
    // 답변 입력 확인
    if (userAnswers.length === 0 || userAnswers.every(a => !a || !a.trim())) {
        alert('답을 입력해주세요.');
        return;
    }
    
    const isCorrect = checkMultipleAnswer(userAnswers, question);
    const resultSection = document.getElementById('resultSection');
    
    // 이미 답변했다고 표시
    App.state.answeredQuestions.add(questionId);
    answeredQuestions.add(questionId); // 하위 호환성
    
    // 결과 영역 표시
    resultSection.style.display = 'block';
    
    if (isCorrect) {
        resultSection.className = 'result-section result-correct show';
        resultSection.innerHTML = '<i class="fas fa-check-circle"></i> <strong>정답입니다!</strong>';
        App.state.stats.correct++;
        stats.correct++; // 하위 호환성
        removeWrongQuestion(question.q_no);
    } else {
        resultSection.className = 'result-section result-incorrect show';
        
        // 정답 텍스트 처리 (괄호 제거)
        let answerText = question.answer.raw_text || '정답 없음';
        
        // 괄호 안 내용 제거
        answerText = answerText.replace(/\([^)]*\)/g, '');
        // • 제거
        answerText = answerText.replace(/[•]/g, '');
        // 여러 공백을 하나로
        answerText = answerText.replace(/\s+/g, ' ').trim();
        
        resultSection.innerHTML = `
            <i class="fas fa-times-circle"></i> <strong>오답입니다.</strong><br>
            <strong>정답:</strong> ${formatCodeBlocks(answerText)}
        `;
        App.state.stats.wrong++;
        stats.wrong++; // 하위 호환성
        addWrongQuestion(question.q_no);
    }
    
    // LocalStorage에 저장
    saveProgress();
    updateStats();
}

// 특수문자 입력 함수
function insertSymbol(symbol) {
    const question = App.state.currentQuestions[App.state.currentIndex];
    
    // 16번, 17번: 순차 입력 모드
    if (question.q_no === 'Q016' || question.q_no === 'Q017') {
        const input = document.getElementById('answerInput_0');
        if (!input) return;
        
        // 같은 기호를 다시 클릭하면 제거
        const currentSymbols = App.state.symbolInputOrder.symbols;
        const symbolIndex = currentSymbols.indexOf(symbol);
        
        if (symbolIndex > -1) {
            // 이미 있는 기호이면 제거
            currentSymbols.splice(symbolIndex, 1);
            App.state.symbolInputOrder.inputIndex = currentSymbols.length;
        } else {
            // 새로운 기호 추가 (16번은 최대 5개, 17번은 1개)
            const maxSymbols = question.q_no === 'Q016' ? 5 : 1;
            
            // 17번은 1개만 입력 가능 (이미 입력된 기호가 있으면 교체)
            if (question.q_no === 'Q017' && currentSymbols.length > 0) {
                currentSymbols[0] = symbol;
                App.state.symbolInputOrder.inputIndex = 1;
            } else if (currentSymbols.length < maxSymbols) {
                currentSymbols.push(symbol);
                App.state.symbolInputOrder.inputIndex = currentSymbols.length;
            }
        }
        
        // 입력창에 표시
        input.value = currentSymbols.join(', ');
        // 하위 호환성
        symbolInputOrder = App.state.symbolInputOrder;
        return;
    }
    
    // 다른 문제: 일반 입력
    const answerInputs = [];
    for (let i = 0; i < 10; i++) {
        const input = document.getElementById(`answerInput_${i}`);
        if (input) {
            answerInputs.push(input);
        }
    }
    
    if (answerInputs.length === 0) return;
    
    const activeElement = document.activeElement;
    if (activeElement && activeElement.classList.contains('answer-input-small')) {
        const selectionStart = activeElement.selectionStart;
        const selectionEnd = activeElement.selectionEnd;
        const value = activeElement.value;
        
        activeElement.value = value.substring(0, selectionStart) + symbol + value.substring(selectionEnd);
        activeElement.focus();
        activeElement.setSelectionRange(selectionStart + symbol.length, selectionStart + symbol.length);
    }
}

// 이전 문제
function prevQuestion() {
    App.state.currentIndex--;
    currentIndex = App.state.currentIndex; // 하위 호환성
    
    if (App.state.currentIndex < 0) {
        App.state.currentIndex = App.state.currentQuestions.length - 1;
        currentIndex = App.state.currentIndex;
        showMessage('첫 번째 문제입니다. 마지막 문제로 이동합니다.');
    }
    displayQuestion(App.state.currentQuestions[App.state.currentIndex]);
    
    // 새 문제이므로 answeredQuestions에서 제거
    const questionId = App.state.currentQuestions[App.state.currentIndex].q_no;
    App.state.answeredQuestions.delete(questionId);
    answeredQuestions.delete(questionId); // 하위 호환성
    
    // 특수문자 입력 순서 초기화
    App.state.symbolInputOrder = {
        symbols: [],
        inputIndex: 0
    };
    symbolInputOrder = App.state.symbolInputOrder; // 하위 호환성
}

// 다음 문제
function nextQuestion() {
    App.state.currentIndex++;
    currentIndex = App.state.currentIndex; // 하위 호환성
    
    if (App.state.currentIndex >= App.state.currentQuestions.length) {
        App.state.currentIndex = 0;
        currentIndex = 0;
        showMessage('모든 문제를 완료했습니다!');
    }
    displayQuestion(App.state.currentQuestions[App.state.currentIndex]);
    
    // 새 문제이므로 answeredQuestions에서 제거
    const questionId = App.state.currentQuestions[App.state.currentIndex].q_no;
    App.state.answeredQuestions.delete(questionId);
    answeredQuestions.delete(questionId); // 하위 호환성
    
    // 특수문자 입력 순서 초기화
    App.state.symbolInputOrder = {
        symbols: [],
        inputIndex: 0
    };
    symbolInputOrder = App.state.symbolInputOrder; // 하위 호환성
}

// 해설 보기
function showExplanation() {
    const explanationDiv = document.getElementById('explanationDiv');
    const question = App.state.currentQuestions[App.state.currentIndex];
    
    if (question.explanation) {
        explanationDiv.innerHTML = formatCodeBlocks(question.explanation);
        explanationDiv.classList.toggle('show');
    } else {
        explanationDiv.innerHTML = '해설이 없습니다.';
        explanationDiv.classList.add('show');
    }
}

// 동영상 열기
function openVideo() {
    const question = App.state.currentQuestions[App.state.currentIndex];
    if (question.video_url) {
        window.open(question.video_url, '_blank');
    }
}

// 문제가 바뀔 때 동영상 버튼 표시/숨김
function updateVideoButton() {
    const videoBtn = document.getElementById('videoBtn');
    const question = App.state.currentQuestions[App.state.currentIndex];
    if (question && question.video_url) {
        videoBtn.style.display = 'inline-block';
    } else {
        videoBtn.style.display = 'none';
    }
}

// 답 보기 (학습 모드 - 통계 반영 안 함)
function showAnswerOnly() {
    const question = App.state.currentQuestions[App.state.currentIndex];
    const resultSection = document.getElementById('resultSection');
    
    // 정답 텍스트 처리 (괄호 제거)
    let answerText = question.answer.raw_text || '정답 없음';
    
    // 괄호 안 내용 제거
    answerText = answerText.replace(/\([^)]*\)/g, '');
    // • 제거
    answerText = answerText.replace(/[•]/g, '');
    // 여러 공백을 하나로
    answerText = answerText.replace(/\s+/g, ' ').trim();
    
    // 결과 영역 표시 (정보성 스타일)
    resultSection.style.display = 'block';
    resultSection.className = 'result-section';
    resultSection.style.background = '#d1ecf1';
    resultSection.style.border = '2px solid #0c5460';
    resultSection.style.color = '#0c5460';
    resultSection.innerHTML = `
        <i class="fas fa-eye"></i> <strong>정답:</strong> ${formatCodeBlocks(answerText)}
    `;
}

// 선택지 선택
function selectChoice(element) {
    document.querySelectorAll('.choice-item').forEach(item => {
        item.style.background = '#f8f9fa';
    });
    element.style.background = '#667eea';
    element.style.color = 'white';
    
    const answerInput = document.getElementById('answerInput_0');
    const key = element.querySelector('.choice-key').textContent.trim();
    if (answerInput) {
        answerInput.value = key;
    }
}

