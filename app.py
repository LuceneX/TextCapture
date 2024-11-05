from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
import pyautogui
from PIL import Image
from translate import Translator
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
import heapq
import re
import os
import signal
import atexit
import spacy
from nltk import word_tokenize
from nltk.probability import FreqDist
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

app = Flask(__name__)
CORS(app)

class TextProcessor:
    def __init__(self):
        # Initialize stopwords and scoring parameters
        self.stopwords = set(stopwords.words('english')).union(STOP_WORDS)
        self.position_weight = 1.5  # Boost for sentences appearing earlier
        self.translator = Translator(to_lang="lv")  # Set Latvian as target language for translation

    def preprocess_text(self, text):
        """Preprocess and clean the text."""
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = re.sub(r'http\S+|www.\S+', '', text)  # Remove URLs
        return text

    def get_sentence_importance(self, sentence, word_freq):
        """Calculate importance based on frequency and position."""
        words = word_tokenize(sentence.lower())
        importance = sum(word_freq[word] for word in words if word.isalnum() and word not in self.stopwords)
        return importance

    def extract_keywords(self, text):
        """Extract key entities from the text using spaCy's NER."""
        doc = nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE"]]

    def summarize_text(self, text, num_sentences=3):
        """Summarize text with improved scoring."""
        text = self.preprocess_text(text)
        sentences = sent_tokenize(text)
        
        # Early exit if too few sentences
        if len(sentences) <= num_sentences:
            return text

        # Calculate word frequencies
        words = word_tokenize(text.lower())
        word_freq = FreqDist(word for word in words if word.isalnum() and word not in self.stopwords)

        # Score sentences, favoring position
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = self.get_sentence_importance(sentence, word_freq)
            score += (self.position_weight if i < num_sentences else 1)
            sentence_scores[sentence] = score

        # Sort and select sentences, ensuring order preservation
        summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(sorted(summary_sentences, key=sentences.index))

        return summary if summary else text[:200] + "..."

    def translate_to_latvian(self, text):
        """Translate English text to Latvian."""
        try:
            return self.translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")  # DEBUGGING
            return "Translation failed"  # Fallback in case of an error


# Create singleton instance
processor = TextProcessor()

def cleanup():
    """Cleanup function to handle server shutdown"""
    print("Shutting down server...")  # DEBUGGING

# Register cleanup handler
atexit.register(cleanup)

@app.route('/')
def home():
    """Root endpoint to verify server is running"""
    return jsonify({
        'status': 'Server is running',
        'available_endpoints': [
            '/process_text (POST)',
            '/capture (POST)'
        ]
    })

@app.route('/process_text', methods=['POST', 'OPTIONS'])
def process_text():
    """Process text endpoint"""
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
            
        text = data['text']
        print(f"Processing text: {text[:100]}...")  # DEBUGGING
        
        summary_en = processor.summarize_text(text)
        if not summary_en:
            return jsonify({'error': 'Could not generate summary'}), 400
            
        summary_lv = processor.translate_to_latvian(summary_en)
        
        return jsonify({
            'summary_en': summary_en,
            'summary_lv': summary_lv,
            'original_length': len(text),
            'summary_length': len(summary_en)
        })
        
    except Exception as e:
        print(f"Error processing text: {e}")  # DEBUGGING
        return jsonify({'error': str(e)}), 500

@app.route('/capture', methods=['POST', 'OPTIONS'])
def capture():
    """Screen capture endpoint"""
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    try:
        data = request.get_json()
        x1 = data.get('x1', 0)
        y1 = data.get('y1', 0)
        x2 = data.get('x2')
        y2 = data.get('y2')
        
        # Capture screen
        screenshot = pyautogui.screenshot(
            region=(x1, y1, x2-x1, y2-y1) if all([x1, y1, x2, y2]) else None
        )
        screenshot.save("test_screenshot.png")  # DEBUGGING
        
        # Extract text using OCR
        text = pytesseract.image_to_string(screenshot)
        text = text.strip()
        
        if not text:
            return jsonify({'error': 'No text detected in image'}), 400
        
        summary_en = processor.summarize_text(text)
        summary_lv = processor.translate_to_latvian(summary_en)
        
        return jsonify({
            'original_text': text,
            'summary_en': summary_en,
            'summary_lv': summary_lv
        })
        
    except Exception as e:
        print(f"Error capturing screen: {e}")  # DEBUGGING
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Write PID file for external management
    with open('server.pid', 'w') as f:
        f.write(str(os.getpid()))  # DEBUGGING
    
    try:
        app.run(host='localhost', port=5000, debug=True)
    finally:
        # Cleanup PID file
        if os.path.exists('server.pid'):
            os.remove('server.pid')  # DEBUGGING
