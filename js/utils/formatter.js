// 텍스트 포맷팅 함수들

// HTML 이스케이프
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 마크다운을 HTML로 변환
function convertMarkdownToHtml(text) {
    if (!text) return '';
    
    // **굵은글씨** → <strong>굵은글씨</strong>
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // [섹션 제목] → <div class="section-title">섹션 제목</div>
    text = text.replace(/\[([^\]]+)\]/g, '<div class="section-title">$1</div>');
    
    return text;
}

// 코드 블록 감지 및 박스로 변환
function formatCodeBlocks(text) {
    if (!text) return '';
    
    // 먼저 마크다운을 HTML로 변환
    text = convertMarkdownToHtml(text);
    
    // <pre> 태그가 이미 있으면 그대로 반환 (들여쓰기 보존)
    if (text.includes('<pre')) {
        return text;
    }
    
    // HTML 태그가 포함되어 있으면 일반 텍스트로 처리
    if (text.includes('<img') || text.includes('<table') || text.includes('<div')) {
        const lines = text.split('\n');
        let result = '';
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            // HTML 태그가 있으면 그대로 유지
            if (line.includes('<img') || line.includes('<table') || line.includes('</table>') || line.includes('<div') || line.includes('</div>') || line.includes('<strong>') || line.includes('</strong>')) {
                result += line + '\n';
            } else {
                // 원형 숫자가 문장 시작에 있을 때만 줄바꿈 추가
                let escapedLine = escapeHtml(line);
                // 원형 숫자가 줄 맨 앞에 있는 경우에만 줄바꿈
                if (/^([❶❷❸❹❺❻❼❽❾➊➋➌➍➎➏➐➑➒➓])/.test(line.trim())) {
                    escapedLine = escapedLine.replace(/^([❶❷❸❹❺❻❼❽❾➊➋➌➍➎➏➐➑➒➓])/, '<br>$1');
                }
                result += escapedLine + '\n';
            }
        }
        return result;
    }
    
    // 코드 블록 패턴: 빈 줄 이후에 나타나는 코드 블록을 감지
    const lines = text.split('\n');
    let result = '';
    let inCodeBlock = false;
    let codeBuffer = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const prevLine = i > 0 ? lines[i - 1] : '';
        
        // 빈 줄 이후에 나오는 것을 코드로 간주
        const isEmpty = line.trim() === '';
        const prevIsEmpty = prevLine.trim() === '';
        
        // 코드 블록 시작 감지: 빈 줄 이후 + 코드 키워드 또는 들여쓰기가 있는 경우
        const isCodeLine = /^(\s*)(#include|#|int main|public class|for\s*\(|while\s*\(|if\s*\(|switch\s*\(|import|package|from|import|def |class |String|int |float |void |char |boolean |➊|❶|❷|❸|❹|❺|❻|❼|❽|❾|➊|➋|➌|➍|➎|➏|➐|➑|➒|➓)/.test(line);
        
        // 이전 줄이 빈 줄이면서 현재 줄이 코드로 보이는 경우
        if (prevIsEmpty && isCodeLine) {
            if (codeBuffer.trim() !== '' && inCodeBlock) {
                // 이전 코드 블록 닫기
                result += '<div class="code-box"><pre><code>' + escapeHtml(codeBuffer.trim()) + '</code></pre></div>';
            }
            inCodeBlock = true;
            codeBuffer = line + '\n';
        } else if (inCodeBlock) {
            // 코드 블록 내부
            // 빈 줄이 2개 이상 연속되면 코드 블록 종료
            if (line.trim() === '' && lines[i + 1] && lines[i + 1].trim() === '') {
                result += '<div class="code-box"><pre><code>' + escapeHtml(codeBuffer.trim()) + '</code></pre></div>';
                codeBuffer = '';
                inCodeBlock = false;
            } else if (line.trim() === '') {
                codeBuffer += '\n';
            } else {
                codeBuffer += line + '\n';
            }
        } else {
            // 일반 텍스트 - HTML 태그가 있으면 그대로 유지, 없으면 escape
            if (line.includes('<img') || line.includes('<table') || line.includes('</table>') || line.includes('<div') || line.includes('</div>')) {
                result += line + '\n';
            } else {
                // 원형 숫자 뒤에 자동 줄바꿈 추가
                let escapedLine = escapeHtml(line);
                // 원형 숫자 패턴: ❶❷❸❹❺❻❼❽❾➊➋➌➍➎➏➐➑➒➓
                escapedLine = escapedLine.replace(/([❶❷❸❹❺❻❼❽❾➊➋➌➍➎➏➐➑➒➓])/g, '$1<br>');
                result += escapedLine + '\n';
            }
        }
    }
    
    // 마지막에 코드 블록이 남아있으면 추가
    if (codeBuffer.trim() !== '') {
        result += '<div class="code-box"><pre><code>' + escapeHtml(codeBuffer.trim()) + '</code></pre></div>';
    }
    
    return result;
}

