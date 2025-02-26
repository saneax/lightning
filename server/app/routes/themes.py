from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import ChatTheme, UserChatPreference, db

themes_bp = Blueprint('themes', __name__)

@themes_bp.route('/themes', methods=['GET'])
@login_required
def get_themes():
    themes = ChatTheme.query.all()
    return jsonify([{
        'id': t.theme_id,
        'name': t.name,
        'primary_color': t.primary_color,
        'secondary_color': t.secondary_color,
        'text_color': t.text_color,
        'accent_color': t.accent_color
    } for t in themes])

@themes_bp.route('/preferences/chat/<int:user_id>', methods=['GET'])
@login_required
def get_chat_preference(user_id):
    pref = UserChatPreference.query.filter_by(
        user_id=current_user.user_id,
        chat_with_user_id=user_id
    ).first()
    
    if not pref:
        # Return default theme if no preference is set
        default_theme = ChatTheme.query.filter_by(name='Default Blue').first()
        return jsonify({'theme': {
            'id': default_theme.theme_id,
            'name': default_theme.name,
            'primary_color': default_theme.primary_color,
            'secondary_color': default_theme.secondary_color,
            'text_color': default_theme.text_color,
            'accent_color': default_theme.accent_color
        }})
    
    return jsonify({'theme': {
        'id': pref.theme.theme_id,
        'name': pref.theme.name,
        'primary_color': pref.theme.primary_color,
        'secondary_color': pref.theme.secondary_color,
        'text_color': pref.theme.text_color,
        'accent_color': pref.theme.accent_color
    }})

@themes_bp.route('/preferences/chat/<int:user_id>', methods=['POST'])
@login_required
def set_chat_preference(user_id):
    data = request.get_json()
    theme_id = data['themeId']
    
    pref = UserChatPreference.query.filter_by(
        user_id=current_user.user_id,
        chat_with_user_id=user_id
    ).first()
    
    if pref:
        pref.theme_id = theme_id
    else:
        pref = UserChatPreference(
            user_id=current_user.user_id,
            chat_with_user_id=user_id,
            theme_id=theme_id
        )
        db.session.add(pref)
    
    db.session.commit()
    return jsonify({'message': 'Theme preference updated successfully'}) 