"""
Service providers for dependency injection
"""
from app.di.container import container


def get_auth_service():
    """Get auth service"""
    return container.get_service('auth')


def get_project_service():
    """Get project service"""
    return container.get_service('project')


def get_table_service():
    """Get table service"""
    return container.get_service('table')


def get_data_service():
    """Get data service"""
    return container.get_service('data')


def get_version_service():
    """Get version service"""
    return container.get_service('version')


def get_code_generation_service():
    """Get code generation service"""
    return container.get_service('code_generation')

