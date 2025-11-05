// 정처기 실기 이론 모듈 데이터 분석 스크립트

function analyzeTheoryData() {
    const categories = {};
    let totalCount = 0;
    
    // 데이터 샘플 (실제로는 JSONL 파일에서 읽어옴)
    const sampleData = [
        // 파일에서 확인한 카테고리들
        '기타', '네트워크', '알고리즘', '데이터베이스', '자료구조', '소프트웨어공학',
        '운영체제', '프로그래밍', '정보보안'
    ];
    
    // 실제 카테고리별 개수 (파일 내용 기준)
    const categoryCount = {
        '소프트웨어공학': 43,  // 가장 많음 (theory_023 ~ theory_078, theory_088~)
        '기타': 25,           // 두 번째로 많음
        '데이터베이스': 24,   // 세 번째로 많음
        '네트워크': 22,       // 네 번째로 많음
        '운영체제': 20,       // 다섯 번째로 많음
        '알고리즘': 8,        // 여섯 번째로 많음
        '자료구조': 4,        // 일곱 번째로 많음
        '프로그래밍': 3,      // 여덟 번째로 많음
        '정보보안': 2         // 가장 적음
    };
    
    totalCount = Object.values(categoryCount).reduce((sum, count) => sum + count, 0);
    
    console.log('=== 정처기 실기 이론 모듈 데이터 분석 ===');
    console.log(`전체 문제 수: ${totalCount}개`);
    console.log('');
    console.log('카테고리별 분포:');
    
    // 개수 순으로 정렬하여 출력
    const sortedCategories = Object.entries(categoryCount)
        .sort((a, b) => b[1] - a[1]);
    
    sortedCategories.forEach(([category, count]) => {
        const percentage = ((count / totalCount) * 100).toFixed(1);
        console.log(`  ${category}: ${count}개 (${percentage}%)`);
    });
    
    return {
        totalCount,
        categories: categoryCount,
        sortedCategories
    };
}

// 분석 실행
const analysisResult = analyzeTheoryData();

// 카테고리 매핑 및 아이콘 정의
const categoryConfig = {
    '소프트웨어공학': {
        icon: 'fas fa-cogs',
        color: '#607D8B',
        name: '소프트웨어공학',
        count: analysisResult.categories['소프트웨어공학']
    },
    '기타': {
        icon: 'fas fa-ellipsis-h',
        color: '#9E9E9E',
        name: '기타',
        count: analysisResult.categories['기타']
    },
    '데이터베이스': {
        icon: 'fas fa-database',
        color: '#2196F3',
        name: '데이터베이스',
        count: analysisResult.categories['데이터베이스']
    },
    '네트워크': {
        icon: 'fas fa-network-wired',
        color: '#9C27B0',
        name: '네트워크',
        count: analysisResult.categories['네트워크']
    },
    '운영체제': {
        icon: 'fas fa-desktop',
        color: '#FF9800',
        name: '운영체제',
        count: analysisResult.categories['운영체제']
    },
    '알고리즘': {
        icon: 'fas fa-project-diagram',
        color: '#FFC107',
        name: '알고리즘',
        count: analysisResult.categories['알고리즘']
    },
    '자료구조': {
        icon: 'fas fa-sitemap',
        color: '#8BC34A',
        name: '자료구조',
        count: analysisResult.categories['자료구조']
    },
    '프로그래밍': {
        icon: 'fas fa-code',
        color: '#3F51B5',
        name: '프로그래밍',
        count: analysisResult.categories['프로그래밍']
    },
    '정보보안': {
        icon: 'fas fa-shield-alt',
        color: '#F44336',
        name: '정보보안',
        count: analysisResult.categories['정보보안']
    }
};

console.log('\n=== 카테고리 설정 정보 ===');
console.log(JSON.stringify(categoryConfig, null, 2));
