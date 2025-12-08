# Parallel Performance Testing Script Specification

## Prompt ID
0007-NF-parallel-perf-testing-script

## Type
New Feature (NF)

## Description
Create a Python script to perform parallel performance testing of REST and gRPC servers for the getUser endpoint. The script should execute concurrent requests to both servers and provide comprehensive performance comparison metrics.

## Objective
Develop a command-line Python script that:
1. Accepts number of requests as a required parameter
2. Executes parallel requests to both REST and gRPC servers simultaneously
3. Collects and analyzes performance metrics
4. Displays comparative results in a clear, structured format

## Requirements

### Input Parameters

#### Required Parameter
- `--requests` / `-r`: Number of parallel requests to execute against each server
  - Type: Integer
  - Minimum: 1
  - Maximum: 10000 (recommended)
  - Description: Total number of getUser requests to run in parallel for each protocol

#### Optional Parameters
- `--user-id-range`: Range of user IDs to randomly select from
  - Type: String (format: "min-max")
  - Default: "1-10000"
  - Example: "1-1000"

- `--output` / `-o`: Output format for results
  - Type: String
  - Options: `console`, `json`, `csv`
  - Default: `console`

- `--rest-url`: REST server base URL
  - Type: String
  - Default: "http://localhost:8080"

- `--grpc-url`: gRPC server address
  - Type: String
  - Default: "localhost:9090"

- `--verbose` / `-v`: Enable verbose logging
  - Type: Boolean flag
  - Default: False

### Server Endpoints

#### REST Endpoint
- **URL**: `{rest-url}/api/users/{id}`
- **Method**: GET
- **Response**: JSON object representing User

#### gRPC Endpoint
- **Service**: `api.performance.UserService`
- **Method**: `GetUser`
- **Request**: `GetUserRequest` with `user_id` field
- **Response**: `GetUserResponse` with User object

### Performance Metrics to Collect

#### 1. Average Response Time
- **Definition**: Mean time from request initiation to response completion
- **Unit**: milliseconds (ms)
- **Calculation**: Sum of all response times / Number of successful requests
- **Per Protocol**: Calculate separately for REST and gRPC

#### 2. Average Payload Size
- **Definition**: Mean size of response data received
- **Unit**: bytes
- **Calculation**: Sum of all response sizes / Number of successful requests
- **Details**:
  - REST: Size of JSON response body
  - gRPC: Size of serialized protobuf message
- **Per Protocol**: Calculate separately for REST and gRPC

#### 3. Network Resource Efficiency
- **Definition**: Composite metric measuring data transfer efficiency
- **Calculation**: Average payload size / Average response time
- **Unit**: bytes per millisecond (bytes/ms)
- **Interpretation**: Higher values indicate better efficiency (more data transferred per unit time)
- **Additional Metrics**:
  - **Throughput**: Requests per second (total successful requests / total duration)
  - **Data Transfer Rate**: Total bytes transferred / Total duration (bytes/s)

### Additional Metrics (Optional but Recommended)

#### Response Time Statistics
- **Minimum Response Time**: Fastest request
- **Maximum Response Time**: Slowest request
- **Median (P50)**: 50th percentile
- **P95**: 95th percentile
- **P99**: 99th percentile
- **Standard Deviation**: Measure of variance

#### Success Metrics
- **Success Count**: Number of successful requests
- **Failure Count**: Number of failed requests
- **Success Rate**: (Success count / Total requests) * 100%
- **Error Types**: Categorize failures by error type

#### Timing Breakdown
- **Connection Time**: Time to establish connection
- **First Byte Time**: Time to receive first byte of response
- **Download Time**: Time to download complete response

## Technical Implementation

### Dependencies
```python
# Required packages
import grpc
import requests
import asyncio
import aiohttp
import concurrent.futures
import statistics
import sys
import argparse
import json
import csv
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import random

# gRPC generated code
import user_service_pb2
import user_service_pb2_grpc
```

### Script Structure

```python
# File: scripts/parallel_perf_test.py

1. Import dependencies
2. Define data classes for metrics
3. Implement REST request function
4. Implement gRPC request function
5. Implement parallel executor for REST
6. Implement parallel executor for gRPC
7. Implement metrics calculation functions
8. Implement results comparison and display
9. Implement output formatters (console, JSON, CSV)
10. Implement argument parsing
11. Main execution flow
```

### Data Structures

#### Metric Result Class
```python
@dataclass
class MetricResult:
    protocol: str  # "REST" or "gRPC"
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float

    # Response time metrics (ms)
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    median_response_time: float
    p95_response_time: float
    p99_response_time: float
    stddev_response_time: float

    # Payload metrics (bytes)
    avg_payload_size: float
    total_bytes_transferred: int

    # Efficiency metrics
    throughput: float  # requests/second
    data_transfer_rate: float  # bytes/second
    network_efficiency: float  # bytes/ms

    # Timing
    total_duration: float  # seconds

    # Errors
    errors: Dict[str, int]  # error_type -> count
```

