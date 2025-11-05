// 랜덤 풀기 모드

window.RandomMode = {
    filter: function(allQuestions) {
        return shuffleArray([...allQuestions]);
    }
};

