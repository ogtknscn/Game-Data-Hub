"""
General validation utilities
"""
from typing import Any


def validate_not_empty(value: Any, field_name: str) -> None:
    """Validate that value is not empty"""
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"{field_name} cannot be empty")


def validate_positive_integer(value: Any, field_name: str) -> None:
    """Validate that value is a positive integer"""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

