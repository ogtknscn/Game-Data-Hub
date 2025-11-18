"""
Code generator interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class ICodeGenerator(ABC):
    """Code generator interface"""
    
    @abstractmethod
    def generate(self, table_data: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """
        Generate code from table data and schema
        Returns: Generated code as string
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension for generated code"""
        pass
    
    @abstractmethod
    def get_mime_type(self) -> str:
        """Get MIME type for generated code"""
        pass

