"""
Organization routes for the Starlink Platform API.
"""
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from src.models import db
from src.models.organization import Organization, OrganizationUser, ServicePlan, OrganizationServicePlan
from src.models.user import User, UserRole
from src.schemas.organization import (
    organization_schema, organizations_schema, organization_user_schema,
    organization_users_schema, service_plan_schema, service_plans_schema,
    organization_service_plan_schema, organization_service_plans_schema
)
from src.utils.responses import success_response, error_response, pagination_response
from src.utils.error_handlers import NotFoundError, ValidationError as APIValidationError
from src.utils.auth import admin_required, permission_required

organization_bp = Blueprint('organization', __name__)

@organization_bp.route('', methods=['GET'])
@jwt_required()
@permission_required('organization', 'read')
def get_organizations():
    """Get all organizations."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Query organizations with pagination
        pagination = Organization.query.paginate(page=page, per_page=per_page)
        
        # Return paginated organizations
        return pagination_response(
            organizations_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get organizations error: {str(e)}")
        return error_response('An error occurred while getting organizations', status_code=500)


@organization_bp.route('/<organization_id>', methods=['GET'])
@jwt_required()
@permission_required('organization', 'read')
def get_organization(organization_id):
    """Get organization by ID."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Return organization
        return success_response(organization_schema.dump(organization))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get organization error: {str(e)}")
        return error_response('An error occurred while getting organization', status_code=500)


@organization_bp.route('', methods=['POST'])
@jwt_required()
@permission_required('organization', 'create')
def create_organization():
    """Create a new organization."""
    try:
        # Validate request data
        data = organization_schema.load(request.json)
        
        # Save organization to database
        db.session.add(data)
        db.session.commit()
        
        # Return created organization
        return success_response(organization_schema.dump(data), 'Organization created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except Exception as e:
        current_app.logger.error(f"Create organization error: {str(e)}")
        return error_response('An error occurred while creating organization', status_code=500)


@organization_bp.route('/<organization_id>', methods=['PUT'])
@jwt_required()
@permission_required('organization', 'update')
def update_organization(organization_id):
    """Update organization by ID."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Validate request data
        data = organization_schema.load(request.json, instance=organization, partial=True)
        
        # Save changes to database
        db.session.commit()
        
        # Return updated organization
        return success_response(organization_schema.dump(data), 'Organization updated successfully')
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update organization error: {str(e)}")
        return error_response('An error occurred while updating organization', status_code=500)


@organization_bp.route('/<organization_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_organization(organization_id):
    """Delete organization by ID."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Delete organization from database
        db.session.delete(organization)
        db.session.commit()
        
        # Return success message
        return success_response(message='Organization deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Delete organization error: {str(e)}")
        return error_response('An error occurred while deleting organization', status_code=500)


@organization_bp.route('/<organization_id>/users', methods=['GET'])
@jwt_required()
@permission_required('organization', 'read')
def get_organization_users(organization_id):
    """Get organization users."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Get organization users
        organization_users = OrganizationUser.query.filter_by(organization_id=organization_id).all()
        
        # Return organization users
        return success_response(organization_users_schema.dump(organization_users))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get organization users error: {str(e)}")
        return error_response('An error occurred while getting organization users', status_code=500)


@organization_bp.route('/<organization_id>/users', methods=['POST'])
@jwt_required()
@permission_required('organization', 'update')
def add_organization_user(organization_id):
    """Add user to organization."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Validate request data
        data = organization_user_schema.load(request.json)
        
        # Check if user exists
        user = User.query.get(data.user_id)
        if not user:
            raise NotFoundError('User not found')
        
        # Check if user is already in organization
        existing = OrganizationUser.query.filter_by(
            organization_id=organization_id,
            user_id=data.user_id
        ).first()
        
        if existing:
            raise APIValidationError('User is already in organization')
        
        # Set organization ID
        data.organization_id = organization_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            organization_user_schema.dump(data),
            'User added to organization successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Add organization user error: {str(e)}")
        return error_response('An error occurred while adding user to organization', status_code=500)


@organization_bp.route('/<organization_id>/users/<user_id>', methods=['DELETE'])
@jwt_required()
@permission_required('organization', 'update')
def remove_organization_user(organization_id, user_id):
    """Remove user from organization."""
    try:
        # Find organization user
        organization_user = OrganizationUser.query.filter_by(
            organization_id=organization_id,
            user_id=user_id
        ).first()
        
        if not organization_user:
            raise NotFoundError('User not found in organization')
        
        # Delete organization user from database
        db.session.delete(organization_user)
        db.session.commit()
        
        # Return success message
        return success_response(message='User removed from organization successfully')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Remove organization user error: {str(e)}")
        return error_response('An error occurred while removing user from organization', status_code=500)


@organization_bp.route('/<organization_id>/service-plans', methods=['GET'])
@jwt_required()
@permission_required('organization', 'read')
def get_organization_service_plans(organization_id):
    """Get organization service plans."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Get organization service plans
        organization_service_plans = OrganizationServicePlan.query.filter_by(organization_id=organization_id).all()
        
        # Return organization service plans
        return success_response(organization_service_plans_schema.dump(organization_service_plans))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get organization service plans error: {str(e)}")
        return error_response('An error occurred while getting organization service plans', status_code=500)


@organization_bp.route('/<organization_id>/service-plans', methods=['POST'])
@jwt_required()
@permission_required('organization', 'update')
def add_organization_service_plan(organization_id):
    """Add service plan to organization."""
    try:
        # Find organization
        organization = Organization.query.get(organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Validate request data
        data = organization_service_plan_schema.load(request.json)
        
        # Check if service plan exists
        service_plan = ServicePlan.query.get(data.service_plan_id)
        if not service_plan:
            raise NotFoundError('Service plan not found')
        
        # Check if service plan is already assigned to organization
        existing = OrganizationServicePlan.query.filter_by(
            organization_id=organization_id,
            service_plan_id=data.service_plan_id
        ).first()
        
        if existing:
            raise APIValidationError('Service plan is already assigned to organization')
        
        # Set organization ID
        data.organization_id = organization_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            organization_service_plan_schema.dump(data),
            'Service plan added to organization successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Add organization service plan error: {str(e)}")
        return error_response('An error occurred while adding service plan to organization', status_code=500)

