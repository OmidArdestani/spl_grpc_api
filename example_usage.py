"""
Example usage of the SPL gRPC API demonstrating the core components:
- RepositoryWrapper with findItem function
- ItemObject with validate and modify methods
"""

# Example 1: Using the core components directly (without gRPC)
print("=" * 60)
print("Example 1: Direct usage of core components")
print("=" * 60)

from spl_app.core.item_object import ItemObject
from spl_app.core.repository_wrapper import RepositoryWrapper

# Create a repository wrapper
repository = RepositoryWrapper()
print(f"Repository initialized with {repository.count()} items\n")

# Use the findItem function
print("Using RepositoryWrapper.findItem():")
item = repository.findItem("item_001")
if item:
    print(f"✓ Found: {item}")
    print(f"  Name: {item.name}")
    print(f"  Description: {item.description}")
    print(f"  Properties: {item.properties}\n")

# Use the ItemObject.validate() method
print("Using ItemObject.validate():")
is_valid, message, errors = item.validate()
print(f"✓ Validation result: {is_valid}")
print(f"  Message: {message}")
if errors:
    print(f"  Errors: {errors}\n")
else:
    print()

# Use the ItemObject.modify() method
print("Using ItemObject.modify():")
success, msg = item.modify(
    name="Modified Product A",
    description="This product has been modified",
    properties={"category": "electronics", "status": "modified", "version": "2.0"}
)
print(f"✓ Modification result: {success}")
print(f"  Message: {msg}")
print(f"  Updated name: {item.name}")
print(f"  Updated properties: {item.properties}\n")

# Verify the modification persisted
print("Verifying the item was modified:")
modified_item = repository.findItem("item_001")
print(f"✓ Found: {modified_item}")
print(f"  Name: {modified_item.name}")
print(f"  Properties: {modified_item.properties}\n")

print("=" * 60)
print("Example 2: Using the gRPC API (requires server running)")
print("=" * 60)
print("\nTo use the gRPC API:")
print("1. Start the server: python spl_app/server/spl_server.py")
print("2. Run the client: python spl_app/client/spl_client.py")
print("\nOr use the client programmatically:")
print("""
from spl_app.client import SPLRepositoryClient

client = SPLRepositoryClient('localhost:50051')
response = client.find_item("item_001")
response = client.validate_item("item_001")
response = client.modify_item("item_001", name="New Name")
client.close()
""")
