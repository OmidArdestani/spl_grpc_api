"""
gRPC Server implementation for SPL Repository Service.
"""
import grpc
from concurrent import futures
import time
import sys
import os

# Add the parent directory to the path to import spl_app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proto import spl_service_pb2
from proto import spl_service_pb2_grpc
from core.repository_wrapper import RepositoryWrapper
from core.item_object import ItemObject


class SPLRepositoryServicer(spl_service_pb2_grpc.SPLRepositoryServicer):
    """
    Implementation of the SPL Repository gRPC service.
    """
    
    def __init__(self):
        """Initialize the service with a RepositoryWrapper instance."""
        self.repository = RepositoryWrapper()
        print(f"SPL Repository initialized with {self.repository.count()} items")
    
    def FindItem(self, request, context):
        """
        Find an item by its ID using the repository wrapper's findItem method.
        
        Args:
            request: FindItemRequest containing item_id
            context: gRPC context
        
        Returns:
            FindItemResponse with the found item or not found status
        """
        item_id = request.item_id
        print(f"FindItem called for item_id: {item_id}")
        
        # Use the repository wrapper's findItem function
        item_obj = self.repository.findItem(item_id)
        
        if item_obj is None:
            # Item not found
            return spl_service_pb2.FindItemResponse(
                found=False,
                message=f"Item with ID '{item_id}' not found"
            )
        
        # Item found - convert to protobuf message
        item_proto = spl_service_pb2.ItemObject(
            id=item_obj.id,
            name=item_obj.name,
            description=item_obj.description,
            properties=item_obj.properties,
            created_at=item_obj.created_at,
            updated_at=item_obj.updated_at
        )
        
        return spl_service_pb2.FindItemResponse(
            item=item_proto,
            found=True,
            message=f"Item '{item_id}' found successfully"
        )
    
    def ValidateItem(self, request, context):
        """
        Validate an item using the ItemObject's validate method.
        
        Args:
            request: ValidateItemRequest containing item_id
            context: gRPC context
        
        Returns:
            ValidateItemResponse with validation result
        """
        item_id = request.item_id
        print(f"ValidateItem called for item_id: {item_id}")
        
        # Find the item first
        item_obj = self.repository.findItem(item_id)
        
        if item_obj is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Item with ID '{item_id}' not found")
            return spl_service_pb2.ValidateItemResponse(
                is_valid=False,
                message=f"Item '{item_id}' not found",
                validation_errors=[f"Item with ID '{item_id}' does not exist"]
            )
        
        # Call the validate method on the ItemObject
        is_valid, message, validation_errors = item_obj.validate()
        
        return spl_service_pb2.ValidateItemResponse(
            is_valid=is_valid,
            message=message,
            validation_errors=validation_errors
        )
    
    def ModifyItem(self, request, context):
        """
        Modify an item using the ItemObject's modify method.
        
        Args:
            request: ModifyItemRequest containing item_id and new values
            context: gRPC context
        
        Returns:
            ModifyItemResponse with modification result
        """
        item_id = request.item_id
        print(f"ModifyItem called for item_id: {item_id}")
        
        # Find the item first
        item_obj = self.repository.findItem(item_id)
        
        if item_obj is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Item with ID '{item_id}' not found")
            return spl_service_pb2.ModifyItemResponse(
                success=False,
                message=f"Item '{item_id}' not found"
            )
        
        # Call the modify method on the ItemObject
        name = request.name if request.name else None
        description = request.description if request.description else None
        properties = dict(request.properties) if request.properties else None
        
        success, message = item_obj.modify(
            name=name,
            description=description,
            properties=properties
        )
        
        if success:
            # Update the item in repository
            self.repository.update_item(item_obj)
            
            # Return the modified item
            modified_item_proto = spl_service_pb2.ItemObject(
                id=item_obj.id,
                name=item_obj.name,
                description=item_obj.description,
                properties=item_obj.properties,
                created_at=item_obj.created_at,
                updated_at=item_obj.updated_at
            )
            
            return spl_service_pb2.ModifyItemResponse(
                success=True,
                message=message,
                modified_item=modified_item_proto
            )
        else:
            return spl_service_pb2.ModifyItemResponse(
                success=False,
                message=message
            )


def serve(port=50051):
    """
    Start the gRPC server.
    
    Args:
        port: Port number to listen on (default: 50051)
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spl_service_pb2_grpc.add_SPLRepositoryServicer_to_server(
        SPLRepositoryServicer(), server
    )
    
    server_address = f'[::]:{port}'
    server.add_insecure_port(server_address)
    server.start()
    
    print(f"SPL gRPC Server started on {server_address}")
    print("Press Ctrl+C to stop the server")
    
    try:
        while True:
            time.sleep(86400)  # Sleep for a day
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop(0)


if __name__ == '__main__':
    serve()
