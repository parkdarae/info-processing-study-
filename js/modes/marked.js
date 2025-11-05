// 체크한 문제 모드

window.MarkedMode = {
    filter: function(allQuestions) {
        const markedQuestions = JSON.parse(localStorage.getItem('markedQuestions') || '[]');
        return allQuestions.filter(q => markedQuestions.includes(q.q_no));
    }
};

