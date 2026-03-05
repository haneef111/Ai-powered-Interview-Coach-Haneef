"""
Complete Flow Test - AI Interview Coach
Tests: Registration → Login → Get Questions
"""
import requests
import json
import time
from datetime import datetime

API_URL = 'http://localhost:5000/api'

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_signup():
    print_section("TEST 1: Sign Up (Create New Account)")
    
    # Generate unique email with timestamp
    timestamp = int(time.time())
    test_user = {
        'name': 'Test User',
        'email': f'testuser{timestamp}@example.com',
        'password': 'test123456',
        'job_role': 'Software Engineer',
        'industry': 'Technology'
    }
    
    print(f"\n📝 Creating account for: {test_user['email']}")
    print(f"   Name: {test_user['name']}")
    print(f"   Job Role: {test_user['job_role']}")
    print(f"   Industry: {test_user['industry']}")
    
    try:
        response = requests.post(f'{API_URL}/auth/register', json=test_user)
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ SIGNUP SUCCESSFUL!")
            print(f"   Token received: {result['token'][:30]}...")
            print(f"   User: {result['user']['name']} ({result['user']['email']})")
            return test_user, result['token']
        else:
            result = response.json()
            print(f"❌ SIGNUP FAILED: {result.get('error', 'Unknown error')}")
            return None, None
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None, None

def test_login(email, password):
    print_section("TEST 2: Login (Existing Account)")
    
    print(f"\n🔐 Logging in as: {email}")
    
    try:
        response = requests.post(f'{API_URL}/auth/login', json={
            'email': email,
            'password': password
        })
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LOGIN SUCCESSFUL!")
            print(f"   Token received: {result['token'][:30]}...")
            print(f"   User: {result['user']['name']} ({result['user']['email']})")
            return result['token']
        else:
            result = response.json()
            print(f"❌ LOGIN FAILED: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def test_get_questions(token):
    print_section("TEST 3: Get Interview Questions")
    
    print("\n📋 Fetching interview questions...")
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{API_URL}/interview/questions', headers=headers)
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            questions = result.get('questions', [])
            print(f"✅ QUESTIONS LOADED SUCCESSFULLY!")
            print(f"   Total questions: {len(questions)}")
            print("\n   Questions:")
            for i, q in enumerate(questions, 1):
                print(f"   {i}. {q}")
            return True
        else:
            result = response.json()
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_health():
    print_section("TEST 0: Backend Health Check")
    
    try:
        response = requests.get(f'{API_URL}/health', timeout=5)
        result = response.json()
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"   Status: {result.get('status')}")
        print(f"   Database: {result.get('database')}")
        
        if response.status_code == 200:
            print("✅ BACKEND IS RUNNING!")
            return True
        else:
            print("❌ BACKEND HEALTH CHECK FAILED")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend!")
        print("   Make sure the backend is running: python backend/app.py")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("\n" + "🚀"*30)
    print("AI INTERVIEW COACH - COMPLETE FLOW TEST")
    print("🚀"*30)
    
    # Test 0: Health Check
    if not test_health():
        print("\n❌ Backend is not running. Please start it first:")
        print("   cd backend && python app.py")
        return
    
    # Test 1: Sign Up
    user_data, signup_token = test_signup()
    if not user_data:
        print("\n❌ Signup test failed. Cannot continue.")
        return
    
    time.sleep(1)  # Brief pause
    
    # Test 2: Login
    login_token = test_login(user_data['email'], user_data['password'])
    if not login_token:
        print("\n❌ Login test failed. Cannot continue.")
        return
    
    time.sleep(1)  # Brief pause
    
    # Test 3: Get Questions
    questions_ok = test_get_questions(login_token)
    
    # Final Summary
    print_section("FINAL SUMMARY")
    
    results = {
        'Backend Health': '✅ PASS',
        'User Registration': '✅ PASS' if signup_token else '❌ FAIL',
        'User Login': '✅ PASS' if login_token else '❌ FAIL',
        'Get Questions': '✅ PASS' if questions_ok else '❌ FAIL'
    }
    
    print()
    for test, result in results.items():
        print(f"   {test}: {result}")
    
    all_passed = all('✅' in r for r in results.values())
    
    if all_passed:
        print("\n" + "🎉"*30)
        print("ALL TESTS PASSED! ✅")
        print("🎉"*30)
        print("\n✅ Your application is working correctly!")
        print("\n📝 Test Account Created:")
        print(f"   Email: {user_data['email']}")
        print(f"   Password: {user_data['password']}")
        print("\n🌐 You can now:")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Click 'Login'")
        print("   3. Use the credentials above to login")
        print("   4. Start a mock interview!")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
