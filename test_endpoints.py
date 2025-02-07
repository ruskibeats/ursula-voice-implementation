import requests
import json
from datetime import datetime, timedelta

# Fix the BASE_URL to use the correct middleware IP
BASE_URL = "http://192.168.0.63:8080"

def test_endpoint(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"Testing {method} {endpoint}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")
        
        status = "✅" if response.status_code in [200, 201] else "❌"
        return f"{status} {method} {endpoint} - Status: {response.status_code}"
    except Exception as e:
        return f"❌ {method} {endpoint} - Error: {str(e)}"

# List of endpoints to test
endpoints_to_test = [
    ("GET", "/tasks"),                # Get all tasks
    ("GET", "/tasks/priority"),       # Get task priorities (if implemented)
    ("GET", "/tasks/recurring"),      # Get recurring tasks (if implemented)
    ("GET", "/tasks/{id}"),           # Get a specific task by ID (if implemented)
    ("POST", "/tasks"),                # Create a new task
    ("PUT", "/tasks/{id}"),           # Update a specific task by ID (if implemented)
    ("DELETE", "/tasks/{id}"),        # Delete a specific task by ID (if implemented)
    # Add more endpoints as needed
]

# Simple POST test for creating a task
post_endpoints_to_test = [
    ("/tasks", {
        "title": "Test Task",
        "description": "Testing task creation",
        "status": "PENDING",
        "priority": "MEDIUM"
    })
]

def run_tests():
    print("🔥 Starting Ursula's Universe API Tests 🔥")
    print("\n🚀 Testing GET Endpoints:")
    for method, endpoint in endpoints_to_test:
        print(test_endpoint(method, endpoint))
        
    print("\n🚀 Testing POST Endpoints:")
    for endpoint, data in post_endpoints_to_test:
        print(test_endpoint("POST", endpoint, data))

if __name__ == "__main__":
    run_tests()
