from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_socketio import SocketIO
from .config import Config
import os

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
socketio = SocketIO()

def create_app(config_class=Config):
    # Determine the base directory for Vercel vs local
    if os.environ.get('VERCEL'):
        # On Vercel, frontend is relative to this file's parent (app/)
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    else:
        # Local development
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    
    app = Flask(__name__, 
                static_folder=os.path.join(base_dir, 'static'), 
                static_url_path='/static',
                template_folder=base_dir)
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

    # Serve frontend static files for root and unknown routes
    @app.route('/')
    def serve_index():
        return send_from_directory(base_dir, 'index.html')

    @app.route('/search.html')
    def serve_search():
        return send_from_directory(base_dir, 'search.html')

    @app.route('/dashboard.html')
    def serve_dashboard():
        return send_from_directory(base_dir, 'dashboard.html')

    @app.route('/sitemap.xml')
    def serve_sitemap():
        return send_from_directory(base_dir, 'sitemap.xml'), 200, {'Content-Type': 'application/xml'}

    @app.route('/robots.txt')
    def serve_robots():
        return send_from_directory(base_dir, 'robots.txt'), 200, {'Content-Type': 'text/plain'}

    @app.route('/static/<path:path>')
    def serve_static_files(path):
        static_dir = os.path.join(base_dir, 'static')
        return send_from_directory(static_dir, path)

    @app.route('/<path:path>')
    def serve_catch_all(path):
        # Skip API and socket.io routes
        if path.startswith('api/') or path.startswith('socket.io/'):
            return None  # Let the route not match
        # Try to serve the requested file
        try:
            return send_from_directory(base_dir, path)
        except FileNotFoundError:
            # If file not found, serve index.html for SPA routing
            return send_from_directory(base_dir, 'index.html')

    return app
