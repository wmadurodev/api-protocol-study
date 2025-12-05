# Python gRPC Client for UserService

A Python client for testing the UserService gRPC server. This client tests all 6 RPC methods exposed by the server.

## Prerequisites

- Python 3.7 or higher
- gRPC server running on `localhost:9090`

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate gRPC Python Code

Run the generation script to create Python code from the proto file:

```bash
./generate_grpc.sh
```

This will generate two files:
- `user_service_pb2.py` - Protocol Buffer message definitions
- `user_service_pb2_grpc.py` - gRPC service definitions

## Usage

### Run All Tests

To test all 6 RPC methods automatically:

```bash
python3 client.py
```

This will execute tests for:
1. **CreateUser** - Create individual users
2. **BulkCreateUsers** - Create multiple users at once
3. **ListUsers** - List users with pagination
4. **GetUser** - Get a specific user by ID
5. **SearchUsers** - Search users by query
6. **GetUserOrders** - Get orders for a specific user

### Use Programmatically

```python
from client import UserServiceClient

# Initialize client
client = UserServiceClient(host='localhost', port=9090)

# Create a user
user = client.create_user(
    username="johndoe",
    email="john@example.com",
    first_name="John",
    last_name="Doe"
)

# Get user by ID
client.get_user(user_id=1)

# List users with pagination
client.list_users(page=0, size=10)

# Search users
client.search_users(query="john", limit=5)

# Get user orders
client.get_user_orders(user_id=1)

# Bulk create users
bulk_users = [
    {
        "username": "user1",
        "email": "user1@example.com",
        "first_name": "User",
        "last_name": "One"
    },
    {
        "username": "user2",
        "email": "user2@example.com",
        "first_name": "User",
        "last_name": "Two"
    }
]
client.bulk_create_users(bulk_users)

# Close connection
client.close()
```

## RPC Methods

### 1. GetUser
Get a specific user by ID.

**Request:**
- `user_id` (int64): The ID of the user

**Response:**
- `user` (User): The user object

### 2. ListUsers
List users with pagination.

**Request:**
- `page` (int32): Page number (0-indexed)
- `size` (int32): Number of users per page

**Response:**
- `users` (repeated User): List of users
- `total_elements` (int64): Total number of users
- `total_pages` (int32): Total number of pages
- `current_page` (int32): Current page number

### 3. CreateUser
Create a new user.

**Request:**
- `username` (string): Username
- `email` (string): Email address
- `first_name` (string): First name
- `last_name` (string): Last name

**Response:**
- `user` (User): The created user

### 4. GetUserOrders
Get all orders for a specific user.

**Request:**
- `user_id` (int64): The ID of the user

**Response:**
- `orders` (repeated Order): List of orders

### 5. SearchUsers
Search users by query string.

**Request:**
- `query` (string): Search query
- `limit` (int32): Maximum number of results

**Response:**
- `users` (repeated User): List of matching users

### 6. BulkCreateUsers
Create multiple users at once.

**Request:**
- `users` (repeated CreateUserRequest): List of users to create

**Response:**
- `users` (repeated User): List of created users

## Server Configuration

The client connects to the gRPC server at:
- **Host:** localhost
- **Port:** 9090

To connect to a different server, modify the initialization:

```python
client = UserServiceClient(host='your-host', port=9090)
```

## Error Handling

All methods include error handling for gRPC errors. If an error occurs, the error code and details will be printed to the console.

Example error output:
```
Error: NOT_FOUND - User not found: 999
```

## Project Structure

```
python-grpc-client/
├── proto/
│   └── user_service.proto       # Proto file (copied from shared/proto)
├── client.py                     # Main client implementation
├── generate_grpc.sh              # Script to generate Python gRPC code
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── user_service_pb2.py          # Generated (after running generate_grpc.sh)
└── user_service_pb2_grpc.py     # Generated (after running generate_grpc.sh)
```

## Troubleshooting

### Import Error: No module named 'user_service_pb2'

Make sure you've run the generation script:
```bash
./generate_grpc.sh
```

### Connection Error: failed to connect to all addresses

Make sure the gRPC server is running:
```bash
# In the grpc-server directory
mvn spring-boot:run
```

### Permission Denied: ./generate_grpc.sh

Make the script executable:
```bash
chmod +x generate_grpc.sh
```
