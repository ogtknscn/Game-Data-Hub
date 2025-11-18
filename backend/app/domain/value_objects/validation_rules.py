"""
Validation rules value objects
"""
from typing import Optional, Callable, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationRule:
    """Immutable validation rule"""
    name: str
    validator: Callable[[Any], bool]
    error_message: str
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate a value
        Returns: (is_valid, error_message)
        """
        try:
            if self.validator(value):
                return True, None
            else:
                return False, self.error_message
        except Exception as e:
            return False, f"Validation error: {str(e)}"


class ValidationRuleSet:
    """Collection of validation rules"""
    
    def __init__(self):
        self._rules: list[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule):
        """Add a validation rule"""
        self._rules.append(rule)
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate value against all rules
        Returns: (is_valid, first_error_message)
        """
        for rule in self._rules:
            is_valid, error = rule.validate(value)
            if not is_valid:
                return False, error
        return True, None

