from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import DirectMessage, User, db
from datetime import datetime

dm_bp = Blueprint('direct_messages', __name__)

@dm_bp.route('/direct/<int:user_id>', methods=['GET'])
@login_required
def get_messages(user_id):
    messages = DirectMessage.query.filter(
        ((DirectMessage.sender_id == current_user.user_id) & 
         (DirectMessage.receiver_id == user_id)) |
        ((DirectMessage.sender_id == user_id) & 
         (DirectMessage.receiver_id == current_user.user_id))
    ).order_by(DirectMessage.created_at).all()
    
    return jsonify([{
        'id': m.message_id,
        'content': m.content,
        'sender_id': m.sender_id,
        'receiver_id': m.receiver_id,
        'created_at': m.created_at.isoformat()
    } for m in messages])

@dm_bp.route('/direct/<int:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    data = request.get_json()
    
    message = DirectMessage(
        sender_id=current_user.user_id,
        receiver_id=user_id,
        content=data['content']
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'id': message.message_id,
        'content': message.content,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'created_at': message.created_at.isoformat()
    }) 