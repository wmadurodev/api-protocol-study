#!/usr/bin/env python3
"""
Parallel Performance Testing Script for REST vs gRPC

This script executes parallel requests to both REST and gRPC servers,
measuring and comparing their performance characteristics.

Usage:
    python parallel_perf_test.py --requests 1000
    python parallel_perf_test.py -r 500 --user-id-range 1-1000
    python parallel_perf_test.py -r 1000 -o json > results.json
    python parallel_perf_test.py -r 1000 -o csv > results.csv

Requirements:
    - REST server running on localhost:8080
    - gRPC server running on localhost:9090
    - Python packages: grpcio, requests
"""

import argparse
import grpc
import json
import random
import requests
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import csv as csv_module
from io import StringIO

# Import gRPC generated code
try:
    sys.path.append('../python-grpc-client')
    import user_service_pb2
    import user_service_pb2_grpc
except ImportError:
    print("Error: gRPC Python code not found!")
    print("Please ensure gRPC code is generated in python-grpc-client/")
    sys.exit(1)


@dataclass
class RequestResult:
    """Result of a single request"""
    success: bool
    response_time: float  # milliseconds
    payload_size: int  # bytes
    user_id: int
    error_message: Optional[str] = None
    error_type: Optional[str] = None


@dataclass
class MetricResult:
    """Aggregated metrics for a protocol"""
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


