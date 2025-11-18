"""
Base code generator
Abstract base class following Template Method pattern
"""
from abc import abstractmethod
from typing import Dict, Any
from app.domain.interfaces.code_generators import ICodeGenerator
from jinja2 import Template


class BaseCodeGenerator(ICodeGenerator):
    """Base code generator with common functionality"""
    
    @abstractmethod
    def get_template(self) -> str:
        """Get Jinja2 template string"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension"""
        pass
    
    @abstractmethod
    def get_mime_type(self) -> str:
        """Get MIME type"""
        pass
    
    def generate(self, table_data: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """Generate code from table data and schema"""
        template_str = self.get_template()
        template = Template(template_str)
        
        # Prepare context
        context = {
            "table_name": schema.get("name", "Table"),
            "columns": schema.get("columns", []),
            "rows": table_data.get("rows", [])
        }
        
        return template.render(**context)

