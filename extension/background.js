chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "summarize") {
      fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: request.text })
      })
        .then(response => response.json())
        .then(data => {
          sendResponse({ summary: data.summary });
        })
        .catch(error => {
          console.error("Error:", error);
          sendResponse({ error: "Failed to fetch summary." });
        });
      return true; // Required for asynchronous response
    }
  });
  