#### Request Result Class
```python
@dataclass
class RequestResult:
    success: bool
    response_time: float  # milliseconds
    payload_size: int  # bytes
    user_id: int
    error_message: str = None
    error_type: str = None
```

### Execution Flow

```
1. Parse command-line arguments
   ├─ Validate inputs
   └─ Set configuration

2. Initialize connections
   ├─ Test REST server availability
   └─ Test gRPC server availability

3. Generate user ID list
   └─ Random sample from specified range

4. Execute parallel REST requests
   ├─ Use ThreadPoolExecutor or asyncio
   ├─ Track start time
   ├─ Execute all requests concurrently
   ├─ Collect individual results
   └─ Track end time

5. Execute parallel gRPC requests
   ├─ Use ThreadPoolExecutor
   ├─ Track start time
   ├─ Execute all requests concurrently
   ├─ Collect individual results
   └─ Track end time

6. Calculate metrics
   ├─ Process REST results
   ├─ Process gRPC results
   └─ Create MetricResult objects

7. Compare results
   ├─ Calculate performance differences
   ├─ Determine winner for each metric
   └─ Generate insights

8. Display results
   ├─ Console output (formatted table)
   ├─ JSON output (structured data)
   └─ CSV output (spreadsheet-friendly)

9. Exit with appropriate status code
```

### Parallel Execution Strategy

#### Option 1: ThreadPoolExecutor (Recommended for Mixed I/O)
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def execute_parallel_requests(request_func, user_ids, max_workers=100):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(request_func, uid) for uid in user_ids]
        for future in as_completed(futures):
            results.append(future.result())
    return results
```

#### Option 2: asyncio with aiohttp (For REST only, fastest)
```python
async def execute_async_rest_requests(user_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user_rest_async(session, uid) for uid in user_ids]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

### Output Formats

#### Console Output (Default)
```
================================================================================
PARALLEL PERFORMANCE TEST RESULTS
================================================================================
Test Configuration:
  - Requests per Protocol: 1000
  - User ID Range: 1-10000
  - REST Server: http://localhost:8080
  - gRPC Server: localhost:9090
  - Test Time: 2024-01-15 14:30:00 UTC

================================================================================
REST RESULTS
================================================================================
Success Rate:         98.5% (985/1000 requests)
Average Response:     12.34 ms
Median Response:      10.50 ms
P95 Response:         25.80 ms
P99 Response:         35.20 ms
Min Response:         5.20 ms
Max Response:         150.30 ms
Std Deviation:        8.45 ms

Avg Payload Size:     245 bytes
Total Transferred:    241,325 bytes
Throughput:           487.2 req/s
Transfer Rate:        117.5 KB/s
Network Efficiency:   19.86 bytes/ms

Failed Requests:      15
Errors:
  - Connection Timeout: 10
  - HTTP 500: 5

================================================================================
gRPC RESULTS
================================================================================
Success Rate:         99.2% (992/1000 requests)
Average Response:     15.67 ms
Median Response:      13.20 ms
P95 Response:         30.10 ms
P99 Response:         42.50 ms
Min Response:         6.80 ms
Max Response:         180.50 ms
Std Deviation:        10.22 ms

Avg Payload Size:     180 bytes
Total Transferred:    178,560 bytes
Throughput:           398.4 req/s
Transfer Rate:        71.1 KB/s
Network Efficiency:   11.48 bytes/ms

Failed Requests:      8
Errors:
  - UNAVAILABLE: 5
  - DEADLINE_EXCEEDED: 3

================================================================================
COMPARISON & ANALYSIS
================================================================================
Metric                  REST          gRPC          Winner      Difference
--------------------------------------------------------------------------------
Avg Response Time       12.34 ms      15.67 ms      REST        +27.0% faster
Avg Payload Size        245 bytes     180 bytes     gRPC        -26.5% smaller
Success Rate            98.5%         99.2%         gRPC        +0.7%
Throughput              487.2 req/s   398.4 req/s   REST        +22.3% higher
Network Efficiency      19.86 b/ms    11.48 b/ms    REST        +72.9% higher

CONCLUSION:
  - REST shows superior response time in this localhost test (+27.0%)
  - gRPC has smaller payload size (-26.5%)
  - REST achieves higher throughput and network efficiency
  - gRPC has slightly better reliability (99.2% vs 98.5%)

NOTES:
  - Test conducted on localhost; production results may vary
  - gRPC via Envoy proxy may add overhead
  - Consider testing under network latency for realistic comparison
```

