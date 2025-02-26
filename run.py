from app import create_app, socketio
from app import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    socketio.run(app,
                host='0.0.0.0',
                port=5000,
                ssl_context=(
                    app.config['SSL_CERTIFICATE'],
                    app.config['SSL_KEY']
                )) 