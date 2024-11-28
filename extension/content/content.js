console.log("Content script loaded.");

// Example: Highlight selected text
document.addEventListener("mouseup", () => {
  const selectedText = window.getSelection().toString();
  if (selectedText.trim()) {
    console.log("Selected text:", selectedText);
  }
});
