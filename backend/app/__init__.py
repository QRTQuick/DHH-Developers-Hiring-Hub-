from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_socketio import SocketIO
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.developers import dev_bp
    from .routes.hiring import hiring_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dev_bp, url_prefix='/api/developers')
    app.register_blueprint(hiring_bp, url_prefix='/api/hiring')

    # Register socket events
    with app.app_context():
        from .utils import socket_events

    return app
