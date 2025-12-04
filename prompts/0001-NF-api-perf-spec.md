# API Performance Testing Project Specification

## Project Overview

This project aims to create a comprehensive performance comparison between three API technologies: gRPC, REST, and GraphQL. The system will consist of a unified React client and three Spring Boot backend services, each implementing the same functionality using different communication protocols.

## Project Structure

```
api-performance-test/
├── client/                    # React frontend application
├── grpc-server/              # Spring Boot gRPC service
├── rest-server/              # Spring Boot REST service
├── graphql-server/           # Spring Boot GraphQL service
└── shared/                   # Shared data models and utilities
```

## System Architecture

### 1. React Client (`client/`)

**Technology Stack:**
- React 18+
- TypeScript
- Axios (for REST calls)
- gRPC-Web (for gRPC calls)
- Apollo Client (for GraphQL calls)
- Chart.js or Recharts (for performance visualization)

**Features:**
- Single-page application with dashboard interface
- Concurrent API call execution
- Real-time performance metrics display
- Comparative charts and tables
- Export results to CSV/JSON

**Metrics to Capture:**
- Response time (latency)
- Payload size (bytes transferred)
- Number of requests
- Success/failure rates
- Time to first byte (TTFB)
- Browser memory consumption

### 2. gRPC Server (`grpc-server/`)

**Technology Stack:**
- Spring Boot 3.x
- gRPC Java
- Protocol Buffers (protobuf)
- Spring Boot Actuator (for metrics)

**Port:** 9090

### 3. REST Server (`rest-server/`)

**Technology Stack:**
- Spring Boot 3.x
- Spring Web MVC
- Jackson (JSON serialization)
- Spring Boot Actuator (for metrics)

**Port:** 8080

### 4. GraphQL Server (`graphql-server/`)

**Technology Stack:**
- Spring Boot 3.x
- Spring for GraphQL
- GraphQL Java
- Spring Boot Actuator (for metrics)

**Port:** 8081

## Common Endpoints/Operations

All three servers must implement the following operations with identical data structures:

### 1. Get User by ID
**Input:** User ID (Long)  
**Output:** User object with fields:
- id: Long
- username: String
- email: String
- firstName: String
- lastName: String
- createdAt: Timestamp
- isActive: Boolean

### 2. List Users (Paginated)
**Input:** 
- page: Integer (default: 0)
- size: Integer (default: 20)

**Output:** List of User objects + metadata:
- users: List<User>
- totalElements: Long
- totalPages: Integer
- currentPage: Integer

### 3. Create User
**Input:** User creation data:
- username: String
- email: String
- firstName: String
- lastName: String

**Output:** Created User object with generated ID

### 4. Get User Orders
**Input:** User ID (Long)  
**Output:** List of Order objects:
- id: Long
- userId: Long
- orderDate: Timestamp
- totalAmount: Decimal
- status: String (PENDING, COMPLETED, CANCELLED)
- items: List<OrderItem>

**OrderItem fields:**
- id: Long
- productName: String
- quantity: Integer
- unitPrice: Decimal

### 5. Search Users
**Input:** Search criteria:
- query: String (searches username, email, firstName, lastName)
- limit: Integer (default: 10)

**Output:** List of matching User objects

### 6. Bulk Create Users
**Input:** List of user creation data (up to 100 users)  
**Output:** List of created User objects

## Data Generation

All servers should use the same seed-based data generation to ensure consistency:
- Pre-generate 10,000 users on startup
- Pre-generate 50,000 orders distributed across users
- Use consistent random seed for reproducibility

## Performance Testing Scenarios

### Test Suite 1: Single Operation Performance
- Execute each operation 100 times sequentially
- Measure average, min, max, p50, p95, p99 latencies
- Record payload sizes

### Test Suite 2: Concurrent Load
- Execute all operations simultaneously
- 10 concurrent users
- 50 concurrent users
- 100 concurrent users
- Measure throughput and response times under load

### Test Suite 3: Data Volume Impact
- Test with varying response sizes:
  - Small: Single user (< 1KB)
  - Medium: 20 users list (~ 10KB)
  - Large: 100 users with orders (~ 100KB)
  - Extra Large: 1000 users with orders (~ 1MB)

### Test Suite 4: Network Simulation
- Test under different network conditions:
  - Fast 3G (750ms RTT, 1.6Mbps down)
  - Slow 3G (2000ms RTT, 400Kbps down)
  - Good 4G (170ms RTT, 9Mbps down)
  - WiFi (28ms RTT, 30Mbps down)

## Server Metrics to Monitor

Each server should expose metrics via Spring Boot Actuator:

1. **JVM Metrics**
   - Heap memory usage
   - Non-heap memory usage
   - Thread count
   - Garbage collection statistics

2. **Application Metrics**
   - Request count
   - Request duration (histogram)
   - Active connections
   - Error rate

3. **System Metrics**
   - CPU usage
   - System memory usage
   - Network I/O

## Client Dashboard Features

### Real-time Performance Panel
- Current request latency for each API
- Live throughput (requests/second)
- Success rate percentage

### Comparison Charts
- Bar chart: Average latency comparison
- Line chart: Latency over time for all APIs
- Pie chart: Payload size distribution
- Stacked bar: Memory consumption

### Results Table
- Sortable columns for all metrics
- Filter by API type
- Export functionality

### Test Controls
- Start/Stop buttons
- Test scenario selector
- Concurrency level slider
- Duration timer

## Implementation Requirements

### All Servers Must:
1. Return identical data structures (semantically equivalent)
2. Implement consistent error handling
3. Use in-memory database (H2) for data storage
4. Include health check endpoints
5. Support CORS for client access
6. Log request/response timing
7. Implement connection pooling

### Client Must:
1. Handle all three protocols correctly
2. Execute tests in parallel threads
3. Aggregate and display results in real-time
4. Store historical test results
5. Provide clear visual comparisons
6. Handle network errors gracefully

## Protocol-Specific Considerations

### gRPC
- Use HTTP/2
- Implement bidirectional streaming for bulk operations
- Define .proto files in `shared/proto/`
- Enable gRPC-Web for browser compatibility

### REST
- Use HTTP/1.1 and HTTP/2
- Follow RESTful conventions
- Implement proper HTTP status codes
- Use JSON for serialization
- Support content negotiation

### GraphQL
- Single endpoint `/graphql`
- Implement DataLoader for N+1 problem prevention
- Support batching
- Enable GraphQL Playground
- Implement pagination with Relay-style connections

## Success Criteria

The project is successful when:
1. All three servers implement identical functionality
2. Client can execute all test scenarios
3. Metrics are accurately captured and displayed
4. Results are reproducible across multiple runs
5. Clear performance differences are observable
6. Documentation includes setup and execution instructions

## Deliverables

1. Source code for all four projects
2. Docker Compose configuration for easy deployment
3. README with setup instructions
4. Performance testing guide
5. Sample performance report with analysis
6. Architecture diagrams

## Testing Protocol

1. Start all three servers
2. Wait for initialization (data generation)
3. Verify health endpoints
4. Run warm-up requests (100 per endpoint)
5. Execute test suite with 5-minute cooldown between scenarios
6. Collect and aggregate results
7. Generate comparison report

## Notes

- All timestamps should use ISO 8601 format
- Decimal values should have precision of 2 decimal places
- Use UTC timezone for all datetime fields
- Implement request/response logging for debugging
- Consider adding distributed tracing (optional enhancement)