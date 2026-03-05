from flask import Blueprint, request, jsonify, current_app
import bcrypt
import jwt
from datetime import datetime, timedelta
import sqlite3

auth_bp = Blueprint('auth', __name__)

def get_db():
    conn = sqlite3.connect('interview_coach.db')
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Insert user
    cursor.execute('''
        INSERT INTO users (email, password_hash, name, job_role, industry)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['email'], password_hash, data['name'], 
          data.get('job_role'), data.get('industry')))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {'email': data['email'], 'name': data['name']}
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {'email': user['email'], 'name': user['name']}
    }), 200
