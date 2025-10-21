"""
gRPC Client implementation for SPL Repository Service.
"""
import grpc
import sys
import os

# Add the parent directory to the path to import spl_app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proto import spl_service_pb2
from proto import spl_service_pb2_grpc


class SPLRepositoryClient:
    """
    Client for the SPL Repository gRPC service.
    """
    
    def __init__(self, server_address='localhost:50051'):
        """
        Initialize the client with server address.
        
        Args:
            server_address: Address of the gRPC server (default: localhost:50051)
        """
        self.channel = grpc.insecure_channel(server_address)
        self.stub = spl_service_pb2_grpc.SPLRepositoryStub(self.channel)
        print(f"Connected to SPL gRPC Server at {server_address}")
    
    def find_item(self, item_id):
        """
        Find an item by its ID.
        
        Args:
            item_id: The unique identifier of the item
        
        Returns:
            FindItemResponse
        """
        print(f"\n--- Finding item: {item_id} ---")
        request = spl_service_pb2.FindItemRequest(item_id=item_id)
        
        try:
            response = self.stub.FindItem(request)
            
            if response.found:
                print(f"✓ {response.message}")
                print(f"  ID: {response.item.id}")
                print(f"  Name: {response.item.name}")
                print(f"  Description: {response.item.description}")
                print(f"  Properties: {dict(response.item.properties)}")
            else:
                print(f"✗ {response.message}")
            
            return response
        except grpc.RpcError as e:
            print(f"✗ RPC failed: {e.code()}: {e.details()}")
            return None
    
    def validate_item(self, item_id):
        """
        Validate an item.
        
        Args:
            item_id: The unique identifier of the item
        
        Returns:
            ValidateItemResponse
        """
        print(f"\n--- Validating item: {item_id} ---")
        request = spl_service_pb2.ValidateItemRequest(item_id=item_id)
        
        try:
            response = self.stub.ValidateItem(request)
            
            if response.is_valid:
                print(f"✓ {response.message}")
            else:
                print(f"✗ {response.message}")
                for error in response.validation_errors:
                    print(f"  - {error}")
            
            return response
        except grpc.RpcError as e:
            print(f"✗ RPC failed: {e.code()}: {e.details()}")
            return None
    
    def modify_item(self, item_id, name=None, description=None, properties=None):
        """
        Modify an item.
        
        Args:
            item_id: The unique identifier of the item
            name: New name for the item (optional)
            description: New description for the item (optional)
            properties: New properties for the item (optional)
        
        Returns:
            ModifyItemResponse
        """
        print(f"\n--- Modifying item: {item_id} ---")
        
        request = spl_service_pb2.ModifyItemRequest(item_id=item_id)
        
        if name:
            request.name = name
            print(f"  New name: {name}")
        if description:
            request.description = description
            print(f"  New description: {description}")
        if properties:
            request.properties.update(properties)
            print(f"  New properties: {properties}")
        
        try:
            response = self.stub.ModifyItem(request)
            
            if response.success:
                print(f"✓ {response.message}")
                if response.modified_item.id:
                    print(f"  Modified item:")
                    print(f"    ID: {response.modified_item.id}")
                    print(f"    Name: {response.modified_item.name}")
                    print(f"    Description: {response.modified_item.description}")
                    print(f"    Properties: {dict(response.modified_item.properties)}")
            else:
                print(f"✗ {response.message}")
            
            return response
        except grpc.RpcError as e:
            print(f"✗ RPC failed: {e.code()}: {e.details()}")
            return None
    
    def close(self):
        """Close the gRPC channel."""
        self.channel.close()
        print("\nConnection closed")


def run_demo():
    """
    Run a demonstration of the SPL Repository client.
    """
    print("=" * 60)
    print("SPL gRPC Client Demo")
    print("=" * 60)
    
    client = SPLRepositoryClient()
    
    # Test 1: Find an existing item
    client.find_item("item_001")
    
    # Test 2: Find a non-existing item
    client.find_item("item_999")
    
    # Test 3: Validate an existing item
    client.validate_item("item_001")
    
    # Test 4: Modify an item
    client.modify_item(
        "item_002",
        name="Updated Product B",
        description="This product has been updated",
        properties={"category": "books", "status": "updated", "version": "2.0"}
    )
    
    # Test 5: Find the modified item to verify changes
    client.find_item("item_002")
    
    # Test 6: Validate the modified item
    client.validate_item("item_002")
    
    # Test 7: Test all items
    print("\n" + "=" * 60)
    print("Testing all sample items")
    print("=" * 60)
    
    for item_id in ["item_001", "item_002", "item_003"]:
        client.find_item(item_id)
    
    client.close()


if __name__ == '__main__':
    run_demo()