#### JSON Output
```json
{
  "test_metadata": {
    "timestamp": "2024-01-15T14:30:00Z",
    "requests_per_protocol": 1000,
    "user_id_range": "1-10000",
    "rest_url": "http://localhost:8080",
    "grpc_url": "localhost:9090"
  },
  "rest": {
    "protocol": "REST",
    "total_requests": 1000,
    "successful_requests": 985,
    "failed_requests": 15,
    "success_rate": 98.5,
    "avg_response_time": 12.34,
    "min_response_time": 5.20,
    "max_response_time": 150.30,
    "median_response_time": 10.50,
    "p95_response_time": 25.80,
    "p99_response_time": 35.20,
    "stddev_response_time": 8.45,
    "avg_payload_size": 245,
    "total_bytes_transferred": 241325,
    "throughput": 487.2,
    "data_transfer_rate": 117500,
    "network_efficiency": 19.86,
    "total_duration": 2.022,
    "errors": {
      "Connection Timeout": 10,
      "HTTP 500": 5
    }
  },
  "grpc": {
    // Similar structure
  },
  "comparison": {
    "avg_response_time_diff_pct": 27.0,
    "avg_payload_size_diff_pct": -26.5,
    "throughput_diff_pct": 22.3,
    "winner": {
      "avg_response_time": "REST",
      "avg_payload_size": "gRPC",
      "success_rate": "gRPC",
      "throughput": "REST",
      "network_efficiency": "REST"
    }
  }
}
```

#### CSV Output
```csv
Metric,REST,gRPC,Winner,Difference_Pct
Total Requests,1000,1000,-,-
Successful Requests,985,992,gRPC,+0.7
Success Rate %,98.5,99.2,gRPC,+0.7
Avg Response Time (ms),12.34,15.67,REST,-27.0
Median Response Time (ms),10.50,13.20,REST,-25.7
P95 Response Time (ms),25.80,30.10,REST,-16.7
Avg Payload Size (bytes),245,180,gRPC,-26.5
Total Bytes Transferred,241325,178560,gRPC,-26.0
Throughput (req/s),487.2,398.4,REST,+22.3
Network Efficiency (bytes/ms),19.86,11.48,REST,+72.9
```

## Usage Examples

### Basic Usage
```bash
# Run 1000 parallel requests against each server
python scripts/parallel_perf_test.py --requests 1000
```

### With Custom User ID Range
```bash
# Test with user IDs between 1 and 1000
python scripts/parallel_perf_test.py -r 500 --user-id-range 1-1000
```

### JSON Output
```bash
# Export results as JSON
python scripts/parallel_perf_test.py -r 1000 -o json > results.json
```

### CSV Output
```bash
# Export results as CSV
python scripts/parallel_perf_test.py -r 1000 -o csv > results.csv
```

### Verbose Mode
```bash
# Enable detailed logging
python scripts/parallel_perf_test.py -r 100 -v
```

### Custom Server URLs
```bash
# Test against custom server addresses
python scripts/parallel_perf_test.py -r 500 \
  --rest-url http://production-rest.example.com:8080 \
  --grpc-url production-grpc.example.com:9090
```

## Error Handling

### Connection Errors
- Detect if servers are unavailable before starting tests
- Provide clear error messages with troubleshooting hints
- Exit gracefully with non-zero status code

### Request Failures
- Catch and categorize all exceptions
- Continue test execution even if some requests fail
- Report failure statistics separately

### Invalid Inputs
- Validate all command-line arguments
- Provide helpful error messages
- Display usage help on invalid input

## Performance Considerations

### Concurrency Limits
- Default max workers: 100 (configurable)
- Avoid overwhelming servers with too many concurrent connections
- Consider server capacity when setting request counts

### Memory Management
- Stream results instead of loading all into memory at once
- Clean up connections properly after each request
- Monitor memory usage for large request counts

### Timing Accuracy
- Use high-resolution timers (time.perf_counter())
- Account for Python GIL overhead
- Minimize overhead in measurement code

## Dependencies Installation

```bash
# Create requirements.txt
pip install grpcio==1.60.0
pip install grpcio-tools==1.60.0
pip install requests==2.31.0
pip install aiohttp==3.9.1

# Or use existing proto-generated code
cd python-grpc-client
# Ensure user_service_pb2.py and user_service_pb2_grpc.py exist
```

## Integration with Existing Project

### Proto Files Location
- Use existing proto files: `shared/proto/user_service.proto`
- Import generated Python code from `python-grpc-client/`

### Server Ports
- REST Server: 8080 (from `rest-server/`)
- gRPC Server: 9090 (from `grpc-server/`)

### User Data
- User IDs range: 1-10000 (matching server data generation)
- Consistent with existing test data

## Success Criteria

The script is successful when:
1. ✅ Accepts required `--requests` parameter
2. ✅ Executes parallel requests to both REST and gRPC servers
3. ✅ Collects all specified performance metrics accurately
4. ✅ Calculates comparative statistics correctly
5. ✅ Displays results in clear, readable format
6. ✅ Supports multiple output formats (console, JSON, CSV)
7. ✅ Handles errors gracefully without crashing
8. ✅ Completes in reasonable time (< 1 minute for 1000 requests)
9. ✅ Provides actionable insights from comparison

## Deliverables

1. Python script: `scripts/parallel_perf_test.py`
2. Usage documentation in script header
3. Requirements file (if needed)
4. Example output samples

## Future Enhancements (Optional)

- Add support for GraphQL endpoint comparison
- Implement progressive load testing (ramp up requests)
- Add visualization (generate charts from results)
- Support for other endpoints (listUsers, getUserOrders, etc.)
- Distributed testing across multiple client machines
- Real-time monitoring dashboard
- Integration with CI/CD pipelines
- Historical results comparison
