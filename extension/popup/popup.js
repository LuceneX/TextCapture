document.getElementById("summarize-btn").addEventListener("click", () => {
    const textInput = document.getElementById("text-input").value;
  
    if (textInput.trim() === "") {
      alert("Please enter text to summarize.");
      return;
    }
  
    chrome.runtime.sendMessage(
      { action: "summarize", text: textInput },
      (response) => {
        if (response.error) {
          document.getElementById("summary-output").innerText = "Error: " + response.error;
        } else {
          document.getElementById("summary-output").innerText = response.summary;
        }
      }
    );
  });
  