"""
API Testing Script for Todo List Application

This script tests all the API endpoints to ensure they're working correctly.
Run this after starting the Flask application to verify functionality.
"""

import requests
import json
from datetime import datetime, date, timedelta

BASE_URL = 'http://localhost:5000/api'

def test_api():
    print("🧪 Testing Todo List API Endpoints\n")
    
    # Test 1: Get initial stats
    print("1. Testing GET /stats")
    response = requests.get(f'{BASE_URL}/stats')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Initial stats: {stats}")
    print()
    
    # Test 2: Create categories
    print("2. Testing POST /categories")
    categories_to_create = [
        {'name': 'Test Work', 'color': '#007bff'},
        {'name': 'Test Personal', 'color': '#28a745'},
        {'name': 'Test Urgent', 'color': '#dc3545'}
    ]
    
    created_categories = []
    for cat_data in categories_to_create:
        response = requests.post(f'{BASE_URL}/categories', json=cat_data)
        print(f"   Creating '{cat_data['name']}': Status {response.status_code}")
        if response.status_code == 201:
            created_categories.append(response.json())
    print()
    
    # Test 3: Get all categories
    print("3. Testing GET /categories")
    response = requests.get(f'{BASE_URL}/categories')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()
        print(f"   Total categories: {len(categories)}")
        for cat in categories:
            print(f"   - {cat['name']} ({cat['task_count']} tasks)")
    print()
    
    # Test 4: Create tasks
    print("4. Testing POST /tasks")
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    reminder_time = (datetime.now() + timedelta(hours=1)).isoformat()
    
    tasks_to_create = [
        {
            'title': 'Test Task 1',
            'description': 'This is a test task with high priority',
            'priority': 'high',
            'category_id': created_categories[0]['id'] if created_categories else None,
            'due_date': tomorrow,
            'reminder_time': reminder_time
        },
        {
            'title': 'Test Task 2',
            'description': 'Medium priority task',
            'priority': 'medium',
            'category_id': created_categories[1]['id'] if created_categories else None
        },
        {
            'title': 'Test Task 3',
            'description': 'Low priority task',
            'priority': 'low',
            'category_id': created_categories[2]['id'] if created_categories else None
        }
    ]
    
    created_tasks = []
    for task_data in tasks_to_create:
        response = requests.post(f'{BASE_URL}/tasks', json=task_data)
        print(f"   Creating '{task_data['title']}': Status {response.status_code}")
        if response.status_code == 201:
            created_tasks.append(response.json())
    print()
    
    # Test 5: Get all tasks
    print("5. Testing GET /tasks")
    response = requests.get(f'{BASE_URL}/tasks')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"   Total tasks: {len(tasks)}")
        for task in tasks:
            print(f"   - {task['title']} [{task['priority']}] {'✓' if task['completed'] else '○'}")
    print()
    
    # Test 6: Update a task
    if created_tasks:
        print("6. Testing PUT /tasks/<id>")
        task_to_update = created_tasks[0]
        update_data = {
            'title': 'Updated Test Task 1',
            'completed': True,
            'description': 'This task has been updated and completed'
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_to_update["id"]}', json=update_data)
        print(f"   Updating task {task_to_update['id']}: Status {response.status_code}")
        if response.status_code == 200:
            updated_task = response.json()
            print(f"   New title: {updated_task['title']}")
            print(f"   Completed: {updated_task['completed']}")
        print()
    
    # Test 7: Toggle task completion
    if len(created_tasks) > 1:
        print("7. Testing PATCH /tasks/<id>/toggle")
        task_to_toggle = created_tasks[1]
        response = requests.patch(f'{BASE_URL}/tasks/{task_to_toggle["id"]}/toggle')
        print(f"   Toggling task {task_to_toggle['id']}: Status {response.status_code}")
        if response.status_code == 200:
            toggled_task = response.json()
            print(f"   Task '{toggled_task['title']}' completed: {toggled_task['completed']}")
        print()
    
    # Test 8: Filter tasks
    print("8. Testing GET /tasks with filters")
    
    # Filter by priority
    response = requests.get(f'{BASE_URL}/tasks', params={'priority': 'high'})
    print(f"   High priority tasks: {len(response.json()) if response.status_code == 200 else 'Error'}")
    
    # Filter by completion status
    response = requests.get(f'{BASE_URL}/tasks', params={'completed': 'true'})
    print(f"   Completed tasks: {len(response.json()) if response.status_code == 200 else 'Error'}")
    
    # Search tasks
    response = requests.get(f'{BASE_URL}/tasks', params={'search': 'test'})
    print(f"   Tasks containing 'test': {len(response.json()) if response.status_code == 200 else 'Error'}")
    
    # Sort by priority
    response = requests.get(f'{BASE_URL}/tasks', params={'sort_by': 'priority'})
    print(f"   Tasks sorted by priority: {len(response.json()) if response.status_code == 200 else 'Error'}")
    print()
    
    # Test 9: Get updated stats
    print("9. Testing GET /stats (after changes)")
    response = requests.get(f'{BASE_URL}/stats')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Final stats: {stats}")
    print()
    
    # Test 10: Clean up (delete test data)
    print("10. Cleaning up test data")
    
    # Delete tasks
    for task in created_tasks:
        response = requests.delete(f'{BASE_URL}/tasks/{task["id"]}')
        print(f"   Deleting task {task['id']}: Status {response.status_code}")
    
    # Delete categories
    for category in created_categories:
        response = requests.delete(f'{BASE_URL}/categories/{category["id"]}')
        print(f"   Deleting category {category['id']}: Status {response.status_code}")
    
    print("\n✅ API testing completed!")

if __name__ == '__main__':
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Make sure the Flask application is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
