# test_api.py
import requests

def test_process_text():
    url = "http://localhost:5000/process_text"
    
    # Test data
    payload = {
        "text": "This is a sample text that I want to summarize. It can be multiple sentences long. The summarization should pick the most important sentences."
    }
    
    # Make the request
    response = requests.post(url, json=payload)
    
    # Print results
    print("Status Code:", response.status_code)
    print("Response:")
    print(response.json())

def test_capture():
    url = "http://localhost:5000/capture"
    
    # Test data for a specific screen region
    payload = {
        "x1": 0,
        "y1": 0,
        "x2": 500,
        "y2": 500
    }
    
    # Make the request
    response = requests.post(url, json=payload)
    
    # Print results
    print("Status Code:", response.status_code)
    print("Response:")
    print(response.json())

if __name__ == "__main__":
    print("Testing text processing endpoint...")
    test_process_text()
    
    print("\nTesting screen capture endpoint...")
    test_capture()