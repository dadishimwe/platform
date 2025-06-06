"""
Telemetry routes for the Starlink Platform API.
"""
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import func
from src.models import db
from src.models.device import Device
from src.models.organization import Organization
from src.models.telemetry import UserTerminalTelemetry, RouterTelemetry, Alert
from src.schemas.telemetry import (
    user_terminal_telemetry_schema, user_terminal_telemetries_schema,
    router_telemetry_schema, router_telemetries_schema,
    alert_schema, alerts_schema
)
from src.utils.responses import success_response, error_response, pagination_response
from src.utils.error_handlers import NotFoundError
from src.utils.auth import permission_required
from src.utils.starlink_api import StarlinkAPI

telemetry_bp = Blueprint('telemetry', __name__)

@telemetry_bp.route('/user-terminals', methods=['GET'])
@jwt_required()
@permission_required('telemetry', 'read')
def get_user_terminal_telemetry():
    """Get user terminal telemetry data."""
    try:
        # Get query parameters
        device_id = request.args.get('device_id')
        organization_id = request.args.get('organization_id')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        limit = min(request.args.get('limit', 100, type=int), 1000)
        
        # Build query
        query = UserTerminalTelemetry.query
        
        # Apply filters
        if device_id:
            query = query.filter_by(device_id=device_id)
        
        if organization_id:
            query = query.join(Device).filter(Device.organization_id == organization_id)
        
        if start_time:
            try:
                start_datetime = datetime.fromisoformat(start_time)
                query = query.filter(UserTerminalTelemetry.time >= start_datetime)
            except ValueError:
                return error_response('Invalid start_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)', status_code=400)
        
        if end_time:
            try:
                end_datetime = datetime.fromisoformat(end_time)
                query = query.filter(UserTerminalTelemetry.time <= end_datetime)
            except ValueError:
                return error_response('Invalid end_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)', status_code=400)
        
        # Order by time descending and limit results
        telemetry_data = query.order_by(UserTerminalTelemetry.time.desc()).limit(limit).all()
        
        # Return telemetry data
        return success_response(user_terminal_telemetries_schema.dump(telemetry_data))
    
    except Exception as e:
        current_app.logger.error(f"Get user terminal telemetry error: {str(e)}")
        return error_response('An error occurred while getting user terminal telemetry', status_code=500)


@telemetry_bp.route('/routers', methods=['GET'])
@jwt_required()
@permission_required('telemetry', 'read')
def get_router_telemetry():
    """Get router telemetry data."""
    try:
        # Get query parameters
        device_id = request.args.get('device_id')
        organization_id = request.args.get('organization_id')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        limit = min(request.args.get('limit', 100, type=int), 1000)
        
        # Build query
        query = RouterTelemetry.query
        
        # Apply filters
        if device_id:
            query = query.filter_by(device_id=device_id)
        
        if organization_id:
            query = query.join(Device).filter(Device.organization_id == organization_id)
        
        if start_time:
            try:
                start_datetime = datetime.fromisoformat(start_time)
                query = query.filter(RouterTelemetry.time >= start_datetime)
            except ValueError:
                return error_response('Invalid start_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)', status_code=400)
        
        if end_time:
            try:
                end_datetime = datetime.fromisoformat(end_time)
                query = query.filter(RouterTelemetry.time <= end_datetime)
            except ValueError:
                return error_response('Invalid end_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)', status_code=400)
        
        # Order by time descending and limit results
        telemetry_data = query.order_by(RouterTelemetry.time.desc()).limit(limit).all()
        
        # Return telemetry data
        return success_response(router_telemetries_schema.dump(telemetry_data))
    
    except Exception as e:
        current_app.logger.error(f"Get router telemetry error: {str(e)}")
        return error_response('An error occurred while getting router telemetry', status_code=500)


