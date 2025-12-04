export interface User {
  id: string | number;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  createdAt: string;
  isActive: boolean;
}

export interface OrderItem {
  id: string | number;
  productName: string;
  quantity: number;
  unitPrice: number;
}

export interface Order {
  id: string | number;
  userId: string | number;
  orderDate: string;
  totalAmount: number;
  status: string;
  items: OrderItem[];
}

export interface PagedUsers {
  users: User[];
  totalElements: number;
  totalPages: number;
  currentPage: number;
}

export interface CreateUserRequest {
  username: string;
  email: string;
  firstName: string;
  lastName: string;
}

export interface PerformanceMetrics {
  apiType: 'REST' | 'gRPC' | 'GraphQL';
  operation: string;
  responseTime: number;
  payloadSize: number;
  timestamp: number;
  success: boolean;
  errorMessage?: string;
}

export interface TestResults {
  [key: string]: {
    count: number;
    totalTime: number;
    avgTime: number;
    minTime: number;
    maxTime: number;
    successRate: number;
    avgPayloadSize: number;
  };
}
