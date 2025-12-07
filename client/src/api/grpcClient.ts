/**
 * gRPC Client for User Service
 *
 * This module provides a wrapper around the generated gRPC-Web client for the UserService.
 * It handles conversion between protobuf messages and TypeScript types.
 *
 * Usage:
 *   import { grpcApi } from './api/grpcClient';
 *
 *   const user = await grpcApi.getUser(1);
 *   const users = await grpcApi.listUsers(0, 20);
 *   const newUser = await grpcApi.createUser({ username: 'test', email: 'test@example.com', ... });
 *
 * Prerequisites:
 * - Envoy proxy must be running on port 8090 (connects to gRPC server on port 9090)
 * - gRPC server must be running
 *
 * To start Envoy proxy:
 *   docker run -d -v "$(pwd)/../envoy.yaml:/etc/envoy/envoy.yaml:ro" \
 *     -p 8090:8090 -p 9901:9901 envoyproxy/envoy:v1.28-latest
 */

import { User, PagedUsers, Order, CreateUserRequest, OrderItem } from '../types';
import { UserServiceClient } from '../generated/User_serviceServiceClientPb';
import * as user_service_pb from '../generated/user_service_pb';

const GRPC_BASE_URL = 'http://localhost:8090';

class GrpcClientWrapper {
  private client: UserServiceClient;

  constructor(baseUrl: string) {
    this.client = new UserServiceClient(baseUrl, null, null);
  }

  // Helper to convert proto timestamp to Date
  private timestampToDate(timestamp: any): string {
    if (!timestamp) return new Date().toISOString();
    return new Date(timestamp.getSeconds() * 1000).toISOString();
  }

  // Helper to convert proto User to our User type
  private convertUser(protoUser: user_service_pb.User): User {
    return {
      id: protoUser.getId(),
      username: protoUser.getUsername(),
      email: protoUser.getEmail(),
      firstName: protoUser.getFirstName(),
      lastName: protoUser.getLastName(),
      createdAt: this.timestampToDate(protoUser.getCreatedAt()),
      isActive: protoUser.getIsActive(),
    };
  }

  // Helper to convert proto OrderItem to our OrderItem type
  private convertOrderItem(protoItem: user_service_pb.OrderItem): OrderItem {
    return {
      id: protoItem.getId(),
      productName: protoItem.getProductName(),
      quantity: protoItem.getQuantity(),
      unitPrice: parseFloat(protoItem.getUnitPrice()),
    };
  }

  // Helper to convert proto Order to our Order type
  private convertOrder(protoOrder: user_service_pb.Order): Order {
    return {
      id: protoOrder.getId(),
      userId: protoOrder.getUserId(),
      orderDate: this.timestampToDate(protoOrder.getOrderDate()),
      totalAmount: parseFloat(protoOrder.getTotalAmount()),
      status: protoOrder.getStatus(),
      items: protoOrder.getItemsList().map(item => this.convertOrderItem(item)),
    };
  }

  async getUser(id: number): Promise<User> {
    const request = new user_service_pb.GetUserRequest();
    request.setUserId(id);

    const response = await this.client.getUser(request, {});
    const protoUser = response.getUser();

    if (!protoUser) {
      throw new Error('User not found');
    }

    return this.convertUser(protoUser);
  }

  async listUsers(page: number = 0, size: number = 20): Promise<PagedUsers> {
    const request = new user_service_pb.ListUsersRequest();
    request.setPage(page);
    request.setSize(size);

    const response = await this.client.listUsers(request, {});

    return {
      users: response.getUsersList().map(user => this.convertUser(user)),
      totalElements: response.getTotalElements(),
      totalPages: response.getTotalPages(),
      currentPage: response.getCurrentPage(),
    };
  }

  async createUser(user: CreateUserRequest): Promise<User> {
    const request = new user_service_pb.CreateUserRequest();
    request.setUsername(user.username);
    request.setEmail(user.email);
    request.setFirstName(user.firstName);
    request.setLastName(user.lastName);

    const response = await this.client.createUser(request, {});
    const protoUser = response.getUser();

    if (!protoUser) {
      throw new Error('Failed to create user');
    }

    return this.convertUser(protoUser);
  }

  async getUserOrders(userId: number): Promise<Order[]> {
    const request = new user_service_pb.GetUserOrdersRequest();
    request.setUserId(userId);

    const response = await this.client.getUserOrders(request, {});

    return response.getOrdersList().map(order => this.convertOrder(order));
  }

  async searchUsers(query: string, limit: number = 10): Promise<User[]> {
    const request = new user_service_pb.SearchUsersRequest();
    request.setQuery(query);
    request.setLimit(limit);

    const response = await this.client.searchUsers(request, {});

    return response.getUsersList().map(user => this.convertUser(user));
  }

  async bulkCreateUsers(users: CreateUserRequest[]): Promise<User[]> {
    const request = new user_service_pb.BulkCreateUsersRequest();

    const protoUsers = users.map(user => {
      const protoUser = new user_service_pb.CreateUserRequest();
      protoUser.setUsername(user.username);
      protoUser.setEmail(user.email);
      protoUser.setFirstName(user.firstName);
      protoUser.setLastName(user.lastName);
      return protoUser;
    });

    request.setUsersList(protoUsers);

    const response = await this.client.bulkCreateUsers(request, {});

    return response.getUsersList().map(user => this.convertUser(user));
  }

  getResponseSize(response: any): number {
    // For gRPC, we can use the serialized binary size
    if (response && typeof response.serializeBinary === 'function') {
      return response.serializeBinary().length;
    }
    return new Blob([JSON.stringify(response)]).size;
  }
}

export const grpcApi = new GrpcClientWrapper(GRPC_BASE_URL);
