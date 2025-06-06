"""
Notification routes for the Starlink Platform API.
"""
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime
from src.models import db
from src.models.notification import (
    NotificationTemplate, Notification, AlertConfiguration,
    AlertNotification, NotificationPreference
)
from src.models.device import Device
from src.models.organization import Organization
from src.schemas.notification import (
    notification_template_schema, notification_templates_schema,
    notification_schema, notifications_schema,
    alert_configuration_schema, alert_configurations_schema,
    alert_notification_schema, alert_notifications_schema,
    notification_preference_schema, notification_preferences_schema
)
from src.utils.responses import success_response, error_response, pagination_response
from src.utils.error_handlers import NotFoundError, ValidationError as APIValidationError
from src.utils.auth import permission_required

notification_bp = Blueprint('notification', __name__)

# Notification routes
@notification_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_notifications():
    """Get notifications for current user."""
    try:
        # Get current user ID from token
        user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        is_read = request.args.get('is_read', type=bool)
        
        # Build query
        query = Notification.query.filter_by(user_id=user_id)
        
        # Apply filters
        if is_read is not None:
            query = query.filter_by(is_read=is_read)
        
        # Query notifications with pagination
        pagination = query.order_by(Notification.created_at.desc()).paginate(page=page, per_page=per_page)
        
        # Return paginated notifications
        return pagination_response(
            notifications_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get user notifications error: {str(e)}")
        return error_response('An error occurred while getting notifications', status_code=500)


@notification_bp.route('/user/<notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read."""
    try:
        # Get current user ID from token
        user_id = get_jwt_identity()
        
        # Find notification
        notification = Notification.query.get(notification_id)
        if not notification:
            raise NotFoundError('Notification not found')
        
        # Check if notification belongs to current user
        if notification.user_id != user_id:
            return error_response('Notification does not belong to current user', status_code=403)
        
        # Mark notification as read
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.session.commit()
        
        # Return success message
        return success_response(message='Notification marked as read')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Mark notification read error: {str(e)}")
        return error_response('An error occurred while marking notification as read', status_code=500)


@notification_bp.route('/user/read-all', methods=['POST'])
@jwt_required()
def mark_all_notifications_read():
    """Mark all notifications as read."""
    try:
        # Get current user ID from token
        user_id = get_jwt_identity()
        
        # Get unread notifications for current user
        unread_notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
        
        # Mark all as read
        now = datetime.utcnow()
        for notification in unread_notifications:
            notification.is_read = True
            notification.read_at = now
        
        db.session.commit()
        
        # Return success message
        return success_response(message=f'Marked {len(unread_notifications)} notifications as read')
    
    except Exception as e:
        current_app.logger.error(f"Mark all notifications read error: {str(e)}")
        return error_response('An error occurred while marking notifications as read', status_code=500)


# Notification Template routes
@notification_bp.route('/templates', methods=['GET'])
@jwt_required()
@permission_required('notification', 'read')
def get_notification_templates():
    """Get all notification templates."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        type = request.args.get('type')
        
        # Build query
        query = NotificationTemplate.query
        
        # Apply filters
        if type:
            query = query.filter_by(type=type)
        
        # Query templates with pagination
        pagination = query.paginate(page=page, per_page=per_page)
        
        # Return paginated templates
        return pagination_response(
            notification_templates_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get notification templates error: {str(e)}")
        return error_response('An error occurred while getting notification templates', status_code=500)


@notification_bp.route('/templates/<template_id>', methods=['GET'])
@jwt_required()
@permission_required('notification', 'read')
def get_notification_template(template_id):
    """Get notification template by ID."""
    try:
        # Find template
        template = NotificationTemplate.query.get(template_id)
        if not template:
            raise NotFoundError('Notification template not found')
        
        # Return template
        return success_response(notification_template_schema.dump(template))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get notification template error: {str(e)}")
        return error_response('An error occurred while getting notification template', status_code=500)


@notification_bp.route('/templates', methods=['POST'])
@jwt_required()
@permission_required('notification', 'create')
def create_notification_template():
    """Create a new notification template."""
    try:
        # Validate request data
        data = notification_template_schema.load(request.json)
        
        # Check if template name already exists
        existing = NotificationTemplate.query.filter_by(name=data.name).first()
        if existing:
            raise APIValidationError('Template name already exists')
        
        # Save template to database
        db.session.add(data)
        db.session.commit()
        
        # Return created template
        return success_response(
            notification_template_schema.dump(data),
            'Notification template created successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Create notification template error: {str(e)}")
        return error_response('An error occurred while creating notification template', status_code=500)


@notification_bp.route('/templates/<template_id>', methods=['PUT'])
@jwt_required()
@permission_required('notification', 'update')
def update_notification_template(template_id):
    """Update notification template by ID."""
    try:
        # Find template
        template = NotificationTemplate.query.get(template_id)
        if not template:
            raise NotFoundError('Notification template not found')
        
        # Validate request data
        data = notification_template_schema.load(request.json, instance=template, partial=True)
        
        # Check if template name already exists if changed
        if 'name' in request.json and request.json['name'] != template.name:
            existing = NotificationTemplate.query.filter_by(name=data.name).first()
            if existing:
                raise APIValidationError('Template name already exists')
        
        # Save changes to database
        db.session.commit()
        
        # Return updated template
        return success_response(
            notification_template_schema.dump(data),
            'Notification template updated successfully'
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Update notification template error: {str(e)}")
        return error_response('An error occurred while updating notification template', status_code=500)


# Alert Configuration routes
@notification_bp.route('/alert-configs', methods=['GET'])
@jwt_required()
@permission_required('notification', 'read')
def get_alert_configurations():
    """Get alert configurations."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        organization_id = request.args.get('organization_id')
        device_id = request.args.get('device_id')
        alert_type = request.args.get('alert_type')
        enabled = request.args.get('enabled', type=bool)
        
        # Build query
        query = AlertConfiguration.query
        
        # Apply filters
        if organization_id:
            query = query.filter_by(organization_id=organization_id)
        
        if device_id:
            query = query.filter_by(device_id=device_id)
        
        if alert_type:
            query = query.filter_by(alert_type=alert_type)
        
        if enabled is not None:
            query = query.filter_by(enabled=enabled)
        
        # Query configurations with pagination
        pagination = query.paginate(page=page, per_page=per_page)
        
        # Return paginated configurations
        return pagination_response(
            alert_configurations_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get alert configurations error: {str(e)}")
        return error_response('An error occurred while getting alert configurations', status_code=500)


@notification_bp.route('/alert-configs/<config_id>', methods=['GET'])
@jwt_required()
@permission_required('notification', 'read')
def get_alert_configuration(config_id):
    """Get alert configuration by ID."""
    try:
        # Find configuration
        config = AlertConfiguration.query.get(config_id)
        if not config:
            raise NotFoundError('Alert configuration not found')
        
        # Return configuration
        return success_response(alert_configuration_schema.dump(config))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get alert configuration error: {str(e)}")
        return error_response('An error occurred while getting alert configuration', status_code=500)


@notification_bp.route('/alert-configs', methods=['POST'])
@jwt_required()
@permission_required('notification', 'create')
def create_alert_configuration():
    """Create a new alert configuration."""
    try:
        # Validate request data
        data = alert_configuration_schema.load(request.json)
        
        # Check if organization exists
        organization = Organization.query.get(data.organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Check if device exists if provided
        if data.device_id:
            device = Device.query.get(data.device_id)
            if not device:
                raise NotFoundError('Device not found')
        
        # Save configuration to database
        db.session.add(data)
        db.session.commit()
        
        # Return created configuration
        return success_response(
            alert_configuration_schema.dump(data),
            'Alert configuration created successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Create alert configuration error: {str(e)}")
        return error_response('An error occurred while creating alert configuration', status_code=500)


@notification_bp.route('/alert-configs/<config_id>', methods=['PUT'])
@jwt_required()
@permission_required('notification', 'update')
def update_alert_configuration(config_id):
    """Update alert configuration by ID."""
    try:
        # Find configuration
        config = AlertConfiguration.query.get(config_id)
        if not config:
            raise NotFoundError('Alert configuration not found')
        
        # Validate request data
        data = alert_configuration_schema.load(request.json, instance=config, partial=True)
        
        # Check if device exists if provided
        if 'device_id' in request.json and data.device_id:
            device = Device.query.get(data.device_id)
            if not device:
                raise NotFoundError('Device not found')
        
        # Save changes to database
        db.session.commit()
        
        # Return updated configuration
        return success_response(
            alert_configuration_schema.dump(data),
            'Alert configuration updated successfully'
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update alert configuration error: {str(e)}")
        return error_response('An error occurred while updating alert configuration', status_code=500)


@notification_bp.route('/alert-configs/<config_id>', methods=['DELETE'])
@jwt_required()
@permission_required('notification', 'delete')
def delete_alert_configuration(config_id):
    """Delete alert configuration by ID."""
    try:
        # Find configuration
        config = AlertConfiguration.query.get(config_id)
        if not config:
            raise NotFoundError('Alert configuration not found')
        
        # Delete configuration from database
        db.session.delete(config)
        db.session.commit()
        
        # Return success message
        return success_response(message='Alert configuration deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Delete alert configuration error: {str(e)}")
        return error_response('An error occurred while deleting alert configuration', status_code=500)


# Notification Preference routes
@notification_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    """Get notification preferences for current user."""
    try:
        # Get current user ID from token
        user_id = get_jwt_identity()
        
        # Get notification preferences
        preferences = NotificationPreference.query.filter_by(user_id=user_id).all()
        
        # Return preferences
        return success_response(notification_preferences_schema.dump(preferences))
    
    except Exception as e:
        current_app.logger.error(f"Get notification preferences error: {str(e)}")
        return error_response('An error occurred while getting notification preferences', status_code=500)


@notification_bp.route('/preferences/<notification_type>', methods=['PUT'])
@jwt_required()
def update_notification_preference(notification_type):
    """Update notification preference."""
    try:
        # Get current user ID from token
        user_id = get_jwt_identity()
        
        # Find preference
        preference = NotificationPreference.query.filter_by(
            user_id=user_id,
            notification_type=notification_type
        ).first()
        
        if not preference:
            # Create new preference
            preference = NotificationPreference(
                user_id=user_id,
                notification_type=notification_type
            )
            db.session.add(preference)
        
        # Update preference
        if 'email_enabled' in request.json:
            preference.email_enabled = request.json['email_enabled']
        
        if 'push_enabled' in request.json:
            preference.push_enabled = request.json['push_enabled']
        
        if 'in_app_enabled' in request.json:
            preference.in_app_enabled = request.json['in_app_enabled']
        
        # Save changes to database
        db.session.commit()
        
        # Return updated preference
        return success_response(
            notification_preference_schema.dump(preference),
            'Notification preference updated successfully'
        )
    
    except Exception as e:
        current_app.logger.error(f"Update notification preference error: {str(e)}")
        return error_response('An error occurred while updating notification preference', status_code=500)

