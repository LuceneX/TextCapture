// content.js
const API_BASE_URL = 'http://localhost:5000';

function getSelectedText() {
    return window.getSelection().toString() || document.body.innerText;
}

async function processText(text) {
    try {
        console.log('Sending request to:', `${API_BASE_URL}/process_text`);
        const response = await fetch(`${API_BASE_URL}/process_text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Send results back to popup
        chrome.runtime.sendMessage({
            type: 'summaryResult',
            data: {
                summaryEn: data.summary_en,
                summaryLv: data.summary_lv
            }
        });
    } catch (error) {
        console.error('Error processing text:', error);
        chrome.runtime.sendMessage({
            type: 'error',
            message: `Failed to process text: ${error.message}`
        });
    }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Received message:', request);
    if (request.action === "captureScreen") {
        const text = getSelectedText();
        processText(text);
    } else if (request.action === "capturePage") {
        const text = document.body.innerText;
        processText(text);
    }
});