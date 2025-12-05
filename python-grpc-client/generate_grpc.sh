#!/bin/bash

# Generate Python gRPC code from proto file
python3 -m grpc_tools.protoc \
  -I./proto \
  --python_out=. \
  --grpc_python_out=. \
  ./proto/user_service.proto

echo "gRPC Python code generated successfully!"
