// 범위 설정 모드

// 범위 필터 적용
async function applyRangeFilter() {
    const config = App.moduleConfig[App.state.currentModule];
    const start = parseInt(document.getElementById('rangeStart').value) || 1;
    const end = parseInt(document.getElementById('rangeEnd').value) || config.maxRange;
    const order = document.querySelector('input[name="rangeOrder"]:checked').value;
    
    // 유효성 검사
    const validStart = Math.max(1, Math.min(start, config.maxRange));
    const validEnd = Math.max(validStart, Math.min(end, config.maxRange));
    
    // 모달 닫기
    closeRangeModal();
    
    // 문제 로드
    try {
        // items.jsonl 로드
        const response = await fetch(config.itemsFile);
        const text = await response.text();
        App.state.allQuestions = text.trim().split('\n').map(line => JSON.parse(line));
        allQuestions = App.state.allQuestions; // 하위 호환성
        
        // tables.jsonl 로드
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
        
        // 범위 필터링 (Q 또는 C 접두사 처리)
        App.state.currentQuestions = App.state.allQuestions.filter(q => {
            const num = parseInt(q.q_no.replace(/^[QC]/, '').replace(/^0+/, '') || '0');
            return num >= validStart && num <= validEnd;
        });
        
        // 순서 적용
        if (order === 'random') {
            App.state.currentQuestions = shuffleArray(App.state.currentQuestions);
        }
        currentQuestions = App.state.currentQuestions; // 하위 호환성
        
        if (App.state.currentQuestions.length === 0) {
            showMessage('해당 범위에 문제가 없습니다.');
            return;
        }
        
        App.state.currentIndex = 0;
        currentIndex = 0; // 하위 호환성
        App.state.currentMode = 'range';
        currentMode = 'range'; // 하위 호환성
        displayQuestion(App.state.currentQuestions[App.state.currentIndex]);
        
        showMessage(`${validStart}~${validEnd}번 문제 ${App.state.currentQuestions.length}개 로드 완료!`);
    } catch (error) {
        console.error('문제 로드 실패:', error);
        showMessage('문제를 불러올 수 없습니다.');
    }
}

