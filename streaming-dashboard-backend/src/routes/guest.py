from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.guest import Guest, GuestSession, db
from src.models.user import User
from datetime import datetime

guest_bp = Blueprint('guest', __name__)

@guest_bp.route('/guests', methods=['GET'])
@jwt_required()
def get_guests():
    """Get all guests for the current user"""
    current_user_id = get_jwt_identity()
    guests = Guest.query.filter_by(user_id=current_user_id).all()
    return jsonify([guest.to_dict() for guest in guests])

@guest_bp.route('/guests', methods=['POST'])
@jwt_required()
def create_guest():
    """Create a new guest invitation"""
    current_user_id = get_jwt_identity()
    data = request.json
    
    if not data.get('guest_name'):
        return jsonify({'error': 'Guest name is required'}), 400
    
    guest = Guest(
        user_id=current_user_id,
        guest_name=data['guest_name'],
        guest_email=data.get('guest_email'),
        video_quality=data.get('video_quality', '720p'),
        audio_quality=data.get('audio_quality', 'high')
    )
    
    db.session.add(guest)
    db.session.commit()
    
    return jsonify(guest.to_dict(include_token=True)), 201

@guest_bp.route('/guests/<int:guest_id>', methods=['GET'])
@jwt_required()
def get_guest(guest_id):
    """Get a specific guest"""
    current_user_id = get_jwt_identity()
    guest = Guest.query.filter_by(id=guest_id, user_id=current_user_id).first()
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    return jsonify(guest.to_dict())

@guest_bp.route('/guests/<int:guest_id>', methods=['PUT'])
@jwt_required()
def update_guest(guest_id):
    """Update guest settings"""
    current_user_id = get_jwt_identity()
    guest = Guest.query.filter_by(id=guest_id, user_id=current_user_id).first()
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    data = request.json
    
    # Update fields
    if 'guest_name' in data:
        guest.guest_name = data['guest_name']
    if 'guest_email' in data:
        guest.guest_email = data['guest_email']
    if 'is_active' in data:
        guest.is_active = data['is_active']
    if 'video_enabled' in data:
        guest.video_enabled = data['video_enabled']
    if 'audio_enabled' in data:
        guest.audio_enabled = data['audio_enabled']
    if 'video_quality' in data:
        guest.video_quality = data['video_quality']
    if 'audio_quality' in data:
        guest.audio_quality = data['audio_quality']
    
    db.session.commit()
    
    return jsonify(guest.to_dict())

@guest_bp.route('/guests/<int:guest_id>', methods=['DELETE'])
@jwt_required()
def delete_guest(guest_id):
    """Delete a guest"""
    current_user_id = get_jwt_identity()
    guest = Guest.query.filter_by(id=guest_id, user_id=current_user_id).first()
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    db.session.delete(guest)
    db.session.commit()
    
    return '', 204

@guest_bp.route('/guests/<int:guest_id>/regenerate-token', methods=['POST'])
@jwt_required()
def regenerate_guest_token(guest_id):
    """Regenerate access token for a guest"""
    current_user_id = get_jwt_identity()
    guest = Guest.query.filter_by(id=guest_id, user_id=current_user_id).first()
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    new_token = guest.generate_new_token()
    db.session.commit()
    
    return jsonify({
        'guest_id': guest_id,
        'new_token': new_token
    })

@guest_bp.route('/guests/<int:guest_id>/invite-link', methods=['GET'])
@jwt_required()
def get_guest_invite_link(guest_id):
    """Get invite link for a guest"""
    current_user_id = get_jwt_identity()
    guest = Guest.query.filter_by(id=guest_id, user_id=current_user_id).first()
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    # TODO: Replace with actual frontend URL
    base_url = request.host_url
    invite_link = f"{base_url}guest/{guest.guest_token}"
    
    return jsonify({
        'guest_id': guest_id,
        'guest_name': guest.guest_name,
        'invite_link': invite_link,
        'token': guest.guest_token
    })

