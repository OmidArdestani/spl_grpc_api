"""
Test suite for SPL gRPC API
Tests the core components: RepositoryWrapper, ItemObject, and their methods
"""
import sys
sys.path.insert(0, '/home/runner/work/spl_grpc_api/spl_grpc_api')

from spl_app.core.item_object import ItemObject
from spl_app.core.repository_wrapper import RepositoryWrapper


def test_item_object_creation():
    """Test creating an ItemObject"""
    print("Test: ItemObject creation")
    item = ItemObject("test_id", "Test Item", "Test Description", {"key": "value"})
    assert item.id == "test_id"
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.properties["key"] == "value"
    print("  ✓ ItemObject creation works correctly\n")


def test_item_object_validate():
    """Test ItemObject.validate() method"""
    print("Test: ItemObject.validate()")
    
    # Valid item
    item = ItemObject("id1", "Valid Item", "Description", {})
    is_valid, message, errors = item.validate()
    assert is_valid == True
    assert len(errors) == 0
    print("  ✓ Valid item passes validation")
    
    # Invalid item (empty name)
    item = ItemObject("id2", "", "Description", {})
    is_valid, message, errors = item.validate()
    assert is_valid == False
    assert len(errors) > 0
    print("  ✓ Invalid item fails validation")
    print(f"    Errors: {errors}\n")


def test_item_object_modify():
    """Test ItemObject.modify() method"""
    print("Test: ItemObject.modify()")
    item = ItemObject("id1", "Original Name", "Original Description", {"key": "value"})
    
    # Modify name
    success, message = item.modify(name="New Name")
    assert success == True
    assert item.name == "New Name"
    print("  ✓ Modifying name works correctly")
    
    # Modify description
    success, message = item.modify(description="New Description")
    assert success == True
    assert item.description == "New Description"
    print("  ✓ Modifying description works correctly")
    
    # Modify properties
    success, message = item.modify(properties={"new_key": "new_value"})
    assert success == True
    assert item.properties["new_key"] == "new_value"
    print("  ✓ Modifying properties works correctly\n")


def test_repository_wrapper_creation():
    """Test creating a RepositoryWrapper"""
    print("Test: RepositoryWrapper creation")
    repo = RepositoryWrapper()
    assert repo.count() == 3  # Should have 3 sample items
    print(f"  ✓ RepositoryWrapper created with {repo.count()} sample items\n")


def test_repository_wrapper_findItem():
    """Test RepositoryWrapper.findItem() method"""
    print("Test: RepositoryWrapper.findItem()")
    repo = RepositoryWrapper()
    
    # Find existing item
    item = repo.findItem("item_001")
    assert item is not None
    assert item.id == "item_001"
    assert item.name == "Sample Product A"
    print("  ✓ Finding existing item works correctly")
    
    # Try to find non-existing item
    item = repo.findItem("non_existing_id")
    assert item is None
    print("  ✓ Finding non-existing item returns None\n")


def test_repository_wrapper_add_update():
    """Test adding and updating items in repository"""
    print("Test: RepositoryWrapper add and update")
    repo = RepositoryWrapper()
    
    # Add new item
    new_item = ItemObject("test_new", "New Item", "New Description", {})
    success = repo.add_item(new_item)
    assert success == True
    assert repo.count() == 4
    print("  ✓ Adding new item works correctly")
    
    # Update item
    new_item.name = "Updated Name"
    success = repo.update_item(new_item)
    assert success == True
    updated = repo.findItem("test_new")
    assert updated.name == "Updated Name"
    print("  ✓ Updating item works correctly\n")


def test_integration_scenario():
    """Test a complete integration scenario"""
    print("Test: Integration scenario")
    print("  Scenario: Find item, validate it, and modify it")
    
    # Step 1: Create repository
    repo = RepositoryWrapper()
    print("  1. Repository created")
    
    # Step 2: Use findItem to get an item
    item = repo.findItem("item_002")
    assert item is not None
    print(f"  2. Found item: {item.name}")
    
    # Step 3: Validate the item
    is_valid, message, errors = item.validate()
    assert is_valid == True
    print(f"  3. Validated item: {message}")
    
    # Step 4: Modify the item
    success, msg = item.modify(
        name="Integration Test Item",
        description="Modified during integration test",
        properties={"test": "integration", "status": "modified"}
    )
    assert success == True
    print(f"  4. Modified item: {msg}")
    
    # Step 5: Update in repository
    repo.update_item(item)
    print("  5. Updated item in repository")
    
    # Step 6: Verify changes persisted
    verified_item = repo.findItem("item_002")
    assert verified_item.name == "Integration Test Item"
    assert verified_item.properties["test"] == "integration"
    print("  6. Verified changes persisted")
    print("  ✓ Integration scenario completed successfully\n")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("SPL gRPC API - Test Suite")
    print("=" * 70)
    print()
    
    try:
        test_item_object_creation()
        test_item_object_validate()
        test_item_object_modify()
        test_repository_wrapper_creation()
        test_repository_wrapper_findItem()
        test_repository_wrapper_add_update()
        test_integration_scenario()
        
        print("=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
