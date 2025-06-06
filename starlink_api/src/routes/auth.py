"""
Authentication routes for the Starlink Platform API.
"""
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import ValidationError
from src.models import db
from src.models.user import User, Role, UserRole
from src.schemas.user import user_schema, login_schema, register_schema
from src.utils.responses import success_response, error_response
from src.utils.auth_middleware import jwt_required_with_refresh

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        # Validate request data
        data = register_schema.load(request.json)
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return error_response('Email already registered', status_code=409)
        
        # Create new user
        new_user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone=data.get('phone', '')
        )
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()
        
        # Assign default role (Client)
        client_role = Role.query.filter_by(name='Client').first()
        if client_role:
            user_role = UserRole(user_id=new_user.id, role_id=client_role.id)
            db.session.add(user_role)
            db.session.commit()
        
        # Return success response
        return success_response(
            message='User registered successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages, status_code=400)
    
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return error_response('An error occurred during registration', status_code=500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return tokens."""
    try:
        # Validate request data
        data = login_schema.load(request.json)
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, data['password']):
            return error_response('Invalid email or password', status_code=401)
        
        # Check if user is active
        if not user.is_active:
            return error_response('Account is disabled', status_code=403)
        
        # Create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Update last login timestamp
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Get user roles
        roles = [role.name for role in user.roles]
        
        # Return tokens and user data
        return success_response({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': roles
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages, status_code=400)
    
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return error_response('An error occurred during login', status_code=500)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        # Get user ID from refresh token
        user_id = get_jwt_identity()
        
        # Create new access token
        access_token = create_access_token(identity=user_id)
        
        # Return new access token
        return success_response({
            'access_token': access_token
        })
    
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return error_response('An error occurred while refreshing token', status_code=500)

@auth_bp.route('/me', methods=['GET'])
@jwt_required_with_refresh
def me():
    """Get current user data."""
    try:
        # Get user ID from token
        user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', status_code=404)
        
        # Get user roles
        roles = [{'id': role.id, 'name': role.name} for role in user.roles]
        
        # Get user permissions
        permissions = []
        for role in user.roles:
            for permission in role.permissions:
                permissions.append({
                    'id': permission.id,
                    'resource': permission.resource,
                    'action': permission.action
                })
        
        # Return user data
        return success_response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login_at': user.last_login_at.isoformat() if user.last_login_at else None,
            'roles': roles,
            'permissions': permissions
        })
    
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return error_response('An error occurred while getting user data', status_code=500)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user."""
    try:
        # Get JWT token
        jti = get_jwt()['jti']
        
        # Add token to blocklist (in a real application, you would store this in Redis or another fast database)
        # For now, we'll just return a success response
        
        return success_response(message='Logged out successfully')
    
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return error_response('An error occurred during logout', status_code=500)

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password."""
    try:
        # Get user ID from token
        user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', status_code=404)
        
        # Get request data
        data = request.json
        
        # Check if current password is correct
        if not check_password_hash(user.password_hash, data.get('current_password')):
            return error_response('Current password is incorrect', status_code=400)
        
        # Check if new password meets requirements
        new_password = data.get('new_password')
        if not new_password or len(new_password) < 8:
            return error_response('New password must be at least 8 characters long', status_code=400)
        
        # Update password
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        # Return success response
        return success_response(message='Password changed successfully')
    
    except Exception as e:
        current_app.logger.error(f"Change password error: {str(e)}")
        db.session.rollback()
        return error_response('An error occurred while changing password', status_code=500)

