import { ApolloClient, InMemoryCache, gql, HttpLink } from '@apollo/client';
import { User, PagedUsers, Order, CreateUserRequest } from '../types';

const GRAPHQL_BASE_URL = 'http://localhost:8081/graphql';

const httpLink = new HttpLink({
  uri: GRAPHQL_BASE_URL,
});

const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'no-cache',
    },
    query: {
      fetchPolicy: 'no-cache',
    },
  },
});

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      username
      email
      firstName
      lastName
      createdAt
      isActive
    }
  }
`;

const LIST_USERS = gql`
  query ListUsers($page: Int, $size: Int) {
    listUsers(page: $page, size: $size) {
      users {
        id
        username
        email
        firstName
        lastName
        createdAt
        isActive
      }
      totalElements
      totalPages
      currentPage
    }
  }
`;

const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      username
      email
      firstName
      lastName
      createdAt
      isActive
    }
  }
`;

const GET_USER_ORDERS = gql`
  query GetUserOrders($userId: ID!) {
    userOrders(userId: $userId) {
      id
      userId
      orderDate
      totalAmount
      status
      items {
        id
        productName
        quantity
        unitPrice
      }
    }
  }
`;

const SEARCH_USERS = gql`
  query SearchUsers($query: String!, $limit: Int) {
    searchUsers(query: $query, limit: $limit) {
      id
      username
      email
      firstName
      lastName
      createdAt
      isActive
    }
  }
`;

const BULK_CREATE_USERS = gql`
  mutation BulkCreateUsers($inputs: [CreateUserInput!]!) {
    bulkCreateUsers(inputs: $inputs) {
      id
      username
      email
      firstName
      lastName
      createdAt
      isActive
    }
  }
`;

export const graphqlApi = {
  async getUser(id: number): Promise<User> {
    const result = await apolloClient.query({
      query: GET_USER,
      variables: { id: id.toString() },
    });
    return result.data.user;
  },

  async listUsers(page: number = 0, size: number = 20): Promise<PagedUsers> {
    const result = await apolloClient.query({
      query: LIST_USERS,
      variables: { page, size },
    });
    return result.data.listUsers;
  },

  async createUser(user: CreateUserRequest): Promise<User> {
    const result = await apolloClient.mutate({
      mutation: CREATE_USER,
      variables: { input: user },
    });
    return result.data.createUser;
  },

  async getUserOrders(userId: number): Promise<Order[]> {
    const result = await apolloClient.query({
      query: GET_USER_ORDERS,
      variables: { userId: userId.toString() },
    });
    return result.data.userOrders;
  },

  async searchUsers(query: string, limit: number = 10): Promise<User[]> {
    const result = await apolloClient.query({
      query: SEARCH_USERS,
      variables: { query, limit },
    });
    return result.data.searchUsers;
  },

  async bulkCreateUsers(users: CreateUserRequest[]): Promise<User[]> {
    const result = await apolloClient.mutate({
      mutation: BULK_CREATE_USERS,
      variables: { inputs: users },
    });
    return result.data.bulkCreateUsers;
  },

  getResponseSize(response: any): number {
    return new Blob([JSON.stringify(response)]).size;
  },
};
