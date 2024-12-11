"""Error handlers and custom exceptions for CLARA application."""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from .logger import logger

class CLARAException(Exception):
    """Base exception class for CLARA application."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert exception to dictionary for JSON response."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

class ValidationError(CLARAException):
    """Raised when input validation fails."""
    pass

class SecurityCheckError(CLARAException):
    """Raised when a security check fails."""
    pass

def register_error_handlers(app):
    """Register error handlers with the Flask application."""
    
    @app.errorhandler(CLARAException)
    def handle_clara_exception(error):
        """Handle custom CLARA exceptions."""
        logger.error("CLARA exception occurred", 
                    error_type=type(error).__name__,
                    message=error.message,
                    status_code=error.status_code)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle HTTP exceptions."""
        logger.error("HTTP exception occurred",
                    error_type=type(error).__name__,
                    description=error.description,
                    code=error.code)
        response = jsonify({
            'message': error.description,
            'status_code': error.code
        })
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle any unhandled exceptions."""
        logger.error("Unhandled exception occurred",
                    error_type=type(error).__name__,
                    error=str(error))
        response = jsonify({
            'message': 'An unexpected error occurred',
            'status_code': 500
        })
        response.status_code = 500
        return response

    # Register handlers for common HTTP status codes
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        logger.warning("Resource not found", path=error.description)
        return jsonify({
            'message': 'Resource not found',
            'status_code': 404
        }), 404

    @app.errorhandler(429)
    def ratelimit_error(error):
        """Handle rate limit exceeded errors."""
        logger.warning("Rate limit exceeded", description=error.description)
        return jsonify({
            'message': 'Rate limit exceeded. Please try again later.',
            'status_code': 429
        }), 429
