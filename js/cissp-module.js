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
        this.difficultWordLearningMode = false; // 어려운 단어 학습 모드
        this.difficultWordLearningIndex = 0;
        this.difficultWordLearningList = [];
        this.sentenceLearningMode = false;
        this.sentenceLearningIndex = 0;
        this.sentenceLearningList = [];
        this.sentencePhrases = []; // 숙어/구문 리스트
        this.sentenceLearningView = 'pattern'; // 'pattern' 또는 'phrase'
        this.phraseTranslations = null; // 구문별 번역 데이터 (JSON 파일에서 로드)
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
            streak: 0,
            memorizedWords: [], // 자주 나오는 단어 암기 완료 목록
            memorizedDifficultWords: [] // 어려운 단어 암기 완료 목록
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

    // 구문별 번역 데이터 로드 (선택적)
    async loadPhraseTranslations() {
        try {
            // 구문별 번역 파일이 있으면 로드 (없어도 동작 가능)
            const response = await fetch('data/cissp_phrase_translations.json');
            if (response.ok) {
                this.phraseTranslations = await response.json();
                console.log('구문별 번역 데이터 로드 완료');
            } else {
                // 파일이 없어도 계속 진행
                this.phraseTranslations = null;
                console.log('구문별 번역 파일이 없습니다. 계속 진행합니다.');
            }
        } catch (error) {
            // 에러가 발생해도 계속 진행
            this.phraseTranslations = null;
            console.log('구문별 번역 데이터 로드 실패 (계속 진행):', error);
        }
    }

    // 데이터 로드
    async loadItems() {
        try {
            // 구문별 번역 데이터 먼저 로드 (선택적)
            await this.loadPhraseTranslations();
            
            const response = await fetch('data/items_cissp.jsonl');
            
            if (!response.ok) {
                console.error(`CISSP 데이터 파일 로드 실패: HTTP ${response.status} ${response.statusText}`);
                this.items = [];
                return [];
            }
            
            const text = await response.text();
            
            if (!text.trim()) {
                console.error('CISSP 데이터 파일이 비어있습니다.');
                this.items = [];
                return [];
            }
            
            // JSONL 파싱 (빈 줄 제외)
            const lines = text.trim().split('\n').filter(line => line.trim());
            this.items = lines.map((line, index) => {
                try {
                    return JSON.parse(line);
                } catch (parseError) {
                    console.error(`라인 ${index + 1} 파싱 오류:`, parseError, line.substring(0, 100));
                    return null;
                }
            }).filter(item => item !== null); // null 제거
            
            console.log(`CISSP ${this.items.length}개 문제 로드 완료`);
            
            if (this.items.length === 0) {
                console.error('CISSP 데이터가 없습니다. 파일을 확인해주세요.');
            }
            
            // 단어 사전도 로드
            await this.loadVocabulary();
            
            return this.items;
        } catch (error) {
            console.error('CISSP 데이터 로드 실패:', error);
            console.error('에러 상세:', error.stack);
            this.items = [];
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
        // 데이터가 없으면 로드 시도
        if (this.items.length === 0) {
            console.log('CISSP 데이터 로드 중...');
            await this.loadItems();
        }
        
        const container = document.getElementById('questionContainer');
        const stats = this.calculateStats();
        
        const hasData = this.items.length > 0;
        
        // 데이터 로드 실패 시 상세 정보 로그
        if (!hasData) {
            console.error('CISSP 데이터가 없습니다. 파일 경로와 내용을 확인해주세요.');
            console.error('예상 파일 경로: data/items_cissp.jsonl');
        }
        
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
                <div class="main-study-modes">
                    <h3 class="section-title"><i class="fas fa-book-reader"></i> 단어 & 문장 학습</h3>
                    <div class="main-mode-grid">
                        <button class="main-mode-card accent" onclick="cisspModule.startWordLearning()">
                            <div class="mode-icon"><i class="fas fa-spell-check"></i></div>
                            <div class="mode-title">자주 나오는 단어 학습</div>
                            <div class="mode-desc" id="word-learning-count">로딩 중...</div>
                        </button>
                        <button class="main-mode-card bookmarked" onclick="cisspModule.startDifficultWordLearning()">
                            <div class="mode-icon"><i class="fas fa-graduation-cap"></i></div>
                            <div class="mode-title">어려운 단어 학습</div>
                            <div class="mode-desc" id="difficult-word-learning-count">로딩 중...</div>
                        </button>
                        <button class="main-mode-card secondary" onclick="cisspModule.startSentenceLearning()">
                            <div class="mode-icon"><i class="fas fa-quote-left"></i></div>
                            <div class="mode-title">자주 나오는 문장 학습</div>
                            <div class="mode-desc" id="sentence-learning-count">로딩 중...</div>
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
                wordCountEl.textContent = `빈도 40 이상 ${frequentWords.length}개 단어`;
            }
            
            // 어려운 단어 개수 계산
            const difficultWords = Object.entries(problemVocab)
                .filter(([word, data]) => {
                    const freq = data.frequency || 0;
                    const wordLen = word.length;
                    // 빈도 1-15, 길이 8 이상, 또는 빈도 1-10인 단어
                    return (freq >= 1 && freq <= 15 && wordLen >= 8) || (freq >= 1 && freq <= 10);
                })
                .sort((a, b) => {
                    // 먼저 길이순 (긴 단어 우선), 그 다음 빈도순 (낮은 빈도 우선)
                    const lenDiff = b[0].length - a[0].length;
                    if (lenDiff !== 0) return lenDiff;
                    return a[1].frequency - b[1].frequency;
                })
                .slice(0, 500); // 최대 500개
            
            const difficultWordCountEl = document.getElementById('difficult-word-learning-count');
            if (difficultWordCountEl) {
                difficultWordCountEl.textContent = `빈도 낮은 어려운 단어 ${difficultWords.length}개`;
            }
            
            // 문장 패턴 개수 계산
            const sentenceCountEl = document.getElementById('sentence-learning-count');
            if (sentenceCountEl) {
                // 문제에서 문장 추출
                const sentences = [];
                for (const item of this.items) {
                    if (item.question_en) {
                        const questionSentences = item.question_en.split(/[.!?]\s+/).filter(s => s.trim().length > 10);
                        for (const sent of questionSentences) {
                            if (sent.trim().length > 10) {
                                sentences.push({
                                    sentence_en: sent.trim(),
                                    sentence_ko: item.question_ko ? item.question_ko.split(/[.!?]\s+/).find((s, idx) => idx < questionSentences.length && s.trim().length > 10) || '' : '',
                                    source: `문제 ${item.q_no}`
                                });
                            }
                        }
                    }
                }
                
                // 패턴별로 그룹화하여 개수 계산
                const patternGroups = this.groupSentencesByPattern(sentences);
                const phraseCount = this.extractCommonPhrases(sentences, 3).length;
                
                sentenceCountEl.textContent = `패턴 ${patternGroups.length}개, 구문 ${phraseCount}개`;
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
            
            // 암기 완료된 단어 목록 가져오기
            const memorizedWords = this.studyData.memorizedWords || [];
            
            // 빈도 40 이상인 단어들 필터링 및 정렬 (암기 완료된 단어 제외)
            const frequentWords = Object.entries(problemVocab)
                .filter(([word, data]) => {
                    // 빈도 40 이상이고 암기 완료되지 않은 단어만
                    return data.frequency >= 40 && !memorizedWords.includes(word.toLowerCase());
                })
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
                alert('학습할 단어가 없습니다. (모든 단어를 암기 완료했거나 조건에 맞는 단어가 없습니다.)');
                return;
            }
            
            // 단어 학습 모드로 전환
            this.wordLearningMode = true;
            this.difficultWordLearningMode = false; // 어려운 단어 학습 모드 비활성화
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
        // 어려운 단어 학습 모드인 경우 해당 렌더링 함수 호출
        if (this.difficultWordLearningMode) {
            this.renderDifficultWordLearning();
            return;
        }
        
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
                                    <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
                                        <button class="btn btn-sm btn-info" onclick="cisspModule.speakSentence('${currentWord.example.replace(/'/g, "\\'").replace(/"/g, '&quot;')}')" title="예문 음성으로 읽기">
                                            <i class="fas fa-volume-up"></i> 예문 읽어주기
                                        </button>
                                        ${this.vocabulary[currentWord.word] && this.vocabulary[currentWord.word].example_parsed ? `
                                            <button class="btn btn-sm btn-secondary" onclick="cisspModule.toggleWordExampleParsed('${currentWord.word}')">
                                                <i class="fas fa-list-ol"></i> 구문별 해석 보기
                                            </button>
                                        ` : ''}
                                    </div>
                                    ${this.vocabulary[currentWord.word] && this.vocabulary[currentWord.word].example_parsed ? `
                                        <div class="word-example-parsed" id="word-example-parsed-${currentWord.word}" style="display: none; margin-top: 10px;">
                                            ${this.renderPhraseTranslation(this.vocabulary[currentWord.word].example_parsed)}
                                        </div>
                                    ` : ''}
                                </div>
                            ` : ''}
                        </div>
                        <div class="word-action-buttons" style="display: flex; gap: 10px; align-items: center; margin-top: 15px; flex-wrap: wrap;">
                            <button class="btn btn-primary btn-show-meaning" onclick="cisspModule.toggleWordMeaning()">
                                <i class="fas fa-eye"></i> 의미 보기
                            </button>
                            <button class="btn btn-info" onclick="cisspModule.speakWord('${currentWord.word.replace(/'/g, "\\'").replace(/"/g, '&quot;')}')" title="음성으로 읽기">
                                <i class="fas fa-volume-up"></i> 읽어주기
                            </button>
                            <label class="memorized-checkbox" style="display: flex; align-items: center; gap: 8px; cursor: pointer; user-select: none;">
                                <input type="checkbox" id="word-memorized-checkbox" data-word="${currentWord.word.replace(/"/g, '&quot;')}" data-is-difficult="false" ${this.isWordMemorized(currentWord.word, false) ? 'checked' : ''} onchange="cisspModule.toggleWordMemorizedFromCheckbox(this)">
                                <span><i class="fas fa-check-circle"></i> 암기 완료</span>
                            </label>
                        </div>
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
        if (this.difficultWordLearningMode) {
            this.prevDifficultWord();
            return;
        }
        
        if (this.wordLearningIndex > 0) {
            this.wordLearningIndex--;
            this.renderWordLearning();
        }
    }
    
    // 다음 단어
    nextWord() {
        if (this.difficultWordLearningMode) {
            this.nextDifficultWord();
            return;
        }
        
        if (this.wordLearningIndex < this.wordLearningList.length - 1) {
            this.wordLearningIndex++;
            this.renderWordLearning();
        }
    }
    
    // 어려운 단어 학습 시작
    async startDifficultWordLearning() {
        try {
            // 빈도 낮은 어려운 단어들 로드
            const problemVocabResponse = await fetch('data/cissp_problem_vocabulary.json');
            const problemVocab = await problemVocabResponse.json();
            
            // 암기 완료된 어려운 단어 목록 가져오기
            const memorizedDifficultWords = this.studyData.memorizedDifficultWords || [];
            
            // 어려운 단어 필터링 기준:
            // 1. 빈도 1-15이고 길이 8 이상인 단어
            // 2. 또는 빈도 1-10인 단어
            // 3. 암기 완료되지 않은 단어만
            const difficultWords = Object.entries(problemVocab)
                .filter(([word, data]) => {
                    const freq = data.frequency || 0;
                    const wordLen = word.length;
                    const isMemorized = memorizedDifficultWords.includes(word.toLowerCase());
                    // 빈도 1-15, 길이 8 이상, 또는 빈도 1-10인 단어이고 암기 완료되지 않은 것만
                    return !isMemorized && ((freq >= 1 && freq <= 15 && wordLen >= 8) || (freq >= 1 && freq <= 10));
                })
                .map(([word, data]) => ({
                    word: word,
                    meaning: data.meaning || '',
                    pos: data.pos || 'unknown',
                    frequency: data.frequency || 0,
                    example: data.example || ''
                }))
                .sort((a, b) => {
                    // 먼저 길이순 (긴 단어 우선), 그 다음 빈도순 (낮은 빈도 우선)
                    const lenDiff = b.word.length - a.word.length;
                    if (lenDiff !== 0) return lenDiff;
                    return a.frequency - b.frequency;
                })
                .slice(0, 500); // 최대 500개
            
            if (difficultWords.length === 0) {
                alert('학습할 어려운 단어가 없습니다. (모든 단어를 암기 완료했거나 조건에 맞는 단어가 없습니다.)');
                return;
            }
            
            // 어려운 단어 학습 모드로 전환
            this.difficultWordLearningMode = true;
            this.wordLearningMode = false; // 일반 단어 학습 모드 비활성화
            this.difficultWordLearningIndex = 0;
            this.difficultWordLearningList = difficultWords;
            
            this.renderDifficultWordLearning();
        } catch (error) {
            console.error('어려운 단어 학습 시작 실패:', error);
            alert('어려운 단어 학습 데이터를 불러올 수 없습니다.');
        }
    }
    
    // 어려운 단어 학습 렌더링
    renderDifficultWordLearning() {
        if (!this.difficultWordLearningList || this.difficultWordLearningList.length === 0) {
            return;
        }
        
        const currentWord = this.difficultWordLearningList[this.difficultWordLearningIndex];
        const progress = ((this.difficultWordLearningIndex + 1) / this.difficultWordLearningList.length * 100).toFixed(1);
        
        // 단어 사전에서 추가 정보 가져오기
        const wordData = this.vocabulary[currentWord.word.toLowerCase()] || {};
        
        // 의미 찾기: 1) currentWord.meaning, 2) wordData.meaning, 3) items_cissp.jsonl에서 한국어 번역 찾기
        let fullMeaning = currentWord.meaning || wordData.meaning || '';
        
        // 의미가 없으면 items_cissp.jsonl에서 한국어 번역 찾기
        if (!fullMeaning || fullMeaning.trim() === '') {
            const wordLower = currentWord.word.toLowerCase();
            
            // items에서 해당 단어가 포함된 문제 찾기 (선택지 우선)
            let foundMeaning = '';
            
            for (const item of this.items) {
                // 선택지에서 먼저 찾기
                for (const [key, value] of Object.entries(item.choices_en || {})) {
                    if (value.toLowerCase().includes(wordLower)) {
                        const koValue = item.choices_ko[key] || '';
                        if (koValue && koValue.trim()) {
                            foundMeaning = koValue.trim();
                            break;
                        }
                    }
                }
                
                if (foundMeaning) break;
                
                // 문제 본문에서 찾기
                if ((item.question_en || '').toLowerCase().includes(wordLower)) {
                    // 문제 본문의 한국어 번역에서 해당 부분 찾기 (간단한 추출)
                    const questionKo = item.question_ko || '';
                    if (questionKo) {
                        // 간단하게 문장의 일부를 추출 (더 정확한 매칭은 복잡하므로 일단 생략)
                    }
                }
            }
            
            fullMeaning = foundMeaning || '의미 없음';
        }
        
        const fullExample = currentWord.example || wordData.example || '';
        
        const container = document.getElementById('questionContainer');
        container.innerHTML = `
            <div class="word-learning-container">
                <div class="word-learning-header">
                    <button class="btn btn-back" onclick="cisspModule.renderDashboard()">
                        <i class="fas fa-arrow-left"></i> 대시보드로
                    </button>
                    <h2><i class="fas fa-graduation-cap"></i> 어려운 단어 학습</h2>
                    <div class="word-learning-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <div class="progress-text">${this.difficultWordLearningIndex + 1} / ${this.difficultWordLearningList.length} (${progress}%)</div>
                    </div>
                </div>
                
                <div class="word-learning-card">
                    <div class="word-card-main">
                        <div class="word-difficulty-badge">어려운 단어</div>
                        <div class="word-frequency-badge">빈도: ${currentWord.frequency}회 | 길이: ${currentWord.word.length}자</div>
                        <div class="word-display">${currentWord.word}</div>
                        <div class="word-pos">${currentWord.pos !== 'unknown' ? currentWord.pos : ''}</div>
                        <div class="word-meaning-display" id="difficult-word-meaning-display" style="display: none;">
                            <div class="word-meaning-text">${fullMeaning}</div>
                            ${fullExample ? `
                                <div class="word-example-display">
                                    <div class="example-label">예문:</div>
                                    <div class="example-text">"${fullExample}"</div>
                                    <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
                                        <button class="btn btn-sm btn-info" onclick="cisspModule.speakSentence('${fullExample.replace(/'/g, "\\'").replace(/"/g, '&quot;')}')" title="예문 음성으로 읽기">
                                            <i class="fas fa-volume-up"></i> 예문 읽어주기
                                        </button>
                                        ${wordData.example_parsed ? `
                                            <button class="btn btn-sm btn-secondary" onclick="cisspModule.toggleDifficultWordExampleParsed('${currentWord.word}')">
                                                <i class="fas fa-list-ol"></i> 구문별 해석 보기
                                            </button>
                                        ` : ''}
                                    </div>
                                    ${wordData.example_parsed ? `
                                        <div class="word-example-parsed" id="difficult-word-example-parsed-${currentWord.word}" style="display: none; margin-top: 10px;">
                                            ${this.renderPhraseTranslation(wordData.example_parsed)}
                                        </div>
                                    ` : ''}
                                </div>
                            ` : ''}
                        </div>
                        <div class="word-action-buttons" style="display: flex; gap: 10px; align-items: center; margin-top: 15px; flex-wrap: wrap;">
                            <button class="btn btn-primary btn-show-meaning" onclick="cisspModule.toggleDifficultWordMeaning()">
                                <i class="fas fa-eye"></i> 의미 보기
                            </button>
                            <button class="btn btn-info" onclick="cisspModule.speakWord('${currentWord.word.replace(/'/g, "\\'").replace(/"/g, '&quot;')}')" title="음성으로 읽기">
                                <i class="fas fa-volume-up"></i> 읽어주기
                            </button>
                            <label class="memorized-checkbox" style="display: flex; align-items: center; gap: 8px; cursor: pointer; user-select: none;">
                                <input type="checkbox" id="difficult-word-memorized-checkbox" data-word="${currentWord.word.replace(/"/g, '&quot;')}" data-is-difficult="true" ${this.isWordMemorized(currentWord.word, true) ? 'checked' : ''} onchange="cisspModule.toggleWordMemorizedFromCheckbox(this)">
                                <span><i class="fas fa-check-circle"></i> 암기 완료</span>
                            </label>
                        </div>
                    </div>
                    
                    <div class="word-learning-controls">
                        <button class="btn btn-secondary" onclick="cisspModule.prevDifficultWord()" ${this.difficultWordLearningIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전
                        </button>
                        <button class="btn btn-primary" onclick="cisspModule.nextDifficultWord()" ${this.difficultWordLearningIndex === this.difficultWordLearningList.length - 1 ? 'disabled' : ''}>
                            다음 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // 의미 보기 상태 초기화
        document.getElementById('difficult-word-meaning-display').style.display = 'none';
    }
    
    // 어려운 단어 의미 토글
    toggleDifficultWordMeaning() {
        const meaningDisplay = document.getElementById('difficult-word-meaning-display');
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
    
    // 어려운 단어 예문 구문별 해석 토글
    toggleDifficultWordExampleParsed(word) {
        const container = document.getElementById(`difficult-word-example-parsed-${word}`);
        if (container) {
            container.style.display = container.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    // 이전 어려운 단어
    prevDifficultWord() {
        if (this.difficultWordLearningIndex > 0) {
            this.difficultWordLearningIndex--;
            this.renderDifficultWordLearning();
        }
    }
    
    // 다음 어려운 단어
    nextDifficultWord() {
        if (this.difficultWordLearningIndex < this.difficultWordLearningList.length - 1) {
            this.difficultWordLearningIndex++;
            this.renderDifficultWordLearning();
        }
    }
    
    // TTS 음성 읽어주기 (공통 함수)
    speakText(text, lang = 'en-US') {
        // 기존 음성 중지
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
            
            // HTML 엔티티 디코딩
            const decodedText = text.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
            
            const utterance = new SpeechSynthesisUtterance(decodedText);
            utterance.lang = lang;
            utterance.rate = 0.9; // 읽기 속도 (0.1 ~ 10)
            utterance.pitch = 1.0; // 음성 높이 (0 ~ 2)
            utterance.volume = 1.0; // 음량 (0 ~ 1)
            
            // 음성 목록이 로드되기를 기다림
            const selectVoice = () => {
                const voices = window.speechSynthesis.getVoices();
                if (voices.length > 0) {
                    // 영어 음성 선택 (가능한 경우)
                    const englishVoice = voices.find(voice => 
                        voice.lang.startsWith('en') && 
                        (voice.name.includes('English') || voice.name.includes('US') || voice.name.includes('UK'))
                    );
                    if (englishVoice) {
                        utterance.voice = englishVoice;
                    }
                    window.speechSynthesis.speak(utterance);
                } else {
                    // 음성 목록이 아직 로드되지 않았으면 잠시 후 재시도
                    setTimeout(() => {
                        const voices = window.speechSynthesis.getVoices();
                        if (voices.length > 0) {
                            const englishVoice = voices.find(voice => 
                                voice.lang.startsWith('en') && 
                                (voice.name.includes('English') || voice.name.includes('US') || voice.name.includes('UK'))
                            );
                            if (englishVoice) {
                                utterance.voice = englishVoice;
                            }
                        }
                        window.speechSynthesis.speak(utterance);
                    }, 100);
                }
            };
            
            // 음성 목록 로드 이벤트 리스너 (한 번만)
            if (!this.voicesLoaded) {
                window.speechSynthesis.onvoiceschanged = () => {
                    this.voicesLoaded = true;
                };
            }
            
            selectVoice();
        } else {
            console.warn('SpeechSynthesis API를 지원하지 않는 브라우저입니다.');
            alert('이 브라우저는 음성 읽기 기능을 지원하지 않습니다.');
        }
    }
    
    // 단어 읽어주기
    speakWord(word) {
        this.speakText(word, 'en-US');
    }
    
    // 문장 읽어주기
    speakSentence(sentence) {
        this.speakText(sentence, 'en-US');
    }
    
    // TTS 중지
    stopSpeaking() {
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
    }
    
    // 단어 암기 완료 여부 확인
    isWordMemorized(word, isDifficult) {
        const wordLower = word.toLowerCase();
        if (isDifficult) {
            return (this.studyData.memorizedDifficultWords || []).includes(wordLower);
        } else {
            return (this.studyData.memorizedWords || []).includes(wordLower);
        }
    }
    
    // 체크박스에서 호출되는 암기 완료 토글 (안전한 문자열 처리)
    toggleWordMemorizedFromCheckbox(checkbox) {
        const word = checkbox.getAttribute('data-word');
        const isDifficult = checkbox.getAttribute('data-is-difficult') === 'true';
        this.toggleWordMemorized(word, isDifficult);
    }
    
    // 단어 암기 완료 토글
    toggleWordMemorized(word, isDifficult) {
        const wordLower = word.toLowerCase();
        
        if (isDifficult) {
            // 어려운 단어 목록
            if (!this.studyData.memorizedDifficultWords) {
                this.studyData.memorizedDifficultWords = [];
            }
            
            const index = this.studyData.memorizedDifficultWords.indexOf(wordLower);
            if (index > -1) {
                // 암기 완료 해제
                this.studyData.memorizedDifficultWords.splice(index, 1);
            } else {
                // 암기 완료 추가
                this.studyData.memorizedDifficultWords.push(wordLower);
            }
        } else {
            // 자주 나오는 단어 목록
            if (!this.studyData.memorizedWords) {
                this.studyData.memorizedWords = [];
            }
            
            const index = this.studyData.memorizedWords.indexOf(wordLower);
            if (index > -1) {
                // 암기 완료 해제
                this.studyData.memorizedWords.splice(index, 1);
            } else {
                // 암기 완료 추가
                this.studyData.memorizedWords.push(wordLower);
            }
        }
        
        // 저장
        this.saveStudyData();
        
        // 현재 단어가 암기 완료되었으면 목록에서 제거하고 다음 단어로 이동
        if (this.isWordMemorized(word, isDifficult)) {
            // 목록에서 제거
            if (isDifficult) {
                this.difficultWordLearningList = this.difficultWordLearningList.filter(w => w.word.toLowerCase() !== wordLower);
                // 인덱스 조정
                if (this.difficultWordLearningIndex >= this.difficultWordLearningList.length) {
                    this.difficultWordLearningIndex = Math.max(0, this.difficultWordLearningList.length - 1);
                }
                // 재렌더링
                if (this.difficultWordLearningList.length > 0) {
                    this.renderDifficultWordLearning();
                } else {
                    alert('모든 단어를 암기 완료했습니다!');
                    this.renderDashboard();
                }
            } else {
                this.wordLearningList = this.wordLearningList.filter(w => w.word.toLowerCase() !== wordLower);
                // 인덱스 조정
                if (this.wordLearningIndex >= this.wordLearningList.length) {
                    this.wordLearningIndex = Math.max(0, this.wordLearningList.length - 1);
                }
                // 재렌더링
                if (this.wordLearningList.length > 0) {
                    this.renderWordLearning();
                } else {
                    alert('모든 단어를 암기 완료했습니다!');
                    this.renderDashboard();
                }
            }
        }
    }
    
    // 구조적 문장 패턴 정의 (24개 이상으로 확장)
    getSentencePatterns() {
        return [
            {
                pattern: /^Which of the following is (?:the )?(?:BEST|MOST|PRIMARY|key|critical|important|essential)/i,
                name: "Which of the following is (BEST/MOST/PRIMARY)",
                category: "question_pattern",
                description: "최선/가장/주요한 것을 묻는 패턴",
                detailedDescription: "이 패턴은 여러 선택지 중에서 가장 적합한 답을 찾는 문제에서 자주 사용됩니다. 'BEST'는 최선의 방법, 'MOST'는 가장 많은/중요한 것, 'PRIMARY'는 주요한 것을 의미합니다. CISSP 시험에서 가장 빈번하게 출제되는 패턴 중 하나입니다. 구문별 해석: 'Which of the following' (다음 중 어느 것입니까) + 'is BEST/MOST/PRIMARY' (가장 ~인가) + 'when/where/in which' (언제/어디서/어느 것에서) + '주제/상황' (주어/목적어).",
                usageExamples: [
                    {
                        en: "Which of the following is key when assessing weakness in authenticator recovery?",
                        ko: "인증자 복구의 취약점을 평가할 때 핵심이 되는 것은 다음 중 무엇인가?",
                        phrases: [
                            {phrase: "Which of the following", translation: "다음 중 어느 것입니까", order: 1, role: "질문 시작"},
                            {phrase: "is key", translation: "핵심인가", order: 2, role: "동사구"},
                            {phrase: "when assessing weakness", translation: "약점을 평가할 때", order: 3, role: "부사구"},
                            {phrase: "in authenticator recovery", translation: "인증자 복구에서", order: 4, role: "전치사구"}
                        ]
                    },
                    {
                        en: "Which of the following is the BEST method to secure data?",
                        ko: "데이터를 보호하는 최선의 방법은 다음 중 무엇인가?",
                        phrases: [
                            {phrase: "Which of the following", translation: "다음 중 어느 것입니까", order: 1, role: "질문 시작"},
                            {phrase: "is the BEST method", translation: "가장 좋은 방법인가", order: 2, role: "동사구"},
                            {phrase: "to secure data", translation: "데이터를 보호하는", order: 3, role: "목적어"}
                        ]
                    },
                    {
                        en: "Which of the following is MOST critical when assessing risk?",
                        ko: "위험을 평가할 때 가장 중요한 것은 다음 중 무엇인가?",
                        phrases: [
                            {phrase: "Which of the following", translation: "다음 중 어느 것입니까", order: 1, role: "질문 시작"},
                            {phrase: "is MOST critical", translation: "가장 중요한가", order: 2, role: "동사구"},
                            {phrase: "when assessing risk", translation: "위험을 평가할 때", order: 3, role: "부사구"}
                        ]
                    }
                ],
                grammarNote: "Which of the following + is/are + (형용사) + 명사 형태로 구성됩니다. 'the following'은 '다음의 것들'을 의미하며, 복수형이지만 단수 동사 'is'를 사용합니다. 'when/where/in which' 같은 부사구나 전치사구가 뒤에 오면 '~할 때/어디서/어느 것에서'라는 조건이나 상황을 나타냅니다.",
                examFrequency: "매우 높음 (CISSP 시험의 약 30% 이상)"
            },
            {
                pattern: /^What is (?:the )?(?:BEST|PRIMARY|MAIN|characteristic of|purpose of|role of)/i,
                name: "What is (BEST/PRIMARY/MAIN/characteristic)",
                category: "question_pattern",
                description: "무엇인지 묻는 패턴",
                detailedDescription: "개념, 특성, 목적, 역할 등을 묻는 직접적인 질문 패턴입니다. 'What is'로 시작하여 명확한 정의나 설명을 요구하는 문제에 사용됩니다. 구문별 해석: 'What is' (무엇인가) + '(the) BEST/PRIMARY/MAIN' (가장 좋은/주요한/주요한) + 'characteristic/purpose/role' (특성/목적/역할) + 'of ~' (~의).",
                usageExamples: [
                    {
                        en: "What is a characteristic of Secure Socket Layer (SSL) and Transport Layer Security (TLS)?",
                        ko: "SSL과 TLS의 특성은 무엇인가?",
                        phrases: [
                            {phrase: "What is", translation: "무엇인가", order: 1, role: "질문 시작"},
                            {phrase: "a characteristic", translation: "특성은", order: 2, role: "주어"},
                            {phrase: "of Secure Socket Layer (SSL) and Transport Layer Security (TLS)", translation: "SSL과 TLS의", order: 3, role: "전치사구"}
                        ]
                    },
                    {
                        en: "What is the PRIMARY purpose of access control?",
                        ko: "접근 통제의 주요 목적은 무엇인가?",
                        phrases: [
                            {phrase: "What is", translation: "무엇인가", order: 1, role: "질문 시작"},
                            {phrase: "the PRIMARY purpose", translation: "주요 목적은", order: 2, role: "주어"},
                            {phrase: "of access control", translation: "접근 통제의", order: 3, role: "전치사구"}
                        ]
                    },
                    {
                        en: "What is the MAIN purpose of conducting a business impact analysis (BIA)?",
                        ko: "업무 영향 분석(BIA)을 수행하는 주요 목적은 무엇인가?",
                        phrases: [
                            {phrase: "What is", translation: "무엇인가", order: 1, role: "질문 시작"},
                            {phrase: "the MAIN purpose", translation: "주요 목적은", order: 2, role: "주어"},
                            {phrase: "of conducting a business impact analysis (BIA)", translation: "업무 영향 분석(BIA)을 수행하는", order: 3, role: "전치사구"}
                        ]
                    }
                ],
                grammarNote: "What is + (형용사) + 명사/동명사 형태입니다. 'What'은 주어이면서 목적어 역할을 합니다. 'characteristic of ~'는 '~의 특성', 'purpose of ~'는 '~의 목적', 'role of ~'는 '~의 역할'을 의미합니다.",
                examFrequency: "높음 (약 15-20%)"
            },
            {
                pattern: /^An organization (?:wants to|is looking to|has decided to|should|must|needs to|is planning to)/i,
                name: "An organization (action)",
                category: "scenario_pattern",
                description: "조직의 행동/의도를 나타내는 패턴",
                detailedDescription: "실제 비즈니스 시나리오를 제시하는 패턴입니다. 조직이 특정 목표를 달성하기 위해 취해야 할 조치나 의사결정을 묻는 문제에 사용됩니다. 구문별 해석: 'An organization' (조직이) + 'wants to/is looking to/has decided to' (원한다/찾고 있다/결정했다) + '목적/행동' (무엇을 할지).",
                usageExamples: [
                    {
                        en: "An organization wants to enable users to authenticate across multiple security domains.",
                        ko: "조직이 여러 보안 도메인에서 사용자 인증을 가능하게 하려고 한다.",
                        phrases: [
                            {phrase: "An organization", translation: "조직이", order: 1, role: "주어"},
                            {phrase: "wants to enable", translation: "가능하게 하려고 한다", order: 2, role: "동사구"},
                            {phrase: "users to authenticate", translation: "사용자가 인증하는 것을", order: 3, role: "목적어"},
                            {phrase: "across multiple security domains", translation: "여러 보안 도메인에서", order: 4, role: "부사구"}
                        ]
                    },
                    {
                        en: "An organization is looking to include mobile devices in its asset management system.",
                        ko: "조직이 자산 관리 시스템에 모바일 장치를 포함하려고 한다.",
                        phrases: [
                            {phrase: "An organization", translation: "조직이", order: 1, role: "주어"},
                            {phrase: "is looking to include", translation: "포함하려고 찾고 있다", order: 2, role: "동사구"},
                            {phrase: "mobile devices", translation: "모바일 장치를", order: 3, role: "목적어"},
                            {phrase: "in its asset management system", translation: "자산 관리 시스템에", order: 4, role: "전치사구"}
                        ]
                    },
                    {
                        en: "An organization has decided to terminate a relationship with a third party vendor.",
                        ko: "조직이 제3자 벤더와의 관계를 종료하기로 결정했다.",
                        phrases: [
                            {phrase: "An organization", translation: "조직이", order: 1, role: "주어"},
                            {phrase: "has decided to terminate", translation: "종료하기로 결정했다", order: 2, role: "동사구"},
                            {phrase: "a relationship", translation: "관계를", order: 3, role: "목적어"},
                            {phrase: "with a third party vendor", translation: "제3자 벤더와의", order: 4, role: "전치사구"}
                        ]
                    }
                ],
                grammarNote: "An organization + (조동사/동사) + to 부정사/동사원형 형태입니다. 'organization'은 단수이므로 단수 동사를 사용합니다. 'wants to'는 '~하려고 한다', 'is looking to'는 '~하려고 찾고 있다', 'has decided to'는 '~하기로 결정했다'는 의미입니다.",
                examFrequency: "높음 (약 20%)"
            },
            {
                pattern: /^Which of the following (?:should|must|would|can|could|will)/i,
                name: "Which of the following (should/must)",
                category: "question_pattern",
                description: "해야 할 것을 묻는 패턴",
                detailedDescription: "의무, 권장사항, 가능성을 묻는 패턴입니다. 'should'는 권장사항, 'must'는 필수사항, 'would/could'는 가능성을 나타냅니다.",
                usageExamples: [
                    "Which of the following should be implemented first?",
                    "Which of the following must be verified during authentication?",
                    "Which of the following would be the most secure?"
                ],
                grammarNote: "Which of the following + 조동사 + 동사원형 형태입니다.",
                examFrequency: "높음 (약 15%)"
            },
            {
                pattern: /^What (?:BEST|PRIMARY|MAIN|MOST) (?:describes|explains|identifies|defines)/i,
                name: "What (BEST/PRIMARY) describes",
                category: "question_pattern",
                description: "설명/정의를 묻는 패턴",
                detailedDescription: "개념이나 용어를 가장 잘 설명하는 것을 찾는 패턴입니다. 정의 문제나 개념 이해 문제에서 자주 사용됩니다.",
                usageExamples: [
                    "What BEST describes the purpose of encryption?",
                    "What PRIMARY explains the difference between authentication and authorization?",
                    "What MOST identifies the key characteristic of a firewall?"
                ],
                grammarNote: "What + (형용사) + 동사(describes/explains 등) 형태입니다.",
                examFrequency: "중간 (약 10%)"
            },
            {
                pattern: /^Which of the following (?:is|are) (?:used|required|needed|designed|implemented)/i,
                name: "Which of the following is used/required",
                category: "question_pattern",
                description: "사용/요구되는 것을 묻는 패턴",
                detailedDescription: "특정 목적을 위해 사용되거나 요구되는 기술, 방법, 도구를 묻는 패턴입니다.",
                usageExamples: [
                    "Which of the following is used to encrypt data?",
                    "Which of the following is required for secure communication?",
                    "Which of the following is designed to prevent unauthorized access?"
                ],
                grammarNote: "Which of the following + is/are + 과거분사 형태입니다. 수동태 구조입니다.",
                examFrequency: "높음 (약 15%)"
            },
            {
                pattern: /^A (?:company|organization|security professional|practitioner) (?:is|has|wants|needs)/i,
                name: "A company/organization (state)",
                category: "scenario_pattern",
                description: "회사/조직의 상태를 나타내는 패턴",
                detailedDescription: "조직이나 전문가의 현재 상태나 상황을 설명하는 패턴입니다.",
                usageExamples: [
                    "A company is experiencing security breaches.",
                    "A security professional has identified vulnerabilities.",
                    "An organization wants to improve compliance."
                ],
                grammarNote: "A + 명사 + 동사 형태입니다.",
                examFrequency: "중간 (약 8%)"
            },
            {
                pattern: /^What (?:testing|method|technique|approach|strategy|control) (?:enables|provides|ensures|protects)/i,
                name: "What method/technique (action)",
                category: "question_pattern",
                description: "방법/기법의 효과를 묻는 패턴",
                detailedDescription: "특정 방법이나 기법이 제공하는 효과나 기능을 묻는 패턴입니다. 구문별 해석: 'What' (무엇이) + 'testing method/technique/approach' (테스트 방법/기법/접근법) + 'enables/provides/ensures' (가능하게 한다/제공한다/보장한다) + '목적/효과' (무엇을).",
                usageExamples: [
                    {
                        en: "What testing technique enables the designer to develop mitigation strategies for potential vulnerabilities?",
                        ko: "잠재적 취약점에 대한 완화 전략을 개발할 수 있게 하는 테스트 기법은 무엇인가?",
                        phrases: [
                            {phrase: "What testing technique", translation: "어떤 테스트 기법이", order: 1, role: "주어"},
                            {phrase: "enables the designer", translation: "설계자가 가능하게 한다", order: 2, role: "동사구"},
                            {phrase: "to develop mitigation strategies", translation: "완화 전략을 개발하는 것을", order: 3, role: "목적어"},
                            {phrase: "for potential vulnerabilities", translation: "잠재적 취약점에 대한", order: 4, role: "전치사구"}
                        ]
                    },
                    {
                        en: "What method provides secure authentication?",
                        ko: "안전한 인증을 제공하는 방법은 무엇인가?",
                        phrases: [
                            {phrase: "What method", translation: "어떤 방법이", order: 1, role: "주어"},
                            {phrase: "provides", translation: "제공한다", order: 2, role: "동사"},
                            {phrase: "secure authentication", translation: "안전한 인증을", order: 3, role: "목적어"}
                        ]
                    },
                    {
                        en: "What approach ensures data confidentiality?",
                        ko: "데이터 기밀성을 보장하는 접근법은 무엇인가?",
                        phrases: [
                            {phrase: "What approach", translation: "어떤 접근법이", order: 1, role: "주어"},
                            {phrase: "ensures", translation: "보장한다", order: 2, role: "동사"},
                            {phrase: "data confidentiality", translation: "데이터 기밀성을", order: 3, role: "목적어"}
                        ]
                    }
                ],
                grammarNote: "What + 명사 + 동사 형태입니다. 'What'은 의문사로 주어 역할을 하며, 'testing method', 'technique', 'approach' 등은 '테스트 방법', '기법', '접근법'을 의미합니다. 'enables'는 '가능하게 한다', 'provides'는 '제공한다', 'ensures'는 '보장한다'는 의미입니다.",
                examFrequency: "중간 (약 10%)"
            },
            {
                pattern: /^Which of the following (?:areas|components|layers|tiers|domains) (?:need|require|have)/i,
                name: "Which of the following areas/components",
                category: "question_pattern",
                description: "영역/구성요소를 묻는 패턴",
                detailedDescription: "시스템의 특정 영역이나 구성요소에 대한 질문 패턴입니다.",
                usageExamples: [
                    "Which of the following areas need additional security controls?",
                    "Which of the following components require encryption?",
                    "Which of the following layers have the most vulnerabilities?"
                ],
                grammarNote: "Which of the following + 복수명사 + 동사 형태입니다.",
                examFrequency: "중간 (약 8%)"
            },
            {
                pattern: /^What is (?:a|an|the) (?:characteristic|feature|benefit|challenge|risk|threat)/i,
                name: "What is a characteristic/feature",
                category: "question_pattern",
                description: "특성/기능을 묻는 패턴",
                detailedDescription: "기술이나 개념의 특성, 기능, 이점, 도전과제 등을 묻는 패턴입니다.",
                usageExamples: [
                    "What is a characteristic of symmetric encryption?",
                    "What is the main benefit of using VPN?",
                    "What is a challenge in implementing cloud security?"
                ],
                grammarNote: "What is + (a/an/the) + 명사 형태입니다.",
                examFrequency: "중간 (약 10%)"
            },
            {
                pattern: /^In which (?:system|layer|tier|domain|phase|stage)/i,
                name: "In which system/layer",
                category: "question_pattern",
                description: "시스템/계층을 묻는 패턴",
                detailedDescription: "특정 시스템, 계층, 도메인, 단계를 묻는 패턴입니다.",
                usageExamples: [
                    "In which system layer does encryption occur?",
                    "In which phase of SDLC should security be considered?",
                    "In which domain does access control belong?"
                ],
                grammarNote: "In which + 명사 형태입니다. 'which'는 의문형용사로 사용됩니다.",
                examFrequency: "낮음 (약 5%)"
            },
            {
                pattern: /^What (?:MUST|SHOULD|CAN) (?:the|a|an)/i,
                name: "What MUST/SHOULD",
                category: "question_pattern",
                description: "필수/권장 사항을 묻는 패턴",
                detailedDescription: "필수사항이나 권장사항을 강조하는 패턴입니다.",
                usageExamples: [
                    "What MUST the administrator do to secure the system?",
                    "What SHOULD be included in a security policy?",
                    "What CAN be done to prevent data breaches?"
                ],
                grammarNote: "What + 조동사(MUST/SHOULD/CAN) + 주어 + 동사 형태입니다.",
                examFrequency: "중간 (약 8%)"
            },
            // 추가 패턴 (12개 → 24개 이상)
            {
                pattern: /^How (?:should|can|must|would|will) (?:the|a|an|you|we|they)/i,
                name: "How should/can/must",
                category: "question_pattern",
                description: "방법을 묻는 패턴",
                detailedDescription: "특정 작업을 수행하는 방법이나 절차를 묻는 패턴입니다. 'How'는 '어떻게'를 의미하며, 방법론이나 절차에 대한 질문에 사용됩니다.",
                usageExamples: [
                    "How should the organization implement access controls?",
                    "How can security professionals detect intrusions?",
                    "How must data be encrypted during transmission?"
                ],
                grammarNote: "How + 조동사 + 주어 + 동사 형태입니다. 'How'는 부사로 사용됩니다.",
                examFrequency: "중간 (약 10%)"
            },
            {
                pattern: /^What would be (?:the|a|an)/i,
                name: "What would be the",
                category: "question_pattern",
                description: "가능성을 묻는 패턴",
                detailedDescription: "가정적 상황이나 가능한 결과를 묻는 패턴입니다. 'would'는 가정법이나 가능성을 나타냅니다.",
                usageExamples: [
                    "What would be the BEST approach in this scenario?",
                    "What would be the PRIMARY concern when migrating to cloud?",
                    "What would be an appropriate response to this threat?"
                ],
                grammarNote: "What would be + (the/a/an) + 명사 형태입니다.",
                examFrequency: "중간 (약 8%)"
            },
            {
                pattern: /^The (?:PRIMARY|BEST|MOST|main|key) (?:important|critical|essential|significant)/i,
                name: "The PRIMARY/BEST/MOST important",
                category: "question_pattern",
                description: "가장 중요한 것을 강조하는 패턴",
                detailedDescription: "중요도나 우선순위를 강조하는 패턴입니다.",
                usageExamples: [
                    "The PRIMARY important factor in security is...",
                    "The BEST critical consideration when...",
                    "The MOST essential element for..."
                ],
                grammarNote: "The + (형용사) + (형용사) + 명사 형태입니다.",
                examFrequency: "낮음 (약 5%)"
            },
            {
                pattern: /^When (?:should|can|must|would|will) (?:the|a|an|you|we|they)/i,
                name: "When should/can/must",
                category: "question_pattern",
                description: "시기를 묻는 패턴",
                detailedDescription: "특정 작업을 수행해야 할 시기나 조건을 묻는 패턴입니다.",
                usageExamples: [
                    "When should encryption be applied?",
                    "When can access be granted?",
                    "When must security controls be reviewed?"
                ],
                grammarNote: "When + 조동사 + 주어 + 동사 형태입니다.",
                examFrequency: "중간 (약 8%)"
            },
            {
                pattern: /^Why (?:is|are|should|would|can|must)/i,
                name: "Why is/are",
                category: "question_pattern",
                description: "이유를 묻는 패턴",
                detailedDescription: "특정 조치나 결정의 이유나 근거를 묻는 패턴입니다.",
                usageExamples: [
                    "Why is encryption important for data protection?",
                    "Why should organizations implement access controls?",
                    "Why must security policies be regularly updated?"
                ],
                grammarNote: "Why + 조동사/be동사 + 주어 형태입니다.",
                examFrequency: "낮음 (약 5%)"
            },
            {
                pattern: /^Where (?:should|can|must|would|will) (?:the|a|an|you|we|they)/i,
                name: "Where should/can/must",
                category: "question_pattern",
                description: "장소/위치를 묻는 패턴",
                detailedDescription: "특정 작업이 수행되어야 할 장소나 위치를 묻는 패턴입니다.",
                usageExamples: [
                    "Where should security controls be implemented?",
                    "Where can sensitive data be stored?",
                    "Where must encryption keys be kept?"
                ],
                grammarNote: "Where + 조동사 + 주어 + 동사 형태입니다.",
                examFrequency: "낮음 (약 3%)"
            },
            {
                pattern: /^Who (?:should|can|must|would|will)/i,
                name: "Who should/can/must",
                category: "question_pattern",
                description: "누구를 묻는 패턴",
                detailedDescription: "특정 작업을 수행해야 할 사람이나 역할을 묻는 패턴입니다.",
                usageExamples: [
                    "Who should have access to sensitive data?",
                    "Who can approve security changes?",
                    "Who must be notified in case of a breach?"
                ],
                grammarNote: "Who + 조동사 + 동사 형태입니다. 'Who'는 주어 역할을 합니다.",
                examFrequency: "낮음 (약 3%)"
            },
            {
                pattern: /^It is (?:important|critical|essential|necessary|required) to/i,
                name: "It is important/critical/essential to",
                category: "scenario_pattern",
                description: "중요성을 강조하는 패턴",
                detailedDescription: "특정 조치의 중요성이나 필요성을 강조하는 패턴입니다.",
                usageExamples: [
                    "It is important to implement strong authentication.",
                    "It is critical to encrypt sensitive data.",
                    "It is essential to regularly update security policies."
                ],
                grammarNote: "It is + 형용사 + to 부정사 형태입니다. 'It'는 가주어, to 부정사가 진주어입니다.",
                examFrequency: "중간 (약 8%)"
            },
            {
                pattern: /^The (?:main|primary|key|principal) (?:purpose|goal|objective|aim) of/i,
                name: "The main/primary purpose of",
                category: "scenario_pattern",
                description: "목적을 설명하는 패턴",
                detailedDescription: "특정 기술이나 조치의 주요 목적을 설명하는 패턴입니다.",
                usageExamples: [
                    "The main purpose of encryption is to protect data confidentiality.",
                    "The primary goal of access control is to prevent unauthorized access.",
                    "The key objective of security policies is to establish guidelines."
                ],
                grammarNote: "The + (형용사) + 명사 + of 형태입니다.",
                examFrequency: "중간 (약 7%)"
            },
            {
                pattern: /^One of the (?:most|best|primary|key) (?:important|critical|essential)/i,
                name: "One of the most important",
                category: "scenario_pattern",
                description: "중요한 것 중 하나를 강조하는 패턴",
                detailedDescription: "여러 중요한 요소 중 하나를 강조하는 패턴입니다.",
                usageExamples: [
                    "One of the most important aspects of security is...",
                    "One of the best practices for encryption is...",
                    "One of the primary concerns in cloud computing is..."
                ],
                grammarNote: "One of the + (형용사) + 복수명사 형태입니다.",
                examFrequency: "중간 (약 7%)"
            },
            {
                pattern: /^The key to/i,
                name: "The key to",
                category: "scenario_pattern",
                description: "핵심을 강조하는 패턴",
                detailedDescription: "성공이나 효과의 핵심 요소를 강조하는 패턴입니다.",
                usageExamples: [
                    "The key to effective security is proper access control.",
                    "The key to preventing breaches is early detection.",
                    "The key to compliance is regular auditing."
                ],
                grammarNote: "The key to + 명사/동명사 형태입니다.",
                examFrequency: "중간 (약 6%)"
            },
            {
                pattern: /^In order to/i,
                name: "In order to",
                category: "scenario_pattern",
                description: "목적을 나타내는 패턴",
                detailedDescription: "특정 목적을 달성하기 위한 조건이나 요구사항을 설명하는 패턴입니다.",
                usageExamples: [
                    "In order to secure the system, encryption must be implemented.",
                    "In order to comply with regulations, audits must be conducted.",
                    "In order to prevent attacks, firewalls should be configured."
                ],
                grammarNote: "In order to + 동사원형 형태입니다. '~하기 위해'를 의미합니다.",
                examFrequency: "중간 (약 8%)"
            },
            {
                pattern: /^To (?:ensure|protect|prevent|maintain|achieve|implement)/i,
                name: "To ensure/protect/prevent",
                category: "scenario_pattern",
                description: "목적을 나타내는 to 부정사 패턴",
                detailedDescription: "목적을 나타내는 to 부정사로 시작하는 패턴입니다.",
                usageExamples: [
                    "To ensure security, strong passwords must be used.",
                    "To protect data, encryption should be applied.",
                    "To prevent attacks, firewalls need to be configured."
                ],
                grammarNote: "To + 동사원형 형태입니다. 목적을 나타내는 부정사입니다.",
                examFrequency: "중간 (약 7%)"
            },
            {
                pattern: /^The (?:first|primary|main|key) (?:step|action|measure|consideration) (?:is|should be|must be)/i,
                name: "The first/primary step",
                category: "scenario_pattern",
                description: "첫 단계나 주요 조치를 설명하는 패턴",
                detailedDescription: "절차나 프로세스의 첫 단계나 주요 조치를 설명하는 패턴입니다.",
                usageExamples: [
                    "The first step in securing a system is to identify vulnerabilities.",
                    "The primary action should be to implement access controls.",
                    "The main measure must be to encrypt sensitive data."
                ],
                grammarNote: "The + (형용사) + 명사 + (is/should be/must be) 형태입니다.",
                examFrequency: "중간 (약 6%)"
            }
        ];
    }
    
    // 문장에서 패턴 추출
    extractSentencePattern(sentence) {
        const patterns = this.getSentencePatterns();
        for (const patternDef of patterns) {
            if (patternDef.pattern.test(sentence)) {
                return patternDef;
            }
        }
        return null;
    }
    
    // 패턴별로 문장 그룹화
    groupSentencesByPattern(sentences) {
        const patternGroups = {};
        
        for (const sentence of sentences) {
            const patternDef = this.extractSentencePattern(sentence.sentence_en);
            
            if (patternDef) {
                const patternKey = patternDef.name;
                
                if (!patternGroups[patternKey]) {
                    patternGroups[patternKey] = {
                        pattern: patternKey,
                        category: patternDef.category,
                        description: patternDef.description,
                        frequency: 0,
                        examples: []
                    };
                }
                
                patternGroups[patternKey].frequency++;
                patternGroups[patternKey].examples.push({
                    sentence_en: sentence.sentence_en,
                    sentence_ko: sentence.sentence_ko,
                    source: sentence.source
                });
            }
        }
        
        // 빈도순으로 정렬하고, 각 패턴의 예시는 최대 10개로 제한
        const sortedGroups = Object.values(patternGroups)
            .sort((a, b) => b.frequency - a.frequency)
            .map(group => ({
                ...group,
                examples: group.examples.slice(0, 10) // 최대 10개 예시
            }));
        
        return sortedGroups;
    }
    
    // 자주 나오는 숙어/구문 추출
    // 구문 설명 데이터
    getPhraseDescriptions() {
        return {
            "assess weakness": {
                meaning: "취약점을 평가하다",
                detailedMeaning: "시스템이나 프로세스의 약점을 식별하고 분석하는 과정을 의미합니다. 보안 평가의 핵심 단계입니다. CISSP 맥락에서는 'assess weakness in authenticator recovery' (인증자 복구에서 취약점을 평가하다)와 같이 사용됩니다.",
                context: "보안 평가, 위험 분석, 감사 과정에서 자주 사용됩니다. 예: 'when assessing weakness in authenticator recovery' (인증자 복구에서 취약점을 평가할 때).",
                grammar: "동사 + 명사 구조 (assess는 타동사). 'assess weakness in ~' 형태로 '~에서 취약점을 평가하다'는 의미입니다.",
                similarPhrases: ["evaluate vulnerability", "analyze weakness", "identify gap"],
                examples: [
                    {
                        en: "key when assessing weakness in authenticator recovery",
                        ko: "인증자 복구에서 취약점을 평가할 때의 핵심",
                        phraseBreakdown: [
                            {phrase: "key", translation: "핵심", role: "명사"},
                            {phrase: "when assessing weakness", translation: "취약점을 평가할 때", role: "부사구"},
                            {phrase: "in authenticator recovery", translation: "인증자 복구에서", role: "전치사구"}
                        ]
                    }
                ]
            },
            "gain access": {
                meaning: "접근 권한을 얻다",
                detailedMeaning: "시스템, 데이터, 리소스에 대한 접근 권한을 획득하는 것을 의미합니다. CISSP 맥락에서는 'gain privileged access to a system' (시스템에 대한 권한 있는 접근을 얻다)와 같이 사용됩니다.",
                context: "접근 제어, 인증, 권한 관리 맥락에서 사용됩니다. 예: 'to gain privileged access to a system' (시스템에 대한 권한 있는 접근을 얻기 위해).",
                grammar: "동사 + 명사 구조. 'gain access to ~' 형태로 '~에 대한 접근을 얻다'는 의미입니다.",
                similarPhrases: ["obtain access", "acquire permission", "get authorization"],
                examples: [
                    {
                        en: "to gain privileged access to a system",
                        ko: "시스템에 대한 권한 있는 접근을 얻기 위해",
                        phraseBreakdown: [
                            {phrase: "to gain", translation: "얻기 위해", role: "부정사"},
                            {phrase: "privileged access", translation: "권한 있는 접근을", role: "목적어"},
                            {phrase: "to a system", translation: "시스템에 대한", role: "전치사구"}
                        ]
                    }
                ]
            },
            "ensure compliance": {
                meaning: "컴플라이언스를 보장하다",
                detailedMeaning: "규정, 표준, 정책을 준수하도록 보장하는 것을 의미합니다. CISSP 맥락에서는 'ensure compliance with regulations' (규정 준수를 보장하다)와 같이 사용됩니다.",
                context: "규정 준수, 감사, 거버넌스 맥락에서 사용됩니다. 예: 'to ensure compliance' (컴플라이언스를 보장하기 위해), 'ensure compliance with PCI-DSS' (PCI-DSS 준수를 보장하다).",
                grammar: "동사 + 명사 구조. 'ensure compliance with ~' 형태로 '~에 대한 준수를 보장하다'는 의미입니다.",
                similarPhrases: ["maintain compliance", "achieve compliance", "verify compliance"],
                examples: [
                    {
                        en: "An organization is required to comply with PCI-DSS, what is the MOST effective approach to ensure compliance?",
                        ko: "조직이 PCI-DSS를 준수해야 하는 경우, 컴플라이언스를 보장하는 가장 효과적인 접근 방식은?",
                        phraseBreakdown: [
                            {phrase: "to ensure", translation: "보장하기 위해", role: "부정사"},
                            {phrase: "compliance", translation: "컴플라이언스를", role: "목적어"},
                            {phrase: "with PCI-DSS", translation: "PCI-DSS에 대한", role: "전치사구"}
                        ]
                    }
                ]
            },
            "mitigate risk": {
                meaning: "위험을 완화하다",
                detailedMeaning: "위험의 가능성이나 영향을 줄이는 조치를 취하는 것을 의미합니다. CISSP 맥락에서는 'develop mitigation strategies for potential vulnerabilities' (잠재적 취약점에 대한 완화 전략을 개발하다)와 같이 사용됩니다.",
                context: "위험 관리, 보안 조치 맥락에서 사용됩니다. 예: 'to mitigate risk' (위험을 완화하기 위해), 'mitigation strategies' (완화 전략).",
                grammar: "동사 + 명사 구조. 'mitigate risk'는 '위험을 완화하다', 'mitigation strategies'는 '완화 전략'을 의미합니다.",
                similarPhrases: ["reduce risk", "minimize risk", "control risk"],
                examples: [
                    {
                        en: "develop mitigation strategies for potential vulnerabilities",
                        ko: "잠재적 취약점에 대한 완화 전략을 개발하다",
                        phraseBreakdown: [
                            {phrase: "develop", translation: "개발하다", role: "동사"},
                            {phrase: "mitigation strategies", translation: "완화 전략을", role: "목적어"},
                            {phrase: "for potential vulnerabilities", translation: "잠재적 취약점에 대한", role: "전치사구"}
                        ]
                    }
                ]
            },
            "implement control": {
                meaning: "통제를 구현하다",
                detailedMeaning: "보안 통제나 관리 통제를 실제로 적용하는 것을 의미합니다. CISSP 맥락에서는 'implement security controls' (보안 통제를 구현하다)와 같이 사용됩니다.",
                context: "보안 구현, 거버넌스 맥락에서 사용됩니다. 예: 'implement access controls' (접근 통제를 구현하다), 'implement security controls' (보안 통제를 구현하다).",
                grammar: "동사 + 명사 구조. 'implement control'는 '통제를 구현하다', 'implement controls'는 '통제들을 구현하다'는 의미입니다.",
                similarPhrases: ["deploy control", "establish control", "apply control"],
                examples: [
                    {
                        en: "Which of the following controls should be implemented to prevent attacks?",
                        ko: "공격을 방지하기 위해 구현해야 하는 통제는 다음 중 무엇인가?",
                        phraseBreakdown: [
                            {phrase: "controls", translation: "통제들이", role: "주어"},
                            {phrase: "should be implemented", translation: "구현되어야 한다", role: "동사구"},
                            {phrase: "to prevent attacks", translation: "공격을 방지하기 위해", role: "부정사구"}
                        ]
                    }
                ]
            },
            "establish policy": {
                meaning: "정책을 수립하다",
                detailedMeaning: "규칙이나 가이드라인을 공식적으로 만들고 시행하는 것을 의미합니다. CISSP 맥락에서는 'establish security policy' (보안 정책을 수립하다)와 같이 사용됩니다.",
                context: "정책 수립, 거버넌스 맥락에서 사용됩니다. 예: 'establish a data retention policy' (데이터 보존 정책을 수립하다), 'establish security policies' (보안 정책을 수립하다).",
                grammar: "동사 + 명사 구조. 'establish policy'는 '정책을 수립하다', 'establish a policy'는 '정책을 수립하다'는 의미입니다.",
                similarPhrases: ["create policy", "develop policy", "formulate policy"],
                examples: [
                    {
                        en: "Which of the following should be included in a hardware retention policy?",
                        ko: "하드웨어 보존 정책에 포함되어야 하는 것은 다음 중 무엇인가?",
                        phraseBreakdown: [
                            {phrase: "should be included", translation: "포함되어야 한다", role: "동사구"},
                            {phrase: "in a hardware retention policy", translation: "하드웨어 보존 정책에", role: "전치사구"}
                        ]
                    }
                ]
            },
            "maintain confidentiality": {
                meaning: "기밀성을 유지하다",
                detailedMeaning: "정보가 무단 접근으로부터 보호되도록 하는 것을 의미합니다. CIA 삼각형의 핵심 요소입니다.",
                context: "정보 보안, 데이터 보호 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["preserve confidentiality", "protect confidentiality", "ensure confidentiality"]
            },
            "protect data": {
                meaning: "데이터를 보호하다",
                detailedMeaning: "데이터의 무결성, 기밀성, 가용성을 보장하는 것을 의미합니다.",
                context: "데이터 보안, 정보 보호 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["secure data", "safeguard data", "defend data"]
            },
            "prevent attack": {
                meaning: "공격을 방지하다",
                detailedMeaning: "보안 공격이 발생하지 않도록 사전에 조치를 취하는 것을 의미합니다.",
                context: "보안 방어, 위협 대응 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["block attack", "stop attack", "thwart attack"]
            },
            "detect threat": {
                meaning: "위협을 탐지하다",
                detailedMeaning: "보안 위협이나 잠재적 공격을 식별하고 인지하는 것을 의미합니다.",
                context: "위협 탐지, 보안 모니터링 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["identify threat", "recognize threat", "discover threat"]
            },
            "respond to incident": {
                meaning: "사고에 대응하다",
                detailedMeaning: "보안 사고나 침해 사고가 발생했을 때 적절한 조치를 취하는 것을 의미합니다.",
                context: "사고 대응, 보안 운영 맥락에서 사용됩니다.",
                grammar: "동사 + 전치사 + 명사 구조",
                similarPhrases: ["handle incident", "address incident", "manage incident"]
            },
            "manage risk": {
                meaning: "위험을 관리하다",
                detailedMeaning: "위험을 식별, 평가, 완화하는 전체 프로세스를 의미합니다.",
                context: "위험 관리, 거버넌스 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["handle risk", "control risk", "address risk"]
            },
            "ensure security": {
                meaning: "보안을 보장하다",
                detailedMeaning: "시스템이나 조직의 보안 상태를 유지하고 보장하는 것을 의미합니다.",
                context: "보안 관리, 거버넌스 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["maintain security", "provide security", "guarantee security"]
            },
            "provide protection": {
                meaning: "보호를 제공하다",
                detailedMeaning: "시스템이나 데이터에 대한 보호 기능을 제공하는 것을 의미합니다.",
                context: "보안 서비스, 보호 조치 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["offer protection", "deliver protection", "supply protection"]
            },
            "identify vulnerability": {
                meaning: "취약점을 식별하다",
                detailedMeaning: "시스템이나 프로세스의 보안 취약점을 찾아내는 것을 의미합니다.",
                context: "취약점 평가, 보안 평가 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["discover vulnerability", "find vulnerability", "detect vulnerability"]
            },
            "implement security": {
                meaning: "보안을 구현하다",
                detailedMeaning: "보안 조치나 보안 시스템을 실제로 적용하는 것을 의미합니다.",
                context: "보안 구현, 보안 아키텍처 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["deploy security", "establish security", "apply security"]
            },
            "maintain integrity": {
                meaning: "무결성을 유지하다",
                detailedMeaning: "데이터나 시스템의 무결성을 보장하고 유지하는 것을 의미합니다. CIA 삼각형의 핵심 요소입니다.",
                context: "데이터 보호, 시스템 보안 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["preserve integrity", "protect integrity", "ensure integrity"]
            },
            "ensure availability": {
                meaning: "가용성을 보장하다",
                detailedMeaning: "시스템이나 서비스가 필요할 때 사용 가능하도록 보장하는 것을 의미합니다. CIA 삼각형의 핵심 요소입니다.",
                context: "시스템 가용성, 서비스 연속성 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["maintain availability", "provide availability", "guarantee availability"]
            },
            "protect information": {
                meaning: "정보를 보호하다",
                detailedMeaning: "정보의 기밀성, 무결성, 가용성을 보장하는 것을 의미합니다.",
                context: "정보 보안, 데이터 보호 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["secure information", "safeguard information", "defend information"]
            },
            "prevent unauthorized": {
                meaning: "무단 접근을 방지하다",
                detailedMeaning: "권한이 없는 접근이나 행동을 막는 것을 의미합니다.",
                context: "접근 제어, 보안 방어 맥락에서 사용됩니다.",
                grammar: "동사 + 형용사 구조",
                similarPhrases: ["block unauthorized", "stop unauthorized", "deny unauthorized"]
            },
            "detect intrusion": {
                meaning: "침입을 탐지하다",
                detailedMeaning: "무단 침입이나 공격을 식별하고 인지하는 것을 의미합니다.",
                context: "침입 탐지, 보안 모니터링 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["identify intrusion", "recognize intrusion", "discover intrusion"]
            },
            "respond to breach": {
                meaning: "침해에 대응하다",
                detailedMeaning: "보안 침해 사고가 발생했을 때 적절한 조치를 취하는 것을 의미합니다.",
                context: "사고 대응, 보안 운영 맥락에서 사용됩니다.",
                grammar: "동사 + 전치사 + 명사 구조",
                similarPhrases: ["handle breach", "address breach", "manage breach"]
            },
            "manage access": {
                meaning: "접근을 관리하다",
                detailedMeaning: "사용자의 접근 권한을 제어하고 관리하는 것을 의미합니다.",
                context: "접근 제어, 권한 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["control access", "regulate access", "administer access"]
            },
            "ensure privacy": {
                meaning: "프라이버시를 보장하다",
                detailedMeaning: "개인정보나 민감한 정보의 프라이버시를 보호하는 것을 의미합니다.",
                context: "개인정보 보호, 데이터 프라이버시 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["maintain privacy", "protect privacy", "preserve privacy"]
            },
            "provide authentication": {
                meaning: "인증을 제공하다",
                detailedMeaning: "사용자나 시스템의 신원을 확인하는 인증 기능을 제공하는 것을 의미합니다.",
                context: "인증 시스템, 접근 제어 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["offer authentication", "deliver authentication", "supply authentication"]
            },
            "implement encryption": {
                meaning: "암호화를 구현하다",
                detailedMeaning: "데이터를 암호화하여 보호하는 기능을 실제로 적용하는 것을 의미합니다.",
                context: "데이터 보호, 암호화 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["deploy encryption", "apply encryption", "use encryption"]
            },
            "establish procedure": {
                meaning: "절차를 수립하다",
                detailedMeaning: "공식적인 절차나 프로세스를 만들고 시행하는 것을 의미합니다.",
                context: "프로세스 관리, 거버넌스 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["create procedure", "develop procedure", "formulate procedure"]
            },
            "maintain compliance": {
                meaning: "컴플라이언스를 유지하다",
                detailedMeaning: "규정이나 표준을 지속적으로 준수하도록 유지하는 것을 의미합니다.",
                context: "규정 준수, 감사 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["preserve compliance", "ensure compliance", "keep compliance"]
            },
            "protect asset": {
                meaning: "자산을 보호하다",
                detailedMeaning: "조직의 정보 자산이나 물리적 자산을 보호하는 것을 의미합니다.",
                context: "자산 관리, 보안 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["secure asset", "safeguard asset", "defend asset"]
            },
            "prevent disclosure": {
                meaning: "공개를 방지하다",
                detailedMeaning: "민감한 정보가 무단으로 공개되거나 노출되는 것을 막는 것을 의미합니다.",
                context: "정보 보호, 데이터 보안 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["block disclosure", "stop disclosure", "avoid disclosure"]
            },
            "detect anomaly": {
                meaning: "이상 징후를 탐지하다",
                detailedMeaning: "정상적인 패턴과 다른 이상 징후나 비정상적인 활동을 식별하는 것을 의미합니다.",
                context: "보안 모니터링, 이상 탐지 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["identify anomaly", "recognize anomaly", "discover anomaly"]
            },
            "respond to threat": {
                meaning: "위협에 대응하다",
                detailedMeaning: "보안 위협이나 공격에 대해 적절한 조치를 취하는 것을 의미합니다.",
                context: "위협 대응, 보안 운영 맥락에서 사용됩니다.",
                grammar: "동사 + 전치사 + 명사 구조",
                similarPhrases: ["handle threat", "address threat", "manage threat"]
            },
            "manage identity": {
                meaning: "신원을 관리하다",
                detailedMeaning: "사용자나 시스템의 신원 정보를 관리하고 제어하는 것을 의미합니다.",
                context: "신원 관리, 접근 제어 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["control identity", "administer identity", "regulate identity"]
            },
            // 추가 구문 (32개 → 64개 이상)
            "conduct assessment": {
                meaning: "평가를 수행하다",
                detailedMeaning: "보안 평가나 위험 평가를 체계적으로 수행하는 것을 의미합니다.",
                context: "보안 평가, 위험 분석 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["perform assessment", "carry out assessment", "execute assessment"]
            },
            "perform analysis": {
                meaning: "분석을 수행하다",
                detailedMeaning: "데이터나 상황을 체계적으로 분석하는 것을 의미합니다.",
                context: "데이터 분석, 보안 분석 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["conduct analysis", "carry out analysis", "execute analysis"]
            },
            "establish baseline": {
                meaning: "기준선을 수립하다",
                detailedMeaning: "성능이나 보안 상태의 기준선을 설정하는 것을 의미합니다.",
                context: "성능 관리, 보안 기준 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["create baseline", "set baseline", "define baseline"]
            },
            "implement safeguard": {
                meaning: "안전장치를 구현하다",
                detailedMeaning: "보안을 위한 안전장치나 보호 조치를 실제로 적용하는 것을 의미합니다.",
                context: "보안 조치, 보호 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["deploy safeguard", "apply safeguard", "install safeguard"]
            },
            "monitor activity": {
                meaning: "활동을 모니터링하다",
                detailedMeaning: "시스템이나 네트워크의 활동을 지속적으로 관찰하고 추적하는 것을 의미합니다.",
                context: "보안 모니터링, 시스템 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["watch activity", "observe activity", "track activity"]
            },
            "review policy": {
                meaning: "정책을 검토하다",
                detailedMeaning: "기존 정책을 검토하고 필요시 수정하는 것을 의미합니다.",
                context: "정책 관리, 거버넌스 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["examine policy", "evaluate policy", "assess policy"]
            },
            "update configuration": {
                meaning: "구성을 업데이트하다",
                detailedMeaning: "시스템이나 소프트웨어의 설정을 업데이트하는 것을 의미합니다.",
                context: "시스템 관리, 구성 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["modify configuration", "change configuration", "adjust configuration"]
            },
            "validate identity": {
                meaning: "신원을 검증하다",
                detailedMeaning: "사용자나 시스템의 신원이 진짜인지 확인하는 것을 의미합니다.",
                context: "인증, 신원 확인 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["verify identity", "confirm identity", "authenticate identity"]
            },
            "verify compliance": {
                meaning: "컴플라이언스를 검증하다",
                detailedMeaning: "규정이나 표준을 준수하고 있는지 확인하는 것을 의미합니다.",
                context: "규정 준수, 감사 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["check compliance", "confirm compliance", "validate compliance"]
            },
            "document procedure": {
                meaning: "절차를 문서화하다",
                detailedMeaning: "절차나 프로세스를 공식 문서로 작성하는 것을 의미합니다.",
                context: "문서화, 프로세스 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["record procedure", "write procedure", "create documentation"]
            },
            "train personnel": {
                meaning: "인력을 교육하다",
                detailedMeaning: "직원이나 인력에게 보안 교육이나 훈련을 제공하는 것을 의미합니다.",
                context: "보안 교육, 인력 개발 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["educate personnel", "instruct personnel", "teach personnel"]
            },
            "audit system": {
                meaning: "시스템을 감사하다",
                detailedMeaning: "시스템의 보안 상태나 설정을 감사하는 것을 의미합니다.",
                context: "보안 감사, 시스템 감사 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["examine system", "review system", "inspect system"]
            },
            "backup data": {
                meaning: "데이터를 백업하다",
                detailedMeaning: "데이터의 복사본을 만들어 보관하는 것을 의미합니다.",
                context: "데이터 보호, 재해 복구 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["copy data", "duplicate data", "save data"]
            },
            "restore service": {
                meaning: "서비스를 복원하다",
                detailedMeaning: "중단된 서비스를 다시 정상 상태로 복원하는 것을 의미합니다.",
                context: "재해 복구, 서비스 연속성 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["recover service", "resume service", "reestablish service"]
            },
            "recover system": {
                meaning: "시스템을 복구하다",
                detailedMeaning: "손상되거나 중단된 시스템을 정상 상태로 복구하는 것을 의미합니다.",
                context: "재해 복구, 시스템 복구 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["restore system", "repair system", "rebuild system"]
            },
            "investigate incident": {
                meaning: "사고를 조사하다",
                detailedMeaning: "보안 사고나 침해 사고의 원인과 범위를 조사하는 것을 의미합니다.",
                context: "사고 대응, 포렌식 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["examine incident", "analyze incident", "probe incident"]
            },
            "report finding": {
                meaning: "발견 사항을 보고하다",
                detailedMeaning: "조사나 평가에서 발견한 사항을 보고하는 것을 의미합니다.",
                context: "보고, 문서화 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["document finding", "present finding", "communicate finding"]
            },
            "approve request": {
                meaning: "요청을 승인하다",
                detailedMeaning: "접근 요청이나 변경 요청을 승인하는 것을 의미합니다.",
                context: "접근 제어, 변경 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["authorize request", "grant request", "accept request"]
            },
            "deny access": {
                meaning: "접근을 거부하다",
                detailedMeaning: "접근 요청을 거부하거나 접근을 차단하는 것을 의미합니다.",
                context: "접근 제어, 보안 방어 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["block access", "refuse access", "reject access"]
            },
            "revoke privilege": {
                meaning: "권한을 취소하다",
                detailedMeaning: "이미 부여된 권한이나 특권을 취소하는 것을 의미합니다.",
                context: "권한 관리, 접근 제어 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["remove privilege", "withdraw privilege", "cancel privilege"]
            },
            "grant permission": {
                meaning: "권한을 부여하다",
                detailedMeaning: "특정 작업이나 리소스에 대한 권한을 부여하는 것을 의미합니다.",
                context: "권한 관리, 접근 제어 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["give permission", "allow permission", "provide permission"]
            },
            "assign role": {
                meaning: "역할을 할당하다",
                detailedMeaning: "사용자에게 특정 역할이나 책임을 할당하는 것을 의미합니다.",
                context: "역할 기반 접근 제어, 권한 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["allocate role", "designate role", "appoint role"]
            },
            "delegate authority": {
                meaning: "권한을 위임하다",
                detailedMeaning: "권한이나 책임을 다른 사람에게 위임하는 것을 의미합니다.",
                context: "권한 관리, 조직 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["transfer authority", "assign authority", "entrust authority"]
            },
            "transfer responsibility": {
                meaning: "책임을 이전하다",
                detailedMeaning: "책임이나 의무를 다른 사람이나 조직으로 이전하는 것을 의미합니다.",
                context: "조직 관리, 책임 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["hand over responsibility", "assign responsibility", "delegate responsibility"]
            },
            "terminate session": {
                meaning: "세션을 종료하다",
                detailedMeaning: "사용자 세션이나 연결을 종료하는 것을 의미합니다.",
                context: "세션 관리, 접근 제어 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["end session", "close session", "finish session"]
            },
            "establish connection": {
                meaning: "연결을 수립하다",
                detailedMeaning: "네트워크나 시스템 간의 연결을 설정하는 것을 의미합니다.",
                context: "네트워크 관리, 연결 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["create connection", "set up connection", "build connection"]
            },
            "maintain session": {
                meaning: "세션을 유지하다",
                detailedMeaning: "사용자 세션이나 연결을 지속적으로 유지하는 것을 의미합니다.",
                context: "세션 관리, 연결 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["keep session", "preserve session", "sustain session"]
            },
            "encrypt data": {
                meaning: "데이터를 암호화하다",
                detailedMeaning: "데이터를 암호화하여 읽을 수 없게 만드는 것을 의미합니다.",
                context: "데이터 보호, 암호화 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["cipher data", "encode data", "scramble data"]
            },
            "decrypt message": {
                meaning: "메시지를 복호화하다",
                detailedMeaning: "암호화된 메시지를 원래 형태로 복원하는 것을 의미합니다.",
                context: "암호화, 통신 보안 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["decode message", "decipher message", "unscramble message"]
            },
            "sign document": {
                meaning: "문서에 서명하다",
                detailedMeaning: "디지털 서명을 사용하여 문서에 서명하는 것을 의미합니다.",
                context: "디지털 서명, 문서 인증 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["authenticate document", "certify document", "validate document"]
            },
            "verify signature": {
                meaning: "서명을 검증하다",
                detailedMeaning: "디지털 서명이 유효한지 확인하는 것을 의미합니다.",
                context: "디지털 서명, 문서 인증 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["validate signature", "confirm signature", "check signature"]
            },
            "validate certificate": {
                meaning: "인증서를 검증하다",
                detailedMeaning: "디지털 인증서가 유효하고 신뢰할 수 있는지 확인하는 것을 의미합니다.",
                context: "PKI, 인증서 관리 맥락에서 사용됩니다.",
                grammar: "동사 + 명사 구조",
                similarPhrases: ["verify certificate", "check certificate", "authenticate certificate"]
            }
        };
    }
    
    extractCommonPhrases(sentences, minFrequency = 3) {
        const phraseFrequency = {};
        const phraseDescriptions = this.getPhraseDescriptions();
        const commonPhrases = Object.keys(phraseDescriptions);
        
        // 모든 문장을 소문자로 변환하여 검색
        const allText = sentences.map(s => s.sentence_en.toLowerCase()).join(' ');
        
        // 각 구문의 빈도 계산
        for (const phrase of commonPhrases) {
            const regex = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
            const matches = allText.match(regex);
            if (matches) {
                phraseFrequency[phrase] = matches.length;
            }
        }
        
        // 빈도순으로 정렬하고 최소 빈도 이상인 것만 반환
        return Object.entries(phraseFrequency)
            .filter(([phrase, freq]) => freq >= minFrequency)
            .sort((a, b) => b[1] - a[1])
            .map(([phrase, frequency]) => {
                const description = phraseDescriptions[phrase] || {};
                return {
                    phrase: phrase,
                    frequency: frequency,
                    meaning: description.meaning || '',
                    detailedMeaning: description.detailedMeaning || '',
                    context: description.context || '',
                    grammar: description.grammar || '',
                    similarPhrases: description.similarPhrases || [],
                    examples: sentences
                        .filter(s => s.sentence_en.toLowerCase().includes(phrase))
                        .slice(0, 5) // 각 구문당 최대 5개 예시
                        .map(s => ({
                            sentence_en: s.sentence_en,
                            sentence_ko: s.sentence_ko,
                            source: s.source
                        }))
                };
            });
    }
    
    // 자주 나오는 문장 학습 시작
    async startSentenceLearning() {
        try {
            // 문제에서 문장 추출
            const sentences = [];
            
            for (const item of this.items) {
                // 문제 본문에서 문장 추출
                if (item.question_en) {
                    const questionSentences = item.question_en.split(/[.!?]\s+/).filter(s => s.trim().length > 10);
                    const questionKoSentences = item.question_ko ? item.question_ko.split(/[.!?]\s+/).filter(s => s.trim().length > 10) : [];
                    
                    for (let i = 0; i < questionSentences.length; i++) {
                        const sent = questionSentences[i].trim();
                        const sentKo = i < questionKoSentences.length ? questionKoSentences[i].trim() : '';
                        
                        if (sent.length > 10) {
                            sentences.push({
                                sentence_en: sent,
                                sentence_ko: sentKo,
                                source: `문제 ${item.q_no}`
                            });
                        }
                    }
                }
            }
            
            if (sentences.length === 0) {
                alert('학습할 문장이 없습니다.');
                return;
            }
            
            // 패턴별로 그룹화
            const patternGroups = this.groupSentencesByPattern(sentences);
            
            // 숙어/구문 추출
            const commonPhrases = this.extractCommonPhrases(sentences, 3);
            
            // 문장 학습 모드로 전환
            this.sentenceLearningMode = true;
            this.sentenceLearningIndex = 0;
            this.sentenceLearningList = patternGroups; // 패턴 그룹 리스트
            this.sentencePhrases = commonPhrases; // 숙어/구문 리스트
            this.sentenceLearningView = 'pattern'; // 'pattern' 또는 'phrase'
            
            this.renderSentenceLearning();
        } catch (error) {
            console.error('문장 학습 시작 실패:', error);
            alert('문장 학습 데이터를 불러올 수 없습니다.');
        }
    }
    
    // 사전 정의된 구문 매핑 (영어 구문 -> 한국어 번역)
    getPhraseMapping() {
        return {
            // 질문 시작 구문
            "which of the following": "다음 중 어느 것입니까",
            "what is": "무엇인가",
            "what are": "무엇인가",
            "what would": "무엇일 것인가",
            "what should": "무엇해야 하는가",
            "what must": "무엇해야 하는가",
            
            // 동사구
            "is key": "핵심입니다",
            "is the best": "가장 좋은 것은",
            "is most": "가장 ~한 것은",
            "is primary": "주요한 것은",
            "is critical": "중요한 것은",
            "is important": "중요한 것은",
            "is essential": "필수적인 것은",
            "is used": "사용되는 것은",
            "is required": "필요한 것은",
            "is needed": "필요한 것은",
            "are key": "핵심입니다",
            "are the best": "가장 좋은 것은",
            "are most": "가장 ~한 것은",
            
            // 부사구
            "when": "~할 때",
            "when assessing": "평가할 때",
            "when assessing weakness": "약점을 평가할 때",
            "where": "~하는 곳",
            "in which": "어느 것에서",
            "for which": "어느 것에 대해",
            "to which": "어느 것에",
            "with which": "어느 것과 함께",
            "by which": "어느 것에 의해",
            
            // 전치사구
            "in a": "에서",
            "in an": "에서",
            "in the": "에서",
            "in authenticator": "인증자에서",
            "in authenticator recovery": "인증자 복구에서",
            "of the": "~의",
            "of a": "~의",
            "of an": "~의",
            "on the": "~에서",
            "at the": "~에서",
            "for the": "~을 위해",
            "to the": "~에게",
            "with the": "~와 함께",
            "by the": "~에 의해",
            "from the": "~로부터",
            
            // 동명사/명사구
            "assessing weakness": "약점 평가",
            "assessing": "평가",
            "weakness": "약점",
            "recovery": "회복",
            "authenticator recovery": "인증자 복구",
            "authenticator": "인증자",
            
            // 복합 구문 (더 정확한 번역)
            "when assessing weakness": "약점을 평가할 때",
            "in authenticator recovery": "인증자 복구에서",
            "in authenticator": "인증자에서",
            
            // 기타 자주 나오는 구문
            "to gain": "얻기 위해",
            "to secure": "보호하기 위해",
            "to protect": "보호하기 위해",
            "to prevent": "방지하기 위해",
            "to ensure": "보장하기 위해",
            "to implement": "구현하기 위해",
            "to establish": "수립하기 위해",
            "to maintain": "유지하기 위해",
            "to mitigate": "완화하기 위해",
            "to identify": "식별하기 위해",
            "to detect": "탐지하기 위해",
            "to respond": "대응하기 위해",
            "to manage": "관리하기 위해",
            
            // 조직/시스템 관련
            "an organization": "조직이",
            "a company": "회사가",
            "a system": "시스템이",
            "a method": "방법이",
            "a technique": "기법이",
            "an approach": "접근법이",
            "a strategy": "전략이",
            "a control": "통제가",
            "a process": "프로세스가",
            "a procedure": "절차가",
            
            // 접근/권한 관련
            "gain access": "접근 권한을 얻다",
            "gain privileged access": "권한 있는 접근을 얻다",
            "to a system": "시스템에 대한",
            "to the system": "시스템에 대한",
            "access to": "~에 대한 접근",
            "privileged access": "권한 있는 접근",
            
            // 보안 관련
            "security controls": "보안 통제",
            "access control": "접근 통제",
            "data protection": "데이터 보호",
            "risk management": "위험 관리",
            "threat detection": "위협 탐지",
            "incident response": "사고 대응",
            "vulnerability assessment": "취약점 평가",
            "security policy": "보안 정책",
            "compliance": "컴플라이언스",
            "ensure compliance": "컴플라이언스를 보장하다"
        };
    }
    
    // 구문 매핑에서 번역 찾기 (대소문자 무시, 부분 매칭)
    findPhraseMapping(englishPhrase) {
        const mappings = this.getPhraseMapping();
        const lowerPhrase = englishPhrase.toLowerCase().trim();
        
        // 정확한 매칭 시도
        if (mappings[lowerPhrase]) {
            return mappings[lowerPhrase];
        }
        
        // 부분 매칭 시도 (긴 구문에서 짧은 구문 찾기)
        const sortedKeys = Object.keys(mappings).sort((a, b) => b.length - a.length);
        for (const key of sortedKeys) {
            if (lowerPhrase.includes(key) || key.includes(lowerPhrase)) {
                return mappings[key];
            }
        }
        
        return null;
    }
    
    // 문장을 의미 단위로 분리 (단락별 해석용) - 개선된 버전
    parseSentenceIntoPhrases(sentence, koreanTranslation) {
        if (!sentence || !koreanTranslation) {
            return [{
                phrase: sentence || '',
                translation: koreanTranslation || '',
                order: 1,
                role: "전체"
            }];
        }
        
        // 저장된 구문별 번역 데이터가 있으면 우선 사용
        const sentenceKey = sentence.toLowerCase().trim();
        if (this.phraseTranslations && this.phraseTranslations[sentenceKey]) {
            const savedPhrases = this.phraseTranslations[sentenceKey];
            // 저장된 구문 데이터가 있으면 그대로 반환
            if (savedPhrases && savedPhrases.length > 0) {
                return savedPhrases.map(p => ({
                    phrase: p.phrase,
                    translation: p.translation,
                    order: p.order,
                    role: p.role
                }));
            }
        }
        
        // 저장된 데이터가 없으면 기존 로직 사용
        const phrases = [];
        const englishWords = sentence.trim().split(/\s+/);
        const mappings = this.getPhraseMapping();
        
        // 사전 정의된 구문 패턴 (우선순위 순서 - 긴 구문부터)
        // 사용자 요구사항: 더 세밀한 분해 (예: "when assessing weakness" -> "when" + "assessing weakness")
        const predefinedPatterns = [
            // 질문 시작 구문
            { pattern: /^(which\s+of\s+the\s+following)/i, role: "질문 시작", minWords: 4 },
            { pattern: /^(what\s+is|what\s+are|what\s+would|what\s+should|what\s+must)/i, role: "질문 시작", minWords: 2 },
            
            // 동사구 (우선순위 높음)
            { pattern: /^(is\s+the\s+best|are\s+the\s+best)/i, role: "동사구", minWords: 3 },
            { pattern: /^(is\s+key|are\s+key)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+most|are\s+most)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+primary|are\s+primary)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+critical|are\s+critical)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+important|are\s+important)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+essential|are\s+essential)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+used|are\s+used)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+required|are\s+required)/i, role: "동사구", minWords: 2 },
            { pattern: /^(is\s+needed|are\s+needed)/i, role: "동사구", minWords: 2 },
            
            // 동명사구 (복합 구문) - "assessing weakness"를 먼저 매칭
            // "when assessing weakness"가 있으면 "when"을 건너뛰고 "assessing weakness"만 추출
            { pattern: /^(when\s+)?assessing\s+weakness/i, role: "동명사구", minWords: 2, skipWhen: true },
            
            // 부사구 (단일 단어 - "when"은 "assessing weakness" 앞에 있지 않은 경우에만)
            { pattern: /^(when|where|in\s+which|for\s+which|to\s+which|with\s+which|by\s+which)/i, role: "부사구", minWords: 1 },
            
            // 전치사구 (단일 전치사 + 명사 - "in authenticator"를 먼저 매칭)
            { pattern: /^(in\s+authenticator)/i, role: "전치사구", minWords: 2 },
            
            // 명사구 (단일 명사 우선 - "recovery"를 먼저 매칭)
            { pattern: /^(recovery|authenticator)/i, role: "명사", minWords: 1 },
            { pattern: /^(in\s+a|in\s+an|in\s+the)/i, role: "전치사구", minWords: 2 },
            { pattern: /^(of\s+the|of\s+a|of\s+an)/i, role: "전치사구", minWords: 2 },
            { pattern: /^(on\s+the|at\s+the|for\s+the|to\s+the|with\s+the|by\s+the|from\s+the)/i, role: "전치사구", minWords: 2 },
            
            // 부정사구
            { pattern: /^(to\s+gain|to\s+secure|to\s+protect|to\s+prevent|to\s+ensure|to\s+implement|to\s+establish|to\s+maintain|to\s+mitigate|to\s+identify|to\s+detect|to\s+respond|to\s+manage)/i, role: "부정사구", minWords: 2 },
            
            // 주어 구문
            { pattern: /^(an?\s+(?:organization|company|system|method|technique|approach|strategy|control|process|procedure))/i, role: "주어", minWords: 2 },
            
            // 단일 명사/동명사 (마지막 우선순위)
            { pattern: /^(assessing|weakness|recovery|authenticator)/i, role: "명사/동명사", minWords: 1 }
        ];
        
        let currentIndex = 0;
        let order = 1;
        
        // 문장을 구문 단위로 분리
        while (currentIndex < englishWords.length) {
            let matched = false;
            let phraseWords = [];
            let phraseRole = "기타";
            let phraseText = '';
            let koreanTranslation_part = '';
            
            // 남은 텍스트
            const remainingText = englishWords.slice(currentIndex).join(' ');
            const remainingLower = remainingText.toLowerCase();
            
            // 사전 정의된 패턴 매칭 시도
            for (const patternInfo of predefinedPatterns) {
                const match = remainingLower.match(patternInfo.pattern);
                if (match) {
                    let matchedText = match[0];
                    let matchedWords = matchedText.split(/\s+/);
                    let actualPhraseText = matchedText;
                    let actualWords = matchedWords;
                    let skipCount = 0;
                    
                    // "when assessing weakness" 같은 경우 "when"을 건너뛰고 "assessing weakness"만 추출
                    if (patternInfo.skipWhen && remainingLower.startsWith('when ')) {
                        // "when" 다음의 구문만 추출
                        const afterWhen = remainingLower.substring(5); // "when " 제거
                        const afterWhenMatch = afterWhen.match(/^assessing\s+weakness/i);
                        if (afterWhenMatch) {
                            actualPhraseText = afterWhenMatch[0];
                            actualWords = actualPhraseText.split(/\s+/);
                            skipCount = 1; // "when" 건너뛰기
                        }
                    }
                    
                    // 원본 대소문자 유지
                    const originalWords = englishWords.slice(currentIndex + skipCount, currentIndex + skipCount + actualWords.length);
                    phraseWords = originalWords;
                    phraseText = phraseWords.join(' ');
                    phraseRole = patternInfo.role;
                    
                    // 사전 정의된 매핑에서 번역 찾기 (실제 추출된 구문으로)
                    const mapping = this.findPhraseMapping(phraseText);
                    if (mapping) {
                        koreanTranslation_part = mapping;
                    } else {
                        // 매핑이 없으면 extractKoreanForPhrase 사용
                        koreanTranslation_part = this.extractKoreanForPhrase(phraseText, sentence, koreanTranslation, englishWords, currentIndex + skipCount);
                    }
                    
                    currentIndex += skipCount + actualWords.length;
                    matched = true;
                    break;
                }
            }
            
            // 패턴이 매칭되지 않으면 단어 단위로 처리
            if (!matched) {
                // 다음 구분점 찾기
                let nextBreak = englishWords.length;
                for (let i = currentIndex; i < englishWords.length; i++) {
                    const word = englishWords[i].toLowerCase();
                    // 구두점이나 특수 문자
                    if (word.match(/[.!?]$/)) {
                        nextBreak = i + 1;
                        break;
                    }
                    // 연결어
                    if (word.match(/^(when|where|which|that|who|what|how|if|because|since|although|while|in|on|at|for|to|of|with|by|from)$/)) {
                        if (i > currentIndex) {
                            nextBreak = i;
                            break;
                        }
                    }
                }
                
                // 현재 위치부터 다음 구분점까지
                phraseWords = englishWords.slice(currentIndex, nextBreak);
                if (phraseWords.length === 0) {
                    phraseWords = [englishWords[currentIndex]];
                    currentIndex++;
                } else {
                    currentIndex = nextBreak;
                }
                
                phraseText = phraseWords.join(' ');
                phraseRole = this.detectPhraseRole(phraseText);
                
                // 사전 정의된 매핑에서 번역 찾기
                const mapping = this.findPhraseMapping(phraseText);
                if (mapping) {
                    koreanTranslation_part = mapping;
                } else {
                    // 매핑이 없으면 extractKoreanForPhrase 사용
                    koreanTranslation_part = this.extractKoreanForPhrase(phraseText, sentence, koreanTranslation, englishWords, currentIndex - phraseWords.length);
                }
            }
            
            if (phraseWords.length > 0 && phraseText) {
                phrases.push({
                    phrase: phraseText,
                    translation: koreanTranslation_part || phraseText,
                    order: order++,
                    role: phraseRole
                });
            }
            
            // 무한 루프 방지
            if (currentIndex >= englishWords.length) break;
            if (phraseWords.length === 0) currentIndex++;
        }
        
        return phrases.length > 0 ? phrases : [{
            phrase: sentence,
            translation: koreanTranslation,
            order: 1,
            role: "전체"
        }];
    }
    
    // 구문의 문법 역할 감지
    detectPhraseRole(phrase) {
        const lowerPhrase = phrase.toLowerCase().trim();
        if (/^(which|what|who|that|it|this|these|those|an?\s+|the\s+)/i.test(phrase)) {
            return "주어";
        }
        if (/^(is|are|was|were|has|have|had|do|does|did|will|would|should|must|can|could|may|might)\s+/i.test(phrase)) {
            return "동사";
        }
        if (/^(in|on|at|for|to|of|with|by|from)\s+/i.test(phrase)) {
            return "전치사구";
        }
        if (/^(when|where|if|because|since|although|while)\s+/i.test(phrase)) {
            return "부사구";
        }
        return "기타";
    }
    
    // 저장된 구문별 번역 데이터에서 번역 찾기
    findPhraseTranslationInData(fullEnglish, englishPhrase) {
        if (!this.phraseTranslations || !fullEnglish || !englishPhrase) {
            return null;
        }
        
        try {
            const sentenceKey = fullEnglish.toLowerCase().trim();
            const phraseKey = englishPhrase.toLowerCase().trim();
            
            // 전체 문장에 대한 구문별 번역 데이터가 있는지 확인
            if (this.phraseTranslations[sentenceKey]) {
                const savedPhrases = this.phraseTranslations[sentenceKey];
                if (Array.isArray(savedPhrases)) {
                    // 해당 구문 찾기
                    for (const phraseData of savedPhrases) {
                        if (phraseData.phrase && phraseData.phrase.toLowerCase().trim() === phraseKey) {
                            return phraseData.translation || null;
                        }
                    }
                }
            }
        } catch (error) {
            console.error('구문 번역 데이터 검색 오류:', error);
        }
        
        return null;
    }

    // 구문에 해당하는 한국어 추출 (개선된 버전 - 저장된 데이터 우선)
    extractKoreanForPhrase(englishPhrase, fullEnglish, fullKorean, allEnglishWords, phraseStartIndex) {
        if (!fullKorean || !englishPhrase) return '';
        
        // 0. 저장된 구문별 번역 데이터에서 먼저 찾기 (최우선)
        const savedTranslation = this.findPhraseTranslationInData(fullEnglish, englishPhrase);
        if (savedTranslation) {
            return savedTranslation;
        }
        
        // 1. 사전 정의된 매핑에서 찾기
        const predefinedMapping = this.findPhraseMapping(englishPhrase);
        if (predefinedMapping) {
            return predefinedMapping;
        }
        
        // 2. 의미 기반 매칭 시도
        const meaningBasedTranslation = this.extractKoreanByMeaning(englishPhrase, fullEnglish, fullKorean);
        if (meaningBasedTranslation) {
            return meaningBasedTranslation;
        }
        
        // 3. 위치 기반 추출 (보조 수단)
        return this.extractKoreanByPosition(englishPhrase, fullEnglish, fullKorean, allEnglishWords, phraseStartIndex);
    }
    
    // 의미 기반 한국어 추출
    extractKoreanByMeaning(englishPhrase, fullEnglish, fullKorean) {
        if (!fullKorean || !englishPhrase) return '';
        
        const lowerPhrase = englishPhrase.toLowerCase().trim();
        const phraseWords = lowerPhrase.split(/\s+/).filter(w => w.length >= 2);
        
        if (phraseWords.length === 0) return '';
        
        // 영어 구문의 핵심 단어 추출 (3글자 이상)
        const keyWords = phraseWords.filter(w => {
            const clean = w.replace(/[^a-z]/g, '');
            return clean.length >= 3;
        });
        
        // 한국어 번역에서 핵심 단어의 의미를 찾기
        // 예: "assessing weakness" -> "평가", "약점" 찾기
        const keywordMappings = {
            "assessing": ["평가", "평가할"],
            "weakness": ["약점", "취약점"],
            "recovery": ["복구", "회복"],
            "authenticator": ["인증자"],
            "key": ["핵심", "중요한"],
            "best": ["가장 좋은", "최선의"],
            "most": ["가장", "대부분"],
            "primary": ["주요한", "주된"],
            "critical": ["중요한", "핵심적인"],
            "important": ["중요한"],
            "essential": ["필수적인"],
            "following": ["다음"],
            "which": ["어느", "어떤"],
            "what": ["무엇"],
            "when": ["때", "~할 때"],
            "where": ["곳", "~하는 곳"],
            "in": ["에서", "~에서"],
            "of": ["의", "~의"],
            "to": ["~에게", "~하기 위해"],
            "for": ["~을 위해", "~에 대해"],
            "with": ["~와 함께", "~과"],
            "by": ["~에 의해", "~로"],
            "from": ["~로부터", "~에서"],
            "organization": ["조직"],
            "company": ["회사"],
            "system": ["시스템"],
            "method": ["방법"],
            "technique": ["기법"],
            "approach": ["접근법"],
            "strategy": ["전략"],
            "control": ["통제", "제어"],
            "process": ["프로세스", "과정"],
            "procedure": ["절차"]
        };
        
        // 핵심 단어의 한국어 의미 찾기
        const foundMeanings = [];
        for (const word of keyWords) {
            if (keywordMappings[word]) {
                foundMeanings.push(...keywordMappings[word]);
            }
        }
        
        // 한국어 번역에서 해당 의미가 포함된 부분 찾기
        if (foundMeanings.length > 0) {
            for (const meaning of foundMeanings) {
                const index = fullKorean.indexOf(meaning);
                if (index !== -1) {
                    // 해당 의미 주변의 문맥 추출
                    const start = Math.max(0, index - 5);
                    const end = Math.min(fullKorean.length, index + meaning.length + 10);
                    const extracted = fullKorean.substring(start, end).trim();
                    
                    // 자연스러운 구분점에서 자르기
                    const cleanExtracted = this.cleanKoreanExtraction(extracted, fullKorean, index);
                    if (cleanExtracted && cleanExtracted.length > 0) {
                        return cleanExtracted;
                    }
                }
            }
        }
        
        return null;
    }
    
    // 한국어 추출 정리 (자연스러운 구분점에서 자르기)
    cleanKoreanExtraction(extracted, fullKorean, originalIndex) {
        if (!extracted) return '';
        
        // 조사나 구분점에서 자르기
        const koreanParticles = ['은', '는', '이', '가', '을', '를', '에', '에서', '의', '와', '과', '로', '으로', '부터', '까지', '만', '도', '조차', '마저'];
        
        // 앞쪽 정리
        let start = 0;
        for (let i = 0; i < extracted.length; i++) {
            const char = extracted[i];
            if (koreanParticles.includes(char) || char === ' ') {
                start = i + 1;
            } else if (i > 5) {
                break;
            }
        }
        
        // 뒤쪽 정리
        let end = extracted.length;
        for (let i = extracted.length - 1; i >= 0; i--) {
            const char = extracted[i];
            if (koreanParticles.includes(char) || char === ' ') {
                end = i;
            } else if (extracted.length - i > 5) {
                break;
            }
        }
        
        return extracted.substring(start, end).trim();
    }
    
    // 위치 기반 한국어 추출
    extractKoreanByPosition(englishPhrase, fullEnglish, fullKorean, allEnglishWords, phraseStartIndex) {
        if (!fullKorean || !fullEnglish) return '';
        
        // 영어 구문의 위치 비율 계산
        const phraseWords = englishPhrase.split(/\s+/);
        const phraseStartRatio = phraseStartIndex / allEnglishWords.length;
        const phraseEndRatio = (phraseStartIndex + phraseWords.length) / allEnglishWords.length;
        
        // 한국어 번역에서 해당 비율의 부분 추출
        const koreanStartIndex = Math.floor(fullKorean.length * phraseStartRatio);
        const koreanEndIndex = Math.ceil(fullKorean.length * phraseEndRatio);
        
        // 최소 길이 보장
        const minLength = Math.max(3, Math.floor(fullKorean.length * 0.1));
        const actualStart = Math.max(0, koreanStartIndex - 2);
        const actualEnd = Math.min(fullKorean.length, Math.max(koreanEndIndex + 2, actualStart + minLength));
        
        let extracted = fullKorean.substring(actualStart, actualEnd).trim();
        
        // 문장 경계에서 자르기 (자연스러운 구분)
        // 앞쪽에서 공백이나 조사 찾기
        const startMatch = extracted.match(/^[^\s은는이가을를에의와과로]*/);
        if (startMatch && startMatch[0].length > 0 && actualStart > 0) {
            extracted = extracted.substring(startMatch[0].length).trim();
        }
        
        // 뒤쪽에서 공백이나 조사 찾기
        const endMatch = extracted.match(/[^\s은는이가을를에의와과로]*$/);
        if (endMatch && endMatch[0].length > 0 && actualEnd < fullKorean.length) {
            extracted = extracted.substring(0, extracted.length - endMatch[0].length).trim();
        }
        
        return extracted || fullKorean.substring(actualStart, actualEnd).trim();
    }
    
    // 단락별 해석 렌더링
    renderPhraseTranslation(phrases) {
        if (!phrases || phrases.length === 0) return '';
        
        return `
            <div class="phrase-translation-container">
                <div class="phrase-translation-header">
                    <i class="fas fa-list-ol"></i> 단락별 해석
                </div>
                <div class="phrase-translation-list">
                    ${phrases.map((p, idx) => `
                        <div class="phrase-item">
                            <div class="phrase-header">
                                <span class="phrase-number">${p.order}</span>
                                <span class="phrase-role">${p.role}</span>
                            </div>
                            <div class="phrase-text">${p.phrase}</div>
                            <div class="phrase-translation">→ ${p.translation || '번역 없음'}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    // 문장 학습 렌더링 (패턴별 표시)
    renderSentenceLearning() {
        if (!this.sentenceLearningList || this.sentenceLearningList.length === 0) {
            return;
        }
        
        // 패턴 뷰와 구문 뷰 전환
        if (this.sentenceLearningView === 'phrase') {
            this.renderPhraseLearning();
            return;
        }
        
        // 패턴 뷰
        const currentPattern = this.sentenceLearningList[this.sentenceLearningIndex];
        const progress = ((this.sentenceLearningIndex + 1) / this.sentenceLearningList.length * 100).toFixed(1);
        
        // 예시 문장들 렌더링
        const examplesHtml = currentPattern.examples.map((example, idx) => {
            const interactiveSentence = this.makeInteractiveText(example.sentence_en, example.sentence_ko);
            const phrases = this.parseSentenceIntoPhrases(example.sentence_en, example.sentence_ko);
            const phraseTranslationHtml = this.renderPhraseTranslation(phrases);
            
            const sentenceEscaped = example.sentence_en.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            return `
                <div class="pattern-example-item">
                    <div class="pattern-example-source">${example.source}</div>
                    <div class="pattern-example-sentence">
                        ${interactiveSentence}
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
                        <button class="btn btn-sm btn-info" onclick="cisspModule.speakSentence('${sentenceEscaped}')" title="음성으로 읽기">
                            <i class="fas fa-volume-up"></i> 읽어주기
                        </button>
                        <button class="btn btn-sm btn-secondary" onclick="cisspModule.togglePatternPhraseTranslation(${idx})">
                            <i class="fas fa-list-ol"></i> 단락별 해석 보기
                        </button>
                        <button class="btn btn-sm btn-secondary" onclick="cisspModule.togglePatternExampleTranslation(${idx})">
                            <i class="fas fa-language"></i> 전체 번역 보기
                        </button>
                    </div>
                    <div class="pattern-phrase-translation" id="pattern-phrase-translation-${idx}" style="display: none; margin-top: 15px;">
                        ${phraseTranslationHtml}
                    </div>
                    <div class="pattern-example-translation" id="pattern-translation-${idx}" style="display: none; margin-top: 15px;">
                        <div class="translation-label">한국어 번역:</div>
                        <div class="translation-text">${example.sentence_ko || '번역 없음'}</div>
                    </div>
                </div>
            `;
        }).join('');
        
        const container = document.getElementById('questionContainer');
        container.innerHTML = `
            <div class="sentence-learning-container">
                <div class="sentence-learning-header">
                    <button class="btn btn-back" onclick="cisspModule.renderDashboard()">
                        <i class="fas fa-arrow-left"></i> 대시보드로
                    </button>
                    <div class="sentence-learning-header-content">
                        <h2><i class="fas fa-quote-left"></i> 자주 나오는 문장 학습</h2>
                        <div class="sentence-view-toggle">
                            <button class="btn btn-sm ${this.sentenceLearningView === 'pattern' ? 'btn-primary' : 'btn-secondary'}" 
                                    onclick="cisspModule.switchSentenceView('pattern')">
                                <i class="fas fa-layer-group"></i> 패턴별
                            </button>
                            <button class="btn btn-sm ${this.sentenceLearningView === 'phrase' ? 'btn-primary' : 'btn-secondary'}" 
                                    onclick="cisspModule.switchSentenceView('phrase')">
                                <i class="fas fa-book"></i> 숙어/구문
                            </button>
                        </div>
                    </div>
                    <div class="sentence-learning-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <div class="progress-text">${this.sentenceLearningIndex + 1} / ${this.sentenceLearningList.length} (${progress}%)</div>
                    </div>
                </div>
                
                <div class="pattern-learning-card">
                    <div class="pattern-header">
                        <div class="pattern-name">
                            <span class="pattern-badge">${currentPattern.category === 'question_pattern' ? '질문 패턴' : '시나리오 패턴'}</span>
                            <h3>${currentPattern.pattern}</h3>
                        </div>
                        <div class="pattern-info">
                            <div class="pattern-frequency">
                                <i class="fas fa-chart-line"></i> 빈도: ${currentPattern.frequency}회
                            </div>
                            <div class="pattern-description">${currentPattern.description}</div>
                            ${currentPattern.detailedDescription ? `
                                <div class="pattern-detailed-description">
                                    <strong>상세 설명:</strong> ${currentPattern.detailedDescription}
                                </div>
                            ` : ''}
                            ${currentPattern.usageExamples && currentPattern.usageExamples.length > 0 ? `
                                <div class="pattern-usage-examples">
                                    <strong>사용 예시:</strong>
                                    <ul>
                                        ${currentPattern.usageExamples.map(ex => {
                                            if (typeof ex === 'string') {
                                                return `<li>${ex}</li>`;
                                            } else if (ex.en && ex.ko) {
                                                // 객체 형태인 경우
                                                const phraseHtml = ex.phrases ? `
                                                    <div class="example-phrases" style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
                                                        <strong>구문별 해석:</strong>
                                                        ${ex.phrases.map(p => `
                                                            <div style="margin: 5px 0;">
                                                                <span style="font-weight: bold; color: #007bff;">[${p.order}] ${p.role}:</span>
                                                                <span style="margin-left: 5px;">${p.phrase}</span>
                                                                <span style="margin-left: 10px; color: #28a745;">→ ${p.translation}</span>
                                                            </div>
                                                        `).join('')}
                                                    </div>
                                                ` : '';
                                                return `
                                                    <li>
                                                        <div style="margin-bottom: 5px;">
                                                            <strong>영어:</strong> ${ex.en}
                                                        </div>
                                                        <div style="margin-bottom: 5px; color: #28a745;">
                                                            <strong>한국어:</strong> ${ex.ko}
                                                        </div>
                                                        ${phraseHtml}
                                                    </li>
                                                `;
                                            }
                                            return `<li>${JSON.stringify(ex)}</li>`;
                                        }).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            ${currentPattern.grammarNote ? `
                                <div class="pattern-grammar-note">
                                    <strong>문법 노트:</strong> ${currentPattern.grammarNote}
                                </div>
                            ` : ''}
                            ${currentPattern.examFrequency ? `
                                <div class="pattern-exam-frequency">
                                    <strong>시험 출현 빈도:</strong> ${currentPattern.examFrequency}
                                </div>
                            ` : ''}
                        </div>
                    </div>
                    
                    <div class="pattern-examples-section">
                        <h4><i class="fas fa-list"></i> 예시 문장 (${currentPattern.examples.length}개)</h4>
                        <div class="pattern-examples-list">
                            ${examplesHtml}
                        </div>
                    </div>
                    
                    <div class="sentence-learning-controls">
                        <button class="btn btn-secondary" onclick="cisspModule.prevSentence()" ${this.sentenceLearningIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전 패턴
                        </button>
                        <button class="btn btn-primary" onclick="cisspModule.nextSentence()" ${this.sentenceLearningIndex === this.sentenceLearningList.length - 1 ? 'disabled' : ''}>
                            다음 패턴 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    // 숙어/구문 학습 렌더링
    renderPhraseLearning() {
        if (!this.sentencePhrases || this.sentencePhrases.length === 0) {
            return;
        }
        
        const currentPhrase = this.sentencePhrases[this.sentenceLearningIndex];
        const progress = ((this.sentenceLearningIndex + 1) / this.sentencePhrases.length * 100).toFixed(1);
        
        // 예시 문장들 렌더링
        const examplesHtml = currentPhrase.examples.map((example, idx) => {
            const interactiveSentence = this.makeInteractiveText(example.sentence_en, example.sentence_ko);
            const phrases = this.parseSentenceIntoPhrases(example.sentence_en, example.sentence_ko);
            const phraseTranslationHtml = this.renderPhraseTranslation(phrases);
            
            const sentenceEscaped = example.sentence_en.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            return `
                <div class="phrase-example-item">
                    <div class="phrase-example-source">${example.source}</div>
                    <div class="phrase-example-sentence">
                        ${interactiveSentence}
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
                        <button class="btn btn-sm btn-info" onclick="cisspModule.speakSentence('${sentenceEscaped}')" title="음성으로 읽기">
                            <i class="fas fa-volume-up"></i> 읽어주기
                        </button>
                        <button class="btn btn-sm btn-secondary" onclick="cisspModule.togglePhrasePhraseTranslation(${idx})">
                            <i class="fas fa-list-ol"></i> 단락별 해석 보기
                        </button>
                        <button class="btn btn-sm btn-secondary" onclick="cisspModule.togglePhraseExampleTranslation(${idx})">
                            <i class="fas fa-language"></i> 전체 번역 보기
                        </button>
                    </div>
                    <div class="phrase-phrase-translation" id="phrase-phrase-translation-${idx}" style="display: none; margin-top: 15px;">
                        ${phraseTranslationHtml}
                    </div>
                    <div class="phrase-example-translation" id="phrase-translation-${idx}" style="display: none; margin-top: 15px;">
                        <div class="translation-label">한국어 번역:</div>
                        <div class="translation-text">${example.sentence_ko || '번역 없음'}</div>
                    </div>
                </div>
            `;
        }).join('');
        
        const container = document.getElementById('questionContainer');
        container.innerHTML = `
            <div class="sentence-learning-container">
                <div class="sentence-learning-header">
                    <button class="btn btn-back" onclick="cisspModule.renderDashboard()">
                        <i class="fas fa-arrow-left"></i> 대시보드로
                    </button>
                    <div class="sentence-learning-header-content">
                        <h2><i class="fas fa-book"></i> 자주 나오는 숙어/구문 학습</h2>
                        <div class="sentence-view-toggle">
                            <button class="btn btn-sm ${this.sentenceLearningView === 'pattern' ? 'btn-secondary' : 'btn-primary'}" 
                                    onclick="cisspModule.switchSentenceView('pattern')">
                                <i class="fas fa-layer-group"></i> 패턴별
                            </button>
                            <button class="btn btn-sm ${this.sentenceLearningView === 'phrase' ? 'btn-primary' : 'btn-secondary'}" 
                                    onclick="cisspModule.switchSentenceView('phrase')">
                                <i class="fas fa-book"></i> 숙어/구문
                            </button>
                        </div>
                    </div>
                    <div class="sentence-learning-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <div class="progress-text">${this.sentenceLearningIndex + 1} / ${this.sentencePhrases.length} (${progress}%)</div>
                    </div>
                </div>
                
                <div class="phrase-learning-card">
                    <div class="phrase-header">
                        <div class="phrase-name">
                            <span class="phrase-badge">숙어/구문</span>
                            <h3>${currentPhrase.phrase}</h3>
                        </div>
                        <div class="phrase-info">
                            <div class="phrase-frequency">
                                <i class="fas fa-chart-line"></i> 빈도: ${currentPhrase.frequency}회
                            </div>
                            ${currentPhrase.meaning ? `
                                <div class="phrase-meaning">
                                    <strong>의미:</strong> ${currentPhrase.meaning}
                                </div>
                            ` : ''}
                            ${currentPhrase.detailedMeaning ? `
                                <div class="phrase-detailed-meaning">
                                    <strong>상세 의미:</strong> ${currentPhrase.detailedMeaning}
                                </div>
                            ` : ''}
                            ${currentPhrase.context ? `
                                <div class="phrase-context">
                                    <strong>사용 맥락:</strong> ${currentPhrase.context}
                                </div>
                            ` : ''}
                            ${currentPhrase.grammar ? `
                                <div class="phrase-grammar">
                                    <strong>문법 구조:</strong> ${currentPhrase.grammar}
                                </div>
                            ` : ''}
                            ${currentPhrase.similarPhrases && currentPhrase.similarPhrases.length > 0 ? `
                                <div class="phrase-similar">
                                    <strong>유사 표현:</strong> ${currentPhrase.similarPhrases.join(', ')}
                                </div>
                            ` : ''}
                        </div>
                    </div>
                    
                    <div class="phrase-examples-section">
                        <h4><i class="fas fa-list"></i> 예시 문장 (${currentPhrase.examples.length}개)</h4>
                        <div class="phrase-examples-list">
                            ${examplesHtml}
                        </div>
                    </div>
                    
                    <div class="sentence-learning-controls">
                        <button class="btn btn-secondary" onclick="cisspModule.prevSentence()" ${this.sentenceLearningIndex === 0 ? 'disabled' : ''}>
                            <i class="fas fa-chevron-left"></i> 이전 구문
                        </button>
                        <button class="btn btn-primary" onclick="cisspModule.nextSentence()" ${this.sentenceLearningIndex === this.sentencePhrases.length - 1 ? 'disabled' : ''}>
                            다음 구문 <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    // 문장 학습 뷰 전환 (패턴/구문)
    switchSentenceView(view) {
        this.sentenceLearningView = view;
        this.sentenceLearningIndex = 0; // 뷰 전환 시 인덱스 초기화
        
        if (view === 'pattern') {
            this.renderSentenceLearning();
        } else {
            this.renderPhraseLearning();
        }
    }
    
    // 패턴 예시 번역 토글
    togglePatternExampleTranslation(index) {
        const translationDisplay = document.getElementById(`pattern-translation-${index}`);
        if (translationDisplay) {
            translationDisplay.style.display = translationDisplay.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    // 패턴 예시 단락별 해석 토글
    togglePatternPhraseTranslation(index) {
        const phraseTranslationDisplay = document.getElementById(`pattern-phrase-translation-${index}`);
        if (phraseTranslationDisplay) {
            phraseTranslationDisplay.style.display = phraseTranslationDisplay.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    // 구문 예시 번역 토글
    togglePhraseExampleTranslation(index) {
        const translationDisplay = document.getElementById(`phrase-translation-${index}`);
        if (translationDisplay) {
            translationDisplay.style.display = translationDisplay.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    // 구문 예시 단락별 해석 토글
    togglePhrasePhraseTranslation(index) {
        const phraseTranslationDisplay = document.getElementById(`phrase-phrase-translation-${index}`);
        if (phraseTranslationDisplay) {
            phraseTranslationDisplay.style.display = phraseTranslationDisplay.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    
    // 이전 문장/패턴
    prevSentence() {
        if (this.sentenceLearningView === 'phrase') {
            if (this.sentenceLearningIndex > 0) {
                this.sentenceLearningIndex--;
                this.renderPhraseLearning();
            }
        } else {
            if (this.sentenceLearningIndex > 0) {
                this.sentenceLearningIndex--;
                this.renderSentenceLearning();
            }
        }
    }
    
    // 다음 문장/패턴
    nextSentence() {
        if (this.sentenceLearningView === 'phrase') {
            if (this.sentenceLearningIndex < this.sentencePhrases.length - 1) {
                this.sentenceLearningIndex++;
                this.renderPhraseLearning();
            }
        } else {
            if (this.sentenceLearningIndex < this.sentenceLearningList.length - 1) {
                this.sentenceLearningIndex++;
                this.renderSentenceLearning();
            }
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

// CISSP 모듈 초기화 시 데이터 미리 로드 (백그라운드)
if (typeof window !== 'undefined') {
    // 페이지 로드 후 데이터 미리 로드
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            cisspModule.loadItems().catch(err => {
                console.error('CISSP 데이터 사전 로드 실패:', err);
            });
        });
    } else {
        // 이미 로드된 경우 즉시 로드
        cisspModule.loadItems().catch(err => {
            console.error('CISSP 데이터 사전 로드 실패:', err);
        });
    }
}


