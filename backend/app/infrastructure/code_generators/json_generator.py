"""
Generic JSON schema generator
"""
from app.infrastructure.code_generators.base_generator import BaseCodeGenerator
import json
from typing import Dict, Any


class JSONGenerator(BaseCodeGenerator):
    """Generic JSON schema generator"""
    
    def generate(self, table_data: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """Generate JSON with schema"""
        result = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": schema.get("name", "Table"),
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    col["name"]: {
                        "type": self._map_data_type(col["data_type"]),
                        "description": f"Column: {col['name']}"
                    }
                    for col in schema.get("columns", [])
                },
                "required": [
                    col["name"]
                    for col in schema.get("columns", [])
                    if col.get("is_required", False)
                ]
            },
            "data": table_data.get("rows", [])
        }
        return json.dumps(result, indent=2)
    
    def _map_data_type(self, data_type: str) -> str:
        """Map GDH data type to JSON schema type"""
        mapping = {
            "string": "string",
            "integer": "integer",
            "float": "number",
            "boolean": "boolean",
            "enum": "string",
            "reference": "integer"
        }
        return mapping.get(data_type, "string")
    
    def get_template(self) -> str:
        """Not used for JSON generator"""
        return ""
    
    def get_file_extension(self) -> str:
        """Get file extension"""
        return ".json"
    
    def get_mime_type(self) -> str:
        """Get MIME type"""
        return "application/json"

