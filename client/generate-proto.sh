#!/bin/bash

# Script to generate TypeScript client code from proto files

PROTO_DIR="../shared/proto"
OUT_DIR="./src/generated"

# Create output directory if it doesn't exist
mkdir -p "$OUT_DIR"

# Generate TypeScript code using protoc and grpc-web plugin
# Note: You need to have protoc and protoc-gen-grpc-web installed
# Install instructions:
# 1. Install protoc: https://grpc.io/docs/protoc-installation/
# 2. Install protoc-gen-grpc-web: https://github.com/grpc/grpc-web/releases

protoc -I="$PROTO_DIR" \
  --js_out=import_style=commonjs,binary:"$OUT_DIR" \
  --grpc-web_out=import_style=typescript,mode=grpcwebtext:"$OUT_DIR" \
  "$PROTO_DIR/user_service.proto"

echo "Proto files generated successfully in $OUT_DIR"
