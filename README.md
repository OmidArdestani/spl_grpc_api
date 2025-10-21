# SPL gRPC API

A Software Product Line (SPL) application with a gRPC-based API for managing items in a repository.

## Overview

This project demonstrates a complete SPL application with the following components:

- **ItemObject**: A class representing items with `validate` and `modify` methods
- **RepositoryWrapper**: A module that manages items with a `findItem` function
- **gRPC API**: A complete gRPC service for remote item management

## Project Structure

```
spl_grpc_api/
├── spl_app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── item_object.py         # ItemObject class with validate and modify methods
│   │   └── repository_wrapper.py  # RepositoryWrapper with findItem function
│   ├── proto/
│   │   ├── __init__.py
│   │   ├── spl_service.proto      # gRPC service definition
│   │   ├── spl_service_pb2.py     # Generated protobuf code
│   │   └── spl_service_pb2_grpc.py # Generated gRPC code
│   ├── server/
│   │   ├── __init__.py
│   │   └── spl_server.py          # gRPC server implementation
│   ├── client/
│   │   ├── __init__.py
│   │   └── spl_client.py          # gRPC client implementation
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Features

### Core Components

#### ItemObject
The `ItemObject` class represents an item in the SPL repository with:
- **Properties**: id, name, description, properties (dict), created_at, updated_at
- **validate()**: Validates the item and returns validation status and errors
- **modify()**: Modifies item properties and validates the changes

#### RepositoryWrapper
The `RepositoryWrapper` class manages the item repository with:
- **findItem(item_id)**: Finds and returns an ItemObject by its ID
- Additional methods: add_item, update_item, delete_item, get_all_items

### gRPC API

The gRPC service provides three operations:

1. **FindItem**: Find an item by its ID
2. **ValidateItem**: Validate an item using its validate method
3. **ModifyItem**: Modify an item using its modify method

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OmidArdestani/spl_grpc_api.git
cd spl_grpc_api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the gRPC server:

```bash
python spl_app/server/spl_server.py
```

The server will start on port 50051 and initialize with sample items.

### Running the Client Demo

In a separate terminal, run the client demo:

```bash
python spl_app/client/spl_client.py
```

This will demonstrate:
- Finding existing and non-existing items
- Validating items
- Modifying items
- Verifying modifications

### Using the Client Programmatically

```python
from spl_app.client import SPLRepositoryClient

# Create client
client = SPLRepositoryClient('localhost:50051')

# Find an item
response = client.find_item("item_001")

# Validate an item
response = client.validate_item("item_001")

# Modify an item
response = client.modify_item(
    "item_001",
    name="New Name",
    description="New Description",
    properties={"key": "value"}
)

# Close connection
client.close()
```

## Sample Items

The repository is initialized with three sample items:

- **item_001**: Sample Product A (electronics, active)
- **item_002**: Sample Product B (books, active)
- **item_003**: Sample Product C (clothing, inactive)

## Development

### Regenerating gRPC Code

If you modify the `.proto` file, regenerate the gRPC code:

```bash
python -m grpc_tools.protoc \
  -I./spl_app/proto \
  --python_out=./spl_app/proto \
  --grpc_python_out=./spl_app/proto \
  ./spl_app/proto/spl_service.proto
```

## API Reference

### FindItem
- **Request**: `FindItemRequest(item_id: string)`
- **Response**: `FindItemResponse(item: ItemObject, found: bool, message: string)`

### ValidateItem
- **Request**: `ValidateItemRequest(item_id: string)`
- **Response**: `ValidateItemResponse(is_valid: bool, message: string, validation_errors: list)`

### ModifyItem
- **Request**: `ModifyItemRequest(item_id: string, name: string, description: string, properties: map)`
- **Response**: `ModifyItemResponse(success: bool, message: string, modified_item: ItemObject)`

## License

MIT License