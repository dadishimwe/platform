"""
Authentication and authorization middleware for the Starlink Platform API.
"""
from functools import wraps
from flask import request, current_app, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from src.models import db
from src.models.user import User, Role, Permission, UserRole
from src.utils.responses import error_response

def jwt_required_with_refresh(fn):
    """
    Custom decorator that verifies JWT and handles token refresh.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT
            verify_jwt_in_request()
            
            # Get user ID from token
            user_id = get_jwt_identity()
            
            # Get user from database
            user = User.query.get(user_id)
            if not user:
                return error_response('User not found', status_code=404)
            
            # Store user in g object for route handlers
            g.current_user = user
            
            # Continue to route handler
            return fn(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"JWT verification error: {str(e)}")
            return error_response('Invalid or expired token', status_code=401)
    
    return wrapper

def role_required(role_name):
    """
    Decorator that checks if user has the required role.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT
                verify_jwt_in_request()
                
                # Get user ID from token
                user_id = get_jwt_identity()
                
                # Get user roles from database
                user_roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user_id).all()
                
                # Check if user has the required role
                if not any(role.name == role_name for role in user_roles):
                    return error_response('Insufficient permissions', status_code=403)
                
                # Continue to route handler
                return fn(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Role verification error: {str(e)}")
                return error_response('Authentication error', status_code=401)
        
        return wrapper
    
    return decorator

def permission_required(resource, action):
    """
    Decorator that checks if user has the required permission.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT
                verify_jwt_in_request()
                
                # Get user ID from token
                user_id = get_jwt_identity()
                
                # Get user permissions from database
                user_permissions = db.session.query(Permission).join(Role.permissions).join(UserRole).filter(UserRole.user_id == user_id).all()
                
                # Check if user has the required permission
                if not any(p.resource == resource and p.action == action for p in user_permissions):
                    return error_response('Insufficient permissions', status_code=403)
                
                # Continue to route handler
                return fn(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Permission verification error: {str(e)}")
                return error_response('Authentication error', status_code=401)
        
        return wrapper
    
    return decorator

def get_current_user():
    """
    Get current authenticated user.
    """
    try:
        # Verify JWT
        verify_jwt_in_request()
        
        # Get user ID from token
        user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(user_id)
        
        return user
    except Exception:
        return None

