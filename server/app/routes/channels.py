from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Channel, ChannelMember, db

channels_bp = Blueprint('channels', __name__)

@channels_bp.route('/', methods=['GET'])
@login_required
def get_channels():
    # Get public channels and private channels where user is a member
    public_channels = Channel.query.filter_by(is_private=False).all()
    private_channels = Channel.query.join(ChannelMember).filter(
        Channel.is_private==True,
        ChannelMember.user_id==current_user.user_id
    ).all()
    
    channels = public_channels + private_channels
    return jsonify([{
        'id': c.channel_id,
        'name': c.name,
        'description': c.description,
        'is_private': c.is_private,
        'sticky_note': c.sticky_note
    } for c in channels])

@channels_bp.route('/', methods=['POST'])
@login_required
def create_channel():
    data = request.get_json()
    
    channel = Channel(
        name=data['name'],
        description=data.get('description', ''),
        is_private=data.get('is_private', False),
        created_by=current_user.user_id
    )
    
    db.session.add(channel)
    db.session.flush()
    
    # Add creator as channel member with creator role
    member = ChannelMember(
        channel_id=channel.channel_id,
        user_id=current_user.user_id,
        role='creator'
    )
    
    db.session.add(member)
    db.session.commit()
    
    return jsonify({
        'id': channel.channel_id,
        'name': channel.name,
        'description': channel.description,
        'is_private': channel.is_private
    }), 201 