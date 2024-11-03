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

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

class TextProcessor:
    def __init__(self):
        self.translator_lv = Translator(to_lang="lv")
        self.stopwords = set(stopwords.words('english') + list(punctuation))
        
    def summarize_text(self, text, num_sentences=3):
        """
        Generate summary using extractive summarization
        """
        if not text:
            return ""
            
        # Tokenize the text into sentences and words
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
            
        # Calculate word frequencies
        words = word_tokenize(text.lower())
        word_freq = FreqDist(word for word in words if word not in self.stopwords)
        
        # Calculate sentence scores
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_freq[word]
                    else:
                        sentence_scores[sentence] += word_freq[word]
        
        # Get top sentences
        summary_sentences = heapq.nlargest(num_sentences, 
                                         sentence_scores, 
                                         key=sentence_scores.get)
        
        # Sort sentences by their original order
        summary_sentences = sorted(summary_sentences, 
                                 key=lambda x: sentences.index(x))
        
        return ' '.join(summary_sentences)
    
    def translate_to_latvian(self, text):
        """Translate text to Latvian"""
        try:
            return self.translator_lv.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return "Translation error occurred"

# Create a single instance of TextProcessor
processor = TextProcessor()

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
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
            
        text = data['text']
        print(f"Received text: {text[:100]}...")  # Print first 100 chars for debugging
        
        # Generate summary
        summary_en = processor.summarize_text(text)
        print(f"Generated English summary: {summary_en}")
        
        # Translate to Latvian
        summary_lv = processor.translate_to_latvian(summary_en)
        print(f"Generated Latvian summary: {summary_lv}")
        
        return jsonify({
            'summary_en': summary_en,
            'summary_lv': summary_lv
        })
        
    except Exception as e:
        print(f"Error processing text: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/capture', methods=['POST', 'OPTIONS'])
def capture():
    """Screen capture endpoint"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    try:
        data = request.get_json()
        x1 = data.get('x1')
        y1 = data.get('y1')
        x2 = data.get('x2')
        y2 = data.get('y2')
        
        # Capture screen
        screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1) if all([x1, y1, x2, y2]) else None)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(screenshot)
        text = text.strip()
        
        # Generate summary
        summary_en = processor.summarize_text(text)
        
        # Translate to Latvian
        summary_lv = processor.translate_to_latvian(summary_en)
        
        return jsonify({
            'original_text': text,
            'summary_en': summary_en,
            'summary_lv': summary_lv
        })
        
    except Exception as e:
        print(f"Error capturing screen: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Server starting on http://localhost:5000")
    print("Available endpoints:")
    print("- POST http://localhost:5000/process_text")
    print("- POST http://localhost:5000/capture")
    app.run(host='0.0.0.0', port=5000, debug=True)