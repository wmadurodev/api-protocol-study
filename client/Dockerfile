FROM node:18-alpine AS build

WORKDIR /app

# Install protoc and dependencies for gRPC code generation
RUN apk add --no-cache \
    bash \
    protobuf \
    protobuf-dev \
    wget \
    && GRPC_WEB_VERSION=1.5.0 \
    && wget https://github.com/grpc/grpc-web/releases/download/${GRPC_WEB_VERSION}/protoc-gen-grpc-web-${GRPC_WEB_VERSION}-linux-x86_64 -O /usr/local/bin/protoc-gen-grpc-web \
    && chmod +x /usr/local/bin/protoc-gen-grpc-web

# Copy proto files from shared directory
COPY shared /app/shared

# Copy package files
COPY client/package.json .

# Install dependencies
RUN npm install

# Copy proto generation script and make it executable
COPY client/generate-proto.sh .
RUN chmod +x generate-proto.sh

# Generate gRPC client code from proto files
RUN ./generate-proto.sh

# Copy source code
COPY client/public ./public
COPY client/src ./src
COPY client/tsconfig.json .

# Build the application
RUN npm run build

FROM nginx:alpine

# Copy built files to nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY client/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
