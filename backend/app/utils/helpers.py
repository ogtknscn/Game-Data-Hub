"""
General helper functions
"""
from typing import Any, Dict


def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary"""
    return dictionary.get(key, default)


def truncate_string(value: str, max_length: int = 100) -> str:
    """Truncate string to max length"""
    if len(value) <= max_length:
        return value
    return value[:max_length - 3] + "..."

