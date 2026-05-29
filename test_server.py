import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_process_text():
    """Test processing text input."""
    text = """
    From: sender@example.com
    Subject: Test Email
    Date: 2024-01-01
    
    This is a test email content.
    """
    
    response = requests.post(
        f"{BASE_URL}/process",
        json={"text": text}
    )
    print(f"Text processing status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")

def test_process_json():
    """Test processing JSON input."""
    json_data = {
        "name": "Test User",
        "age": 30,
        "email": "test@example.com"
    }
    
    response = requests.post(
        f"{BASE_URL}/process",
        json={"json_data": json.dumps(json_data)}
    )
    print(f"JSON processing status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")

def main():
    print("Testing server endpoints...\n")
    
    # Test health check
    test_health()
    
    # Test text processing
    test_process_text()
    
    # Test JSON processing
    test_process_json()

if __name__ == "__main__":
    main() 