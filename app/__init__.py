from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app, message_queue='redis://')
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.channels import bp as channels_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(channels_bp)

    return app 