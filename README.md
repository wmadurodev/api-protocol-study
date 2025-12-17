# API Performance Testing Project

A comprehensive performance comparison system for REST, gRPC, and GraphQL APIs built with Spring Boot backends and a React TypeScript frontend.

## Project Overview

This project implements the same functionality across three different API technologies to enable direct performance comparisons:

- **gRPC Server** (Port 9090) - Protocol Buffers with HTTP/2
- **REST Server** (Port 8080) - JSON over HTTP/1.1
- **GraphQL Server** (Port 8081) - GraphQL with single endpoint
- **React Client** (Port 3000) - Performance testing dashboard
- **Python gRPC Client** - Standalone Python client for gRPC testing and automation
- **Performance Scripts** - Parallel performance testing tools for REST vs gRPC comparison

## Project Structure

```
api-performance-test/
├── client/                    # React TypeScript frontend
│   ├── src/
│   │   ├── api/              # API client implementations
│   │   ├── components/       # React components
│   │   ├── types/            # TypeScript type definitions
│   │   └── utils/            # Utility functions
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── grpc-server/              # Spring Boot gRPC service
│   ├── src/main/java/
│   ├── pom.xml
│   └── Dockerfile
├── rest-server/              # Spring Boot REST service
│   ├── src/main/java/
│   ├── pom.xml
│   └── Dockerfile
├── graphql-server/           # Spring Boot GraphQL service
│   ├── src/main/java/
│   ├── pom.xml
│   └── Dockerfile
├── python-grpc-client/       # Python gRPC client for testing
│   ├── client.py             # Client implementation
│   ├── generate_grpc.sh      # gRPC code generation script
│   ├── requirements.txt
│   └── README.md
├── scripts/                  # Performance testing scripts
│   ├── parallel_perf_test.py # Parallel REST vs gRPC testing
│   └── README.md
├── shared/                   # Shared data models
│   └── proto/                # Protocol Buffer definitions
├── docker-compose.yml        # Docker orchestration
└── README.md
```

## Features

### Common Operations

All three servers implement identical operations:

1. **Get User by ID** - Retrieve a single user
2. **List Users** - Paginated user listing (default: 20 per page)
3. **Create User** - Create a new user
4. **Get User Orders** - Retrieve all orders for a user
5. **Search Users** - Search users by query string
6. **Bulk Create Users** - Create multiple users at once

### Data Generation

Each server pre-generates consistent test data on startup:
- **10,000 users** with random names and emails
- **50,000 orders** distributed across users
- Consistent seed (12345) ensures reproducibility

### Performance Metrics

The client tracks and displays:
- Response time (latency in ms)
- Payload size (bytes)
- Success/failure rates
- Min/Max/Average statistics
- Real-time metrics visualization

## Prerequisites

### For Local Development

- **Java 17+** (for Spring Boot servers)
- **Maven 3.9+** (for building Spring Boot projects)
- **Node.js 18+** (for React client)
- **npm** or **yarn** (for JavaScript dependencies)

### For Docker Deployment

- **Docker 20.10+**
- **Docker Compose 2.0+**

## Quick Start with Docker

The easiest way to run the entire system:

```bash
# Clone the repository
cd /home/maduro/repo-study/data-protocol

# Start all services
docker-compose up --build

# Services will be available at:
# - REST API: http://localhost:8080
# - GraphQL API: http://localhost:8081
# - gRPC API: localhost:9090
# - Client Dashboard: http://localhost:3000
```

Wait for all services to initialize (data generation takes ~10 seconds), then open http://localhost:3000 in your browser.

## Local Development Setup

### 1. Start the gRPC Server

```bash
cd grpc-server
mvn clean install
mvn spring-boot:run
```

Server starts on port 9090.

### 2. Start the REST Server

```bash
cd rest-server
mvn clean install
mvn spring-boot:run
```

Server starts on port 8080.

### 3. Start the GraphQL Server

```bash
cd graphql-server
mvn clean install
mvn spring-boot:run
```

Server starts on port 8081. GraphiQL playground available at http://localhost:8081/graphiql

### 4. Start the React Client

```bash
cd client
npm install
npm start
```

Client starts on port 3000.

## Testing the APIs

### REST API Examples

```bash
# Get user by ID
curl http://localhost:8080/api/users/1

# List users (paginated)
curl http://localhost:8080/api/users?page=0&size=20

# Create user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","firstName":"Test","lastName":"User"}'

# Get user orders
curl http://localhost:8080/api/users/1/orders

# Search users
curl "http://localhost:8080/api/users/search?query=john&limit=10"
```