@guest_bp.route('/guest-access/<guest_token>', methods=['GET'])
def get_guest_by_token(guest_token):
    """Get guest information by token (for guest access)"""
    guest = Guest.query.filter_by(guest_token=guest_token, is_active=True).first()
    
    if not guest:
        return jsonify({'error': 'Invalid or expired guest token'}), 404
    
    return jsonify(guest.to_dict())

@guest_bp.route('/guest-access/<guest_token>/connect', methods=['POST'])
def connect_guest(guest_token):
    """Mark guest as connected"""
    guest = Guest.query.filter_by(guest_token=guest_token, is_active=True).first()
    
    if not guest:
        return jsonify({'error': 'Invalid or expired guest token'}), 404
    
    guest.is_connected = True
    guest.last_connected_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'status': 'connected',
        'guest_name': guest.guest_name,
        'video_quality': guest.video_quality,
        'audio_quality': guest.audio_quality
    })

@guest_bp.route('/guest-access/<guest_token>/disconnect', methods=['POST'])
def disconnect_guest(guest_token):
    """Mark guest as disconnected"""
    guest = Guest.query.filter_by(guest_token=guest_token, is_active=True).first()
    
    if not guest:
        return jsonify({'error': 'Invalid or expired guest token'}), 404
    
    guest.is_connected = False
    
    db.session.commit()
    
    return jsonify({'status': 'disconnected'})

@guest_bp.route('/guest-access/<guest_token>/update-quality', methods=['POST'])
def update_guest_quality(guest_token):
    """Update guest connection quality metrics"""
    guest = Guest.query.filter_by(guest_token=guest_token, is_active=True).first()
    
    if not guest:
        return jsonify({'error': 'Invalid or expired guest token'}), 404
    
    data = request.json
    
    if 'latency_ms' in data:
        guest.latency_ms = data['latency_ms']
    if 'connection_quality' in data:
        guest.connection_quality = data['connection_quality']
    
    db.session.commit()
    
    return jsonify({'status': 'updated'})

@guest_bp.route('/guest-sessions', methods=['GET'])
@jwt_required()
def get_guest_sessions():
    """Get guest sessions for the current user's guests"""
    current_user_id = get_jwt_identity()
    
    # Get all guests for the current user
    guest_ids = [g.id for g in Guest.query.filter_by(user_id=current_user_id).all()]
    
    sessions = GuestSession.query.filter(GuestSession.guest_id.in_(guest_ids)).order_by(GuestSession.connected_at.desc()).all()
    
    return jsonify([session.to_dict() for session in sessions])

@guest_bp.route('/guest-sessions', methods=['POST'])
def create_guest_session():
    """Create a new guest session (called by WebRTC system)"""
    data = request.json
    
    if not data.get('guest_token') or not data.get('session_id'):
        return jsonify({'error': 'Guest token and session ID are required'}), 400
    
    guest = Guest.query.filter_by(guest_token=data['guest_token'], is_active=True).first()
    
    if not guest:
        return jsonify({'error': 'Invalid guest token'}), 404
    
    session = GuestSession(
        guest_id=guest.id,
        session_id=data['session_id']
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify(session.to_dict()), 201

@guest_bp.route('/guest-sessions/<int:session_id>/end', methods=['POST'])
def end_guest_session(session_id):
    """End a guest session"""
    session = GuestSession.query.get_or_404(session_id)
    
    data = request.json
    
    session.disconnected_at = datetime.utcnow()
    
    # Update session metrics if provided
    if 'avg_latency_ms' in data:
        session.avg_latency_ms = data['avg_latency_ms']
    if 'min_latency_ms' in data:
        session.min_latency_ms = data['min_latency_ms']
    if 'max_latency_ms' in data:
        session.max_latency_ms = data['max_latency_ms']
    if 'packets_lost' in data:
        session.packets_lost = data['packets_lost']
    if 'packets_sent' in data:
        session.packets_sent = data['packets_sent']
    if 'bytes_sent' in data:
        session.bytes_sent = data['bytes_sent']
    if 'bytes_received' in data:
        session.bytes_received = data['bytes_received']
    
    db.session.commit()
    
    return jsonify(session.to_dict())

