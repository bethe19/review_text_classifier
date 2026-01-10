import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_predict():
    print("Testing single prediction endpoint...")
    test_review = "The food was amazing and the service was excellent!"
    
    response = requests.post(
        f"{API_URL}/predict",
        json={"review": test_review}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_batch_predict():
    print("Testing batch prediction endpoint...")
    test_reviews = [
        "Great restaurant!",
        "Terrible food and service",
        "It was okay"
    ]
    
    response = requests.post(
        f"{API_URL}/predict/batch",
        json=test_reviews
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    try:
        test_health()
        test_predict()
        test_batch_predict()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the API is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

