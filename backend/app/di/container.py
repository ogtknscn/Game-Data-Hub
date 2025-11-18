"""
Dependency Injection Container
Using dependency-injector library pattern (manual implementation)
Note: Repositories are created per-request with session from FastAPI dependency injection
"""
from typing import Dict, Any
from app.application.services.code_generation_service import CodeGenerationService


class Container:
    """
    Dependency Injection Container
    Manages service lifecycle and dependencies
    Note: Stateless services only - repositories are created per-request
    """
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._initialized = False
    
    def _init_services(self):
        """Initialize stateless services"""
        # Code generation service is stateless
        self._services['code_generation'] = CodeGenerationService()
    
    def initialize(self):
        """Initialize container"""
        if not self._initialized:
            self._init_services()
            self._initialized = True
    
    def get_service(self, service_name: str):
        """Get a service by name"""
        if not self._initialized:
            self.initialize()
        return self._services.get(service_name)
    
    def wire(self, modules=None):
        """Wire dependencies (for compatibility with dependency-injector pattern)"""
        self.initialize()


# Global container instance
container = Container()

