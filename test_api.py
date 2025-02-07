import httpx
import asyncio
import json
from datetime import datetime
from typing import Dict, Any

BASE_URL = "http://192.168.0.63:8080"

async def test_endpoint(client: httpx.AsyncClient, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict:
    print(f"Testing {method} {endpoint}...")
    try:
        if method == "GET":
            response = await client.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = await client.post(f"{BASE_URL}{endpoint}", json=data)
        elif method == "PUT":
            response = await client.put(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Response status: {response.status_code}")
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else str(response.content),
            "success": 200 <= response.status_code < 300
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": None,
            "response": str(e),
            "success": False
        }

async def run_tests():
    async with httpx.AsyncClient() as client:
        tests = [
            # System Health
            ("GET", "/health"),
            ("GET", "/metrics"),
            
            # Tasks - Basic Operations
            ("GET", "/tasks"),
            ("GET", "/tasks/RED"),
            ("GET", "/tasks/ORANGE"),
            ("GET", "/tasks/YELLOW"),
            ("GET", "/tasks/GREEN"),
            ("GET", "/tasks/all"),
            ("GET", "/tasks/completed"),
            ("GET", "/tasks/pending"),
            
            # Task Roll Call
            ("GET", "/tasks/roll_call/daily"),
            ("GET", "/tasks/roll_call/urgent"),
            ("GET", "/tasks/roll_call/high"),
            ("GET", "/tasks/roll_call/normal"),
            ("GET", "/tasks/roll_call/low"),
            ("GET", "/tasks/roll_call/patterns"),
            ("GET", "/tasks/roll_call/summary"),
            
            # Voice Management
            ("GET", "/voice/patterns"),
            ("GET", "/voice/patterns/emotions"),
            ("GET", "/voice/patterns/prosody"),
            ("GET", "/voice/patterns/active"),
            ("GET", "/voice/settings"),
            
            # Russ Management
            ("GET", "/russ/status"),
            ("GET", "/russ/patterns"),
            ("GET", "/russ/triggers"),
            ("GET", "/russ/stories"),
            ("GET", "/russ/schedule"),
            ("GET", "/russ/medications"),
            ("GET", "/russ/activities"),
            
            # Universe/Family
            ("GET", "/universe/family"),
            ("GET", "/universe/characters"),
            ("GET", "/universe/locations"),
            ("GET", "/universe/rules"),
            ("GET", "/universe/schedule"),
            ("GET", "/universe/relationships"),
            ("GET", "/universe/network"),
            
            # Data Management
            ("GET", "/data/sources"),
            ("GET", "/data/types"),
            ("GET", "/data/status"),
            ("GET", "/data/summary"),
            
            # POST Endpoints
            ("POST", "/tasks/create", {
                "title": "Test Task",
                "priority": "normal",
                "due_date": datetime.now().isoformat()
            }),
            ("POST", "/tasks/ai_enrich", {
                "task_id": "123",
                "context": "test context"
            }),
            ("POST", "/tasks/ai_rollcall", {
                "date": datetime.now().isoformat()
            }),
            ("POST", "/voice/analyze", {
                "text": "Test voice analysis",
                "context": "normal"
            }),
            ("POST", "/russ/event", {
                "type": "medication",
                "timestamp": datetime.now().isoformat(),
                "details": "test event"
            }),
            
            # PUT Endpoints
            ("PUT", "/tasks/123/status", {
                "status": "completed",
                "completion_time": datetime.now().isoformat()
            }),
            ("PUT", "/tasks/123/priority", {
                "priority": "high"
            }),
            ("PUT", "/voice/settings", {
                "volume": "medium",
                "speed": "normal"
            }),
            ("PUT", "/russ/status", {
                "status": "active",
                "mood": "good"
            })
        ]
        
        results = []
        for test in tests:
            method, endpoint, *data = test
            data = data[0] if data else None
            result = await test_endpoint(client, method, endpoint, data)
            results.append(result)
        return results

def generate_report(results: list) -> str:
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    report = [
        "API Endpoint Test Report",
        "=====================",
        f"Total Tests: {total_count}",
        f"Successful: {success_count}",
        f"Failed: {total_count - success_count}",
        f"Success Rate: {(success_count/total_count)*100:.1f}%",
        "\nDetailed Results:",
        "----------------"
    ]
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        report.append(f"\n{status} {result['method']} {result['endpoint']}")
        report.append(f"   Status: {result['status_code']}")
        if not result["success"]:
            report.append(f"   Error: {result['response']}")
    
    return "\n".join(report)

if __name__ == "__main__":
    print("Starting API endpoint tests...")
    results = asyncio.run(run_tests())
    
    # Generate and save report
    report = generate_report(results)
    print("\n" + report)
    
    # Save detailed results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"api_test_results_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to api_test_results_{timestamp}.json")
