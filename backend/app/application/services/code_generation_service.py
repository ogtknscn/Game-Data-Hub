"""
Code generation service
Orchestrates code generators
"""
from typing import Dict, Any, List
from app.domain.interfaces.code_generators import ICodeGenerator
from app.infrastructure.code_generators.unity_generator import UnityGenerator
from app.infrastructure.code_generators.unreal_generator import UnrealGenerator
from app.infrastructure.code_generators.json_generator import JSONGenerator


class CodeGenerationService:
    """Code generation service"""
    
    def __init__(self):
        self._generators: Dict[str, ICodeGenerator] = {
            "unity": UnityGenerator(),
            "unreal": UnrealGenerator(),
            "json": JSONGenerator()
        }
    
    def generate_code(
        self,
        generator_type: str,
        table_data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> str:
        """Generate code using specified generator"""
        generator = self._generators.get(generator_type.lower())
        if not generator:
            raise ValueError(f"Unknown generator type: {generator_type}")
        
        return generator.generate(table_data, schema)
    
    def get_supported_generators(self) -> List[str]:
        """Get list of supported generator types"""
        return list(self._generators.keys())
    
    def get_file_extension(self, generator_type: str) -> str:
        """Get file extension for generator type"""
        generator = self._generators.get(generator_type.lower())
        if not generator:
            raise ValueError(f"Unknown generator type: {generator_type}")
        return generator.get_file_extension()
    
    def get_mime_type(self, generator_type: str) -> str:
        """Get MIME type for generator type"""
        generator = self._generators.get(generator_type.lower())
        if not generator:
            raise ValueError(f"Unknown generator type: {generator_type}")
        return generator.get_mime_type()

