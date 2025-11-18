"""
Custom exception classes
"""
from typing import Optional


class GDHException(Exception):
    """Base exception for GDH application"""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(GDHException):
    """Resource not found exception"""
    
    def __init__(self, resource: str, identifier: Optional[str] = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=404)


class ValidationError(GDHException):
    """Validation error exception"""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class UnauthorizedError(GDHException):
    """Unauthorized access exception"""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenError(GDHException):
    """Forbidden access exception"""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class ConflictError(GDHException):
    """Resource conflict exception"""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=409)

