// CISSP 문제집 학습 모듈 (영어/한국어 이중언어 지원)
class CISSPModule {
    constructor() {
        this.items = [];
        this.currentItem = null;
        this.currentIndex = 0;
        this.studyMode = 'quiz'; // 'quiz' 또는 'card'
        this.languageMode = 'en'; // 'en' = 영어, 'ko' = 한국어
        this.studyData = this.loadStudyData();
        this.selectedAnswer = null;
        this.selectedAnswers = []; // 복수 답안용
        this.vocabulary = {}; // 단어 사전
        this.cardStep = 1;
        this.showKoreanInline = false; // 한글 인라인 표시 여부
        // 단어/문장 학습 모드
        this.wordLearningMode = false;
        this.wordLearningIndex = 0;
        this.wordLearningList = [];
        this.sentenceLearningMode = false;
        this.sentenceLearningIndex = 0;
        this.sentenceLearningList = [];
    }

    // 학습 데이터 로드
    loadStudyData() {
        const saved = localStorage.getItem('cissp_study_data');
        if (saved) {
            return JSON.parse(saved);
        }
        return {
            completedItems: [],
            wrongItems: [],
            bookmarkedItems: [],
            stats: { correct: 0, wrong: 0, total: 0 },
            lastStudyDate: null,
            streak: 0
        };
    }

    // 학습 데이터 저장
    saveStudyData() {
        localStorage.setItem('cissp_study_data', JSON.stringify(this.studyData));
    }

    // 단어 사전 로드 (주요 단어 + 문제 단어 병합)
    async loadVocabulary() {
        try {
            // 주요 단어 사전 로드 (기존 565개)
            const mainVocabResponse = await fetch('data/cissp_vocabulary.json');
            const mainVocab = await mainVocabResponse.json();
            console.log(`CISSP 주요 단어 사전 ${Object.keys(mainVocab).length}개 로드`);
            
            // 문제 단어 사전 로드 (새로 추출한 단어)
            let problemVocab = {};
            try {
                const problemVocabResponse = await fetch('data/cissp_problem_vocabulary.json');
                problemVocab = await problemVocabResponse.json();
                console.log(`CISSP 문제 단어 사전 ${Object.keys(problemVocab).length}개 로드`);
            } catch (error) {
                console.log('문제 단어 사전 로드 실패 (주요 단어만 사용):', error);
            }
            
            // 두 사전 병합 (주요 단어가 우선순위)
            this.vocabulary = { ...problemVocab, ...mainVocab };
            console.log(`총 ${Object.keys(this.vocabulary).length}개 단어 사전 병합 완료`);
        } catch (error) {
            console.log('단어 사전 로드 실패 (기본 사전 사용):', error);
            this.vocabulary = this.getDefaultVocabulary();
        }
    }

    // 기본 단어 사전 (파일이 없을 경우)
    getDefaultVocabulary() {
        return {
            "confidentiality": { meaning: "기밀성", pos: "noun", example: "Confidentiality ensures that information is not disclosed to unauthorized individuals." },
            "integrity": { meaning: "무결성", pos: "noun", example: "Data integrity ensures that information has not been altered." },
            "availability": { meaning: "가용성", pos: "noun", example: "Availability ensures that systems and data are accessible when needed." },
            "authentication": { meaning: "인증", pos: "noun", example: "Authentication verifies the identity of a user or system." },
            "authorization": { meaning: "권한 부여", pos: "noun", example: "Authorization determines what actions a user can perform." },
            "encryption": { meaning: "암호화", pos: "noun", example: "Encryption converts data into a coded format." },
            "vulnerability": { meaning: "취약점", pos: "noun", example: "A vulnerability is a weakness that can be exploited." },
            "threat": { meaning: "위협", pos: "noun", example: "A threat is a potential cause of an unwanted incident." },
            "risk": { meaning: "위험", pos: "noun", example: "Risk is the potential for loss or damage." },
            "mitigation": { meaning: "완화, 경감", pos: "noun", example: "Risk mitigation reduces the impact of potential threats." },
            "compliance": { meaning: "준수, 컴플라이언스", pos: "noun", example: "Compliance ensures adherence to laws and regulations." },
            "audit": { meaning: "감사", pos: "noun", example: "An audit examines and verifies organizational processes." },
            "policy": { meaning: "정책", pos: "noun", example: "A security policy defines rules for protecting information." },
            "incident": { meaning: "사고, 인시던트", pos: "noun", example: "A security incident is an event that threatens information security." },
            "firewall": { meaning: "방화벽", pos: "noun", example: "A firewall controls network traffic based on security rules." },
            "malware": { meaning: "악성코드", pos: "noun", example: "Malware is software designed to cause harm." },
            "phishing": { meaning: "피싱", pos: "noun", example: "Phishing attempts to steal sensitive information through deception." },
            "access control": { meaning: "접근 제어", pos: "noun", example: "Access control restricts who can access resources." },
            "biometric": { meaning: "생체 인식의", pos: "adjective", example: "Biometric authentication uses physical characteristics." },
            "cryptography": { meaning: "암호학", pos: "noun", example: "Cryptography is the science of secure communication." }
        };
    }

    // 데이터 로드
    async loadItems() {
        try {
            const response = await fetch('data/items_cissp.jsonl');
            const text = await response.text();
            
            if (!text.trim()) {
                console.log('CISSP 데이터 파일이 비어있습니다.');
                this.items = [];
                return [];
            }
            
            this.items = text.trim().split('\n').map(line => JSON.parse(line));
            console.log(`CISSP ${this.items.length}개 문제 로드 완료`);
            
            // 단어 사전도 로드
            await this.loadVocabulary();
            
            return this.items;
        } catch (error) {
            console.error('CISSP 데이터 로드 실패:', error);
            return [];
        }
    }