class PerformanceTester:
    """Main class for running parallel performance tests"""

    def __init__(self, rest_url: str, grpc_url: str, verbose: bool = False):
        self.rest_base_url = rest_url
        self.grpc_address = grpc_url
        self.verbose = verbose

    def log(self, message: str):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", file=sys.stderr)

    def test_connectivity(self) -> Tuple[bool, bool]:
        """Test if both servers are available"""
        self.log("Testing server connectivity...")

        # Test REST
        rest_ok = False
        try:
            response = requests.get(f"{self.rest_base_url}/api/users/1", timeout=5)
            rest_ok = response.status_code in [200, 404]
            self.log(f"REST server: {'OK' if rest_ok else 'FAILED'}")
        except Exception as e:
            self.log(f"REST server: FAILED - {e}")

        # Test gRPC
        grpc_ok = False
        try:
            channel = grpc.insecure_channel(self.grpc_address)
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            request = user_service_pb2.GetUserRequest(user_id=1)
            stub.GetUser(request, timeout=5)
            grpc_ok = True
            channel.close()
            self.log("gRPC server: OK")
        except Exception as e:
            self.log(f"gRPC server: FAILED - {e}")

        return rest_ok, grpc_ok

    def fetch_user_rest(self, user_id: int) -> RequestResult:
        """Fetch a user via REST API"""
        start_time = time.perf_counter()
        try:
            response = requests.get(
                f"{self.rest_base_url}/api/users/{user_id}",
                timeout=30
            )
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000  # Convert to ms

            if response.status_code == 200:
                payload_size = len(response.content)
                return RequestResult(
                    success=True,
                    response_time=response_time,
                    payload_size=payload_size,
                    user_id=user_id
                )
            else:
                return RequestResult(
                    success=False,
                    response_time=response_time,
                    payload_size=0,
                    user_id=user_id,
                    error_message=f"HTTP {response.status_code}",
                    error_type=f"HTTP_{response.status_code}"
                )
        except requests.exceptions.Timeout:
            end_time = time.perf_counter()
            return RequestResult(
                success=False,
                response_time=(end_time - start_time) * 1000,
                payload_size=0,
                user_id=user_id,
                error_message="Request timeout",
                error_type="TIMEOUT"
            )
        except Exception as e:
            end_time = time.perf_counter()
            return RequestResult(
                success=False,
                response_time=(end_time - start_time) * 1000,
                payload_size=0,
                user_id=user_id,
                error_message=str(e),
                error_type=type(e).__name__
            )

    def fetch_user_grpc(self, user_id: int, channel, stub) -> RequestResult:
        """Fetch a user via gRPC API"""
        start_time = time.perf_counter()
        try:
            request = user_service_pb2.GetUserRequest(user_id=user_id)
            response = stub.GetUser(request, timeout=30)
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000  # Convert to ms

            payload_size = response.ByteSize()
            return RequestResult(
                success=True,
                response_time=response_time,
                payload_size=payload_size,
                user_id=user_id
            )
        except grpc.RpcError as e:
            end_time = time.perf_counter()
            return RequestResult(
                success=False,
                response_time=(end_time - start_time) * 1000,
                payload_size=0,
                user_id=user_id,
                error_message=e.details(),
                error_type=e.code().name
            )
        except Exception as e:
            end_time = time.perf_counter()
            return RequestResult(
                success=False,
                response_time=(end_time - start_time) * 1000,
                payload_size=0,
                user_id=user_id,
                error_message=str(e),
                error_type=type(e).__name__
            )

    def execute_rest_requests(self, user_ids: List[int], max_workers: int = 100) -> Tuple[List[RequestResult], float]:
        """Execute parallel REST requests"""
        self.log(f"Starting {len(user_ids)} parallel REST requests...")
        start_time = time.perf_counter()
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.fetch_user_rest, uid) for uid in user_ids]
            for i, future in enumerate(as_completed(futures), 1):
                results.append(future.result())
                if self.verbose and i % 100 == 0:
                    self.log(f"REST: {i}/{len(user_ids)} completed")

        end_time = time.perf_counter()
        total_duration = end_time - start_time
        self.log(f"REST requests completed in {total_duration:.2f}s")
        return results, total_duration

    def execute_grpc_requests(self, user_ids: List[int], max_workers: int = 100) -> Tuple[List[RequestResult], float]:
        """Execute parallel gRPC requests"""
        self.log(f"Starting {len(user_ids)} parallel gRPC requests...")
        start_time = time.perf_counter()
        results = []

        # Create channel and stub (reused across threads)
        channel = grpc.insecure_channel(
            self.grpc_address,
            options=[
                ('grpc.max_send_message_length', 50 * 1024 * 1024),
                ('grpc.max_receive_message_length', 50 * 1024 * 1024),
            ]
        )
        stub = user_service_pb2_grpc.UserServiceStub(channel)

        def fetch_with_shared_channel(user_id):
            return self.fetch_user_grpc(user_id, channel, stub)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(fetch_with_shared_channel, uid) for uid in user_ids]
            for i, future in enumerate(as_completed(futures), 1):
                results.append(future.result())
                if self.verbose and i % 100 == 0:
                    self.log(f"gRPC: {i}/{len(user_ids)} completed")

        channel.close()
        end_time = time.perf_counter()
        total_duration = end_time - start_time
        self.log(f"gRPC requests completed in {total_duration:.2f}s")
        return results, total_duration

    def calculate_metrics(self, results: List[RequestResult], protocol: str, duration: float) -> MetricResult:
        """Calculate performance metrics from request results"""
        total_requests = len(results)
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]

        successful_count = len(successful_results)
        failed_count = len(failed_results)
        success_rate = (successful_count / total_requests * 100) if total_requests > 0 else 0

        # Calculate response time statistics (only for successful requests)
        if successful_results:
            response_times = [r.response_time for r in successful_results]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            median_response_time = statistics.median(response_times)
            sorted_times = sorted(response_times)
            p95_response_time = sorted_times[int(len(sorted_times) * 0.95)] if sorted_times else 0
            p99_response_time = sorted_times[int(len(sorted_times) * 0.99)] if sorted_times else 0
            stddev_response_time = statistics.stdev(response_times) if len(response_times) > 1 else 0

            # Payload statistics
            payload_sizes = [r.payload_size for r in successful_results]
            avg_payload_size = statistics.mean(payload_sizes)
            total_bytes = sum(payload_sizes)

            # Efficiency metrics
            throughput = successful_count / duration if duration > 0 else 0
            data_transfer_rate = total_bytes / duration if duration > 0 else 0
            network_efficiency = avg_payload_size / avg_response_time if avg_response_time > 0 else 0
        else:
            avg_response_time = min_response_time = max_response_time = 0
            median_response_time = p95_response_time = p99_response_time = stddev_response_time = 0
            avg_payload_size = total_bytes = 0
            throughput = data_transfer_rate = network_efficiency = 0

        # Categorize errors
        errors = {}
        for result in failed_results:
            error_type = result.error_type or "UNKNOWN"
            errors[error_type] = errors.get(error_type, 0) + 1

        return MetricResult(
            protocol=protocol,
            total_requests=total_requests,
            successful_requests=successful_count,
            failed_requests=failed_count,
            success_rate=success_rate,
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            median_response_time=median_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time,
            stddev_response_time=stddev_response_time,
            avg_payload_size=avg_payload_size,
            total_bytes_transferred=total_bytes,
            throughput=throughput,
            data_transfer_rate=data_transfer_rate,
            network_efficiency=network_efficiency,
            total_duration=duration,
            errors=errors
        )


