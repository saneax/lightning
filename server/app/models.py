from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DirectMessage(db.Model):
    __tablename__ = 'direct_messages'
    
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

class ChatTheme(db.Model):
    __tablename__ = 'chat_themes'
    
    theme_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    primary_color = db.Column(db.String(7), nullable=False)
    secondary_color = db.Column(db.String(7), nullable=False)
    text_color = db.Column(db.String(7), nullable=False)
    accent_color = db.Column(db.String(7), nullable=False)

class UserChatPreference(db.Model):
    __tablename__ = 'user_chat_preferences'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    chat_with_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('chat_themes.theme_id'))

    theme = db.relationship('ChatTheme') 