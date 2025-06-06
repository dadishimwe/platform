"""
Device routes for the Starlink Platform API.
"""
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from src.models import db
from src.models.device import Device, DeviceConfiguration, DeviceStatus, IpAllocation
from src.models.organization import Organization
from src.schemas.device import (
    device_schema, devices_schema, device_configuration_schema,
    device_configurations_schema, device_status_schema, device_statuses_schema,
    ip_allocation_schema, ip_allocations_schema
)
from src.utils.responses import success_response, error_response, pagination_response
from src.utils.error_handlers import NotFoundError, ValidationError as APIValidationError
from src.utils.auth import permission_required

device_bp = Blueprint('device', __name__)

@device_bp.route('', methods=['GET'])
@jwt_required()
@permission_required('device', 'read')
def get_devices():
    """Get all devices."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        organization_id = request.args.get('organization_id')
        device_type = request.args.get('device_type')
        is_active = request.args.get('is_active', type=bool)
        
        # Build query
        query = Device.query
        
        # Apply filters
        if organization_id:
            query = query.filter_by(organization_id=organization_id)
        
        if device_type:
            query = query.filter_by(device_type=device_type)
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        # Query devices with pagination
        pagination = query.paginate(page=page, per_page=per_page)
        
        # Return paginated devices
        return pagination_response(
            devices_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get devices error: {str(e)}")
        return error_response('An error occurred while getting devices', status_code=500)


@device_bp.route('/<device_id>', methods=['GET'])
@jwt_required()
@permission_required('device', 'read')
def get_device(device_id):
    """Get device by ID."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Return device
        return success_response(device_schema.dump(device))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get device error: {str(e)}")
        return error_response('An error occurred while getting device', status_code=500)


@device_bp.route('', methods=['POST'])
@jwt_required()
@permission_required('device', 'create')
def create_device():
    """Create a new device."""
    try:
        # Validate request data
        data = device_schema.load(request.json)
        
        # Check if organization exists
        organization = Organization.query.get(data.organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Check if device ID already exists
        existing = Device.query.filter_by(device_id=data.device_id).first()
        if existing:
            raise APIValidationError('Device ID already exists')
        
        # Save device to database
        db.session.add(data)
        db.session.commit()
        
        # Return created device
        return success_response(device_schema.dump(data), 'Device created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Create device error: {str(e)}")
        return error_response('An error occurred while creating device', status_code=500)


@device_bp.route('/<device_id>', methods=['PUT'])
@jwt_required()
@permission_required('device', 'update')
def update_device(device_id):
    """Update device by ID."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Validate request data
        data = device_schema.load(request.json, instance=device, partial=True)
        
        # Save changes to database
        db.session.commit()
        
        # Return updated device
        return success_response(device_schema.dump(data), 'Device updated successfully')
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update device error: {str(e)}")
        return error_response('An error occurred while updating device', status_code=500)


@device_bp.route('/<device_id>', methods=['DELETE'])
@jwt_required()
@permission_required('device', 'delete')
def delete_device(device_id):
    """Delete device by ID."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Delete device from database
        db.session.delete(device)
        db.session.commit()
        
        # Return success message
        return success_response(message='Device deleted successfully')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Delete device error: {str(e)}")
        return error_response('An error occurred while deleting device', status_code=500)


@device_bp.route('/<device_id>/configurations', methods=['GET'])
@jwt_required()
@permission_required('device', 'read')
def get_device_configurations(device_id):
    """Get device configurations."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Get device configurations
        configurations = DeviceConfiguration.query.filter_by(device_id=device_id).all()
        
        # Return device configurations
        return success_response(device_configurations_schema.dump(configurations))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get device configurations error: {str(e)}")
        return error_response('An error occurred while getting device configurations', status_code=500)


@device_bp.route('/<device_id>/configurations', methods=['POST'])
@jwt_required()
@permission_required('device', 'update')
def add_device_configuration(device_id):
    """Add configuration to device."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Validate request data
        data = device_configuration_schema.load(request.json)
        
        # Check if configuration key already exists for device
        existing = DeviceConfiguration.query.filter_by(
            device_id=device_id,
            config_key=data.config_key
        ).first()
        
        if existing:
            # Update existing configuration
            existing.config_value = data.config_value
            db.session.commit()
            return success_response(
                device_configuration_schema.dump(existing),
                'Device configuration updated successfully'
            )
        
        # Set device ID
        data.device_id = device_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            device_configuration_schema.dump(data),
            'Device configuration added successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Add device configuration error: {str(e)}")
        return error_response('An error occurred while adding device configuration', status_code=500)


@device_bp.route('/<device_id>/status', methods=['GET'])
@jwt_required()
@permission_required('device', 'read')
def get_device_status(device_id):
    """Get device status."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Get device status
        status = DeviceStatus.query.filter_by(device_id=device_id).first()
        if not status:
            return success_response(None)
        
        # Return device status
        return success_response(device_status_schema.dump(status))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get device status error: {str(e)}")
        return error_response('An error occurred while getting device status', status_code=500)


@device_bp.route('/<device_id>/status', methods=['POST'])
@jwt_required()
@permission_required('device', 'update')
def update_device_status(device_id):
    """Update device status."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Validate request data
        data = device_status_schema.load(request.json)
        
        # Check if status already exists for device
        status = DeviceStatus.query.filter_by(device_id=device_id).first()
        
        if status:
            # Update existing status
            status.status = data.status
            status.details = data.details
            db.session.commit()
            return success_response(
                device_status_schema.dump(status),
                'Device status updated successfully'
            )
        
        # Set device ID
        data.device_id = device_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            device_status_schema.dump(data),
            'Device status added successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update device status error: {str(e)}")
        return error_response('An error occurred while updating device status', status_code=500)


@device_bp.route('/<device_id>/ip-allocations', methods=['GET'])
@jwt_required()
@permission_required('device', 'read')
def get_device_ip_allocations(device_id):
    """Get device IP allocations."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Get device IP allocations
        ip_allocations = IpAllocation.query.filter_by(device_id=device_id).all()
        
        # Return device IP allocations
        return success_response(ip_allocations_schema.dump(ip_allocations))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get device IP allocations error: {str(e)}")
        return error_response('An error occurred while getting device IP allocations', status_code=500)


@device_bp.route('/<device_id>/ip-allocations', methods=['POST'])
@jwt_required()
@permission_required('device', 'update')
def add_device_ip_allocation(device_id):
    """Add IP allocation to device."""
    try:
        # Find device
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundError('Device not found')
        
        # Validate request data
        data = ip_allocation_schema.load(request.json)
        
        # Set device ID
        data.device_id = device_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            ip_allocation_schema.dump(data),
            'Device IP allocation added successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Add device IP allocation error: {str(e)}")
        return error_response('An error occurred while adding device IP allocation', status_code=500)