def format_console_output(rest_metrics: MetricResult, grpc_metrics: MetricResult, config: dict):
    """Format results as console output"""
    output = []
    output.append("=" * 80)
    output.append("PARALLEL PERFORMANCE TEST RESULTS")
    output.append("=" * 80)
    output.append("Test Configuration:")
    output.append(f"  - Requests per Protocol: {config['requests']}")
    output.append(f"  - User ID Range: {config['user_id_range']}")
    output.append(f"  - REST Server: {config['rest_url']}")
    output.append(f"  - gRPC Server: {config['grpc_url']}")
    output.append(f"  - Test Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    output.append("")

    # REST Results
    output.append("=" * 80)
    output.append("REST RESULTS")
    output.append("=" * 80)
    output.append(f"Success Rate:         {rest_metrics.success_rate:.1f}% ({rest_metrics.successful_requests}/{rest_metrics.total_requests} requests)")
    output.append(f"Average Response:     {rest_metrics.avg_response_time:.2f} ms")
    output.append(f"Median Response:      {rest_metrics.median_response_time:.2f} ms")
    output.append(f"P95 Response:         {rest_metrics.p95_response_time:.2f} ms")
    output.append(f"P99 Response:         {rest_metrics.p99_response_time:.2f} ms")
    output.append(f"Min Response:         {rest_metrics.min_response_time:.2f} ms")
    output.append(f"Max Response:         {rest_metrics.max_response_time:.2f} ms")
    output.append(f"Std Deviation:        {rest_metrics.stddev_response_time:.2f} ms")
    output.append("")
    output.append(f"Avg Payload Size:     {rest_metrics.avg_payload_size:.0f} bytes")
    output.append(f"Total Transferred:    {rest_metrics.total_bytes_transferred:,} bytes")
    output.append(f"Throughput:           {rest_metrics.throughput:.1f} req/s")
    output.append(f"Transfer Rate:        {rest_metrics.data_transfer_rate / 1024:.1f} KB/s")
    output.append(f"Network Efficiency:   {rest_metrics.network_efficiency:.2f} bytes/ms")
    output.append("")
    if rest_metrics.errors:
        output.append(f"Failed Requests:      {rest_metrics.failed_requests}")
        output.append("Errors:")
        for error_type, count in sorted(rest_metrics.errors.items()):
            output.append(f"  - {error_type}: {count}")
    output.append("")

    # gRPC Results
    output.append("=" * 80)
    output.append("gRPC RESULTS")
    output.append("=" * 80)
    output.append(f"Success Rate:         {grpc_metrics.success_rate:.1f}% ({grpc_metrics.successful_requests}/{grpc_metrics.total_requests} requests)")
    output.append(f"Average Response:     {grpc_metrics.avg_response_time:.2f} ms")
    output.append(f"Median Response:      {grpc_metrics.median_response_time:.2f} ms")
    output.append(f"P95 Response:         {grpc_metrics.p95_response_time:.2f} ms")
    output.append(f"P99 Response:         {grpc_metrics.p99_response_time:.2f} ms")
    output.append(f"Min Response:         {grpc_metrics.min_response_time:.2f} ms")
    output.append(f"Max Response:         {grpc_metrics.max_response_time:.2f} ms")
    output.append(f"Std Deviation:        {grpc_metrics.stddev_response_time:.2f} ms")
    output.append("")
    output.append(f"Avg Payload Size:     {grpc_metrics.avg_payload_size:.0f} bytes")
    output.append(f"Total Transferred:    {grpc_metrics.total_bytes_transferred:,} bytes")
    output.append(f"Throughput:           {grpc_metrics.throughput:.1f} req/s")
    output.append(f"Transfer Rate:        {grpc_metrics.data_transfer_rate / 1024:.1f} KB/s")
    output.append(f"Network Efficiency:   {grpc_metrics.network_efficiency:.2f} bytes/ms")
    output.append("")
    if grpc_metrics.errors:
        output.append(f"Failed Requests:      {grpc_metrics.failed_requests}")
        output.append("Errors:")
        for error_type, count in sorted(grpc_metrics.errors.items()):
            output.append(f"  - {error_type}: {count}")
    output.append("")

    # Comparison
    output.append("=" * 80)
    output.append("COMPARISON & ANALYSIS")
    output.append("=" * 80)
    output.append(f"{'Metric':<25} {'REST':<15} {'gRPC':<15} {'Winner':<10} {'Difference'}")
    output.append("-" * 80)

    def compare(metric_name, rest_val, grpc_val, unit, lower_is_better=True):
        if rest_val == 0 and grpc_val == 0:
            winner = "TIE"
            diff = "0%"
        elif lower_is_better:
            if rest_val < grpc_val:
                winner = "REST"
                diff_pct = ((grpc_val - rest_val) / grpc_val * 100) if grpc_val else 0
                diff = f"+{diff_pct:.1f}% faster"
            elif grpc_val < rest_val:
                winner = "gRPC"
                diff_pct = ((rest_val - grpc_val) / rest_val * 100) if rest_val else 0
                diff = f"+{diff_pct:.1f}% faster"
            else:
                winner = "TIE"
                diff = "0%"
        else:  # higher is better
            if rest_val > grpc_val:
                winner = "REST"
                diff_pct = ((rest_val - grpc_val) / grpc_val * 100) if grpc_val else 0
                diff = f"+{diff_pct:.1f}% higher"
            elif grpc_val > rest_val:
                winner = "gRPC"
                diff_pct = ((grpc_val - rest_val) / rest_val * 100) if rest_val else 0
                diff = f"+{diff_pct:.1f}% higher"
            else:
                winner = "TIE"
                diff = "0%"

        output.append(f"{metric_name:<25} {rest_val:.2f} {unit:<10} {grpc_val:.2f} {unit:<10} {winner:<10} {diff}")

    compare("Avg Response Time", rest_metrics.avg_response_time, grpc_metrics.avg_response_time, "ms", lower_is_better=True)
    compare("Avg Payload Size", rest_metrics.avg_payload_size, grpc_metrics.avg_payload_size, "bytes", lower_is_better=True)
    compare("Success Rate", rest_metrics.success_rate, grpc_metrics.success_rate, "%", lower_is_better=False)
    compare("Throughput", rest_metrics.throughput, grpc_metrics.throughput, "req/s", lower_is_better=False)
    compare("Network Efficiency", rest_metrics.network_efficiency, grpc_metrics.network_efficiency, "b/ms", lower_is_better=False)

    output.append("")
    output.append("CONCLUSION:")

    # Determine overall winner
    if rest_metrics.avg_response_time < grpc_metrics.avg_response_time:
        time_diff = ((grpc_metrics.avg_response_time - rest_metrics.avg_response_time) / grpc_metrics.avg_response_time * 100)
        output.append(f"  - REST shows superior response time (+{time_diff:.1f}% faster)")
    else:
        time_diff = ((rest_metrics.avg_response_time - grpc_metrics.avg_response_time) / rest_metrics.avg_response_time * 100)
        output.append(f"  - gRPC shows superior response time (+{time_diff:.1f}% faster)")

    if grpc_metrics.avg_payload_size < rest_metrics.avg_payload_size:
        size_diff = ((rest_metrics.avg_payload_size - grpc_metrics.avg_payload_size) / rest_metrics.avg_payload_size * 100)
        output.append(f"  - gRPC has smaller payload size (-{size_diff:.1f}%)")
    else:
        size_diff = ((grpc_metrics.avg_payload_size - rest_metrics.avg_payload_size) / grpc_metrics.avg_payload_size * 100)
        output.append(f"  - REST has smaller payload size (-{size_diff:.1f}%)")

    output.append("")
    output.append("NOTES:")
    output.append("  - Test conducted on localhost; production results may vary")
    output.append("  - gRPC via Envoy proxy may add overhead in browser environments")
    output.append("  - Consider testing under network latency for realistic comparison")

    return "\n".join(output)


def format_json_output(rest_metrics: MetricResult, grpc_metrics: MetricResult, config: dict):
    """Format results as JSON"""
    result = {
        "test_metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requests_per_protocol": config["requests"],
            "user_id_range": config["user_id_range"],
            "rest_url": config["rest_url"],
            "grpc_url": config["grpc_url"]
        },
        "rest": asdict(rest_metrics),
        "grpc": asdict(grpc_metrics),
        "comparison": {
            "avg_response_time_diff_pct": ((grpc_metrics.avg_response_time - rest_metrics.avg_response_time) / grpc_metrics.avg_response_time * 100) if grpc_metrics.avg_response_time else 0,
            "avg_payload_size_diff_pct": ((grpc_metrics.avg_payload_size - rest_metrics.avg_payload_size) / grpc_metrics.avg_payload_size * 100) if grpc_metrics.avg_payload_size else 0,
            "throughput_diff_pct": ((rest_metrics.throughput - grpc_metrics.throughput) / grpc_metrics.throughput * 100) if grpc_metrics.throughput else 0,
            "winner": {
                "avg_response_time": "REST" if rest_metrics.avg_response_time < grpc_metrics.avg_response_time else "gRPC",
                "avg_payload_size": "gRPC" if grpc_metrics.avg_payload_size < rest_metrics.avg_payload_size else "REST",
                "success_rate": "gRPC" if grpc_metrics.success_rate > rest_metrics.success_rate else "REST",
                "throughput": "REST" if rest_metrics.throughput > grpc_metrics.throughput else "gRPC",
                "network_efficiency": "REST" if rest_metrics.network_efficiency > grpc_metrics.network_efficiency else "gRPC"
            }
        }
    }
    return json.dumps(result, indent=2)