    // 언어 모드 토글
    toggleLanguageMode() {
        this.languageMode = this.languageMode === 'en' ? 'ko' : 'en';
        App.state.languageMode = this.languageMode;
        
        // 현재 문제 다시 렌더링
        if (this.currentItem) {
            if (this.studyMode === 'card') {
                this.renderCardMode(this.currentItem);
            } else {
                this.renderQuestion(this.currentItem);
            }
        }
        
        this.updateLanguageToggleButton();
    }

    // 언어 토글 버튼 업데이트
    updateLanguageToggleButton() {
        const btn = document.getElementById('languageToggleBtn');
        if (btn) {
            btn.innerHTML = this.languageMode === 'en' 
                ? '<i class="fas fa-globe"></i> EN 🇺🇸'
                : '<i class="fas fa-globe"></i> KO 🇰🇷';
            btn.className = this.languageMode === 'en' 
                ? 'btn btn-lang-en'
                : 'btn btn-lang-ko';
        }
    }

    // 문제 텍스트 가져오기 (언어별)
    getQuestionText(item) {
        if (this.languageMode === 'ko' && item.question_ko) {
            return item.question_ko;
        }
        return item.question_en || item.question || '';
    }

    // 선택지 텍스트 가져오기 (언어별)
    getChoices(item) {
        if (this.languageMode === 'ko' && item.choices_ko) {
            return item.choices_ko;
        }
        return item.choices_en || item.choices || item.options || {};
    }

    // 영어 텍스트를 인터랙티브하게 변환 (문장/단어 클릭 가능, 한글 인라인 표시)
    makeInteractiveText(text, koreanText = '') {
        if (this.languageMode !== 'en') {
            return text;
        }
        
        // 문장 단위로 분리
        const sentences = text.split(/(?<=[.!?])\s+/);
        const koreanSentences = koreanText ? koreanText.split(/(?<=[.!?])\s+/) : [];
        
        return sentences.map((sentence, sIndex) => {
            // 단어 단위로 분리
            const words = sentence.split(/(\s+|[,.;:!?()[\]{}])/);
            
            const interactiveWords = words.map((word, wIndex) => {
                // 공백이나 구두점은 그대로
                if (/^\s+$/.test(word) || /^[,.;:!?()[\]{}]$/.test(word)) {
                    return word;
                }
                
                // 단어에 클릭 이벤트 추가
                const cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
                if (cleanWord && cleanWord.length > 2) {
                    // 사전에서 단어 찾기
                    const wordData = this.vocabulary[cleanWord] || this.vocabulary[word.toLowerCase()];
                    const koreanMeaning = wordData && wordData.meaning ? wordData.meaning : '';
                    
                    // 한글 인라인 표시가 켜져있고 의미가 있으면 표시
                    let koreanInline = '';
                    if (this.showKoreanInline && koreanMeaning) {
                        koreanInline = `<span class="korean-inline">(${koreanMeaning})</span>`;
                    }
                    
                    return `<span class="interactive-word" onclick="cisspModule.showWordPopup('${cleanWord}', event)">${word}${koreanInline}</span>`;
                }
                return word;
            }).join('');
            
            // 한국어 번역 가져오기 (해당 문장 인덱스에 맞는 번역)
            const koreanTranslation = koreanSentences[sIndex] || '';
            const escapedSentence = sentence.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            const escapedKorean = koreanTranslation.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            
            // 문장에 클릭 이벤트 추가 및 한국어 번역 data 속성 추가
            return `<span class="interactive-sentence-wrapper">
                <span class="interactive-sentence" onclick="cisspModule.toggleSentenceTranslation(this, event)" 
                      data-sentence="${escapedSentence}" 
                      data-korean="${escapedKorean}">${interactiveWords}</span>
            </span>`;
        }).join(' ');
    }
    
    // 한글 인라인 표시 토글
    toggleKoreanInline() {
        this.showKoreanInline = !this.showKoreanInline;
        
        // 버튼 상태 업데이트
        const btn = document.getElementById('koreanConvertBtn');
        if (btn) {
            btn.classList.toggle('active', this.showKoreanInline);
            btn.innerHTML = `<i class="fas fa-language"></i> ${this.showKoreanInline ? '한글 숨기기' : '한글 변환'}`;
        }
        
        // 문제 다시 렌더링
        if (this.currentItem) {
            this.renderQuestion(this.currentItem);
        }
    }

    // 단어 팝업 표시 (두 사전 모두에서 검색)
    showWordPopup(word, event) {
        event.stopPropagation();
        
        // 여러 변형으로 단어 검색
        const wordLower = word.toLowerCase();
        let wordData = this.vocabulary[word] || 
                      this.vocabulary[wordLower] || 
                      this.vocabulary[word.charAt(0).toUpperCase() + wordLower.slice(1)];
        
        let content;
        if (wordData) {
            // 의미가 있는 경우
            const meaning = wordData.meaning || '';
            const pos = wordData.pos && wordData.pos !== 'unknown' ? wordData.pos : '';
            const frequency = wordData.frequency ? ` (빈도: ${wordData.frequency})` : '';
            const hasExampleParsed = wordData.example_parsed && Array.isArray(wordData.example_parsed) && wordData.example_parsed.length > 0;
            
            content = `
                <div class="word-popup-content">
                    <div class="word-title">${word}</div>
                    ${meaning ? `<div class="word-meaning">${meaning}${frequency}</div>` : ''}
                    ${pos ? `<div class="word-pos">${pos}</div>` : ''}
                    ${wordData.example ? `
                        <div class="word-example">
                            <div class="example-text">"${wordData.example}"</div>
                            ${hasExampleParsed ? `
                                <button class="btn-phrase-toggle" onclick="cisspModule.togglePhraseTranslation('${word}', event)">
                                    <i class="fas fa-list-ol"></i> 구문별 해석 보기
                                </button>
                                <div class="phrase-translation-container" id="phrase-translation-${word}" style="display: none;">
                                    ${this.renderPhraseTranslation(wordData.example_parsed)}
                                </div>
                            ` : ''}
                        </div>
                    ` : ''}
                    ${!meaning && !pos && !wordData.example ? `
                        <div class="word-meaning" style="color: #999;">사전에 등록되어 있지만 의미가 아직 추가되지 않았습니다.</div>
                    ` : ''}
                </div>
            `;
        } else {
            // 단어를 찾을 수 없는 경우
            content = `
                <div class="word-popup-content">
                    <div class="word-title">${word}</div>
                    <div class="word-meaning" style="color: #999;">
                        <i class="fas fa-info-circle"></i> 사전에 없는 단어입니다.<br>
                        <small style="font-size: 0.85em; margin-top: 5px; display: block;">
                            이 단어는 아직 번역되지 않았습니다.
                        </small>
                    </div>
                </div>
            `;
        }
        
        this.showPopup(content, event);
    }
    
