const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    try {
        console.log('Fetching config.js from Vercel...');
        const response = await page.goto('https://info-processing-study-daryong2.agency/js/config.js', {
            waitUntil: 'networkidle',
            timeout: 10000
        });
        
        if (response && response.ok()) {
            const content = await response.text();
            
            // CISSP 모듈 확인
            const hasCissp = content.includes("'cissp'") || content.includes('"cissp"');
            const hasCisspTitle = content.includes('CISSP 문제집');
            const configVersion = content.match(/App\.configVersion\s*=\s*['"]([^'"]+)['"]/);
            
            console.log('\n=== Vercel config.js 검증 결과 ===');
            console.log('CISSP 모듈 존재:', hasCissp ? '✅ 있음' : '❌ 없음');
            console.log('CISSP 제목 존재:', hasCisspTitle ? '✅ 있음' : '❌ 없음');
            console.log('Config 버전:', configVersion ? configVersion[1] : '❌ 없음');
            
            if (hasCissp && hasCisspTitle) {
                console.log('\n✅ Vercel 배포 버전에 CISSP 모듈이 포함되어 있습니다!');
                
                // CISSP 모듈 상세 확인
                const cisspMatch = content.match(/'cissp':\s*\{[^}]+\}/s);
                if (cisspMatch) {
                    console.log('\n=== CISSP 모듈 설정 ===');
                    console.log(cisspMatch[0].substring(0, 300));
                }
            } else {
                console.log('\n❌ Vercel 배포 버전에 CISSP 모듈이 없습니다!');
                console.log('\n=== config.js 내용 (처음 1000자) ===');
                console.log(content.substring(0, 1000));
            }
        } else {
            console.log('❌ config.js를 가져올 수 없습니다.');
        }
        
        await page.waitForTimeout(2000);
    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
})();