@telemetry_bp.route('/alerts', methods=['GET'])
@jwt_required()
@permission_required('telemetry', 'read')
def get_alerts():
    """Get alerts."""
    try:
        # Get query parameters
        device_id = request.args.get('device_id')
        organization_id = request.args.get('organization_id')
        is_active = request.args.get('is_active', type=bool)
        severity = request.args.get('severity')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Build query
        query = Alert.query
        
        # Apply filters
        if device_id:
            query = query.filter_by(device_id=device_id)
        
        if organization_id:
            query = query.join(Device).filter(Device.organization_id == organization_id)
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        if severity:
            query = query.filter_by(severity=severity)
        
        # Query alerts with pagination
        pagination = query.order_by(Alert.start_time.desc()).paginate(page=page, per_page=per_page)
        
        # Return paginated alerts
        return pagination_response(
            alerts_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get alerts error: {str(e)}")
        return error_response('An error occurred while getting alerts', status_code=500)


@telemetry_bp.route('/alerts/<alert_id>', methods=['GET'])
@jwt_required()
@permission_required('telemetry', 'read')
def get_alert(alert_id):
    """Get alert by ID."""
    try:
        # Find alert
        alert = Alert.query.get(alert_id)
        if not alert:
            raise NotFoundError('Alert not found')
        
        # Return alert
        return success_response(alert_schema.dump(alert))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get alert error: {str(e)}")
        return error_response('An error occurred while getting alert', status_code=500)


@telemetry_bp.route('/sync', methods=['POST'])
@jwt_required()
@permission_required('telemetry', 'create')
def sync_telemetry():
    """Sync telemetry data from Starlink API."""
    try:
        # Get request data
        data = request.json
        account_number = data.get('account_number')
        
        if not account_number:
            return error_response('Account number is required', status_code=400)
        
        # Initialize Starlink API client
        starlink_api = StarlinkAPI()
        
        # Get telemetry data from Starlink API
        telemetry_data = starlink_api.get_telemetry(account_number)
        if not telemetry_data:
            return error_response('Failed to get telemetry data from Starlink API', status_code=500)
        
        # Process telemetry data
        processed_data = starlink_api.process_telemetry_data(telemetry_data)
        if not processed_data:
            return error_response('Failed to process telemetry data', status_code=500)
        
        # Extract data
        data_rows = processed_data['data']
        metadata = processed_data['metadata']
        
        # Process each row of data
        user_terminal_count = 0
        router_count = 0
        ip_allocation_count = 0
        
        for row in data_rows:
            device_type = row.get('DeviceType')
            
            if device_type == 'u':  # User Terminal
                # Process user terminal telemetry
                user_terminal_count += 1
            
            elif device_type == 'r':  # Router
                # Process router telemetry
                router_count += 1
            
            elif device_type == 'i':  # IP Allocation
                # Process IP allocation
                ip_allocation_count += 1
        
        # Return success message
        return success_response({
            'user_terminal_count': user_terminal_count,
            'router_count': router_count,
            'ip_allocation_count': ip_allocation_count
        }, 'Telemetry data synced successfully')
    
    except Exception as e:
        current_app.logger.error(f"Sync telemetry error: {str(e)}")
        return error_response('An error occurred while syncing telemetry data', status_code=500)


@telemetry_bp.route('/stats/usage', methods=['GET'])
@jwt_required()
@permission_required('telemetry', 'read')
def get_usage_stats():
    """Get usage statistics."""
    try:
        # Get query parameters
        device_id = request.args.get('device_id')
        organization_id = request.args.get('organization_id')
        period = request.args.get('period', 'day')  # day, week, month
        
        if not device_id and not organization_id:
            return error_response('Either device_id or organization_id is required', status_code=400)
        
        # Determine time range based on period
        end_time = datetime.utcnow()
        if period == 'day':
            start_time = end_time - timedelta(days=1)
        elif period == 'week':
            start_time = end_time - timedelta(weeks=1)
        elif period == 'month':
            start_time = end_time - timedelta(days=30)
        else:
            return error_response('Invalid period. Use day, week, or month', status_code=400)
        
        # Build query for router telemetry
        query = db.session.query(
            func.sum(RouterTelemetry.wan_tx_bytes).label('total_tx_bytes'),
            func.sum(RouterTelemetry.wan_rx_bytes).label('total_rx_bytes')
        )
        
        # Apply filters
        if device_id:
            query = query.filter(RouterTelemetry.device_id == device_id)
        
        if organization_id:
            query = query.join(Device).filter(Device.organization_id == organization_id)
        
        # Filter by time range
        query = query.filter(RouterTelemetry.time.between(start_time, end_time))
        
        # Execute query
        result = query.first()
        
        # Calculate total usage
        total_tx_bytes = result.total_tx_bytes or 0
        total_rx_bytes = result.total_rx_bytes or 0
        total_bytes = total_tx_bytes + total_rx_bytes
        
        # Convert to GB
        total_tx_gb = total_tx_bytes / (1024 * 1024 * 1024)
        total_rx_gb = total_rx_bytes / (1024 * 1024 * 1024)
        total_gb = total_bytes / (1024 * 1024 * 1024)
        
        # Return usage statistics
        return success_response({
            'period': period,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'upload_bytes': total_tx_bytes,
            'download_bytes': total_rx_bytes,
            'total_bytes': total_bytes,
            'upload_gb': round(total_tx_gb, 2),
            'download_gb': round(total_rx_gb, 2),
            'total_gb': round(total_gb, 2)
        })
    
    except Exception as e:
        current_app.logger.error(f"Get usage stats error: {str(e)}")
        return error_response('An error occurred while getting usage statistics', status_code=500)


@telemetry_bp.route('/stats/performance', methods=['GET'])
@jwt_required()
@permission_required('telemetry', 'read')
def get_performance_stats():
    """Get performance statistics."""
    try:
        # Get query parameters
        device_id = request.args.get('device_id')
        organization_id = request.args.get('organization_id')
        period = request.args.get('period', 'day')  # day, week, month
        
        if not device_id and not organization_id:
            return error_response('Either device_id or organization_id is required', status_code=400)
        
        # Determine time range based on period
        end_time = datetime.utcnow()
        if period == 'day':
            start_time = end_time - timedelta(days=1)
        elif period == 'week':
            start_time = end_time - timedelta(weeks=1)
        elif period == 'month':
            start_time = end_time - timedelta(days=30)
        else:
            return error_response('Invalid period. Use day, week, or month', status_code=400)
        
        # Build query for user terminal telemetry
        query = db.session.query(
            func.avg(UserTerminalTelemetry.downlink_throughput).label('avg_downlink_throughput'),
            func.avg(UserTerminalTelemetry.uplink_throughput).label('avg_uplink_throughput'),
            func.avg(UserTerminalTelemetry.ping_latency_ms_avg).label('avg_ping_latency'),
            func.avg(UserTerminalTelemetry.ping_drop_rate_avg).label('avg_ping_drop_rate'),
            func.avg(UserTerminalTelemetry.obstruction_percent_time).label('avg_obstruction_percent'),
            func.avg(UserTerminalTelemetry.signal_quality).label('avg_signal_quality')
        )
        
        # Apply filters
        if device_id:
            query = query.filter(UserTerminalTelemetry.device_id == device_id)
        
        if organization_id:
            query = query.join(Device).filter(Device.organization_id == organization_id)
        
        # Filter by time range
        query = query.filter(UserTerminalTelemetry.time.between(start_time, end_time))
        
        # Execute query
        result = query.first()
        
        # Return performance statistics
        return success_response({
            'period': period,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'avg_downlink_throughput': round(result.avg_downlink_throughput or 0, 2),
            'avg_uplink_throughput': round(result.avg_uplink_throughput or 0, 2),
            'avg_ping_latency': round(result.avg_ping_latency or 0, 2),
            'avg_ping_drop_rate': round(result.avg_ping_drop_rate or 0, 4),
            'avg_obstruction_percent': round(result.avg_obstruction_percent or 0, 2),
            'avg_signal_quality': round(result.avg_signal_quality or 0, 2)
        })
    
    except Exception as e:
        current_app.logger.error(f"Get performance stats error: {str(e)}")
        return error_response('An error occurred while getting performance statistics', status_code=500)

