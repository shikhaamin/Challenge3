"""
Comprehensive test suite for the Hack(H)er413 API.
Tests all endpoints: users, availabilities, and tasks.
"""

import time
from fastapi.testclient import TestClient
from MainAPI import app

client = TestClient(app)


def test_full_workflow():
    """Test creating users, availabilities, and tasks."""
    print("\n" + "="*60)
    print("COMPREHENSIVE API TEST")
    print("="*60)
    
    # Generate unique email using timestamp to avoid conflicts
    unique_email = f"user.{int(time.time())}@example.com"
    unique_name = f"Test User {int(time.time())}"
    
    # Test 1: Create a new user
    print("\n[1] POST /users/ (create new user)")
    new_user_payload = {
        "email": unique_email,
        "name": unique_name
    }
    response = client.post("/users/", json=new_user_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    user_data = response.json()
    user_id = user_data["id"]
    print(f"✓ User created with ID: {user_id}")
    
    # Test 2: Get all users
    print("\n[2] GET /users/ (get all users)")
    response = client.get("/users/")
    print(f"Status: {response.status_code}")
    users = response.json()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"  - {u['name']} ({u['email']})")
    assert response.status_code == 200
    assert len(users) > 0
    print("✓ Successfully retrieved all users")
    
    # Test 3: Get specific user by ID
    print(f"\n[3] GET /users/{user_id} (get specific user)")
    response = client.get(f"/users/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print(f"✓ Retrieved user: {response.json()['name']}")
    
    # Test 4: Create availability
    print("\n[4] POST /availabilities/ (create availability)")
    availability_payload = {
        "user_id": user_id,
        "start_time": "2026-02-22 09:00:00",
        "end_time": "2026-02-22 17:00:00",
        "is_available": True
    }
    response = client.post("/availabilities/", json=availability_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    availability_data = response.json()
    availability_id = availability_data["id"]
    print(f"✓ Availability created with ID: {availability_id}")
    
    # Test 5: Get all availabilities
    print("\n[5] GET /availabilities/ (get all availabilities)")
    response = client.get("/availabilities/")
    print(f"Status: {response.status_code}")
    availabilities = response.json()
    print(f"Total availabilities: {len(availabilities)}")
    assert response.status_code == 200
    print("✓ Successfully retrieved all availabilities")
    
    # Test 6: Create a task
    print("\n[6] POST /tasks/ (create task)")
    task_payload = {
        "user_id": user_id,
        "title": "Implement API",
        "description": "Build FastAPI backend for Hack(H)er413",
        "completed": False
    }
    response = client.post("/tasks/", json=task_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["id"]
    print(f"✓ Task created with ID: {task_id}")
    
    # Test 7: Get all tasks
    print("\n[7] GET /tasks/ (get all tasks)")
    response = client.get("/tasks/")
    print(f"Status: {response.status_code}")
    tasks = response.json()
    print(f"Total tasks: {len(tasks)}")
    for t in tasks:
        status = "✓ Done" if t.get("completed") else "⚠ Pending"
        print(f"  - {t['title']} ({status})")
    assert response.status_code == 200
    print("✓ Successfully retrieved all tasks")
    
    # Test 8: Verify user has relationships
    print(f"\n[8] GET /users/{user_id} (verify relationships)")
    response = client.get(f"/users/{user_id}")
    user_full = response.json()
    print(f"User: {user_full['name']}")
    print(f"  Availabilities: {len(user_full.get('availabilities', []))}")
    print(f"  Tasks: {len(user_full.get('tasks', []))}")
    assert len(user_full.get("availabilities", [])) > 0, "No availabilities found"
    assert len(user_full.get("tasks", [])) > 0, "No tasks found"
    print("✓ User relationships properly linked")
    
    # Test 9: Duplicate email (should fail)
    print("\n[9] POST /users/ (duplicate email - should fail)")
    dup_payload = {
        "email": unique_email,
        "name": "Duplicate User"
    }
    response = client.post("/users/", json=dup_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 400, "Expected 400 for duplicate email"
    print("✓ Correctly rejected duplicate email")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_full_workflow()
