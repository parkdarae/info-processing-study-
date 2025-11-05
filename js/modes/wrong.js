// 오답만 풀기 모드

window.WrongMode = {
    filter: function(allQuestions) {
        const wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
        return allQuestions.filter(q => wrongQuestions.includes(q.q_no));
    }
};

