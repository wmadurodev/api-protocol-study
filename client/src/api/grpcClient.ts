import { User, PagedUsers, Order, CreateUserRequest } from '../types';

// gRPC-Web client will be imported from generated code
// For now, this is a placeholder implementation that shows the structure

const GRPC_BASE_URL = 'http://localhost:8090';

// Note: This implementation requires generated TypeScript code from proto files
// Run './generate-proto.sh' to generate the required client code

// Placeholder for the generated UserServiceClient
// import { UserServiceClient } from '../generated/user_service_grpc_web_pb';
// import * as user_service_pb from '../generated/user_service_pb';

// For now, we'll create a mock implementation
class GrpcClientWrapper {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  // Helper to convert proto timestamp to Date
  private timestampToDate(timestamp: any): string {
    if (!timestamp) return new Date().toISOString();
    return new Date(timestamp.seconds * 1000).toISOString();
  }

  // Helper to convert proto User to our User type
  private convertUser(protoUser: any): User {
    return {
      id: protoUser.id?.toString() || '0',
      username: protoUser.username || '',
      email: protoUser.email || '',
      firstName: protoUser.firstName || protoUser.first_name || '',
      lastName: protoUser.lastName || protoUser.last_name || '',
      createdAt: this.timestampToDate(protoUser.createdAt || protoUser.created_at),
      isActive: protoUser.isActive ?? protoUser.is_active ?? true,
    };
  }

  async getUser(id: number): Promise<User> {
    // This is a placeholder - actual implementation will use generated gRPC client
    // const request = new user_service_pb.GetUserRequest();
    // request.setUserId(id);
    // const response = await this.client.getUser(request, {});
    // return this.convertUser(response.getUser());

    throw new Error(
      'gRPC client not yet configured. Please:\n' +
      '1. Run ./generate-proto.sh to generate client code\n' +
      '2. Start Envoy proxy: docker run -d -v "$(pwd)/envoy.yaml:/etc/envoy/envoy.yaml:ro" ' +
      '-p 8090:8090 -p 9901:9901 envoyproxy/envoy:v1.28-latest\n' +
      '3. Ensure gRPC server is running on port 9090'
    );
  }

  async listUsers(page: number = 0, size: number = 20): Promise<PagedUsers> {
    throw new Error('gRPC client not yet configured. See getUser() error for setup instructions.');
  }

  async createUser(user: CreateUserRequest): Promise<User> {
    throw new Error('gRPC client not yet configured. See getUser() error for setup instructions.');
  }

  async getUserOrders(userId: number): Promise<Order[]> {
    throw new Error('gRPC client not yet configured. See getUser() error for setup instructions.');
  }

  async searchUsers(query: string, limit: number = 10): Promise<User[]> {
    throw new Error('gRPC client not yet configured. See getUser() error for setup instructions.');
  }

  async bulkCreateUsers(users: CreateUserRequest[]): Promise<User[]> {
    throw new Error('gRPC client not yet configured. See getUser() error for setup instructions.');
  }

  getResponseSize(response: any): number {
    return new Blob([JSON.stringify(response)]).size;
  }
}

export const grpcApi = new GrpcClientWrapper(GRPC_BASE_URL);

/*
 * SETUP INSTRUCTIONS:
 *
 * 1. Install protoc compiler:
 *    - Mac: brew install protobuf
 *    - Linux: apt-get install protobuf-compiler
 *    - Or download from: https://github.com/protocolbuffers/protobuf/releases
 *
 * 2. Install protoc-gen-grpc-web plugin:
 *    - Download from: https://github.com/grpc/grpc-web/releases
 *    - Make it executable and add to PATH
 *
 * 3. Generate TypeScript client code:
 *    chmod +x generate-proto.sh
 *    ./generate-proto.sh
 *
 * 4. Install npm dependencies:
 *    npm install
 *
 * 5. Start Envoy proxy (required for browser to gRPC communication):
 *    docker run -d -v "$(pwd)/../envoy.yaml:/etc/envoy/envoy.yaml:ro" \
 *      -p 8090:8090 -p 9901:9901 envoyproxy/envoy:v1.28-latest
 *
 * 6. Start the gRPC server:
 *    cd ../grpc-server && mvn spring-boot:run
 *
 * 7. Update this file to use the generated client code (uncomment imports above)
 */
