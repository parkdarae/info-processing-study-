const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    try {
        console.log('Fetching menu.js from deployed site...');
        const response = await page.goto('https://info-processing-study-daryong2.agency/js/components/menu.js?v=20251105004', {
            waitUntil: 'networkidle',
            timeout: 10000
        });
        
        if (response && response.ok()) {
            const content = await response.text();
            console.log('\n=== Deployed menu.js content (first 2000 chars) ===');
            console.log(content.substring(0, 2000));
            
            // switchModule 함수 확인
            const switchModuleMatch = content.match(/function switchModule\([^)]*\)\s*\{[^}]*\}/s);
            if (switchModuleMatch) {
                console.log('\n=== switchModule function in deployed menu.js ===');
                console.log(switchModuleMatch[0].substring(0, 1000));
            }
            
            // CISSP 관련 코드 확인
            const cisspMatches = content.match(/cissp/gi);
            console.log('\n=== CISSP mentions in deployed menu.js ===');
            console.log(`Found ${cisspMatches ? cisspMatches.length : 0} mentions of "cissp"`);
            
            // CISSP 모듈 추가 코드 확인
            const hasCisspAdd = content.includes('CISSP 모듈을 강제로 추가') || 
                               content.includes('App.moduleConfig[\'cissp\']') ||
                               content.includes('App.moduleConfig["cissp"]');
            console.log(`Has CISSP module add logic: ${hasCisspAdd}`);
        } else {
            console.log('Failed to fetch menu.js');
        }
        
        await page.waitForTimeout(2000);
    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
})();

