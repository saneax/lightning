from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Message, Channel, ChannelMember, db
from app import socketio

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/channels/<int:channel_id>/messages', methods=['GET'])
@login_required
def get_messages(channel_id):
    # Check if user is member of the channel
    member = ChannelMember.query.filter_by(
        channel_id=channel_id,
        user_id=current_user.user_id
    ).first()
    
    if not member:
        return jsonify({'error': 'Not authorized'}), 403
    
    messages = Message.query.filter_by(channel_id=channel_id)\
        .order_by(Message.created_at.desc())\
        .limit(50).all()
    
    return jsonify([{
        'id': m.message_id,
        'content': m.content,
        'username': m.user.username,
        'created_at': m.created_at.isoformat()
    } for m in messages]) 