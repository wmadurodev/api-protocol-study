import axios from 'axios';
import { User, PagedUsers, Order, CreateUserRequest } from '../types';

const REST_BASE_URL = 'http://localhost:8080/api';

const restClient = axios.create({
  baseURL: REST_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const restApi = {
  async getUser(id: number): Promise<User> {
    const response = await restClient.get<User>(`/users/${id}`);
    return response.data;
  },

  async listUsers(page: number = 0, size: number = 20): Promise<PagedUsers> {
    const response = await restClient.get<PagedUsers>('/users', {
      params: { page, size },
    });
    return response.data;
  },

  async createUser(user: CreateUserRequest): Promise<User> {
    const response = await restClient.post<User>('/users', user);
    return response.data;
  },

  async getUserOrders(userId: number): Promise<Order[]> {
    const response = await restClient.get<Order[]>(`/users/${userId}/orders`);
    return response.data;
  },

  async searchUsers(query: string, limit: number = 10): Promise<User[]> {
    const response = await restClient.get<User[]>('/users/search', {
      params: { query, limit },
    });
    return response.data;
  },

  async bulkCreateUsers(users: CreateUserRequest[]): Promise<User[]> {
    const response = await restClient.post<User[]>('/users/bulk', users);
    return response.data;
  },

  getResponseSize(response: any): number {
    return new Blob([JSON.stringify(response)]).size;
  },
};
