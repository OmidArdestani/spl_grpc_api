"""
RepositoryWrapper module for SPL application.
Provides access to the item repository with findItem functionality.
"""
from typing import Optional, Dict
from .item_object import ItemObject


class RepositoryWrapper:
    """
    RepositoryWrapper provides access to the item repository.
    It manages items and provides methods to find items by ID.
    """
    
    def __init__(self):
        """Initialize the repository with an empty item store."""
        self._items: Dict[str, ItemObject] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize the repository with some sample items."""
        # Add some sample items for demonstration
        sample_items = [
            ItemObject(
                item_id="item_001",
                name="Sample Product A",
                description="This is a sample product in the SPL",
                properties={"category": "electronics", "status": "active"}
            ),
            ItemObject(
                item_id="item_002",
                name="Sample Product B",
                description="Another sample product",
                properties={"category": "books", "status": "active"}
            ),
            ItemObject(
                item_id="item_003",
                name="Sample Product C",
                description="Yet another sample product",
                properties={"category": "clothing", "status": "inactive"}
            ),
        ]
        
        for item in sample_items:
            self._items[item.id] = item
    
    def findItem(self, item_id: str) -> Optional[ItemObject]:
        """
        Find an item by its ID.
        
        Args:
            item_id: The unique identifier of the item to find
        
        Returns:
            ItemObject if found, None otherwise
        """
        return self._items.get(item_id)
    
    def add_item(self, item: ItemObject) -> bool:
        """
        Add a new item to the repository.
        
        Args:
            item: The ItemObject to add
        
        Returns:
            True if added successfully, False if item with same ID already exists
        """
        if item.id in self._items:
            return False
        
        self._items[item.id] = item
        return True
    
    def update_item(self, item: ItemObject) -> bool:
        """
        Update an existing item in the repository.
        
        Args:
            item: The ItemObject with updated data
        
        Returns:
            True if updated successfully, False if item doesn't exist
        """
        if item.id not in self._items:
            return False
        
        self._items[item.id] = item
        return True
    
    def delete_item(self, item_id: str) -> bool:
        """
        Delete an item from the repository.
        
        Args:
            item_id: The unique identifier of the item to delete
        
        Returns:
            True if deleted successfully, False if item doesn't exist
        """
        if item_id not in self._items:
            return False
        
        del self._items[item_id]
        return True
    
    def get_all_items(self) -> Dict[str, ItemObject]:
        """
        Get all items in the repository.
        
        Returns:
            Dictionary of all items with item_id as key
        """
        return self._items.copy()
    
    def count(self) -> int:
        """
        Get the total number of items in the repository.
        
        Returns:
            Number of items
        """
        return len(self._items)
