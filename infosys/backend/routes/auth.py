from flask import Blueprint, request, jsonify, current_app
import bcrypt
import jwt
from datetime import datetime, timedelta
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

def get_db():
    return current_app.db

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        print(f"Registration attempt for: {data.get('email')}")
        
        db = get_db()
        
        if db is None:
            print("Database connection is None")
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Check if user exists
        existing_user = db.users.find_one({'email': data['email']})
        if existing_user:
            print(f"User already exists: {data['email']}")
            return jsonify({'error': 'Email already exists'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        print(f"Password hashed successfully, type: {type(password_hash)}")
        
        user = {
            'email': data['email'],
            'password_hash': password_hash,
            'name': data['name'],
            'job_role': data.get('job_role', ''),
            'industry': data.get('industry', ''),
            'created_at': datetime.utcnow(),
            'interviews': []
        }
        
        print(f"Inserting user into database...")
        result = db.users.insert_one(user)
        print(f"User inserted with ID: {result.inserted_id}")
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': str(result.inserted_id),
            'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        print(f"Registration successful for: {data['email']}")
        
        return jsonify({
            'token': token,
            'user': {'email': user['email'], 'name': user['name']}
        }), 201
        
    except Exception as e:
        print(f"Registration error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        print(f"Login attempt for: {data.get('email')}")
        
        db = get_db()
        
        if db is None:
            print("Database connection is None")
            return jsonify({'error': 'Database connection failed'}), 500
        
        user = db.users.find_one({'email': data['email']})
        
        if not user:
            print(f"User not found: {data.get('email')}")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        print(f"User found: {user['email']}")
        print(f"Password hash type: {type(user['password_hash'])}")
        
        # Handle both bytes and Binary types from MongoDB
        stored_hash = user['password_hash']
        if isinstance(stored_hash, bytes):
            password_hash = stored_hash
        else:
            # If it's a Binary object from MongoDB, convert to bytes
            password_hash = bytes(stored_hash)
        
        # Verify password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), password_hash):
            print("Password verification failed")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        print("Password verified successfully")
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        print(f"Login successful for: {user['email']}")
        
        return jsonify({
            'token': token,
            'user': {'email': user['email'], 'name': user['name']}
        }), 200
        
    except Exception as e:
        print(f"Login error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Login failed. Please try again.'}), 500
