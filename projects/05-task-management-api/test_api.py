# Test script for Task Management API
# Run this after starting the API server

import requests
import json

# Base URL for the API
BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

def main():
    print("Testing Task Management API")
    print("Make sure the API server is running on http://localhost:5000")
    
    # 1. Health Check
    print("\n1. Health Check")
    response = requests.get(f'{BASE_URL}/health')
    print_response("Health Check", response)
    
    # 2. Get All Tasks (should be empty initially)
    print("\n2. Get All Tasks (Initial)")
    response = requests.get(f'{BASE_URL}/tasks')
    print_response("Get All Tasks", response)
    
    # 3. Create First Task
    print("\n3. Create First Task")
    task1_data = {
        'title': 'Learn Flask',
        'description': 'Complete Flask tutorial and build projects',
        'completed': False
    }
    response = requests.post(f'{BASE_URL}/tasks', json=task1_data)
    print_response("Create Task 1", response)
    task1_id = response.json()['id']
    
    # 4. Create Second Task
    print("\n4. Create Second Task")
    task2_data = {
        'title': 'Build REST API',
        'description': 'Create a RESTful API with Flask',
        'completed': False
    }
    response = requests.post(f'{BASE_URL}/tasks', json=task2_data)
    print_response("Create Task 2", response)
    task2_id = response.json()['id']
    
    # 5. Get All Tasks (should have 2 tasks now)
    print("\n5. Get All Tasks (After Creating)")
    response = requests.get(f'{BASE_URL}/tasks')
    print_response("Get All Tasks", response)
    
    # 6. Get Single Task
    print("\n6. Get Single Task")
    response = requests.get(f'{BASE_URL}/tasks/{task1_id}')
    print_response(f"Get Task {task1_id}", response)
    
    # 7. Update Task (Mark as completed)
    print("\n7. Update Task (Mark as Completed)")
    update_data = {
        'completed': True
    }
    response = requests.put(f'{BASE_URL}/tasks/{task1_id}', json=update_data)
    print_response(f"Update Task {task1_id}", response)
    
    # 8. Update Task (Change title and description)
    print("\n8. Update Task (Change Title and Description)")
    update_data = {
        'title': 'Learn Flask - COMPLETED',
        'description': 'Finished Flask tutorial and built projects!'
    }
    response = requests.put(f'{BASE_URL}/tasks/{task1_id}', json=update_data)
    print_response(f"Update Task {task1_id}", response)
    
    # 9. Get All Tasks (to see updated task)
    print("\n9. Get All Tasks (After Updates)")
    response = requests.get(f'{BASE_URL}/tasks')
    print_response("Get All Tasks", response)
    
    # 10. Delete Task
    print("\n10. Delete Task")
    response = requests.delete(f'{BASE_URL}/tasks/{task2_id}')
    print_response(f"Delete Task {task2_id}", response)
    
    # 11. Get All Tasks (should have 1 task now)
    print("\n11. Get All Tasks (After Deletion)")
    response = requests.get(f'{BASE_URL}/tasks')
    print_response("Get All Tasks", response)
    
    # 12. Test Error Handling - Get non-existent task
    print("\n12. Test Error Handling (Get Non-existent Task)")
    response = requests.get(f'{BASE_URL}/tasks/999')
    print_response("Get Non-existent Task", response)
    
    print("\n" + "="*50)
    print("API Testing Complete!")
    print("="*50)

if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API server!")
        print("Make sure the API is running on http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"\nError: {e}")

