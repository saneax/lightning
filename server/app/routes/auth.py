from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from app.models import User, db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'token': user.get_auth_token(),
            'user': {
                'id': user.user_id,
                'username': user.username,
                'email': user.email
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401 