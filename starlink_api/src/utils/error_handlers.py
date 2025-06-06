"""
Error handling utilities for the Starlink Platform API.
"""
from flask import jsonify

class APIError(Exception):
    """Base class for API errors."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Convert error to dictionary."""
        error_dict = dict(self.payload or ())
        error_dict['message'] = self.message
        error_dict['status'] = 'error'
        return error_dict


class NotFoundError(APIError):
    """Resource not found error."""
    def __init__(self, message="Resource not found", payload=None):
        super().__init__(message, 404, payload)


class ValidationError(APIError):
    """Validation error."""
    def __init__(self, message="Validation error", payload=None):
        super().__init__(message, 400, payload)


class AuthenticationError(APIError):
    """Authentication error."""
    def __init__(self, message="Authentication error", payload=None):
        super().__init__(message, 401, payload)


class AuthorizationError(APIError):
    """Authorization error."""
    def __init__(self, message="Authorization error", payload=None):
        super().__init__(message, 403, payload)


class RateLimitError(APIError):
    """Rate limit error."""
    def __init__(self, message="Rate limit exceeded", payload=None):
        super().__init__(message, 429, payload)


class ServerError(APIError):
    """Server error."""
    def __init__(self, message="Internal server error", payload=None):
        super().__init__(message, 500, payload)


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle API errors."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Bad request'
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized'
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Forbidden'
        }), 403
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed'
        }), 405
    
    @app.errorhandler(429)
    def handle_rate_limit_exceeded(error):
        """Handle 429 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Rate limit exceeded'
        }), 429
    
    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Handle 500 errors."""
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

