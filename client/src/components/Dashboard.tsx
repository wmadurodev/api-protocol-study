import React from 'react';
import { PerformanceMetrics, TestResults } from '../types';

interface DashboardProps {
  metrics: PerformanceMetrics[];
  results: TestResults;
}

const Dashboard: React.FC<DashboardProps> = ({ metrics, results }) => {
  if (metrics.length === 0) {
    return (
      <div className="dashboard">
        <h2>Test Results</h2>
        <div className="empty-state">
          <p>No test results yet. Run a test to see performance metrics.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h2>Test Results</h2>

      <div className="results-summary">
        <h3>Summary</h3>
        <table className="results-table">
          <thead>
            <tr>
              <th>API + Operation</th>
              <th>Count</th>
              <th>Avg Time (ms)</th>
              <th>Min Time (ms)</th>
              <th>Max Time (ms)</th>
              <th>Success Rate</th>
              <th>Avg Payload (bytes)</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(results).map(([key, result]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{result.count}</td>
                <td>{result.avgTime.toFixed(2)}</td>
                <td>{result.minTime.toFixed(2)}</td>
                <td>{result.maxTime.toFixed(2)}</td>
                <td>{result.successRate.toFixed(1)}%</td>
                <td>{result.avgPayloadSize.toFixed(0)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="recent-metrics">
        <h3>Recent Metrics</h3>
        <div className="metrics-list">
          {metrics.slice(-20).reverse().map((metric, index) => (
            <div
              key={index}
              className={`metric-card ${metric.success ? 'success' : 'error'}`}
            >
              <div className="metric-header">
                <span>
                  {metric.apiType} - {metric.operation}
                </span>
                <span>{metric.responseTime.toFixed(2)}ms</span>
              </div>
              <div className="metric-details">
                <span>Payload: {metric.payloadSize} bytes</span>
                <span>
                  {new Date(metric.timestamp).toLocaleTimeString()}
                </span>
                {!metric.success && (
                  <span style={{ color: '#f56565' }}>
                    Error: {metric.errorMessage}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
