#!/usr/bin/env python3
"""
Python gRPC Client for UserService

This client tests all 6 RPC methods exposed by the gRPC server:
1. GetUser
2. ListUsers
3. CreateUser
4. GetUserOrders
5. SearchUsers
6. BulkCreateUsers

Before running:
1. Install dependencies: pip install -r requirements.txt
2. Generate gRPC code: ./generate_grpc.sh
3. Ensure the gRPC server is running on localhost:9090
"""

import grpc
import sys
from datetime import datetime

# Import generated gRPC code
try:
    import user_service_pb2
    import user_service_pb2_grpc
except ImportError:
    print("Error: gRPC Python code not generated yet!")
    print("Please run: ./generate_grpc.sh")
    sys.exit(1)


class UserServiceClient:
    """Client for testing UserService gRPC endpoints"""

    def __init__(self, host='localhost', port=9090):
        """Initialize the gRPC client"""
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)
        print(f"Connected to gRPC server at {host}:{port}")

    def close(self):
        """Close the gRPC channel"""
        self.channel.close()
        print("Connection closed")

    def get_user(self, user_id):
        """Test GetUser RPC method"""
        print(f"\n=== Testing GetUser (user_id={user_id}) ===")
        try:
            request = user_service_pb2.GetUserRequest(user_id=user_id)
            response = self.stub.GetUser(request)
            print(f"Success! User: {response.user.username} ({response.user.email})")
            print(f"  ID: {response.user.id}")
            print(f"  Name: {response.user.first_name} {response.user.last_name}")
            print(f"  Active: {response.user.is_active}")
            return response.user
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            return None

    def list_users(self, page=0, size=10):
        """Test ListUsers RPC method"""
        print(f"\n=== Testing ListUsers (page={page}, size={size}) ===")
        try:
            request = user_service_pb2.ListUsersRequest(page=page, size=size)
            response = self.stub.ListUsers(request)
            print(f"Success! Found {len(response.users)} users")
            print(f"  Total elements: {response.total_elements}")
            print(f"  Total pages: {response.total_pages}")
            print(f"  Current page: {response.current_page}")
            for user in response.users:
                print(f"  - {user.id}: {user.username} ({user.email})")
            return response.users
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            return None

    def create_user(self, username, email, first_name, last_name):
        """Test CreateUser RPC method"""
        print(f"\n=== Testing CreateUser (username={username}) ===")
        try:
            request = user_service_pb2.CreateUserRequest(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            response = self.stub.CreateUser(request)
            print(f"Success! Created user: {response.user.username}")
            print(f"  ID: {response.user.id}")
            print(f"  Email: {response.user.email}")
            print(f"  Name: {response.user.first_name} {response.user.last_name}")
            return response.user
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            return None

    def get_user_orders(self, user_id):
        """Test GetUserOrders RPC method"""
        print(f"\n=== Testing GetUserOrders (user_id={user_id}) ===")
        try:
            request = user_service_pb2.GetUserOrdersRequest(user_id=user_id)
            response = self.stub.GetUserOrders(request)
            print(f"Success! Found {len(response.orders)} orders")
            for order in response.orders:
                print(f"  - Order {order.id}: ${order.total_amount} ({order.status})")
                print(f"    Items: {len(order.items)}")
                for item in order.items:
                    print(f"      - {item.product_name}: {item.quantity} x ${item.unit_price}")
            return response.orders
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            return None

    def search_users(self, query, limit=10):
        """Test SearchUsers RPC method"""
        print(f"\n=== Testing SearchUsers (query='{query}', limit={limit}) ===")
        try:
            request = user_service_pb2.SearchUsersRequest(query=query, limit=limit)
            response = self.stub.SearchUsers(request)
            print(f"Success! Found {len(response.users)} users")
            for user in response.users:
                print(f"  - {user.id}: {user.username} ({user.email})")
            return response.users
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            return None

    def bulk_create_users(self, users_data):
        """Test BulkCreateUsers RPC method

        Args:
            users_data: List of dicts with keys: username, email, first_name, last_name
        """
        print(f"\n=== Testing BulkCreateUsers (count={len(users_data)}) ===")
        try:
            users_requests = [
                user_service_pb2.CreateUserRequest(
                    username=user['username'],
                    email=user['email'],
                    first_name=user['first_name'],
                    last_name=user['last_name']
                )
                for user in users_data
            ]
            request = user_service_pb2.BulkCreateUsersRequest(users=users_requests)
            response = self.stub.BulkCreateUsers(request)
            print(f"Success! Created {len(response.users)} users")
            for user in response.users:
                print(f"  - {user.id}: {user.username} ({user.email})")
            return response.users
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            return None


def run_all_tests():
    """Run tests for all UserService RPC methods"""
    print("=" * 60)
    print("UserService gRPC Client - Testing All Methods")
    print("=" * 60)

    client = UserServiceClient()

    try:
        # Test 1: Create a single user
        user1 = client.create_user(
            username="testuser1",
            email="testuser1@example.com",
            first_name="Test",
            last_name="User1"
        )

        # Test 2: Create another user
        user2 = client.create_user(
            username="testuser2",
            email="testuser2@example.com",
            first_name="Test",
            last_name="User2"
        )

        # Test 3: Bulk create users
        bulk_users = [
            {
                "username": "bulkuser1",
                "email": "bulkuser1@example.com",
                "first_name": "Bulk",
                "last_name": "User1"
            },
            {
                "username": "bulkuser2",
                "email": "bulkuser2@example.com",
                "first_name": "Bulk",
                "last_name": "User2"
            },
            {
                "username": "bulkuser3",
                "email": "bulkuser3@example.com",
                "first_name": "Bulk",
                "last_name": "User3"
            }
        ]
        client.bulk_create_users(bulk_users)

        # Test 4: List users
        client.list_users(page=0, size=10)

        # Test 5: Get specific user
        if user1:
            client.get_user(user1.id)

        # Test 6: Search users
        client.search_users(query="test", limit=5)

        # Test 7: Get user orders
        if user1:
            client.get_user_orders(user1.id)

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)

    finally:
        client.close()


if __name__ == "__main__":
    run_all_tests()
