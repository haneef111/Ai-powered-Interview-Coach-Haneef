"""
Simple test script to verify all backend routes are working
Run this after starting the backend server
"""
import requests
import json

API_URL = 'http://localhost:5000/api'

def test_health():
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f'{API_URL}/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_register():
    print("\n2. Testing Registration...")
    try:
        data = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User',
            'job_role': 'Software Engineer',
            'industry': 'Technology'
        }
        response = requests.post(f'{API_URL}/auth/register', json=data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        
        if response.status_code == 201:
            return result.get('token')
        elif 'already exists' in result.get('error', ''):
            print("   User already exists, trying login...")
            return test_login()
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_login():
    print("\n3. Testing Login...")
    try:
        data = {
            'email': 'test@example.com',
            'password': 'test123'
        }
        response = requests.post(f'{API_URL}/auth/login', json=data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        
        if response.status_code == 200:
            return result.get('token')
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_questions(token):
    print("\n4. Testing Get Questions...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{API_URL}/interview/questions', headers=headers)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Questions count: {len(result.get('questions', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("="*60)
    print("AI Interview Coach - Backend Route Testing")
    print("="*60)
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed! Is the server running?")
        return
    
    # Test registration
    token = test_register()
    if not token:
        print("\n❌ Registration failed!")
        return
    
    print(f"\n✓ Got token: {token[:20]}...")
    
    # Test questions
    if test_questions(token):
        print("\n✓ Questions endpoint working!")
    else:
        print("\n❌ Questions endpoint failed!")
    
    print("\n" + "="*60)
    print("✅ All basic tests completed!")
    print("="*60)
    print("\nYou can now:")
    print("1. Open frontend/index.html in your browser")
    print("2. Register a new account")
    print("3. Start a mock interview")
    print("="*60)

if __name__ == '__main__':
    main()
