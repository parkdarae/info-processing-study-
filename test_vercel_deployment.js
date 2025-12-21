const { chromium } = require('playwright');

// 사용법: node test_vercel_deployment.js [도메인]
// 예: node test_vercel_deployment.js https://info-processing-study-daryong2.agency

const domain = process.argv[2] || 'https://info-processing-study-daryong2.agency';

(async () => {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    console.log(`\n=== Vercel 배포 테스트: ${domain} ===\n`);
    
    try {
        // 1. config.js 확인
        console.log('1. config.js 확인 중...');
        const configResponse = await page.goto(`${domain}/js/config.js`, {
            waitUntil: 'networkidle',
            timeout: 10000
        });
        
        if (configResponse && configResponse.ok()) {
            const configContent = await configResponse.text();
            const hasCissp = configContent.includes("'cissp'") || configContent.includes('"cissp"');
            const hasCisspTitle = configContent.includes('CISSP 문제집');
            const configVersion = configContent.match(/App\.configVersion\s*=\s*['"]([^'"]+)['"]/);
            
            console.log('   ✅ config.js 로드 성공');
            console.log('   - CISSP 모듈:', hasCissp ? '✅ 있음' : '❌ 없음');
            console.log('   - CISSP 제목:', hasCisspTitle ? '✅ 있음' : '❌ 없음');
            console.log('   - Config 버전:', configVersion ? configVersion[1] : '❌ 없음');
            
            if (!hasCissp || !hasCisspTitle) {
                console.log('\n   ⚠️ config.js에 CISSP 모듈이 없습니다!');
                console.log('   Fallback 로직이 작동해야 합니다.\n');
            }
        } else {
            console.log('   ❌ config.js 로드 실패');
        }
        
        // 2. 메인 페이지 로드
        console.log('\n2. 메인 페이지 로드 중...');
        await page.goto(domain, {
            waitUntil: 'networkidle',
            timeout: 30000
        });
        console.log('   ✅ 메인 페이지 로드 완료');
        
        // 3. 환영 팝업 닫기
        const welcomePopup = page.locator('#welcomePopup');
        if (await welcomePopup.isVisible()) {
            await page.evaluate(() => {
                localStorage.setItem('welcomeShown', 'true');
                const popup = document.getElementById('welcomePopup');
                if (popup) popup.classList.remove('show');
            });
            await page.waitForTimeout(500);
            console.log('   ✅ 환영 팝업 닫기 완료');
        }
        
        // 4. App 객체 확인
        console.log('\n3. App 객체 확인 중...');
        await page.waitForTimeout(2000); // 스크립트 로드 대기
        
        const appState = await page.evaluate(() => {
            return {
                hasApp: typeof window.App !== 'undefined',
                hasConfig: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined',
                modules: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    ? Object.keys(window.App.moduleConfig) : [],
                hasCissp: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    && !!window.App.moduleConfig.cissp,
                configVersion: typeof window.App !== 'undefined' && window.App.configVersion 
                    ? window.App.configVersion : 'unknown',
                switchModuleExists: typeof window.switchModule === 'function'
            };
        });
        
        console.log('   - App 객체:', appState.hasApp ? '✅ 있음' : '❌ 없음');
        console.log('   - App.moduleConfig:', appState.hasConfig ? '✅ 있음' : '❌ 없음');
        console.log('   - 모듈 개수:', appState.modules.length);
        console.log('   - CISSP 모듈:', appState.hasCissp ? '✅ 있음' : '❌ 없음');
        console.log('   - Config 버전:', appState.configVersion);
        console.log('   - switchModule 함수:', appState.switchModuleExists ? '✅ 있음' : '❌ 없음');
        
        // 5. CISSP 모듈 전환 테스트
        console.log('\n4. CISSP 모듈 전환 테스트 중...');
        const switchResult = await page.evaluate(() => {
            let error = null;
            let success = false;
            
            try {
                if (typeof switchModule === 'function') {
                    switchModule('cissp');
                    success = true;
                } else {
                    error = 'switchModule 함수가 없습니다';
                }
            } catch (e) {
                error = e.message;
            }
            
            // 전환 후 상태 확인
            const afterState = {
                hasCissp: typeof App !== 'undefined' && App.moduleConfig && !!App.moduleConfig.cissp,
                modules: typeof App !== 'undefined' && App.moduleConfig ? Object.keys(App.moduleConfig) : [],
                currentModule: typeof App !== 'undefined' && App.state ? App.state.currentModule : null
            };
            
            // 오류 메시지 확인
            const errorVisible = document.body.textContent.includes('알 수 없는 모듈');
            
            return { success, error, afterState, errorVisible };
        });
        
        console.log('   - switchModule 호출:', switchResult.success ? '✅ 성공' : '❌ 실패');
        if (switchResult.error) {
            console.log('   - 오류:', switchResult.error);
        }
        console.log('   - 전환 후 CISSP 모듈:', switchResult.afterState.hasCissp ? '✅ 있음' : '❌ 없음');
        console.log('   - 현재 모듈:', switchResult.afterState.currentModule);
        console.log('   - 오류 메시지 표시:', switchResult.errorVisible ? '❌ 표시됨' : '✅ 없음');
        
        // 6. 최종 결과
        console.log('\n=== 최종 결과 ===');
        const allPassed = appState.hasCissp || switchResult.afterState.hasCissp;
        
        if (allPassed && !switchResult.errorVisible) {
            console.log('✅ 모든 테스트 통과! CISSP 모듈이 정상적으로 작동합니다.');
        } else if (switchResult.afterState.hasCissp && !switchResult.errorVisible) {
            console.log('✅ Fallback 로직 작동! CISSP 모듈이 추가되었습니다.');
        } else {
            console.log('❌ 테스트 실패! CISSP 모듈이 작동하지 않습니다.');
            console.log('\n문제 해결 방법:');
            console.log('1. Vercel 대시보드에서 빌드 캐시 클리어');
            console.log('2. 프로젝트 재배포');
            console.log('3. 브라우저 캐시 클리어 (Ctrl+Shift+R)');
        }
        
        await page.waitForTimeout(2000);
    } catch (error) {
        console.error('\n❌ 테스트 중 오류 발생:', error);
    } finally {
        await browser.close();
    }
})();

