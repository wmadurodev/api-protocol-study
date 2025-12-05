# gRPC Client Setup Guide

This guide explains how to set up and use the gRPC client for testing the gRPC server from the browser-based React client.

## Why gRPC-Web is Needed

Browsers cannot directly communicate with gRPC servers because:
- gRPC uses HTTP/2 features that browsers don't expose
- gRPC requires bidirectional streaming over HTTP/2

**Solution**: Use **gRPC-Web** with an **Envoy proxy** that translates browser requests to gRPC calls.

## Architecture

```
Browser Client (React)  →  Envoy Proxy (port 8090)  →  gRPC Server (port 9090)
     (gRPC-Web)                (HTTP/1.1 → HTTP/2)           (gRPC)
```

## Setup Steps

### 1. Install Dependencies

```bash
cd client
npm install
```

This will install:
- `grpc-web`: gRPC-Web client library
- `google-protobuf`: Protocol Buffers runtime

### 2. Install Protocol Buffer Compiler

You need `protoc` and `protoc-gen-grpc-web` to generate TypeScript client code.

**Mac:**
```bash
brew install protobuf

# Download protoc-gen-grpc-web
wget https://github.com/grpc/grpc-web/releases/download/1.4.2/protoc-gen-grpc-web-1.4.2-darwin-x86_64
chmod +x protoc-gen-grpc-web-1.4.2-darwin-x86_64
sudo mv protoc-gen-grpc-web-1.4.2-darwin-x86_64 /usr/local/bin/protoc-gen-grpc-web
```

**Linux:**
```bash
sudo apt-get install protobuf-compiler

# Download protoc-gen-grpc-web
wget https://github.com/grpc/grpc-web/releases/download/1.4.2/protoc-gen-grpc-web-1.4.2-linux-x86_64
chmod +x protoc-gen-grpc-web-1.4.2-linux-x86_64
sudo mv protoc-gen-grpc-web-1.4.2-linux-x86_64 /usr/local/bin/protoc-gen-grpc-web
```

### 3. Generate TypeScript Client Code

```bash
cd client
chmod +x generate-proto.sh
./generate-proto.sh
```

This generates TypeScript client code from the proto files in `client/src/generated/`.

### 4. Update grpcClient.ts

After generating the code, update `client/src/api/grpcClient.ts` to import and use the generated client:

```typescript
import { UserServiceClient } from '../generated/user_service_grpc_web_pb';
import * as user_service_pb from '../generated/user_service_pb';
```

Then implement the actual gRPC calls using the generated client (replace the placeholder implementation).

### 5. Start the Services

**Option A: Using Docker Compose (Recommended)**

```bash
# From the project root
docker-compose up -d
```

This starts:
- gRPC Server (port 9090)
- REST Server (port 8080)
- GraphQL Server (port 8081)
- Envoy Proxy (port 8090, 9901)
- React Client (port 3000)

**Option B: Manual Start**

```bash
# Terminal 1: Start gRPC Server
cd grpc-server
mvn spring-boot:run

# Terminal 2: Start Envoy Proxy
docker run -d -v "$(pwd)/envoy.yaml:/etc/envoy/envoy.yaml:ro" \\
  -p 8090:8090 -p 9901:9901 \\
  --network host \\
  envoyproxy/envoy:v1.28-latest

# Terminal 3: Start React Client
cd client
npm start
```

### 6. Test gRPC Client

Open the React app at `http://localhost:3000` and select "gRPC" as the API type in the performance tester.

## Ports

- **9090**: gRPC Server (backend, not directly accessible from browser)
- **8090**: Envoy Proxy (gRPC-Web, accessible from browser)
- **9901**: Envoy Admin Interface
- **3000**: React Client
- **8080**: REST Server
- **8081**: GraphQL Server

## Troubleshooting

### Error: "gRPC client not yet configured"

This means you haven't generated the TypeScript client code yet. Follow steps 2-4 above.

### Error: "Failed to fetch" or CORS error

Check that:
1. Envoy proxy is running: `docker ps | grep envoy`
2. gRPC server is running: `curl localhost:9090/actuator/health`
3. Envoy can reach the gRPC server (check network connectivity)

### Check Envoy Status

```bash
# View Envoy logs
docker logs <envoy-container-id>

# Access Envoy admin interface
curl localhost:9901/stats
```

### Debug gRPC Server

```bash
# Check if gRPC server is running
curl localhost:9090/actuator/health

# View gRPC server logs
cd grpc-server
mvn spring-boot:run
```

## Generated Code Structure

After running `generate-proto.sh`, you'll have:

```
client/src/generated/
├── user_service_pb.js          # Protocol Buffer messages
├── user_service_pb.d.ts        # TypeScript types for messages
├── user_service_grpc_web_pb.js # gRPC-Web client
└── user_service_grpc_web_pb.d.ts # TypeScript types for client
```

## Next Steps

1. Complete the implementation in `grpcClient.ts` using the generated code
2. Test all gRPC operations: getUser, listUsers, createUser, etc.
3. Compare performance between REST, GraphQL, and gRPC in the dashboard

## Resources

- [gRPC-Web Documentation](https://github.com/grpc/grpc-web)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs/envoy/latest/)
- [Protocol Buffers Documentation](https://developers.google.com/protocol-buffers)
