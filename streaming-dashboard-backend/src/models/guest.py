from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid

class Guest(db.Model):
    """Model for managing guest connections"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Host user
    guest_token = db.Column(db.String(255), unique=True, nullable=False)  # Unique token for guest access
    guest_name = db.Column(db.String(100), nullable=False)
    guest_email = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_connected = db.Column(db.Boolean, default=False)
    connection_quality = db.Column(db.String(20), default='unknown')  # good, fair, poor, unknown
    latency_ms = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_connected_at = db.Column(db.DateTime, nullable=True)
    
    # WebRTC connection settings
    video_enabled = db.Column(db.Boolean, default=True)
    audio_enabled = db.Column(db.Boolean, default=True)
    video_quality = db.Column(db.String(20), default='720p')  # 1080p, 720p, 480p, 360p
    audio_quality = db.Column(db.String(20), default='high')  # high, medium, low

    def __init__(self, **kwargs):
        if 'guest_token' not in kwargs:
            kwargs['guest_token'] = str(uuid.uuid4())
        super(Guest, self).__init__(**kwargs)

    def generate_new_token(self):
        """Generate a new access token for the guest"""
        self.guest_token = str(uuid.uuid4())
        return self.guest_token

    def to_dict(self, include_token=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'is_active': self.is_active,
            'is_connected': self.is_connected,
            'connection_quality': self.connection_quality,
            'latency_ms': self.latency_ms,
            'video_enabled': self.video_enabled,
            'audio_enabled': self.audio_enabled,
            'video_quality': self.video_quality,
            'audio_quality': self.audio_quality,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_connected_at': self.last_connected_at.isoformat() if self.last_connected_at else None
        }
        
        if include_token:
            data['guest_token'] = self.guest_token
        
        return data

    def __repr__(self):
        return f'<Guest {self.guest_name} for User {self.user_id}>'


class GuestSession(db.Model):
    """Track guest connection sessions"""
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    session_id = db.Column(db.String(255), nullable=False)  # WebRTC session ID
    connected_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    disconnected_at = db.Column(db.DateTime, nullable=True)
    avg_latency_ms = db.Column(db.Integer, nullable=True)
    min_latency_ms = db.Column(db.Integer, nullable=True)
    max_latency_ms = db.Column(db.Integer, nullable=True)
    packets_lost = db.Column(db.Integer, default=0)
    packets_sent = db.Column(db.Integer, default=0)
    bytes_sent = db.Column(db.BigInteger, default=0)
    bytes_received = db.Column(db.BigInteger, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'guest_id': self.guest_id,
            'session_id': self.session_id,
            'connected_at': self.connected_at.isoformat() if self.connected_at else None,
            'disconnected_at': self.disconnected_at.isoformat() if self.disconnected_at else None,
            'avg_latency_ms': self.avg_latency_ms,
            'min_latency_ms': self.min_latency_ms,
            'max_latency_ms': self.max_latency_ms,
            'packets_lost': self.packets_lost,
            'packets_sent': self.packets_sent,
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received
        }

    def __repr__(self):
        return f'<GuestSession {self.session_id} for Guest {self.guest_id}>'

