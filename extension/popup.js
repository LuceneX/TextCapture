// Utility functions
const setLoading = (isLoading) => {
  const loader = document.getElementById('loader');
  const buttons = document.querySelectorAll('button');
  loader.style.display = isLoading ? 'block' : 'none';
  buttons.forEach(button => button.disabled = isLoading);
};

const showError = (message) => {
  const errorElement = document.getElementById('errorMessage');
  errorElement.textContent = message;
  errorElement.style.display = 'block';
  setTimeout(() => {
      errorElement.style.display = 'none';
  }, 5000);
};

const updateSummaries = (summaryEn, summaryLv) => {
  document.getElementById('summaryEn').textContent = summaryEn || 'No summary available';
  document.getElementById('summaryLv').textContent = summaryLv || 'Nav pieejams kopsavilkums';
};

// Event listeners
document.getElementById('captureScreen').addEventListener('click', async () => {
  setLoading(true);
  try {
      const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
      await chrome.tabs.sendMessage(tab.id, {action: "captureScreen"});
  } catch (error) {
      showError('Failed to capture selected text. Please try again.');
      setLoading(false);
  }
});

document.getElementById('capturePage').addEventListener('click', async () => {
  setLoading(true);
  try {
      const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
      await chrome.tabs.sendMessage(tab.id, {action: "capturePage"});
  } catch (error) {
      showError('Failed to capture page text. Please try again.');
      setLoading(false);
  }
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  setLoading(false);
  
  if (message.type === 'summaryResult') {
      updateSummaries(message.data.summaryEn, message.data.summaryLv);
  } else if (message.type === 'error') {
      showError(message.message);
  }
});