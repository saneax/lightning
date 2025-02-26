import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/chatapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SSL/TLS Configuration
    SSL_CERTIFICATE = 'path/to/cert.pem'
    SSL_KEY = 'path/to/key.pem'
    
    # Redis configuration for Socket.IO
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=1) 