    // 구문별 해석 렌더링
    renderPhraseTranslation(exampleParsed) {
        if (!exampleParsed || !Array.isArray(exampleParsed)) {
            return '';
        }
        
        // order 순서대로 정렬
        const sorted = [...exampleParsed].sort((a, b) => (a.order || 0) - (b.order || 0));
        
        return `
            <div class="phrase-translation-list">
                ${sorted.map((phrase, index) => `
                    <div class="phrase-item" data-order="${phrase.order}">
                        <div class="phrase-header">
                            <span class="phrase-number">(${phrase.order})</span>
                            <span class="phrase-text">${phrase.phrase}</span>
                            ${phrase.role ? `<span class="phrase-role">${phrase.role}</span>` : ''}
                        </div>
                        <div class="phrase-translation">→ ${phrase.translation}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    // 구문별 해석 토글
    togglePhraseTranslation(word, event) {
        event.stopPropagation();
        const container = document.getElementById(`phrase-translation-${word}`);
        const button = event.target.closest('.btn-phrase-toggle');
        
        if (container) {
            const isVisible = container.style.display !== 'none';
            container.style.display = isVisible ? 'none' : 'block';
            
            if (button) {
                const icon = button.querySelector('i');
                const text = button.childNodes[button.childNodes.length - 1];
                if (isVisible) {
                    icon.className = 'fas fa-list-ol';
                    text.textContent = ' 구문별 해석 보기';
                } else {
                    icon.className = 'fas fa-chevron-up';
                    text.textContent = ' 구문별 해석 숨기기';
                }
            }
        }
    }

    // 문장 번역 토글 (인라인 표시)
    toggleSentenceTranslation(element, event) {
        event.stopPropagation();
        
        const koreanText = element.getAttribute('data-korean');
        if (!koreanText) {
            return;
        }
        
        // 이미 번역이 표시되어 있는지 확인
        const wrapper = element.closest('.interactive-sentence-wrapper');
        let translationDiv = wrapper.querySelector('.sentence-translation-inline');
        
        if (translationDiv) {
            // 이미 표시되어 있으면 제거
            translationDiv.remove();
            element.classList.remove('has-translation');
        } else {
            // 표시되지 않았으면 추가
            translationDiv = document.createElement('div');
            translationDiv.className = 'sentence-translation-inline';
            translationDiv.innerHTML = koreanText;
            wrapper.appendChild(translationDiv);
            element.classList.add('has-translation');
        }
    }

    // 팝업 표시
    showPopup(content, event) {
        // 기존 팝업 제거
        const existingPopup = document.querySelector('.cissp-popup');
        if (existingPopup) {
            existingPopup.remove();
        }
        
        const popup = document.createElement('div');
        popup.className = 'cissp-popup';
        popup.innerHTML = content;
        
        // 위치 설정
        const rect = event.target.getBoundingClientRect();
        popup.style.top = (rect.bottom + window.scrollY + 10) + 'px';
        popup.style.left = Math.max(10, rect.left + window.scrollX - 50) + 'px';
        
        document.body.appendChild(popup);
        
        // 외부 클릭시 닫기
        setTimeout(() => {
            document.addEventListener('click', function closePopup(e) {
                if (!popup.contains(e.target)) {
                    popup.remove();
                    document.removeEventListener('click', closePopup);
                }
            });
        }, 100);
    }

    // 북마크 토글
    toggleBookmark(itemId) {
        const index = this.studyData.bookmarkedItems.indexOf(itemId);
        
        if (index === -1) {
            this.studyData.bookmarkedItems.push(itemId);
        } else {
            this.studyData.bookmarkedItems.splice(index, 1);
        }
        
        this.saveStudyData();
        
        if (this.currentItem) {
            this.renderQuestion(this.currentItem);
        }
    }

    // 북마크 상태 확인
    isBookmarked(itemId) {
        return this.studyData.bookmarkedItems.includes(itemId);
    }

    // 문제 렌더링
    renderQuestion(item) {
        const container = document.getElementById('questionContainer');
        const isBookmarked = this.isBookmarked(item.id);
        
        const questionText = this.getQuestionText(item);
        const questionKorean = this.languageMode === 'en' && item.question_ko ? item.question_ko : '';
        const choices = this.getChoices(item);
        const choicesKorean = this.languageMode === 'en' && item.choices_ko ? item.choices_ko : {};
        
        // 영어 모드에서 인터랙티브 텍스트 적용 (한국어 번역 포함)
        const displayQuestion = this.languageMode === 'en' 
            ? this.makeInteractiveText(questionText, questionKorean)
            : questionText;
        
        // 복수 답안 여부 확인
        const isMultipleAnswer = Array.isArray(item.answer) && item.answer.length > 1;
        const requiredCount = isMultipleAnswer ? item.answer.length : 1;
        
        // 선택지 HTML 생성
        let choicesHTML = '';
        const choiceKeys = Object.keys(choices);
        
        if (isMultipleAnswer) {
            // 복수 선택: 체크박스 사용
            choicesHTML = choiceKeys.map(key => {
                const text = choices[key];
                const koreanText = choicesKorean[key] || '';
                const displayText = this.languageMode === 'en' 
                    ? this.makeInteractiveText(text, koreanText)
                    : text;
                return `
                    <div class="choice-item choice-checkbox" data-key="${key}" onclick="cisspModule.selectChoice(this, '${key}')">
                        <input type="checkbox" id="choice_${key}" class="choice-check">
                        <label for="choice_${key}">
                            <span class="choice-key">${key}</span>
                            <span class="choice-text">${displayText}</span>
                        </label>
                    </div>
                `;
            }).join('');
            choicesHTML += `<div class="multiple-hint">
                <i class="fas fa-info-circle"></i> ${requiredCount}개를 선택하세요
            </div>`;
        } else {
            // 단일 선택
            choicesHTML = choiceKeys.map(key => {
                const text = choices[key];
                const koreanText = choicesKorean[key] || '';
                const displayText = this.languageMode === 'en' 
                    ? this.makeInteractiveText(text, koreanText)
                    : text;
                return `
                    <div class="choice-item" data-key="${key}" onclick="cisspModule.selectChoice(this, '${key}')">
                        <span class="choice-key">${key}</span>
                        <span class="choice-text">${displayText}</span>
                    </div>
                `;
            }).join('');
        }
        
        // 이미지 HTML
        let imagesHTML = '';
        if (item.images && item.images.length > 0) {
            imagesHTML = `
                <div class="question-images">
                    ${item.images.map(img => `<img src="images/cissp/${img}" alt="문제 이미지" onerror="this.style.display='none'">`).join('')}
                </div>
            `;
        }
        
        container.innerHTML = `
            <div class="question-card cissp-card">
                <div class="question-header">
                    <div class="question-no">Q.${item.q_no}</div>
                    <div class="header-buttons">
                        <button id="languageToggleBtn" class="btn ${this.languageMode === 'en' ? 'btn-lang-en' : 'btn-lang-ko'}" onclick="cisspModule.toggleLanguageMode()">
                            <i class="fas fa-globe"></i> ${this.languageMode === 'en' ? 'EN 🇺🇸' : 'KO 🇰🇷'}
                        </button>
                        ${this.languageMode === 'en' ? `
                        <button id="koreanConvertBtn" class="btn korean-convert-btn ${this.showKoreanInline ? 'active' : ''}" onclick="cisspModule.toggleKoreanInline()">
                            <i class="fas fa-language"></i> ${this.showKoreanInline ? '한글 숨기기' : '한글 변환'}
                        </button>
                        ` : ''}
                        <button class="btn ${isBookmarked ? 'btn-bookmarked' : 'btn-secondary'}" onclick="cisspModule.toggleBookmark('${item.id}')">
                            <i class="fas fa-star"></i> ${isBookmarked ? '✓' : '☆'}
                        </button>
                    </div>
                </div>
                
                ${this.languageMode === 'en' ? `<div class="lang-hint"><i class="fas fa-hand-pointer"></i> 단어/문장을 클릭하면 해석을 볼 수 있습니다</div>` : ''}
                
                <div class="question-text">
                    ${displayQuestion}
                </div>
                
                ${imagesHTML}
                
                <div class="choices">
                    ${choicesHTML}
                </div>
                
                <div class="action-buttons">
                    <div class="main-controls">
                        <button class="btn btn-primary" onclick="cisspModule.checkAnswer()">
                            <i class="fas fa-check"></i> 제출
                        </button>
                        <button class="btn btn-info" onclick="cisspModule.showAnswerOnly()">
                            <i class="fas fa-eye"></i> 답
                        </button>
                    </div>
                    <div class="navigation-controls">
                        <button class="btn btn-secondary" onclick="cisspModule.previousItem()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="cisspModule.renderDashboard()">
                            <i class="fas fa-home"></i>
                        </button>
                        <button class="btn btn-secondary" onclick="cisspModule.nextItem()" ${this.currentIndex === this.items.length - 1 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
                
                <div class="result-section" id="cisspResultSection" style="display: none;"></div>
            </div>
        `;
    }

    // 선택지 클릭
    selectChoice(element, key) {
        const item = this.currentItem;
        const isMultipleAnswer = Array.isArray(item.answer) && item.answer.length > 1;
        
        if (isMultipleAnswer) {
            // 복수 선택: 체크박스 토글
            const checkbox = element.querySelector('.choice-check');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                
                if (!this.selectedAnswers) this.selectedAnswers = [];
                const index = this.selectedAnswers.indexOf(key);
                
                if (checkbox.checked) {
                    if (index === -1) this.selectedAnswers.push(key);
                    element.classList.add('selected');
                } else {
                    if (index > -1) this.selectedAnswers.splice(index, 1);
                    element.classList.remove('selected');
                }
            }
        } else {
            // 단일 선택
            document.querySelectorAll('.choice-item').forEach(item => {
                item.classList.remove('selected');
            });
            
            element.classList.add('selected');
            this.selectedAnswer = key;
        }
    }

