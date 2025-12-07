# Testing gRPC GetUser Method Through Envoy Middleware

## Architecture Overview

This guide explains how to test the `GetUser` gRPC method through the Envoy proxy middleware using the Linux terminal.

### Service Architecture

```
Client (Terminal) → Envoy Proxy (8090) → gRPC Server (9090)
```

- **Envoy Proxy**: Listens on port `8090`, routes requests to the backend
- **gRPC Backend**: Runs on `localhost:9090`
- **Service**: `api.performance.UserService`
- **Method**: `GetUser`

### Proto Definition

```protobuf
message GetUserRequest {
  int64 user_id = 1;
}

message GetUserResponse {
  User user = 1;
}

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}
```

## Prerequisites

### Required Tools

1. **grpcurl** - For native gRPC calls
```bash
# Install grpcurl
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
# or via package manager
sudo pacman -S grpcurl  # Arch/Manjaro
```

2. **curl** - For gRPC-Web calls (pre-installed on most Linux systems)

3. **jq** (optional) - For JSON formatting
```bash
sudo pacman -S jq
```

### Verify Services are Running

```bash
# Check if Envoy is running on port 8090
sudo netstat -tlnp | grep 8090

# Check if gRPC server is running on port 9090
sudo netstat -tlnp | grep 9090

# Alternative using ss
ss -tlnp | grep -E '8090|9090'
```

## Method 1: Testing with grpcurl (Recommended)

### Basic GetUser Request

```bash
grpcurl -plaintext \
  -d '{"user_id": 1}' \
  localhost:8090 \
  api.performance.UserService/GetUser
```

**Parameters:**
- `-plaintext`: Use insecure connection (no TLS)
- `-d`: Request data in JSON format
- `localhost:8090`: Envoy proxy address
- `api.performance.UserService/GetUser`: Fully qualified method name

### Expected Response

```json
{
  "user": {
    "id": "1",
    "username": "john_doe",
    "email": "john@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "createdAt": "2024-01-15T10:30:00Z",
    "isActive": true
  }
}
```

### Test Different User IDs

```bash
# Test user ID 2
grpcurl -plaintext \
  -d '{"user_id": 2}' \
  localhost:8090 \
  api.performance.UserService/GetUser

# Test user ID 100
grpcurl -plaintext \
  -d '{"user_id": 100}' \
  localhost:8090 \
  api.performance.UserService/GetUser
```

### List Available Services

```bash
# List all services
grpcurl -plaintext localhost:8090 list

# List methods in UserService
grpcurl -plaintext localhost:8090 list api.performance.UserService

# Describe the GetUser method
grpcurl -plaintext localhost:8090 describe api.performance.UserService.GetUser
```

### Using Proto Files (Alternative)

If reflection is not enabled, specify the proto file:

```bash
grpcurl -plaintext \
  -proto shared/proto/user_service.proto \
  -d '{"user_id": 1}' \
  localhost:8090 \
  api.performance.UserService/GetUser
```

## Method 2: Testing with curl (gRPC-Web)

Envoy is configured with the gRPC-Web filter, allowing HTTP/1.1 clients to communicate with gRPC services.

### Using curl with JSON

```bash
curl -X POST http://localhost:8090/api.performance.UserService/GetUser \
  -H "Content-Type: application/grpc-web+json" \
  -H "Accept: application/grpc-web+json" \
  -d '{"user_id": 1}'
```

### Format Response with jq

```bash
curl -s -X POST http://localhost:8090/api.performance.UserService/GetUser \
  -H "Content-Type: application/grpc-web+json" \
  -H "Accept: application/grpc-web+json" \
  -d '{"user_id": 1}' | jq '.'
```

### Test with Binary Format (gRPC-Web+proto)

```bash
curl -X POST http://localhost:8090/api.performance.UserService/GetUser \
  -H "Content-Type: application/grpc-web+proto" \
  -H "Accept: application/grpc-web+proto" \
  --data-binary @request.bin \
  --output response.bin
```

## Method 3: Using Python grpcio Client

### Python Script Example

