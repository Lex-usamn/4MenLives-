from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import os
import base64
from src.models.user import db

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform_name = db.Column(db.String(50), nullable=False)  # twitch, youtube, facebook, tiktok, instagram
    platform_username = db.Column(db.String(100), nullable=True)
    access_token = db.Column(db.Text, nullable=True)  # Encrypted
    refresh_token = db.Column(db.Text, nullable=True)  # Encrypted
    stream_key = db.Column(db.Text, nullable=True)  # Encrypted
    ingest_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, **kwargs):
        super(Platform, self).__init__(**kwargs)
        self._cipher = self._get_cipher()

    def _get_cipher(self):
        """Get or create encryption key for sensitive data"""
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # Generate a new key if not exists (for development)
            key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = base64.urlsafe_b64encode(key).decode()
        else:
            key = base64.urlsafe_b64decode(key.encode())
        return Fernet(key)

    def set_access_token(self, token):
        """Encrypt and store access token"""
        if token:
            self.access_token = self._cipher.encrypt(token.encode()).decode()

    def get_access_token(self):
        """Decrypt and return access token"""
        if self.access_token:
            return self._cipher.decrypt(self.access_token.encode()).decode()
        return None

    def set_refresh_token(self, token):
        """Encrypt and store refresh token"""
        if token:
            self.refresh_token = self._cipher.encrypt(token.encode()).decode()

    def get_refresh_token(self):
        """Decrypt and return refresh token"""
        if self.refresh_token:
            return self._cipher.decrypt(self.refresh_token.encode()).decode()
        return None

    def set_stream_key(self, key):
        """Encrypt and store stream key"""
        if key:
            self.stream_key = self._cipher.encrypt(key.encode()).decode()

    def get_stream_key(self):
        """Decrypt and return stream key"""
        if self.stream_key:
            return self._cipher.decrypt(self.stream_key.encode()).decode()
        return None

    def to_dict(self, include_sensitive=False):
        """Convert to dictionary, optionally including sensitive data"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'platform_name': self.platform_name,
            'platform_username': self.platform_username,
            'ingest_url': self.ingest_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                'access_token': self.get_access_token(),
                'refresh_token': self.get_refresh_token(),
                'stream_key': self.get_stream_key()
            })
        
        return data

    def __repr__(self):
        return f'<Platform {self.platform_name} for User {self.user_id}>'


class StreamSession(db.Model):
    """Track streaming sessions and metrics"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    stream_title = db.Column(db.String(255), nullable=True)
    started_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    ended_at = db.Column(db.DateTime, nullable=True)
    max_viewers = db.Column(db.Integer, default=0)
    total_messages = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'platform_id': self.platform_id,
            'stream_title': self.stream_title,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'max_viewers': self.max_viewers,
            'total_messages': self.total_messages,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<StreamSession {self.id} for Platform {self.platform_id}>'