    // 정답 확인
    checkAnswer() {
        const item = this.currentItem;
        const isMultipleAnswer = Array.isArray(item.answer) && item.answer.length > 1;
        const resultSection = document.getElementById('cisspResultSection');
        
        let isCorrect = false;
        let userAnswer = '';
        let correctAnswer = '';
        
        if (isMultipleAnswer) {
            if (!this.selectedAnswers || this.selectedAnswers.length === 0) {
                alert('답안을 선택해주세요.');
                return;
            }
            
            const userAnswers = [...this.selectedAnswers].sort();
            const correctAnswers = [...item.answer].sort();
            isCorrect = JSON.stringify(userAnswers) === JSON.stringify(correctAnswers);
            
            userAnswer = userAnswers.join(', ');
            correctAnswer = correctAnswers.join(', ');
        } else {
            if (!this.selectedAnswer) {
                alert('답안을 선택해주세요.');
                return;
            }
            
            const correctAnswerValue = Array.isArray(item.answer) ? item.answer[0] : item.answer;
            isCorrect = this.selectedAnswer.toUpperCase() === correctAnswerValue.toUpperCase();
            userAnswer = this.selectedAnswer;
            correctAnswer = correctAnswerValue;
        }
        
        // 통계 업데이트
        this.studyData.stats.total++;
        if (isCorrect) {
            this.studyData.stats.correct++;
            // 오답 목록에서 제거
            const wrongIndex = this.studyData.wrongItems.indexOf(item.id);
            if (wrongIndex > -1) {
                this.studyData.wrongItems.splice(wrongIndex, 1);
            }
        } else {
            this.studyData.stats.wrong++;
            // 오답 목록에 추가
            if (!this.studyData.wrongItems.includes(item.id)) {
                this.studyData.wrongItems.push(item.id);
            }
        }
        
        // 완료 목록에 추가
        if (!this.studyData.completedItems.includes(item.id)) {
            this.studyData.completedItems.push(item.id);
        }
        
        this.saveStudyData();
        
        // 결과 표시
        resultSection.style.display = 'block';
        if (isCorrect) {
            resultSection.className = 'result-section correct';
            resultSection.innerHTML = `
                <i class="fas fa-check-circle"></i> <strong>정답입니다!</strong><br>
                정답: ${correctAnswer}
            `;
        } else {
            resultSection.className = 'result-section wrong';
            resultSection.innerHTML = `
                <i class="fas fa-times-circle"></i> <strong>오답입니다.</strong><br>
                선택: ${userAnswer}<br>
                정답: ${correctAnswer}
            `;
        }
        
        // 선택지 상태 표시
        document.querySelectorAll('.choice-item').forEach(el => {
            const key = el.dataset.key;
            const correctKeys = Array.isArray(item.answer) ? item.answer : [item.answer];
            
            if (correctKeys.includes(key)) {
                el.classList.add('correct');
            } else if ((isMultipleAnswer && this.selectedAnswers?.includes(key)) || 
                       (!isMultipleAnswer && this.selectedAnswer === key)) {
                if (!correctKeys.includes(key)) {
                    el.classList.add('incorrect');
                }
            }
        });
    }