def format_csv_output(rest_metrics: MetricResult, grpc_metrics: MetricResult):
    """Format results as CSV"""
    output = StringIO()
    writer = csv_module.writer(output)

    # Header
    writer.writerow(["Metric", "REST", "gRPC", "Winner", "Difference_Pct"])

    # Data rows
    def write_comparison(metric_name, rest_val, grpc_val, lower_is_better=True):
        if rest_val == 0 and grpc_val == 0:
            winner = "TIE"
            diff_pct = 0
        elif lower_is_better:
            if rest_val < grpc_val:
                winner = "REST"
                diff_pct = ((grpc_val - rest_val) / grpc_val * 100) if grpc_val else 0
            else:
                winner = "gRPC"
                diff_pct = ((rest_val - grpc_val) / rest_val * 100) if rest_val else 0
        else:
            if rest_val > grpc_val:
                winner = "REST"
                diff_pct = ((rest_val - grpc_val) / grpc_val * 100) if grpc_val else 0
            else:
                winner = "gRPC"
                diff_pct = ((grpc_val - rest_val) / rest_val * 100) if rest_val else 0

        writer.writerow([metric_name, f"{rest_val:.2f}", f"{grpc_val:.2f}", winner, f"{diff_pct:.2f}"])

    writer.writerow(["Total Requests", rest_metrics.total_requests, grpc_metrics.total_requests, "-", "-"])
    writer.writerow(["Successful Requests", rest_metrics.successful_requests, grpc_metrics.successful_requests, "-", "-"])
    write_comparison("Success Rate %", rest_metrics.success_rate, grpc_metrics.success_rate, lower_is_better=False)
    write_comparison("Avg Response Time (ms)", rest_metrics.avg_response_time, grpc_metrics.avg_response_time, lower_is_better=True)
    write_comparison("Median Response Time (ms)", rest_metrics.median_response_time, grpc_metrics.median_response_time, lower_is_better=True)
    write_comparison("P95 Response Time (ms)", rest_metrics.p95_response_time, grpc_metrics.p95_response_time, lower_is_better=True)
    write_comparison("Avg Payload Size (bytes)", rest_metrics.avg_payload_size, grpc_metrics.avg_payload_size, lower_is_better=True)
    writer.writerow(["Total Bytes Transferred", rest_metrics.total_bytes_transferred, grpc_metrics.total_bytes_transferred, "-", "-"])
    write_comparison("Throughput (req/s)", rest_metrics.throughput, grpc_metrics.throughput, lower_is_better=False)
    write_comparison("Network Efficiency (bytes/ms)", rest_metrics.network_efficiency, grpc_metrics.network_efficiency, lower_is_better=False)

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description="Parallel Performance Testing: REST vs gRPC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parallel_perf_test.py --requests 1000
  python parallel_perf_test.py -r 500 --user-id-range 1-1000
  python parallel_perf_test.py -r 1000 -o json > results.json
  python parallel_perf_test.py -r 1000 -o csv > results.csv
        """
    )

    parser.add_argument(
        "-r", "--requests",
        type=int,
        required=True,
        help="Number of parallel requests to execute for each protocol"
    )
    parser.add_argument(
        "--user-id-range",
        type=str,
        default="1-10000",
        help="Range of user IDs to randomly select from (format: min-max)"
    )
    parser.add_argument(
        "-o", "--output",
        choices=["console", "json", "csv"],
        default="console",
        help="Output format (default: console)"
    )
    parser.add_argument(
        "--rest-url",
        type=str,
        default="http://localhost:8080",
        help="REST server base URL (default: http://localhost:8080)"
    )
    parser.add_argument(
        "--grpc-url",
        type=str,
        default="localhost:9090",
        help="gRPC server address (default: localhost:9090)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Parse user ID range
    try:
        min_id, max_id = map(int, args.user_id_range.split("-"))
        if min_id < 1 or max_id < min_id:
            raise ValueError("Invalid range")
    except ValueError:
        print("Error: Invalid user-id-range format. Use 'min-max' (e.g., '1-10000')", file=sys.stderr)
        sys.exit(1)

    # Initialize tester
    tester = PerformanceTester(args.rest_url, args.grpc_url, args.verbose)

    # Test connectivity
    rest_ok, grpc_ok = tester.test_connectivity()
    if not rest_ok or not grpc_ok:
        print("\nError: One or more servers are unavailable:", file=sys.stderr)
        if not rest_ok:
            print(f"  - REST server not reachable at {args.rest_url}", file=sys.stderr)
        if not grpc_ok:
            print(f"  - gRPC server not reachable at {args.grpc_url}", file=sys.stderr)
        print("\nPlease ensure both servers are running before running the test.", file=sys.stderr)
        sys.exit(1)

    # Generate random user IDs
    user_ids = [random.randint(min_id, max_id) for _ in range(args.requests)]

    # Execute tests
    tester.log(f"Starting parallel performance test with {args.requests} requests...")

    rest_results, rest_duration = tester.execute_rest_requests(user_ids)
    grpc_results, grpc_duration = tester.execute_grpc_requests(user_ids)

    # Calculate metrics
    rest_metrics = tester.calculate_metrics(rest_results, "REST", rest_duration)
    grpc_metrics = tester.calculate_metrics(grpc_results, "gRPC", grpc_duration)

    # Prepare config for output
    config = {
        "requests": args.requests,
        "user_id_range": args.user_id_range,
        "rest_url": args.rest_url,
        "grpc_url": args.grpc_url
    }

    # Format and display output
    if args.output == "console":
        print(format_console_output(rest_metrics, grpc_metrics, config))
    elif args.output == "json":
        print(format_json_output(rest_metrics, grpc_metrics, config))
    elif args.output == "csv":
        print(format_csv_output(rest_metrics, grpc_metrics))


if __name__ == "__main__":
    main()
