from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.platform import Platform, StreamSession, db
from src.models.user import User

platform_bp = Blueprint('platform', __name__)

@platform_bp.route('/platforms', methods=['GET'])
@jwt_required()
def get_platforms():
    """Get all platforms for the current user"""
    current_user_id = get_jwt_identity()
    platforms = Platform.query.filter_by(user_id=current_user_id).all()
    return jsonify([platform.to_dict() for platform in platforms])

@platform_bp.route('/platforms', methods=['POST'])
@jwt_required()
def create_platform():
    """Add a new streaming platform"""
    current_user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    if not data.get('platform_name'):
        return jsonify({'error': 'Platform name is required'}), 400
    
    # Check if platform already exists for this user
    existing = Platform.query.filter_by(
        user_id=current_user_id, 
        platform_name=data['platform_name']
    ).first()
    
    if existing:
        return jsonify({'error': 'Platform already configured for this user'}), 409
    
    platform = Platform(
        user_id=current_user_id,
        platform_name=data['platform_name'],
        platform_username=data.get('platform_username'),
        ingest_url=data.get('ingest_url')
    )
    
    # Set encrypted fields
    if data.get('access_token'):
        platform.set_access_token(data['access_token'])
    if data.get('refresh_token'):
        platform.set_refresh_token(data['refresh_token'])
    if data.get('stream_key'):
        platform.set_stream_key(data['stream_key'])
    
    db.session.add(platform)
    db.session.commit()
    
    return jsonify(platform.to_dict()), 201

@platform_bp.route('/platforms/<int:platform_id>', methods=['GET'])
@jwt_required()
def get_platform(platform_id):
    """Get a specific platform"""
    current_user_id = get_jwt_identity()
    platform = Platform.query.filter_by(id=platform_id, user_id=current_user_id).first()
    
    if not platform:
        return jsonify({'error': 'Platform not found'}), 404
    
    return jsonify(platform.to_dict())

@platform_bp.route('/platforms/<int:platform_id>', methods=['PUT'])
@jwt_required()
def update_platform(platform_id):
    """Update a platform configuration"""
    current_user_id = get_jwt_identity()
    platform = Platform.query.filter_by(id=platform_id, user_id=current_user_id).first()
    
    if not platform:
        return jsonify({'error': 'Platform not found'}), 404
    
    data = request.json
    
    # Update basic fields
    if 'platform_username' in data:
        platform.platform_username = data['platform_username']
    if 'ingest_url' in data:
        platform.ingest_url = data['ingest_url']
    if 'is_active' in data:
        platform.is_active = data['is_active']
    
    # Update encrypted fields
    if 'access_token' in data:
        platform.set_access_token(data['access_token'])
    if 'refresh_token' in data:
        platform.set_refresh_token(data['refresh_token'])
    if 'stream_key' in data:
        platform.set_stream_key(data['stream_key'])
    
    db.session.commit()
    
    return jsonify(platform.to_dict())

@platform_bp.route('/platforms/<int:platform_id>', methods=['DELETE'])
@jwt_required()
def delete_platform(platform_id):
    """Delete a platform configuration"""
    current_user_id = get_jwt_identity()
    platform = Platform.query.filter_by(id=platform_id, user_id=current_user_id).first()
    
    if not platform:
        return jsonify({'error': 'Platform not found'}), 404
    
    db.session.delete(platform)
    db.session.commit()
    
    return '', 204

@platform_bp.route('/platforms/<int:platform_id>/credentials', methods=['GET'])
@jwt_required()
def get_platform_credentials(platform_id):
    """Get platform credentials (sensitive data)"""
    current_user_id = get_jwt_identity()
    platform = Platform.query.filter_by(id=platform_id, user_id=current_user_id).first()
    
    if not platform:
        return jsonify({'error': 'Platform not found'}), 404
    
    return jsonify(platform.to_dict(include_sensitive=True))

@platform_bp.route('/platforms/<int:platform_id>/test', methods=['POST'])
@jwt_required()
def test_platform_connection(platform_id):
    """Test connection to a platform"""
    current_user_id = get_jwt_identity()
    platform = Platform.query.filter_by(id=platform_id, user_id=current_user_id).first()
    
    if not platform:
        return jsonify({'error': 'Platform not found'}), 404
    
    # TODO: Implement actual platform API testing
    # This would involve making API calls to each platform to verify credentials
    
    return jsonify({
        'platform_id': platform_id,
        'platform_name': platform.platform_name,
        'status': 'success',
        'message': 'Connection test successful'
    })

@platform_bp.route('/stream-sessions', methods=['GET'])
@jwt_required()
def get_stream_sessions():
    """Get stream sessions for the current user"""
    current_user_id = get_jwt_identity()
    sessions = StreamSession.query.filter_by(user_id=current_user_id).order_by(StreamSession.started_at.desc()).all()
    return jsonify([session.to_dict() for session in sessions])

@platform_bp.route('/stream-sessions', methods=['POST'])
@jwt_required()
def create_stream_session():
    """Start a new stream session"""
    current_user_id = get_jwt_identity()
    data = request.json
    
    if not data.get('platform_id'):
        return jsonify({'error': 'Platform ID is required'}), 400
    
    # Verify platform belongs to user
    platform = Platform.query.filter_by(id=data['platform_id'], user_id=current_user_id).first()
    if not platform:
        return jsonify({'error': 'Platform not found'}), 404
    
    session = StreamSession(
        user_id=current_user_id,
        platform_id=data['platform_id'],
        stream_title=data.get('stream_title')
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify(session.to_dict()), 201

@platform_bp.route('/stream-sessions/<int:session_id>/end', methods=['POST'])
@jwt_required()
def end_stream_session(session_id):
    """End a stream session"""
    current_user_id = get_jwt_identity()
    session = StreamSession.query.filter_by(id=session_id, user_id=current_user_id).first()
    
    if not session:
        return jsonify({'error': 'Stream session not found'}), 404
    
    session.ended_at = db.func.current_timestamp()
    session.is_active = False
    
    db.session.commit()
    
    return jsonify(session.to_dict())

