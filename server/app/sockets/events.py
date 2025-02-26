from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from app.models import Message, ChannelMember

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False

@socketio.on('join')
def handle_join(data):
    channel_id = data['channelId']
    member = ChannelMember.query.filter_by(
        channel_id=channel_id,
        user_id=current_user.user_id
    ).first()
    
    if member:
        join_room(f"channel_{channel_id}")
        emit('status', {'msg': f"{current_user.username} joined"}, room=f"channel_{channel_id}")

@socketio.on('message')
def handle_message(data):
    channel_id = data['channelId']
    content = data['content']
    
    member = ChannelMember.query.filter_by(
        channel_id=channel_id,
        user_id=current_user.user_id
    ).first()
    
    if member:
        message = Message(
            channel_id=channel_id,
            user_id=current_user.user_id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        
        emit('message', {
            'id': message.message_id,
            'content': message.content,
            'username': current_user.username,
            'created_at': message.created_at.isoformat()
        }, room=f"channel_{channel_id}") 