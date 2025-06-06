"""
User routes for the Starlink Platform API.
"""
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from src.models import db
from src.models.user import User, Role, UserRole
from src.schemas.user import user_schema, users_schema, user_update_schema
from src.utils.responses import success_response, error_response, pagination_response
from src.utils.error_handlers import NotFoundError, ValidationError as APIValidationError
from src.utils.auth import admin_required, permission_required

user_bp = Blueprint('user', __name__)

@user_bp.route('', methods=['GET'])
@jwt_required()
@permission_required('user', 'read')
def get_users():
    """Get all users."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Query users with pagination
        pagination = User.query.paginate(page=page, per_page=per_page)
        
        # Return paginated users
        return pagination_response(
            users_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get users error: {str(e)}")
        return error_response('An error occurred while getting users', status_code=500)


@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
@permission_required('user', 'read')
def get_user(user_id):
    """Get user by ID."""
    try:
        # Find user
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('User not found')
        
        # Return user
        return success_response(user_schema.dump(user))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return error_response('An error occurred while getting user', status_code=500)


@user_bp.route('', methods=['POST'])
@jwt_required()
@permission_required('user', 'create')
def create_user():
    """Create a new user."""
    try:
        # Validate request data
        data = user_schema.load(request.json)
        
        # Check if email already exists
        if User.query.filter_by(email=data.email).first():
            raise APIValidationError('Email already exists')
        
        # Save user to database
        db.session.add(data)
        db.session.commit()
        
        # Return created user
        return success_response(user_schema.dump(data), 'User created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Create user error: {str(e)}")
        return error_response('An error occurred while creating user', status_code=500)


@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user by ID."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        
        # Find user
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('User not found')
        
        # Check if user is updating their own profile or has admin permission
        if current_user_id != user_id:
            # Check if user has permission to update other users
            admin_required(lambda: None)()
        
        # Validate request data
        data = user_update_schema.load(request.json, instance=user, partial=True)
        
        # Save changes to database
        db.session.commit()
        
        # Return updated user
        return success_response(user_schema.dump(data), 'User updated successfully')
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update user error: {str(e)}")
        return error_response('An error occurred while updating user', status_code=500)


@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """Delete user by ID."""
    try:
        # Find user
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('User not found')
        
        # Delete user from database
        db.session.delete(user)
        db.session.commit()
        
        # Return success message
        return success_response(message='User deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Delete user error: {str(e)}")
        return error_response('An error occurred while deleting user', status_code=500)


@user_bp.route('/<user_id>/roles', methods=['GET'])
@jwt_required()
@permission_required('user', 'read')
def get_user_roles(user_id):
    """Get user roles."""
    try:
        # Find user
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('User not found')
        
        # Get user roles
        user_roles = UserRole.query.filter_by(user_id=user_id).all()
        roles = []
        
        for user_role in user_roles:
            role = Role.query.get(user_role.role_id)
            if role:
                roles.append({
                    'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'organization_id': user_role.organization_id
                })
        
        # Return user roles
        return success_response(roles)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get user roles error: {str(e)}")
        return error_response('An error occurred while getting user roles', status_code=500)

