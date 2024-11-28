from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline
from bs4 import BeautifulSoup
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Load the Hugging Face Transformer pipeline for text summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Utility function to clean HTML content
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

@app.route('/')
def index():
    """
    Serve the frontend HTML file.
    """
    return send_from_directory('.', 'index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        raw_text = data.get("text", "")
        if not raw_text:
            return jsonify({"error": "No text provided"}), 400
        
        clean_text = clean_html(raw_text)
        summary = summarizer(clean_text, max_length=130, min_length=30, do_sample=False)
        return jsonify({"summary": summary[0]["summary_text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
