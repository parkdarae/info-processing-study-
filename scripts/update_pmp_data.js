// PMP 데이터 업데이트 스크립트
function updatePMPData(extractedQuestions) {
    console.log('PMP 데이터 업데이트 시작...');
    
    if (!extractedQuestions || extractedQuestions.length === 0) {
        console.error('추출된 문제가 없습니다.');
        return false;
    }
    
    // JSONL 형태로 변환
    const jsonlContent = extractedQuestions.map(q => JSON.stringify(q)).join('\n');
    
    // 로컬 스토리지에 임시 저장
    localStorage.setItem('pmp_extracted_data', jsonlContent);
    
    // 브라우저에서 파일 다운로드
    const blob = new Blob([jsonlContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'items_pmp_real.jsonl';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log(`✅ PMP 데이터 업데이트 완료: ${extractedQuestions.length}개 문제`);
    return true;
}

// 추출된 데이터 품질 검증
function validatePMPData(questions) {
    console.log('📊 PMP 데이터 품질 검증 시작...');
    
    const validation = {
        totalQuestions: questions.length,
        validQuestions: 0,
        questionsWithAnswers: 0,
        questionsWithExplanations: 0,
        labelDistribution: {},
        issues: []
    };
    
    questions.forEach((q, index) => {
        let isValid = true;
        
        // 필수 필드 검증
        if (!q.question || q.question.trim() === '') {
            validation.issues.push(`문제 ${q.q_no}: 문제 내용 없음`);
            isValid = false;
        }
        
        if (!q.options || q.options.length !== 4) {
            validation.issues.push(`문제 ${q.q_no}: 선택지 개수 오류 (${q.options?.length || 0}개)`);
            isValid = false;
        }
        
        if (!q.answer || !['A', 'B', 'C', 'D'].includes(q.answer)) {
            validation.issues.push(`문제 ${q.q_no}: 정답 형식 오류 (${q.answer})`);
            isValid = false;
        } else {
            validation.questionsWithAnswers++;
        }
        
        if (q.explanation && q.explanation !== '해설이 없습니다.' && q.explanation.trim() !== '') {
            validation.questionsWithExplanations++;
        }
        
        // 라벨 분포 계산
        if (q.labels && q.labels.length > 0) {
            q.labels.forEach(label => {
                validation.labelDistribution[label] = (validation.labelDistribution[label] || 0) + 1;
            });
        }
        
        if (isValid) {
            validation.validQuestions++;
        }
    });
    
    // 검증 결과 출력
    console.log('📋 검증 결과:');
    console.log(`- 총 문제 수: ${validation.totalQuestions}`);
    console.log(`- 유효한 문제: ${validation.validQuestions}`);
    console.log(`- 정답 있는 문제: ${validation.questionsWithAnswers}`);
    console.log(`- 해설 있는 문제: ${validation.questionsWithExplanations}`);
    console.log('- 라벨 분포:', validation.labelDistribution);
    
    if (validation.issues.length > 0) {
        console.warn('⚠️ 발견된 문제들:');
        validation.issues.forEach(issue => console.warn(issue));
    }
    
    return validation;
}

// 라벨별 통계 생성
function generateLabelStats(questions) {
    const stats = {
        knowledgeAreas: {},
        processGroups: {},
        total: questions.length
    };
    
    questions.forEach(q => {
        if (q.labels) {
            q.labels.forEach(label => {
                if (label.startsWith('project_')) {
                    stats.knowledgeAreas[label] = (stats.knowledgeAreas[label] || 0) + 1;
                } else {
                    stats.processGroups[label] = (stats.processGroups[label] || 0) + 1;
                }
            });
        }
    });
    
    return stats;
}

// 데이터 품질 개선 제안
function suggestDataImprovements(validation) {
    const suggestions = [];
    
    if (validation.validQuestions < validation.totalQuestions * 0.8) {
        suggestions.push('❌ 유효하지 않은 문제가 20% 이상입니다. 파싱 규칙을 개선하세요.');
    }
    
    if (validation.questionsWithExplanations < validation.totalQuestions * 0.5) {
        suggestions.push('⚠️ 해설이 없는 문제가 50% 이상입니다. 해설 추출 규칙을 확인하세요.');
    }
    
    if (Object.keys(validation.labelDistribution).length < 5) {
        suggestions.push('📊 라벨 다양성이 부족합니다. 라벨링 키워드를 확장하세요.');
    }
    
    return suggestions;
}

// 전역 함수로 노출
window.updatePMPData = updatePMPData;
window.validatePMPData = validatePMPData;
window.generateLabelStats = generateLabelStats;
window.suggestDataImprovements = suggestDataImprovements;
