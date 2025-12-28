const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    const allLogs = [];
    
    // 로그 수집을 위한 콘솔 리스너
    page.on('console', msg => {
        const text = msg.text();
        const type = msg.type();
        allLogs.push({ type, text, timestamp: Date.now() });
        console.log(`[${type}] ${text}`);
    });
    
    // 네트워크 요청 모니터링
    page.on('response', response => {
        const url = response.url();
        if (url.includes('config.js') || url.includes('menu.js') || url.includes('index.html')) {
            console.log(`[NETWORK] ${url.split('/').pop()} loaded: ${url}, Status: ${response.status()}`);
        }
    });
    
    try {
        console.log('Navigating to https://info-processing-study-daryong2.agency/');
        await page.goto('https://info-processing-study-daryong2.agency/', { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        console.log('Page loaded, waiting for scripts...');
        await page.waitForTimeout(5000); // 스크립트 로드 대기
        
        // 환영 팝업 닫기
        try {
            await page.evaluate(() => {
                const welcomePopup = document.getElementById('welcomePopup');
                if (welcomePopup && welcomePopup.classList.contains('show')) {
                    welcomePopup.classList.remove('show');
                }
                const closeBtn = document.querySelector('.welcome-popup .close, .welcome-popup button');
                if (closeBtn) closeBtn.click();
            });
            await page.waitForTimeout(500);
        } catch (e) {
            console.log('Welcome popup handling:', e.message);
        }
        
        // 초기 상태 확인
        const initialState = await page.evaluate(() => {
            return {
                hasApp: typeof window.App !== 'undefined',
                hasConfig: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined',
                modules: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    ? Object.keys(window.App.moduleConfig) : [],
                hasCissp: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    && !!window.App.moduleConfig.cissp,
                configVersion: typeof window.App !== 'undefined' ? window.App.configVersion : 'unknown',
                switchModuleExists: typeof switchModule === 'function',
                indexHtmlVersion: document.querySelector('script[src*="config.js"]')?.src || 'not found'
            };
        });
        console.log('\n=== Initial State ===');
        console.log(JSON.stringify(initialState, null, 2));
        
        // switchModule 함수의 실제 코드 확인
        const switchModuleCode = await page.evaluate(() => {
            if (typeof switchModule === 'function') {
                return switchModule.toString().substring(0, 500); // 처음 500자만
            }
            return 'switchModule not found';
        });
        console.log('\n=== switchModule function code (first 500 chars) ===');
        console.log(switchModuleCode);
        
        // switchModule 직접 호출 및 상세 로깅
        console.log('\n=== Calling switchModule("cissp") ===');
        const switchModuleResult = await page.evaluate(() => {
            const logs = [];
            const originalLog = console.log;
            const originalError = console.error;
            const originalWarn = console.warn;
            
            // 콘솔 오버라이드
            console.log = (...args) => {
                logs.push({ type: 'log', args: args.map(a => String(a)) });
                originalLog.apply(console, args);
            };
            console.error = (...args) => {
                logs.push({ type: 'error', args: args.map(a => String(a)) });
                originalError.apply(console, args);
            };
            console.warn = (...args) => {
                logs.push({ type: 'warn', args: args.map(a => String(a)) });
                originalWarn.apply(console, args);
            };
            
            const result = {
                before: {
                    hasCissp: typeof window.App !== 'undefined' && 
                             typeof window.App.moduleConfig !== 'undefined' && 
                             !!window.App.moduleConfig.cissp,
                    modules: typeof window.App !== 'undefined' && 
                            typeof window.App.moduleConfig !== 'undefined' 
                            ? Object.keys(window.App.moduleConfig) : [],
                    configVersion: typeof window.App !== 'undefined' ? window.App.configVersion : 'unknown'
                },
                switchModuleExists: typeof switchModule === 'function',
                error: null,
                success: false
            };
            
            try {
                if (typeof switchModule === 'function') {
                    // switchModule 호출 전 App.moduleConfig 직접 확인
                    result.beforeDirectCheck = {
                        cisspExists: !!window.App?.moduleConfig?.cissp,
                        cisspValue: window.App?.moduleConfig?.cissp || null,
                        allKeys: Object.keys(window.App?.moduleConfig || {})
                    };
                    
                    switchModule('cissp');
                    result.success = true;
                    
                    // switchModule 호출 후 즉시 확인
                    result.afterImmediate = {
                        cisspExists: !!window.App?.moduleConfig?.cissp,
                        cisspValue: window.App?.moduleConfig?.cissp || null,
                        allKeys: Object.keys(window.App?.moduleConfig || {})
                    };
                } else {
                    result.error = 'switchModule function not found';
                }
            } catch (error) {
                result.error = error.message;
                result.errorStack = error.stack;
            }
            
            // 최종 상태
            result.after = {
                hasCissp: typeof window.App !== 'undefined' && 
                         typeof window.App.moduleConfig !== 'undefined' && 
                         !!window.App.moduleConfig.cissp,
                modules: typeof window.App !== 'undefined' && 
                        typeof window.App.moduleConfig !== 'undefined' 
                        ? Object.keys(window.App.moduleConfig) : []
            };
            
            result.logs = logs;
            
            // 원래 함수 복원
            console.log = originalLog;
            console.error = originalError;
            console.warn = originalWarn;
            
            return result;
        });
        
        console.log('\n=== switchModule Result ===');
        console.log(JSON.stringify(switchModuleResult, null, 2));
        
        if (switchModuleResult.logs && switchModuleResult.logs.length > 0) {
            console.log('\n=== Console logs during switchModule ===');
            switchModuleResult.logs.forEach(log => {
                console.log(`[${log.type}]`, ...log.args);
            });
        }
        
        await page.waitForTimeout(2000);
        
        // 오류 다이얼로그 확인
        const pageText = await page.textContent('body');
        const hasError = pageText && (pageText.includes('알 수 없는 모듈') || pageText.includes('Unknown module'));
        console.log('\n=== Error Check ===');
        console.log('Error text found in page:', hasError);
        if (hasError) {
            const errorMatch = pageText.match(/알 수 없는 모듈[^]*?/);
            if (errorMatch) {
                console.log('Error context:', errorMatch[0].substring(0, 200));
            }
        }
        
        // 최종 상태 확인
        const finalState = await page.evaluate(() => {
            return {
                hasApp: typeof window.App !== 'undefined',
                hasConfig: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined',
                modules: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    ? Object.keys(window.App.moduleConfig) : [],
                hasCissp: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    && !!window.App.moduleConfig.cissp,
                configVersion: typeof window.App !== 'undefined' ? window.App.configVersion : 'unknown',
                errorVisible: document.body.innerText.includes('알 수 없는 모듈'),
                cisspModuleValue: typeof window.App !== 'undefined' && typeof window.App.moduleConfig !== 'undefined' 
                    ? window.App.moduleConfig.cissp : null
            };
        });
        console.log('\n=== Final State ===');
        console.log(JSON.stringify(finalState, null, 2));
        
        // 관련 로그 필터링
        console.log('\n=== Relevant Logs ===');
        const relevantLogs = allLogs.filter(log => 
            log.text.includes('CISSP') || 
            log.text.includes('모듈') || 
            log.text.includes('switchModule') || 
            log.text.includes('config.js') ||
            log.text.includes('알 수 없는')
        );
        relevantLogs.forEach(log => {
            console.log(`[${log.type}] ${log.text}`);
        });
        
        await page.waitForTimeout(3000);
        
    } catch (error) {
        console.error('Error during debugging:', error);
        console.error('Stack:', error.stack);
    } finally {
        await browser.close();
    }
})();
