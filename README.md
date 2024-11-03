# Text Summarization App Documentation

## Overview
The Text Summarization App is a Python-based tool designed to capture and summarize text, supporting both Latvian and English. This app leverages text processing, OCR, and translation capabilities to provide users with concise summaries of their input, either in the original or translated language. It features a Flask API for easy interaction, making it accessible for integration into larger systems.

## Key Features
Multilingual Summarization: Supports text summarization in both Latvian and English.
OCR Capability: Extracts text from images using Tesseract OCR for summarization.
API-Based: Utilizes a Flask API, allowing users to interact with the app programmatically.
Translation Support: Translates text between Latvian and English using the translate library.
##Prerequisites
Ensure the following before installation:

Python: Version 3.8 or higher.
Tesseract OCR: Installed on your system and accessible. Refer to Tesseract installation for setup instructions.
##Installation
Clone the Repository: Start by downloading the source code from the repository.
```bash
Copy code
git clone <repository-url>
cd <repository-directory>
Install Dependencies: Run the following to install the required libraries.
``` 
Copy code:
```bash
pip install -r requirements.txt
```
The requirements.txt file includes the following packages:
pytesseract for OCR
Pillow for image processing
pyautogui for screen capture (if needed)
flask and flask-cors for the API
translate for translation services
nltk for natural language processing
## Setup Instructions
Configure Tesseract Path (if necessary): Ensure that Tesseract is correctly installed and its executable path is added to your system’s environment variables.
Start the Flask Server:
bash
Copy code:
```bash
python app.py
```
By default, the Flask server will start on localhost:5000. You can change the port in the app.py file if needed.
API Usage
The app is built as an API with Flask, and the main endpoints include options to upload text, images, or specify language preferences for summarization.

## Sample API Endpoints

Summarize Text: POST /summarize
Request Body: JSON with text, language, and summarize parameters.
Response: Summarized text in the specified language.
OCR and Summarize: POST /ocr
Request Body: Upload an image file (PNG, JPEG).
Response: Text summary extracted from the image.
For testing purposes, test_api.py provides examples of API calls and can be executed to verify the functionality of each endpoint.

## Example Requests
Summarize Text in English

Copy code:
```
curl -X POST http://localhost:5000/summarize -H "Content-Type: application/json" -d '{"text": "Input text here", "language": "en", "summarize": true}'
OCR and Summarize Image Text
```
Copy code:
```
curl -X POST http://localhost:5000/ocr -F "file=@/path/to/image.png"
```
## Troubleshooting
### Tesseract Not Found:
If OCR fails, ensure Tesseract is installed and accessible in your system’s PATH.
### CORS Issues:
If accessing the API from a browser, check flask-cors settings in app.py to ensure the correct configuration.
### Future Enhancements
#### GUI Option:
- Add a graphical interface for easier use.
#### Expanded Language Support:
- Integrate additional languages for wider usability.
#### Advanced Summarization Models:
- Leverage transformer-based models for improved summarization quality.
