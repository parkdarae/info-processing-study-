// 전역 상태 관리 객체
window.App = window.App || {};

// 전역 변수
App.state = {
    currentModule: 'keyword130',
    allQuestions: [],
    allTables: {},
    currentQuestions: [],
    currentIndex: 0,
    currentMode: null,
    stats: {
        total: 0,
        correct: 0,
        wrong: 0,
        wrongQuestions: []
    },
    answeredQuestions: new Set(),
    symbolInputOrder: {
        symbols: [],
        inputIndex: 0
    },
    // CISSP 이중언어 모드 상태
    languageMode: 'ko', // 'ko' = 한국어, 'en' = 영어 학습모드
    vocabulary: {} // 단어 사전 데이터
};

// 모듈 설정
App.moduleConfig = {
    'keyword130': {
        title: '정보처리기사 실기 핵심 키워드130 문제은행',
        itemsFile: 'items.jsonl',
        tablesFile: 'tables.jsonl',
        maxRange: 130
    },
    'code_control': {
        title: '코드-제어문14문제',
        itemsFile: 'items_code_control.jsonl',
        tablesFile: 'tables_code_control.jsonl',
        maxRange: 14
    },
    'theory_frequent': {
        title: '⭐ 실기 최빈출 50개',
        itemsFile: 'data/items_theory_frequent.jsonl',
        tablesFile: '',
        type: 'flashcard',
        maxRange: 50,
        isTheoryFrequent: true
    },
    'pmp': {
        title: '📋 PMP 문제집',
        itemsFile: 'data/items_pmp.jsonl',
        tablesFile: '',
        type: 'pmp',
        maxRange: 20,
        isPMP: true
    },
    'cissp': {
        title: '🔐 CISSP 문제집 (1850문제)',
        itemsFile: 'data/items_cissp.jsonl',
        tablesFile: '',
        vocabularyFile: 'data/cissp_vocabulary.json',
        type: 'cissp',
        maxRange: 1850,
        isCISSP: true,
        supportsBilingual: true
    },
    'theory': {
        title: '정처기 실기 이론',
        itemsFile: 'data/items_theory.jsonl',
        tablesFile: '',
        type: 'theory',
        maxRange: 175,
        categories: ['정보보안', '데이터베이스', '네트워크', '운영체제', '소프트웨어공학', '프로그래밍', '자료구조', '알고리즘', '기타']
    },
    '2025_round1': {
        title: '정보처리기사 실기 2025년 1회 기출문제',
        itemsFile: 'data/items_2025_round1.jsonl',
        tablesFile: 'data/tables_2025_round1.jsonl',
        maxRange: 19,
        isPastExam: true
    },
    '2025_round2': {
        title: '정보처리기사 실기 2025년 2회 기출문제',
        itemsFile: 'data/items_2025_round2.jsonl',
        tablesFile: 'data/tables_2025_round2.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2024_round3': {
        title: '정보처리기사 실기 2024년 3회 기출문제',
        itemsFile: 'data/items_2024_round3.jsonl',
        tablesFile: 'data/tables_2024_round3.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2024_round2': {
        title: '정보처리기사 실기 2024년 2회 기출문제',
        itemsFile: 'data/items_2024_round2.jsonl',
        tablesFile: 'data/tables_2024_round2.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2024_round1': {
        title: '정보처리기사 실기 2024년 1회 기출문제',
        itemsFile: 'data/items_2024_round1.jsonl',
        tablesFile: 'data/tables_2024_round1.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2023_round3': {
        title: '정보처리기사 실기 2023년 3회 기출문제',
        itemsFile: 'data/items_2023_round3.jsonl',
        tablesFile: 'data/tables_2023_round3.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2023_round2': {
        title: '정보처리기사 실기 2023년 2회 기출문제',
        itemsFile: 'data/items_2023_round2.jsonl',
        tablesFile: 'data/tables_2023_round2.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2023_round1': {
        title: '정보처리기사 실기 2023년 1회 기출문제',
        itemsFile: 'data/items_2023_round1.jsonl',
        tablesFile: 'data/tables_2023_round1.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2022_round3': {
        title: '정보처리기사 실기 2022년 3회 기출문제',
        itemsFile: 'data/items_2022_round3.jsonl',
        tablesFile: 'data/tables_2022_round3.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2022_round2': {
        title: '정보처리기사 실기 2022년 2회 기출문제',
        itemsFile: 'data/items_2022_round2.jsonl',
        tablesFile: 'data/tables_2022_round2.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    '2022_round1': {
        title: '정보처리기사 실기 2022년 1회 기출문제',
        itemsFile: 'data/items_2022_round1.jsonl',
        tablesFile: 'data/tables_2022_round1.jsonl',
        maxRange: 21,
        isPastExam: true
    },
    '2021_round1': {
        title: '정보처리기사 실기 2021년 1회 기출문제',
        itemsFile: 'data/items_2021_round1.jsonl',
        tablesFile: 'data/tables_2021_round1.jsonl',
        maxRange: 20,
        isPastExam: true
    },
    // 문제패턴별 카테고리
    'category_programming': {
        title: '💻 프로그래밍 (108문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '프로그래밍',
        isCategoryMode: true,
        maxRange: 108
    },
    'category_network': {
        title: '🌐 네트워크 (32문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '네트워크',
        isCategoryMode: true,
        maxRange: 32
    },
    'category_database': {
        title: '🗄️ 데이터베이스 (29문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '데이터베이스',
        isCategoryMode: true,
        maxRange: 29
    },
    'category_software': {
        title: '⚙️ 소프트웨어공학 (19문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '소프트웨어공학',
        isCategoryMode: true,
        maxRange: 19
    },
    'category_sql': {
        title: '📊 SQL (15문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: 'SQL',
        isCategoryMode: true,
        maxRange: 15
    },
    'category_security': {
        title: '🔒 정보보안 (14문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '정보보안',
        isCategoryMode: true,
        maxRange: 14
    },
    'category_os': {
        title: '🖥️ 운영체제 (9문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '운영체제',
        isCategoryMode: true,
        maxRange: 9
    },
    'category_datastructure': {
        title: '📚 자료구조 (4문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '자료구조',
        isCategoryMode: true,
        maxRange: 4
    },
    'category_algorithm': {
        title: '🧮 알고리즘 (1문제)',
        itemsFile: 'data/items_all.jsonl',
        tablesFile: '',
        category: '알고리즘',
        isCategoryMode: true,
        maxRange: 1
    }
};

// 동의어 사전
App.synonyms = {
    '애자일': ['agile', 'Agile', 'AGILE'],
    '클래스': ['class', 'Class', 'CLASS'],
    '함수': ['function', 'Function', 'FUNCTION'],
    '변수': ['variable', 'Variable', 'VARIABLE']
};

// 하위 호환성을 위한 전역 변수 별칭
var currentModule = App.state.currentModule;
var allQuestions = App.state.allQuestions;
var allTables = App.state.allTables;
var currentQuestions = App.state.currentQuestions;
var currentIndex = App.state.currentIndex;
var currentMode = App.state.currentMode;
var stats = App.state.stats;
var answeredQuestions = App.state.answeredQuestions;
var symbolInputOrder = App.state.symbolInputOrder;
var moduleConfig = App.moduleConfig;
var synonyms = App.synonyms;

