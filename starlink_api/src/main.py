"""
Main application file for the Starlink Platform API.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from src.models import db
from src.config.config import Config
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.organization import organization_bp
from src.routes.device import device_bp
from src.routes.telemetry import telemetry_bp
from src.routes.support import support_bp
from src.routes.notification import notification_bp
from src.utils.error_handlers import register_error_handlers
from src.utils.init_db import init_db

def create_app(config_class=Config):
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(organization_bp, url_prefix='/api/organizations')
    app.register_blueprint(device_bp, url_prefix='/api/devices')
    app.register_blueprint(telemetry_bp, url_prefix='/api/telemetry')
    app.register_blueprint(support_bp, url_prefix='/api/support')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    
    # Register error handlers
    register_error_handlers(app)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'status': 'error',
            'message': 'Token has expired',
            'code': 'token_expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'status': 'error',
            'message': 'Invalid token',
            'code': 'invalid_token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'status': 'error',
            'message': 'Authorization token is missing',
            'code': 'authorization_required'
        }), 401
    
    # Create database tables and initialize data
    with app.app_context():
        db.create_all()
        
        # Initialize database with default data if INIT_DB environment variable is set
        if os.environ.get('INIT_DB', 'false').lower() == 'true':
            init_db()
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'ok',
            'message': 'Starlink Platform API is running'
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

