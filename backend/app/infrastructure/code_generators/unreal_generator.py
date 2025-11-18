"""
Unreal Engine JSON/DataTable generator
"""
from typing import Dict, Any
from app.infrastructure.code_generators.base_generator import BaseCodeGenerator
import json


class UnrealGenerator(BaseCodeGenerator):
    """Unreal Engine JSON/DataTable generator"""
    
    def get_template(self) -> str:
        """Get Unreal JSON template"""
        return """{
    "TableName": "{{ table_name }}",
    "Columns": [
        {% for column in columns %}
        {
            "Name": "{{ column.name }}",
            "Type": "{{ column.data_type }}",
            "Required": {{ column.is_required|lower }}
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "Rows": [
        {% for row in rows %}
        {
            {% for column in columns %}
            "{{ column.name }}": {{ row.cells[column.name]|tojson }}{% if not loop.last %},{% endif %}
            {% endfor %}
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ]
}
"""
    
    def generate(self, table_data: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """Generate Unreal JSON format"""
        result = {
            "TableName": schema.get("name", "Table"),
            "Columns": [
                {
                    "Name": col["name"],
                    "Type": col["data_type"],
                    "Required": col.get("is_required", False)
                }
                for col in schema.get("columns", [])
            ],
            "Rows": table_data.get("rows", [])
        }
        return json.dumps(result, indent=2)
    
    def get_file_extension(self) -> str:
        """Get file extension"""
        return ".json"
    
    def get_mime_type(self) -> str:
        """Get MIME type"""
        return "application/json"

