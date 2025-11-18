"""
Schema validator
Validates table schemas and column definitions
"""
from typing import List, Dict, Any
from app.domain.value_objects.data_types import DataType, DataTypeDefinition
from app.core.exceptions import ValidationError


class SchemaValidator:
    """Schema validator"""
    
    @staticmethod
    def validate_column_definition(column: Dict[str, Any]) -> bool:
        """Validate column definition"""
        required_fields = ["name", "data_type"]
        for field in required_fields:
            if field not in column:
                raise ValidationError(f"Column missing required field: {field}")
        
        # Validate data type
        try:
            data_type = DataType.from_string(column["data_type"])
        except ValueError as e:
            raise ValidationError(str(e))
        
        # Validate enum type
        if data_type == DataType.ENUM:
            if "enum_values" not in column or not column["enum_values"]:
                raise ValidationError("Enum type requires enum_values")
        
        # Validate reference type
        if data_type == DataType.REFERENCE:
            if "reference_table_id" not in column or not column["reference_table_id"]:
                raise ValidationError("Reference type requires reference_table_id")
        
        return True
    
    @staticmethod
    def validate_table_schema(schema: Dict[str, Any]) -> bool:
        """Validate table schema"""
        if "columns" not in schema:
            raise ValidationError("Table schema must have columns")
        
        columns = schema["columns"]
        if not isinstance(columns, list):
            raise ValidationError("Columns must be a list")
        
        if len(columns) == 0:
            raise ValidationError("Table must have at least one column")
        
        # Validate each column
        for column in columns:
            SchemaValidator.validate_column_definition(column)
        
        # Check for duplicate column names
        column_names = [col["name"] for col in columns]
        if len(column_names) != len(set(column_names)):
            raise ValidationError("Duplicate column names are not allowed")
        
        return True

