"""
ItemObject class for SPL application.
Represents an item in the repository with validation and modification capabilities.
"""
from typing import Dict, List, Optional
import time


class ItemObject:
    """
    ItemObject represents an item in the SPL repository.
    It provides validate and modify methods as specified.
    """
    
    def __init__(self, item_id: str, name: str = "", description: str = "", 
                 properties: Optional[Dict[str, str]] = None):
        """
        Initialize an ItemObject.
        
        Args:
            item_id: Unique identifier for the item
            name: Name of the item
            description: Description of the item
            properties: Additional properties as key-value pairs
        """
        self.id = item_id
        self.name = name
        self.description = description
        self.properties = properties if properties is not None else {}
        self.created_at = int(time.time())
        self.updated_at = int(time.time())
    
    def validate(self) -> tuple[bool, str, List[str]]:
        """
        Validate the item object.
        
        Returns:
            A tuple of (is_valid, message, validation_errors)
        """
        validation_errors = []
        
        # Check if ID is not empty
        if not self.id or not self.id.strip():
            validation_errors.append("Item ID cannot be empty")
        
        # Check if name is not empty
        if not self.name or not self.name.strip():
            validation_errors.append("Item name cannot be empty")
        
        # Check if description has reasonable length
        if self.description and len(self.description) > 1000:
            validation_errors.append("Description cannot exceed 1000 characters")
        
        # Check if properties are valid
        if self.properties:
            for key, value in self.properties.items():
                if not key or not key.strip():
                    validation_errors.append("Property key cannot be empty")
                if not isinstance(value, str):
                    validation_errors.append(f"Property value for '{key}' must be a string")
        
        is_valid = len(validation_errors) == 0
        message = "Item is valid" if is_valid else "Item validation failed"
        
        return is_valid, message, validation_errors
    
    def modify(self, name: Optional[str] = None, description: Optional[str] = None,
               properties: Optional[Dict[str, str]] = None) -> tuple[bool, str]:
        """
        Modify the item object.
        
        Args:
            name: New name for the item (optional)
            description: New description for the item (optional)
            properties: New properties for the item (optional)
        
        Returns:
            A tuple of (success, message)
        """
        try:
            if name is not None:
                self.name = name
            
            if description is not None:
                self.description = description
            
            if properties is not None:
                self.properties = properties
            
            self.updated_at = int(time.time())
            
            # Validate after modification
            is_valid, _, validation_errors = self.validate()
            if not is_valid:
                return False, f"Modification failed validation: {', '.join(validation_errors)}"
            
            return True, "Item modified successfully"
        except Exception as e:
            return False, f"Error modifying item: {str(e)}"
    
    def to_dict(self) -> Dict:
        """
        Convert the ItemObject to a dictionary.
        
        Returns:
            Dictionary representation of the item
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'properties': self.properties,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __str__(self) -> str:
        """String representation of the ItemObject."""
        return f"ItemObject(id={self.id}, name={self.name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the ItemObject."""
        return (f"ItemObject(id={self.id}, name={self.name}, "
                f"description={self.description}, properties={self.properties})")
