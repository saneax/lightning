from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from app.routes.direct_messages import dm_bp
from app.routes.themes import themes_bp

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {"origins": Config.FRONTEND_URL},
        r"/socket.io/*": {"origins": Config.FRONTEND_URL}
    })

    db.init_app(app)
    socketio.init_app(app, message_queue='redis://', cors_allowed_origins=Config.FRONTEND_URL)
    login_manager.init_app(app)

    from app.routes import auth_bp, channels_bp, messages_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(channels_bp, url_prefix='/api/channels')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(dm_bp, url_prefix='/api/messages')
    app.register_blueprint(themes_bp, url_prefix='/api')

    return app 