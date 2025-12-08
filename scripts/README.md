# Performance Testing Scripts

## parallel_perf_test.py

A Python script for parallel performance testing of REST vs gRPC servers.

### Prerequisites

1. **Running Servers**:
   - REST server on `localhost:8080`
   - gRPC server on `localhost:9090`

2. **Python Dependencies**:
   ```bash
   pip install grpcio requests
   ```

3. **gRPC Generated Code**:
   The script imports from `python-grpc-client/` directory. Ensure the gRPC Python code is generated:
   ```bash
   cd ../python-grpc-client
   ./generate_grpc.sh  # or run protoc manually
   ```

### Basic Usage

```bash
# Run 1000 parallel requests against each server
python parallel_perf_test.py --requests 1000

# Short form
python parallel_perf_test.py -r 1000
```

### Advanced Usage

#### Custom User ID Range
```bash
# Test with user IDs between 1 and 1000
python parallel_perf_test.py -r 500 --user-id-range 1-1000
```

#### JSON Output
```bash
# Export results as JSON
python parallel_perf_test.py -r 1000 -o json > results.json
```

#### CSV Output
```bash
# Export results as CSV (for Excel/Google Sheets)
python parallel_perf_test.py -r 1000 -o csv > results.csv
```

#### Verbose Mode
```bash
# See detailed progress logs
python parallel_perf_test.py -r 100 -v
```

#### Custom Server URLs
```bash
# Test against different servers
python parallel_perf_test.py -r 500 \
  --rest-url http://production-rest:8080 \
  --grpc-url production-grpc:9090
```

### Metrics Collected

The script measures and compares:

1. **Average Response Time** - Mean latency in milliseconds
2. **Average Payload Size** - Mean response size in bytes
3. **Network Resource Efficiency** - bytes/ms ratio
4. **Throughput** - Requests per second
5. **Success Rate** - Percentage of successful requests
6. **Response Time Percentiles** - P50, P95, P99
7. **Data Transfer Rate** - Total bytes per second

### Example Output

```
================================================================================
PARALLEL PERFORMANCE TEST RESULTS
================================================================================
Test Configuration:
  - Requests per Protocol: 1000
  - User ID Range: 1-10000
  - REST Server: http://localhost:8080
  - gRPC Server: localhost:9090

================================================================================
REST RESULTS
================================================================================
Success Rate:         98.5% (985/1000 requests)
Average Response:     12.34 ms
Median Response:      10.50 ms
P95 Response:         25.80 ms
Avg Payload Size:     245 bytes
Throughput:           487.2 req/s
Network Efficiency:   19.86 bytes/ms

================================================================================
gRPC RESULTS
================================================================================
Success Rate:         99.2% (992/1000 requests)
Average Response:     15.67 ms
Median Response:      13.20 ms
P95 Response:         30.10 ms
Avg Payload Size:     180 bytes
Throughput:           398.4 req/s
Network Efficiency:   11.48 bytes/ms

================================================================================
COMPARISON & ANALYSIS
================================================================================
Metric                  REST          gRPC          Winner      Difference
--------------------------------------------------------------------------------
Avg Response Time       12.34 ms      15.67 ms      REST        +27.0% faster
Avg Payload Size        245 bytes     180 bytes     gRPC        -26.5% smaller
Throughput              487.2 req/s   398.4 req/s   REST        +22.3% higher
```

### Troubleshooting

#### "gRPC Python code not found"
- Ensure you've generated the gRPC code in `python-grpc-client/`
- Run `./generate_grpc.sh` or manually run protoc

#### "REST server not reachable"
- Check if REST server is running: `curl http://localhost:8080/api/users/1`
- Start REST server: `cd rest-server && ./mvnw spring-boot:run`

#### "gRPC server not reachable"
- Check if gRPC server is running on port 9090
- Start gRPC server: `cd grpc-server && ./mvnw spring-boot:run`

#### Using Docker Compose
```bash
# Start all servers
docker-compose up -d rest-server grpc-server

# Wait for servers to be ready
sleep 10

# Run the test
python scripts/parallel_perf_test.py -r 1000
```

### Performance Tips

1. **Warm-up**: Run a small test first (e.g., `-r 100`) to warm up the servers
2. **Concurrency**: The script uses 100 concurrent workers by default
3. **Request Count**: Start with 100-1000 requests, increase gradually
4. **Multiple Runs**: Run the test 3-5 times and average the results for accuracy

### Integration with CI/CD

```bash
#!/bin/bash
# ci-performance-test.sh

# Start servers
docker-compose up -d

# Wait for health checks
sleep 30

# Run performance test and save results
python scripts/parallel_perf_test.py -r 1000 -o json > performance-results.json

# Parse results and fail if performance regression detected
# (add your custom logic here)

# Cleanup
docker-compose down
```

### Related Documentation

- Specification: `prompts/0007-NF-parallel-perf-testing-script.md`
- Performance Analysis: `docs/grpc-vs-rest-performance-analysis.md`
- Testing gRPC: `docs/testing-grpc-getuser-envoy.md`
