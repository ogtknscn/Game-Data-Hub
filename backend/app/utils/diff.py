"""
Diff algorithm implementation
O(n) time complexity for cell-by-cell comparison
"""
from typing import Dict, Any, List, Tuple


def calculate_cell_diff(old_cells: Dict[int, Any], new_cells: Dict[int, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Calculate diff between old and new cell values
    Time complexity: O(n) where n is the number of cells
    
    Returns: {cell_id: {old_value, new_value}}
    """
    changes: Dict[str, Dict[str, Any]] = {}
    
    # Check all cells in both old and new
    all_cell_ids = set(old_cells.keys()) | set(new_cells.keys())
    
    for cell_id in all_cell_ids:
        old_value = old_cells.get(cell_id)
        new_value = new_cells.get(cell_id)
        
        # Only record if values differ
        if old_value != new_value:
            changes[str(cell_id)] = {
                "old_value": old_value,
                "new_value": new_value
            }
    
    return changes


def calculate_row_diff(old_row: Dict[str, Any], new_row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate diff between old and new row
    Time complexity: O(n) where n is the number of columns
    """
    changes: Dict[str, Any] = {}
    
    # Get all column names
    all_columns = set(old_row.get("cells", {}).keys()) | set(new_row.get("cells", {}).keys())
    
    for column_name in all_columns:
        old_value = old_row.get("cells", {}).get(column_name)
        new_value = new_row.get("cells", {}).get(column_name)
        
        if old_value != new_value:
            changes[column_name] = {
                "old_value": old_value,
                "new_value": new_value
            }
    
    return changes


def format_diff_for_display(changes: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format diff changes for display
    Time complexity: O(n) where n is the number of changes
    """
    formatted = []
    
    for cell_id, change in changes.items():
        formatted.append({
            "cell_id": cell_id,
            "old_value": change.get("old_value"),
            "new_value": change.get("new_value"),
            "has_change": change.get("old_value") != change.get("new_value")
        })
    
    return formatted

