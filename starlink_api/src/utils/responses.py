"""
Response utilities for the Starlink Platform API.
"""
from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    """Create a success response."""
    response = {
        'status': 'success'
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message, status_code=400, errors=None):
    """Create an error response."""
    response = {
        'status': 'error',
        'message': message
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code


def pagination_response(data, page, per_page, total):
    """Create a paginated response."""
    return success_response({
        'items': data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

