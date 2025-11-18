"""
Data type value objects
Immutable value objects for data type definitions
"""
from enum import Enum
from typing import List, Optional, Any


class DataType(Enum):
    """Supported data types"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ENUM = "enum"
    REFERENCE = "reference"
    
    @classmethod
    def from_string(cls, value: str) -> 'DataType':
        """Convert string to DataType"""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid data type: {value}")


class DataTypeDefinition:
    """Immutable data type definition value object"""
    
    def __init__(
        self,
        data_type: DataType,
        enum_values: Optional[List[str]] = None,
        reference_table_id: Optional[int] = None
    ):
        self._data_type = data_type
        self._enum_values = tuple(enum_values) if enum_values else None
        self._reference_table_id = reference_table_id
        self._validate()
    
    def _validate(self):
        """Validate data type definition"""
        if self._data_type == DataType.ENUM and not self._enum_values:
            raise ValueError("Enum type requires enum_values")
        if self._data_type == DataType.REFERENCE and not self._reference_table_id:
            raise ValueError("Reference type requires reference_table_id")
    
    @property
    def data_type(self) -> DataType:
        """Get data type"""
        return self._data_type
    
    @property
    def enum_values(self) -> Optional[tuple]:
        """Get enum values (immutable)"""
        return self._enum_values
    
    @property
    def reference_table_id(self) -> Optional[int]:
        """Get reference table ID"""
        return self._reference_table_id
    
    def validate_value(self, value: Any) -> bool:
        """Validate a value against this data type"""
        if value is None:
            return True  # Null values handled separately
        
        if self._data_type == DataType.STRING:
            return isinstance(value, str)
        elif self._data_type == DataType.INTEGER:
            return isinstance(value, int)
        elif self._data_type == DataType.FLOAT:
            return isinstance(value, (int, float))
        elif self._data_type == DataType.BOOLEAN:
            return isinstance(value, bool)
        elif self._data_type == DataType.ENUM:
            return value in self._enum_values
        elif self._data_type == DataType.REFERENCE:
            return isinstance(value, int) and value > 0
        
        return False

