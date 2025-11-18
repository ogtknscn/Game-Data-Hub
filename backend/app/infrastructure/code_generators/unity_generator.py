"""
Unity C# ScriptableObject generator
"""
from app.infrastructure.code_generators.base_generator import BaseCodeGenerator


class UnityGenerator(BaseCodeGenerator):
    """Unity C# ScriptableObject generator"""
    
    def get_template(self) -> str:
        """Get Unity ScriptableObject template"""
        return """using UnityEngine;

[CreateAssetMenu(fileName = "{{ table_name }}", menuName = "Game Data/{{ table_name }}")]
public class {{ table_name }}Data : ScriptableObject
{
    {% for column in columns %}
    public {{ column.data_type|title }} {{ column.name }};
    {% endfor %}
}

[System.Serializable]
public class {{ table_name }}Database : ScriptableObject
{
    public {{ table_name }}Data[] items;
    
    public {{ table_name }}Data GetById(int id)
    {
        foreach (var item in items)
        {
            if (item.id == id) return item;
        }
        return null;
    }
}
"""
    
    def get_file_extension(self) -> str:
        """Get file extension"""
        return ".cs"
    
    def get_mime_type(self) -> str:
        """Get MIME type"""
        return "text/x-csharp"

