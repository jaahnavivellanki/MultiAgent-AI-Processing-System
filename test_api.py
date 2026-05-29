import requests
import json
import os

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print("\nTesting Health Check:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_process_text():
    data = {
        "text": "This is a test email from test@example.com"
    }
    response = requests.post(f"{BASE_URL}/process", json=data)
    print("\nTesting Process with Text:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_process_json():
    data = {
        "json_data": json.dumps({
            "invoice_id": "INV-2024-001",
            "amount": 1500.00
        })
    }
    response = requests.post(f"{BASE_URL}/process", json=data)
    print("\nTesting Process with JSON:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_email_input():
    """Test the API with an email input"""
    email_content = """From: customer@example.com
Subject: URGENT: Invoice Dispute
Date: 2024-03-20

Dear Team,

I am writing to dispute invoice #12345. The amount charged is incorrect and I need immediate resolution.

Best regards,
John Smith"""

    response = requests.post(
        f"{BASE_URL}/process/",
        data={"input_text": email_content}
    )
    print("\n=== Email Test Results ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_json_input():
    """Test the API with a JSON input"""
    json_content = """{
        "invoice_id": "INV-2024-001",
        "amount": 15000.00,
        "items": [
            {"name": "Product A", "quantity": 10, "price": 1500.00}
        ]
    }"""

    response = requests.post(
        f"{BASE_URL}/process/",
        data={"input_text": json_content}
    )
    print("\n=== JSON Test Results ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_pdf_input():
    """Test the API with a PDF file"""
    pdf_path = "sample_invoice_policy.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"\nError: {pdf_path} not found!")
        return

    with open(pdf_path, "rb") as pdf_file:
        files = {"file": ("sample.pdf", pdf_file, "application/pdf")}
        response = requests.post(
            f"{BASE_URL}/process/",
            files=files
        )
    
    print("\n=== PDF Test Results ===")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def main():
    """Run all tests"""
    print("Starting API tests...")
    
    try:
        test_health()
        test_process_text()
        test_process_json()
        test_email_input()
        test_json_input()
        test_pdf_input()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the Django server is running.")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")

if __name__ == "__main__":
    main()