```bash
# Navigate to python client directory
cd python-grpc-client

# Activate virtual environment
source .venv/bin/activate

# Create test script
cat > test_getuser.py << 'EOF'
import grpc
import user_service_pb2
import user_service_pb2_grpc

def test_get_user(user_id):
    # Connect to Envoy proxy
    with grpc.insecure_channel('localhost:8090') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)

        # Create request
        request = user_service_pb2.GetUserRequest(user_id=user_id)

        # Make the call
        try:
            response = stub.GetUser(request)
            print(f"User ID: {response.user.id}")
            print(f"Username: {response.user.username}")
            print(f"Email: {response.user.email}")
            print(f"Name: {response.user.first_name} {response.user.last_name}")
            print(f"Active: {response.user.is_active}")
            print(f"Created: {response.user.created_at}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    test_get_user(1)
EOF

# Run the test
python test_getuser.py
```

## Monitoring and Debugging

### Check Envoy Admin Interface

```bash
# View Envoy stats
curl http://localhost:9901/stats

# View cluster information
curl http://localhost:9901/clusters

# View configuration
curl http://localhost:9901/config_dump
```

### Enable Verbose Output

```bash
# grpcurl with verbose output
grpcurl -plaintext -v \
  -d '{"user_id": 1}' \
  localhost:8090 \
  api.performance.UserService/GetUser
```

### Monitor Envoy Logs

```bash
# If running Envoy in Docker
docker logs -f envoy

# If running as systemd service
journalctl -u envoy -f
```

## Troubleshooting

### Connection Refused

```bash
# Error: Failed to dial target host "localhost:8090"
# Solution: Verify Envoy is running
ps aux | grep envoy
sudo netstat -tlnp | grep 8090
```

### Service Not Found

```bash
# Error: Service not found
# Solution: Check if gRPC server reflection is enabled
grpcurl -plaintext localhost:8090 list

# If reflection is not available, use -proto flag
grpcurl -plaintext -proto shared/proto/user_service.proto ...
```

### Timeout Errors

```bash
# Error: DeadlineExceeded
# Solution: Check if backend gRPC server is running
curl http://localhost:9901/clusters | grep grpc_backend

# Increase timeout (Envoy config: timeout: 60s)
```

### CORS Errors (when testing from browser)

The Envoy configuration allows CORS with these settings:
- Origins: `*`
- Methods: `GET, PUT, DELETE, POST, OPTIONS`
- Headers: Includes gRPC-Web specific headers

## Performance Testing

### Load Testing with grpcurl

```bash
# Install ghz for load testing
go install github.com/bojand/ghz/cmd/ghz@latest

# Run load test
ghz --insecure \
  --proto shared/proto/user_service.proto \
  --call api.performance.UserService.GetUser \
  -d '{"user_id": 1}' \
  -n 1000 \
  -c 10 \
  localhost:8090
```

### Benchmark Script

```bash
#!/bin/bash
# benchmark_getuser.sh

echo "Running GetUser benchmark through Envoy..."
for i in {1..100}; do
    time grpcurl -plaintext \
      -d "{\"user_id\": $((RANDOM % 100 + 1))}" \
      localhost:8090 \
      api.performance.UserService/GetUser > /dev/null 2>&1
done
```

## Security Considerations

### TLS Configuration (Production)

For production, modify Envoy to use TLS:

```bash
# Test with TLS (when configured)
grpcurl \
  -cacert /path/to/ca.crt \
  -d '{"user_id": 1}' \
  localhost:8090 \
  api.performance.UserService/GetUser
```

### Authentication Headers

```bash
# Add authentication token
grpcurl -plaintext \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"user_id": 1}' \
  localhost:8090 \
  api.performance.UserService/GetUser
```

## Quick Reference

### Common Commands

```bash
# Basic GetUser call
grpcurl -plaintext -d '{"user_id": 1}' localhost:8090 api.performance.UserService/GetUser

# List all services
grpcurl -plaintext localhost:8090 list

# Check Envoy health
curl http://localhost:9901/ready

# View Envoy stats
curl http://localhost:9901/stats/prometheus

# Test with curl (gRPC-Web)
curl -X POST http://localhost:8090/api.performance.UserService/GetUser \
  -H "Content-Type: application/grpc-web+json" \
  -d '{"user_id": 1}'
```

### Port Reference

- `8090` - Envoy proxy listener (client-facing)
- `9090` - gRPC backend server
- `9901` - Envoy admin interface

## Additional Resources

- [gRPC Documentation](https://grpc.io/docs/)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs/envoy/latest/)
- [grpcurl GitHub](https://github.com/fullstorydev/grpcurl)
- [gRPC-Web Protocol](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md)