### GraphQL API Examples

```bash
# Query user by ID
curl -X POST http://localhost:8081/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"query { user(id: 1) { id username email firstName lastName } }"}'

# List users
curl -X POST http://localhost:8081/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"query { listUsers(page: 0, size: 20) { users { id username } totalElements } }"}'

# Create user mutation
curl -X POST http://localhost:8081/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { createUser(input: {username: \"test\", email: \"test@example.com\", firstName: \"Test\", lastName: \"User\"}) { id username } }"}'
```

## Using the Performance Dashboard

1. Open http://localhost:3000 in your browser
2. Select an API type (REST or GraphQL)
3. Choose an operation to test
4. Set the number of iterations
5. Click "Run Test" to execute
6. View real-time metrics and statistics
7. Use "Run All Tests" to compare all APIs across all operations
8. Export results for further analysis

## Additional Testing Tools

### Python gRPC Client

A standalone Python client for testing the gRPC server with all 6 RPC methods. This provides a programmatic way to interact with the gRPC service outside of the web dashboard, useful for automation, scripting, and command-line testing.

See [python-grpc-client/README.md](python-grpc-client/README.md) for detailed usage instructions, including:
- Setup and dependency installation
- Generating gRPC Python code from proto files
- Using the client programmatically or running automated tests
- All 6 RPC method examples (CreateUser, BulkCreateUsers, ListUsers, GetUser, SearchUsers, GetUserOrders)

### Performance Testing Scripts

High-performance parallel testing scripts for comparing REST and gRPC server performance. These scripts execute concurrent requests and provide detailed metrics, percentiles, and comparative analysis between protocols.

See [scripts/README.md](scripts/README.md) for comprehensive documentation, including:
- Running parallel performance tests with configurable request counts
- Exporting results in JSON or CSV formats
- Metrics collected (latency, throughput, payload size, percentiles)
- Integration with CI/CD pipelines
- Advanced configuration options

## Performance Testing Protocol

For consistent results:

1. Start all servers
2. Wait 30 seconds for initialization
3. Run warm-up requests (100 per endpoint)
4. Execute test suite
5. Allow 5-minute cooldown between scenarios
6. Repeat tests 3 times and average results

## Architecture Highlights

### gRPC Server
- Protocol Buffers for efficient serialization
- HTTP/2 for multiplexing
- Binary protocol reduces payload size
- Strongly-typed service definitions

### REST Server
- Standard HTTP/1.1 with JSON
- RESTful resource-based URLs
- Content negotiation support
- CORS enabled for browser access

### GraphQL Server
- Single `/graphql` endpoint
- Client-specified queries reduce over-fetching
- Strongly-typed schema
- DataLoader pattern for N+1 prevention

### React Client
- TypeScript for type safety
- Axios for REST calls
- Apollo Client for GraphQL
- Real-time performance tracking
- Responsive dashboard UI

## Health Checks

All servers expose health endpoints via Spring Boot Actuator:

```bash
# Check server health
curl http://localhost:8080/actuator/health  # REST
curl http://localhost:8081/actuator/health  # GraphQL
curl http://localhost:9090/actuator/health  # gRPC (via HTTP)

# View metrics
curl http://localhost:8080/actuator/metrics
```

## Troubleshooting

### Servers won't start

- Ensure ports 8080, 8081, 9090, 3000 are not in use
- Check Java version: `java -version` (requires 17+)
- Check Maven version: `mvn -version` (requires 3.9+)

### Client can't connect to servers

- Verify all servers are running and healthy
- Check CORS configuration if running locally
- Ensure firewall isn't blocking ports

### Data generation is slow

- Data generation on startup takes ~10 seconds
- Monitor logs for "Data generation completed" message
- Increase JVM heap if needed: `-Xmx2g`

## Performance Considerations

- **gRPC** typically shows lower latency and smaller payloads
- **REST** has wider tooling support and HTTP caching
- **GraphQL** reduces over-fetching but adds query parsing overhead
- Network conditions significantly impact relative performance
- Test with realistic data volumes for your use case

## Future Enhancements

- Add gRPC-Web support for browser-native gRPC
- Implement WebSocket/SSE for real-time updates
- Add distributed tracing with OpenTelemetry
- Include memory and CPU profiling
- Add automated benchmark reports
- Implement authentication/authorization
- Add more complex nested queries
- Support for batching operations

## License

This project is provided as-is for educational and testing purposes.

## Contributing

This is a demonstration project. Feel free to fork and customize for your needs.

## Support

For issues or questions, please review the troubleshooting section or check server logs for detailed error messages.
