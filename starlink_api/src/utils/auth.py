"""
Authentication utilities for the Starlink Platform API.
"""
import os
import requests
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.models.user import User, Role, Permission, UserRole, RolePermission

def token_required(f):
    """Decorator to verify JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired'}), 401
    return decorated


def admin_required(f):
    """Decorator to verify admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            
            for user_role in user_roles:
                role = Role.query.get(user_role.role_id)
                if role and role.name == 'Super Admin':
                    return f(*args, **kwargs)
            
            return jsonify({'message': 'Admin privileges required'}), 403
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired'}), 401
    return decorated


def permission_required(resource, action):
    """Decorator to verify permission."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user_roles = UserRole.query.filter_by(user_id=user_id).all()
                
                # Check if user has Super Admin role
                for user_role in user_roles:
                    role = Role.query.get(user_role.role_id)
                    if role and role.name == 'Super Admin':
                        return f(*args, **kwargs)
                
                # Check if user has required permission
                permission = Permission.query.filter_by(resource=resource, action=action).first()
                if not permission:
                    return jsonify({'message': 'Permission not found'}), 403
                
                for user_role in user_roles:
                    role_permission = RolePermission.query.filter_by(
                        role_id=user_role.role_id,
                        permission_id=permission.id
                    ).first()
                    
                    if role_permission:
                        return f(*args, **kwargs)
                
                return jsonify({'message': 'Permission denied'}), 403
            except Exception as e:
                return jsonify({'message': 'Token is invalid or expired'}), 401
        return decorated
    return decorator


def get_starlink_access_token():
    """Get access token from Starlink API."""
    try:
        response = requests.post(
            f"{current_app.config['STARLINK_API_URL']}/auth/connect/token",
            headers={'Content-type': 'application/x-www-form-urlencoded'},
            data={
                'client_id': current_app.config['STARLINK_CLIENT_ID'],
                'client_secret': current_app.config['STARLINK_CLIENT_SECRET'],
                'grant_type': 'client_credentials',
            }
        )
        response.raise_for_status()
        return response.json().get('access_token')
    except Exception as e:
        current_app.logger.error(f"Failed to get Starlink access token: {str(e)}")
        return None

