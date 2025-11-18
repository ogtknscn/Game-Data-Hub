"""
Data validator
Validates cell values against column definitions
"""
from typing import Any, Optional
from app.domain.value_objects.data_types import DataType, DataTypeDefinition
from app.core.exceptions import ValidationError


class DataValidator:
    """Data validator"""
    
    @staticmethod
    def validate_cell_value(
        value: Any,
        data_type: str,
        is_required: bool = False,
        enum_values: Optional[list] = None,
        reference_table_id: Optional[int] = None
    ) -> bool:
        """Validate cell value against column definition"""
        # Check required
        if is_required and value is None:
            raise ValidationError("Required field cannot be null")
        
        if value is None:
            return True  # Null values are allowed if not required
        
        # Validate by type
        try:
            data_type_enum = DataType.from_string(data_type)
        except ValueError:
            raise ValidationError(f"Invalid data type: {data_type}")
        
        type_def = DataTypeDefinition(
            data_type_enum,
            enum_values=enum_values,
            reference_table_id=reference_table_id
        )
        
        if not type_def.validate_value(value):
            raise ValidationError(f"Value {value} does not match data type {data_type}")
        
        return True
    
    @staticmethod
    def parse_value(value: str, data_type: str) -> Any:
        """Parse string value to appropriate type"""
        if value is None or value == "":
            return None
        
        try:
            data_type_enum = DataType.from_string(data_type)
        except ValueError:
            raise ValidationError(f"Invalid data type: {data_type}")
        
        if data_type_enum == DataType.INTEGER:
            return int(value)
        elif data_type_enum == DataType.FLOAT:
            return float(value)
        elif data_type_enum == DataType.BOOLEAN:
            return value.lower() in ("true", "1", "yes")
        else:
            return value

