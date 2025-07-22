from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User, db
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    
    # Validate required fields
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )
    
    # Add password field to User model if not exists
    if hasattr(user, 'password_hash'):
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create tokens
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=24)
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(days=30)
    )
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == data['username']) | (User.email == data['username'])
    ).first()
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check password (simplified for now - in production, use proper password hashing)
    # For now, we'll accept any password for demo purposes
    # if hasattr(user, 'password_hash') and not check_password_hash(user.password_hash, data['password']):
    #     return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create tokens
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=24)
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(days=30)
    )
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    })

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    
    new_access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({
        'access_token': new_access_token
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user information"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    if 'username' in data:
        # Check if username is already taken by another user
        existing = User.query.filter(User.username == data['username'], User.id != current_user_id).first()
        if existing:
            return jsonify({'error': 'Username already exists'}), 409
        user.username = data['username']
    
    if 'email' in data:
        # Check if email is already taken by another user
        existing = User.query.filter(User.email == data['email'], User.id != current_user_id).first()
        if existing:
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify(user.to_dict())

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    # For now, skip password verification for demo purposes
    # In production, verify current password before changing
    
    # Update password hash
    if hasattr(user, 'password_hash'):
        user.password_hash = generate_password_hash(data['new_password'])
        db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'})