    // 답만 보기
    showAnswerOnly() {
        const item = this.currentItem;
        const resultSection = document.getElementById('cisspResultSection');
        
        const correctAnswer = Array.isArray(item.answer) 
            ? item.answer.join(', ') 
            : item.answer;
        
        resultSection.style.display = 'block';
        resultSection.className = 'result-section info';
        resultSection.innerHTML = `
            <i class="fas fa-eye"></i> <strong>정답:</strong> ${correctAnswer}
        `;
        
        // 정답 선택지 하이라이트
        document.querySelectorAll('.choice-item').forEach(el => {
            const key = el.dataset.key;
            const correctKeys = Array.isArray(item.answer) ? item.answer : [item.answer];
            
            if (correctKeys.includes(key)) {
                el.classList.add('correct');
            }
        });
    }

    // 이전 문제
    previousItem() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.currentItem = this.items[this.currentIndex];
            this.selectedAnswer = null;
            this.selectedAnswers = [];
            this.renderQuestion(this.currentItem);
        }
    }

    // 다음 문제
    nextItem() {
        if (this.currentIndex < this.items.length - 1) {
            this.currentIndex++;
            this.currentItem = this.items[this.currentIndex];
            this.selectedAnswer = null;
            this.selectedAnswers = [];
            this.renderQuestion(this.currentItem);
        }
    }

    // 학습 시작
    async startStudy(mode = 'sequential') {
        if (this.items.length === 0) {
            await this.loadItems();
        }
        
        if (this.items.length === 0) {
            alert('문제 데이터가 없습니다. PDF 파싱을 먼저 진행해주세요.');
            return;
        }
        
        let studyItems = [...this.items];
        
        if (mode === 'random') {
            studyItems = this.shuffleArray(studyItems);
        } else if (mode === 'wrong') {
            studyItems = this.items.filter(item => this.studyData.wrongItems.includes(item.id));
            if (studyItems.length === 0) {
                alert('오답 문제가 없습니다.');
                return;
            }
        } else if (mode === 'bookmarked') {
            studyItems = this.items.filter(item => this.studyData.bookmarkedItems.includes(item.id));
            if (studyItems.length === 0) {
                alert('체크한 문제가 없습니다.');
                return;
            }
        }
        
        this.items = studyItems;
        this.currentIndex = 0;
        this.currentItem = this.items[0];
        this.selectedAnswer = null;
        this.selectedAnswers = [];
        this.studyMode = 'quiz';
        
        this.renderQuestion(this.currentItem);
    }

    // 범위 학습
    startRangeStudy(start, end) {
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
        this.selectedAnswers = [];
        
        this.renderQuestion(this.currentItem);
    }

    // 범위 설정 모달
    showRangeModal() {
        const totalQuestions = this.items.length || 1850;
        const rangeStart = prompt(`시작 문제 번호 (1~${totalQuestions}):`, '1');
        
        if (!rangeStart) return;
        
        const rangeEnd = prompt(`끝 문제 번호 (${rangeStart}~${totalQuestions}):`, Math.min(parseInt(rangeStart) + 49, totalQuestions).toString());
        
        if (!rangeEnd) return;
        
        const start = parseInt(rangeStart);
        const end = parseInt(rangeEnd);
        
        if (isNaN(start) || isNaN(end)) {
            alert('숫자를 입력해주세요.');
            return;
        }
        
        if (start < 1 || end < 1 || start > end) {
            alert('올바른 범위를 입력해주세요.');
            return;
        }
        
        this.startRangeStudy(start, end);
    }

    // 배열 섞기
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
            total: this.items.length || 1850,
            completed: this.studyData.completedItems.length,
            wrong: this.studyData.wrongItems.length,
            bookmarked: this.studyData.bookmarkedItems.length,
            accuracy: 0
        };
        
        const totalAttempts = this.studyData.stats.correct + this.studyData.stats.wrong;
        stats.accuracy = totalAttempts > 0 
            ? Math.round((this.studyData.stats.correct / totalAttempts) * 100) 
            : 0;
        
        return stats;
    }

    // 대시보드 렌더링
    async renderDashboard() {
        if (this.items.length === 0) {
            await this.loadItems();
        }
        
        const container = document.getElementById('questionContainer');
        const stats = this.calculateStats();
        
        const hasData = this.items.length > 0;
        
        container.innerHTML = `
            <div class="cissp-dashboard">
                <div class="dashboard-header cissp-header">
                    <h2><i class="fas fa-shield-alt"></i> CISSP 문제집</h2>
                    <div class="total-count">
                        <span class="count-number">${stats.total}</span>
                        <span class="count-label">개 문제</span>
                    </div>
                    ${!hasData ? '<div class="no-data-warning"><i class="fas fa-exclamation-triangle"></i> PDF 파싱 후 문제를 사용할 수 있습니다</div>' : ''}
                </div>
                
                <!-- 언어 모드 선택 -->
                <div class="language-selector">
                    <h3><i class="fas fa-globe"></i> 학습 언어</h3>
                    <div class="language-options">
                        <button class="lang-btn ${this.languageMode === 'ko' ? 'active' : ''}" onclick="cisspModule.setLanguageMode('ko')">
                            <span class="flag">🇰🇷</span>
                            <span class="lang-name">한국어</span>
                            <span class="lang-desc">한국어로 문제 풀기</span>
                        </button>
                        <button class="lang-btn ${this.languageMode === 'en' ? 'active' : ''}" onclick="cisspModule.setLanguageMode('en')">
                            <span class="flag">🇺🇸</span>
                            <span class="lang-name">English</span>
                            <span class="lang-desc">영어 + 해석 학습</span>
                        </button>
                    </div>
                </div>
                
                <!-- 학습 통계 -->
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
                            <i class="fas fa-times-circle" style="color: #dc3545;"></i>
                            <div class="stat-content">
                                <div class="stat-number">${stats.wrong}</div>
                                <div class="stat-label">오답</div>
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
                    </div>
                </div>
                
                <!-- 주요 학습 모드 -->
                <div class="main-study-modes">
                    <h3 class="section-title"><i class="fas fa-graduation-cap"></i> 학습 시작하기</h3>
                    <div class="main-mode-grid">
                        <button class="main-mode-card primary" onclick="cisspModule.startStudy('sequential')" ${!hasData ? 'disabled' : ''}>
                            <div class="mode-icon"><i class="fas fa-play-circle"></i></div>
                            <div class="mode-title">순차학습</div>
                            <div class="mode-desc">처음부터 순서대로</div>
                        </button>
                        <button class="main-mode-card secondary" onclick="cisspModule.startStudy('random')" ${!hasData ? 'disabled' : ''}>
                            <div class="mode-icon"><i class="fas fa-random"></i></div>
                            <div class="mode-title">랜덤학습</div>
                            <div class="mode-desc">무작위로 섞어서</div>
                        </button>
                        <button class="main-mode-card wrong-mode" onclick="cisspModule.startStudy('wrong')" ${!hasData ? 'disabled' : ''}>
                            <div class="mode-icon"><i class="fas fa-redo"></i></div>
                            <div class="mode-title">오답 복습</div>
                            <div class="mode-desc">${stats.wrong}개 문제</div>
                        </button>
                        <button class="main-mode-card bookmarked" onclick="cisspModule.startStudy('bookmarked')" ${!hasData ? 'disabled' : ''}>
                            <div class="mode-icon"><i class="fas fa-star"></i></div>
                            <div class="mode-title">체크문제</div>
                            <div class="mode-desc">${stats.bookmarked}개 문제</div>
                        </button>
                    </div>
                </div>
                
                <!-- 범위학습 -->
                <div class="range-study-section">
                    <button class="range-study-btn" onclick="cisspModule.showRangeModal()" ${!hasData ? 'disabled' : ''}>
                        <i class="fas fa-sliders-h"></i> 범위를 지정해서 학습하기
                    </button>
                </div>
                
                <!-- 단어/문장 학습 모드 -->
                <div class="vocab-sentence-learning-section">
                    <h3 class="section-title"><i class="fas fa-book-reader"></i> 단어 & 문장 학습</h3>
                    <div class="vocab-sentence-grid">
                        <button class="vocab-sentence-card vocab-card" onclick="cisspModule.startWordLearning()">
                            <div class="vocab-sentence-icon"><i class="fas fa-spell-check"></i></div>
                            <div class="vocab-sentence-title">자주 나오는 단어 학습</div>
                            <div class="vocab-sentence-desc">빈도 40 이상 단어</div>
                            <div class="vocab-sentence-count" id="word-learning-count">로딩 중...</div>
                        </button>
                        <button class="vocab-sentence-card sentence-card" onclick="cisspModule.startSentenceLearning()">
                            <div class="vocab-sentence-icon"><i class="fas fa-quote-left"></i></div>
                            <div class="vocab-sentence-title">자주 나오는 문장 학습</div>
                            <div class="vocab-sentence-desc">빈출 문장 패턴</div>
                            <div class="vocab-sentence-count" id="sentence-learning-count">로딩 중...</div>
                        </button>
                    </div>
                </div>
                
                <!-- 통계 초기화 -->
                <div class="reset-section">
                    <button class="btn btn-secondary" onclick="cisspModule.resetStats()">
                        <i class="fas fa-undo"></i> 학습 기록 초기화
                    </button>
                </div>
            </div>
        `;
        
        // 단어/문장 학습 카운트 업데이트
        this.updateWordSentenceCounts();
    }
    
    // 단어/문장 학습 카운트 업데이트
    async updateWordSentenceCounts() {
        try {
            // 빈도 40 이상인 단어 개수 계산
            const problemVocabResponse = await fetch('data/cissp_problem_vocabulary.json');
            const problemVocab = await problemVocabResponse.json();
            
            const frequentWords = Object.entries(problemVocab)
                .filter(([word, data]) => data.frequency >= 40)
                .sort((a, b) => b[1].frequency - a[1].frequency)
                .slice(0, 1000);
            
            const wordCountEl = document.getElementById('word-learning-count');
            if (wordCountEl) {
                wordCountEl.textContent = `${frequentWords.length}개 단어`;
            }
            
            // 문장 개수는 문제에서 추출 (최대 200개)
            const sentenceCountEl = document.getElementById('sentence-learning-count');
            if (sentenceCountEl) {
                // 문제에서 문장 패턴 추출하여 개수 계산
                const sentenceCount = Math.min(200, this.items.length);
                sentenceCountEl.textContent = `${sentenceCount}개 문장`;
            }
        } catch (error) {
            console.error('단어/문장 카운트 업데이트 실패:', error);
            const wordCountEl = document.getElementById('word-learning-count');
            if (wordCountEl) wordCountEl.textContent = '로드 실패';
            const sentenceCountEl = document.getElementById('sentence-learning-count');
            if (sentenceCountEl) sentenceCountEl.textContent = '로드 실패';
        }
    }
    
    // 자주 나오는 단어 학습 시작
    async startWordLearning() {
        try {
            // 빈도 40 이상인 단어들 로드
            const problemVocabResponse = await fetch('data/cissp_problem_vocabulary.json');
            const problemVocab = await problemVocabResponse.json();
            
            // 빈도 40 이상인 단어들 필터링 및 정렬
            const frequentWords = Object.entries(problemVocab)
                .filter(([word, data]) => data.frequency >= 40)
                .map(([word, data]) => ({
                    word: word,
                    meaning: data.meaning || '',
                    pos: data.pos || 'unknown',
                    frequency: data.frequency,
                    example: data.example || ''
                }))
                .sort((a, b) => b.frequency - a.frequency)
                .slice(0, 1000);
            
            if (frequentWords.length === 0) {
                alert('학습할 단어가 없습니다.');
                return;
            }
            
            // 단어 학습 모드로 전환
            this.wordLearningMode = true;
            this.wordLearningIndex = 0;
            this.wordLearningList = frequentWords;
            
            this.renderWordLearning();
        } catch (error) {
            console.error('단어 학습 시작 실패:', error);
            alert('단어 학습 데이터를 불러올 수 없습니다.');
        }
    }
    
    // 단어 학습 렌더링
    renderWordLearning() {
        if (!this.wordLearningList || this.wordLearningList.length === 0) {
            return;
        }
        
        const currentWord = this.wordLearningList[this.wordLearningIndex];
        const progress = ((this.wordLearningIndex + 1) / this.wordLearningList.length * 100).toFixed(1);
        
        const container = document.getElementById('questionContainer');
        container.innerHTML = `
            <div class="word-learning-container">
                <div class="word-learning-header">
                    <button class="btn btn-back" onclick="cisspModule.renderDashboard()">
                        <i class="fas fa-arrow-left"></i> 대시보드로
                    </button>
                    <h2><i class="fas fa-spell-check"></i> 자주 나오는 단어 학습</h2>
                    <div class="word-learning-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <div class="progress-text">${this.wordLearningIndex + 1} / ${this.wordLearningList.length} (${progress}%)</div>
                    </div>
                </div>
                
                <div class="word-learning-card">
                    <div class="word-card-main">
                        <div class="word-frequency-badge">빈도: ${currentWord.frequency}</div>
                        <div class="word-display">${currentWord.word}</div>
                        <div class="word-pos">${currentWord.pos !== 'unknown' ? currentWord.pos : ''}</div>
                        <div class="word-meaning-display" id="word-meaning-display" style="display: none;">
                            <div class="word-meaning-text">${currentWord.meaning || '의미 없음'}</div>
                            ${currentWord.example ? `
                                <div class="word-example-display">
                                    <div class="example-label">예문:</div>
                                    <div class="example-text">"${currentWord.example}"</div>
                                    ${this.vocabulary[currentWord.word] && this.vocabulary[currentWord.word].example_parsed ? `
                                        <button class="btn btn-sm btn-secondary" onclick="cisspModule.toggleWordExampleParsed('${currentWord.word}')" style="margin-top: 10px;">
                                            <i class="fas fa-list-ol"></i> 구문별 해석 보기
                                        </button>
                                        <div class="word-example-parsed" id="word-example-parsed-${currentWord.word}" style="display: none; margin-top: 10px;">
                                            ${this.renderPhraseTranslation(this.vocabulary[currentWord.word].example_parsed)}
                                        </div>
                                    ` : ''}
                                </div>
                            ` : ''}
                        </div>
                        <button class="btn btn-primary btn-show-meaning" onclick="cisspModule.toggleWordMeaning()">
                            <i class="fas fa-eye"></i> 의미 보기
                        </button>
                    </div>
                    
                    <div class="word-learning-controls">
                        <button class="btn btn-secondary" onclick="cisspModule.prevWord()" ${this.wordLearningIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전
                        </button>
                        <button class="btn btn-primary" onclick="cisspModule.nextWord()" ${this.wordLearningIndex === this.wordLearningList.length - 1 ? 'disabled' : ''}>
                            다음 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    // 단어 의미 토글
    toggleWordMeaning() {
        const meaningDisplay = document.getElementById('word-meaning-display');
        const btn = document.querySelector('.btn-show-meaning');
        
        if (meaningDisplay.style.display === 'none') {
            meaningDisplay.style.display = 'block';
            if (btn) {
                btn.innerHTML = '<i class="fas fa-eye-slash"></i> 의미 숨기기';
            }
        } else {
            meaningDisplay.style.display = 'none';
            if (btn) {
                btn.innerHTML = '<i class="fas fa-eye"></i> 의미 보기';
            }
        }
    }
    
    // 이전 단어
    prevWord() {
        if (this.wordLearningIndex > 0) {
            this.wordLearningIndex--;
            this.renderWordLearning();
        }
    }
    
    // 다음 단어
    nextWord() {
        if (this.wordLearningIndex < this.wordLearningList.length - 1) {
            this.wordLearningIndex++;
            this.renderWordLearning();
        }
    }
    
    // 자주 나오는 문장 학습 시작
    async startSentenceLearning() {
        try {
            // 문제에서 문장 패턴 추출
            const sentences = [];
            const seenPatterns = new Set();
            
            for (const item of this.items) {
                // 문제 본문에서 문장 추출
                if (item.question_en) {
                    const questionSentences = item.question_en.split(/[.!?]\s+/).filter(s => s.trim().length > 10);
                    const questionKoSentences = item.question_ko ? item.question_ko.split(/[.!?]\s+/).filter(s => s.trim().length > 10) : [];
                    
                    for (let i = 0; i < questionSentences.length; i++) {
                        const sent = questionSentences[i].trim();
                        const sentKo = i < questionKoSentences.length ? questionKoSentences[i].trim() : '';
                        
                        // 패턴 추출 (첫 5단어)
                        const pattern = sent.toLowerCase().split(/\s+/).slice(0, 5).join(' ');
                        
                        if (!seenPatterns.has(pattern) && sent.length > 10) {
                            sentences.push({
                                sentence_en: sent,
                                sentence_ko: sentKo,
                                pattern: pattern,
                                source: `문제 ${item.q_no}`
                            });
                            seenPatterns.add(pattern);
                            
                            if (sentences.length >= 200) break;
                        }
                    }
                }
                
                if (sentences.length >= 200) break;
            }
            
            if (sentences.length === 0) {
                alert('학습할 문장이 없습니다.');
                return;
            }
            
            // 문장 학습 모드로 전환
            this.sentenceLearningMode = true;
            this.sentenceLearningIndex = 0;
            this.sentenceLearningList = sentences;
            
            this.renderSentenceLearning();
        } catch (error) {
            console.error('문장 학습 시작 실패:', error);
            alert('문장 학습 데이터를 불러올 수 없습니다.');
        }
    }
    
    // 문장 학습 렌더링
    renderSentenceLearning() {
        if (!this.sentenceLearningList || this.sentenceLearningList.length === 0) {
            return;
        }
        
        const currentSentence = this.sentenceLearningList[this.sentenceLearningIndex];
        const progress = ((this.sentenceLearningIndex + 1) / this.sentenceLearningList.length * 100).toFixed(1);
        
        // 영어 문장을 인터랙티브하게 변환
        const interactiveSentence = this.makeInteractiveText(currentSentence.sentence_en, currentSentence.sentence_ko);
        
        const container = document.getElementById('questionContainer');
        container.innerHTML = `
            <div class="sentence-learning-container">
                <div class="sentence-learning-header">
                    <button class="btn btn-back" onclick="cisspModule.renderDashboard()">
                        <i class="fas fa-arrow-left"></i> 대시보드로
                    </button>
                    <h2><i class="fas fa-quote-left"></i> 자주 나오는 문장 학습</h2>
                    <div class="sentence-learning-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <div class="progress-text">${this.sentenceLearningIndex + 1} / ${this.sentenceLearningList.length} (${progress}%)</div>
                    </div>
                </div>
                
                <div class="sentence-learning-card">
                    <div class="sentence-card-main">
                        <div class="sentence-source">${currentSentence.source}</div>
                        <div class="sentence-display">
                            ${interactiveSentence}
                        </div>
                        <div class="sentence-translation-display" id="sentence-translation-display" style="display: none;">
                            <div class="translation-label">한국어 번역:</div>
                            <div class="translation-text">${currentSentence.sentence_ko || '번역 없음'}</div>
                        </div>
                        <button class="btn btn-primary btn-show-translation" onclick="cisspModule.toggleSentenceTranslation()">
                            <i class="fas fa-language"></i> 번역 보기
                        </button>
                    </div>
                    
                    <div class="sentence-learning-controls">
                        <button class="btn btn-secondary" onclick="cisspModule.prevSentence()" ${this.sentenceLearningIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전
                        </button>
                        <button class="btn btn-primary" onclick="cisspModule.nextSentence()" ${this.sentenceLearningIndex === this.sentenceLearningList.length - 1 ? 'disabled' : ''}>
                            다음 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    // 문장 번역 토글
    toggleSentenceTranslation() {
        const translationDisplay = document.getElementById('sentence-translation-display');
        const btn = document.querySelector('.btn-show-translation');
        
        if (translationDisplay.style.display === 'none') {
            translationDisplay.style.display = 'block';
            if (btn) {
                btn.innerHTML = '<i class="fas fa-eye-slash"></i> 번역 숨기기';
            }
        } else {
            translationDisplay.style.display = 'none';
            if (btn) {
                btn.innerHTML = '<i class="fas fa-language"></i> 번역 보기';
            }
        }
    }
    
    // 이전 문장
    prevSentence() {
        if (this.sentenceLearningIndex > 0) {
            this.sentenceLearningIndex--;
            this.renderSentenceLearning();
        }
    }
    
    // 다음 문장
    nextSentence() {
        if (this.sentenceLearningIndex < this.sentenceLearningList.length - 1) {
            this.sentenceLearningIndex++;
            this.renderSentenceLearning();
        }
    }

    // 단어 예문 구문별 해석 토글
    toggleWordExampleParsed(word) {
        const container = document.getElementById(`word-example-parsed-${word}`);
        if (container) {
            container.style.display = container.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    // 언어 모드 설정
    setLanguageMode(mode) {
        this.languageMode = mode;
        App.state.languageMode = mode;
        
        // 버튼 상태 업데이트
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.closest('.lang-btn').classList.add('active');
    }

    // 통계 초기화
    resetStats() {
        if (confirm('학습 기록을 모두 초기화하시겠습니까?')) {
            this.studyData = {
                completedItems: [],
                wrongItems: [],
                bookmarkedItems: [],
                stats: { correct: 0, wrong: 0, total: 0 },
                lastStudyDate: null,
                streak: 0
            };
            this.saveStudyData();
            this.renderDashboard();
        }
    }

}

// 전역 인스턴스
const cisspModule = new CISSPModule();
window.cisspModule = cisspModule;


