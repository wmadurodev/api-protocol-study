# gRPC Client Quick Start

## Problem
The client had no gRPC support - only REST and GraphQL were implemented. Browsers cannot directly call gRPC servers.

## Solution
Added gRPC-Web support with Envoy proxy as a translator.

## Quick Setup (3 Steps)

### 1. Install Tools & Generate Client Code

```bash
# Install protoc (Mac)
brew install protobuf

# Or Linux
sudo apt-get install protobuf-compiler

# Download protoc-gen-grpc-web plugin
# Mac:
wget https://github.com/grpc/grpc-web/releases/download/1.4.2/protoc-gen-grpc-web-1.4.2-darwin-x86_64
chmod +x protoc-gen-grpc-web-1.4.2-darwin-x86_64
sudo mv protoc-gen-grpc-web-1.4.2-darwin-x86_64 /usr/local/bin/protoc-gen-grpc-web

# Linux:
wget https://github.com/grpc/grpc-web/releases/download/1.4.2/protoc-gen-grpc-web-1.4.2-linux-x86_64
chmod +x protoc-gen-grpc-web-1.4.2-linux-x86_64
sudo mv protoc-gen-grpc-web-1.4.2-linux-x86_64 /usr/local/bin/protoc-gen-grpc-web

# Generate TypeScript client code
cd client
npm install
./generate-proto.sh
```

### 2. Start Services

```bash
# Start gRPC server
cd grpc-server
mvn spring-boot:run

# In another terminal, start Envoy proxy
docker run -d \\
  -v "$(pwd)/../envoy.yaml:/etc/envoy/envoy.yaml:ro" \\
  -p 8090:8090 -p 9901:9901 \\
  --network host \\
  envoyproxy/envoy:v1.28-latest
```

### 3. Complete the Implementation

Edit `client/src/api/grpcClient.ts` and uncomment the imports to use the generated code:

```typescript
import { UserServiceClient } from '../generated/user_service_grpc_web_pb';
import * as user_service_pb from '../generated/user_service_pb';
```

Then replace the placeholder methods with actual gRPC-Web calls.

## Alternative: Use Docker Compose

```bash
docker-compose up -d
```

This starts everything: gRPC server, Envoy proxy, REST server, GraphQL server, and the client.

## What Was Added

### Files Created:
1. **`client/package.json`** - Added `grpc-web` and `google-protobuf` dependencies
2. **`client/src/api/grpcClient.ts`** - gRPC client wrapper (needs completion after code generation)
3. **`client/generate-proto.sh`** - Script to generate TypeScript client code
4. **`envoy.yaml`** - Envoy proxy configuration for gRPC-Web
5. **`docker-compose.yml`** - Added Envoy service

### Files Modified:
1. **`client/src/utils/performanceTester.ts`** - Added gRPC support alongside REST and GraphQL
2. **`performanceTester.ts` APIType** - Changed from `'REST' | 'GraphQL'` to `'REST' | 'GraphQL' | 'gRPC'`

## Architecture

```
React Client (port 3000)
    ↓ HTTP/1.1 (gRPC-Web)
Envoy Proxy (port 8090)
    ↓ HTTP/2 (gRPC)
gRPC Server (port 9090)
```

## Testing

1. Start the React client: `cd client && npm start`
2. Open http://localhost:3000
3. Select "gRPC" as the API type
4. Run performance tests

## Key Points

- **Browsers need gRPC-Web**: Standard gRPC won't work directly from browsers
- **Envoy is required**: Acts as a translator between gRPC-Web and gRPC
- **Code generation needed**: Must generate TypeScript client from .proto files
- **Port 8090**: Client connects here (Envoy), not directly to port 9090 (gRPC server)

## Status

✅ Dependencies added
✅ Client wrapper created
✅ PerformanceTester updated
✅ Envoy configured
✅ Docker Compose updated
⚠️ **Needs completion**: Generate client code and complete grpcClient.ts implementation

## Next Steps

1. Install protoc and protoc-gen-grpc-web
2. Run `./generate-proto.sh`
3. Complete the implementation in `grpcClient.ts`
4. Test gRPC operations from the React client

See `GRPC_CLIENT_SETUP.md` for detailed instructions.
