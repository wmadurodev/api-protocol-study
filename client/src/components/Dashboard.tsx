import React, { useState, useMemo } from 'react';
import { PerformanceMetrics, TestResults } from '../types';
import Spinner from './Spinner';

interface DashboardProps {
  metrics: PerformanceMetrics[];
  results: TestResults;
  isRunning: boolean;
}

interface MethodComparison {
  method: string;
  REST?: number;
  gRPC?: number;
  GraphQL?: number;
  avgTime: number;
}

const Dashboard: React.FC<DashboardProps> = ({ metrics, results, isRunning }) => {
  const [summaryExpanded, setSummaryExpanded] = useState(false);
  const [recentMetricsExpanded, setRecentMetricsExpanded] = useState(false);

  const comparisonData = useMemo(() => {
    const methodMap = new Map<string, { REST?: number; gRPC?: number; GraphQL?: number }>();

    Object.entries(results).forEach(([key, result]) => {
      const parts = key.split('-');
      if (parts.length === 2) {
        const apiType = parts[0] as 'REST' | 'gRPC' | 'GraphQL';
        const method = parts[1];

        if (!methodMap.has(method)) {
          methodMap.set(method, {});
        }

        const methodData = methodMap.get(method)!;
        methodData[apiType] = result.avgTime;
      }
    });

    const comparisons: MethodComparison[] = Array.from(methodMap.entries()).map(([method, apiTimes]) => {
      const times = Object.values(apiTimes).filter((t): t is number => t !== undefined);
      const avgTime = times.reduce((sum, t) => sum + t, 0) / times.length;

      return {
        method,
        ...apiTimes,
        avgTime
      };
    });

    return comparisons.sort((a, b) => b.avgTime - a.avgTime);
  }, [results]);

  if (metrics.length === 0 && !isRunning) {
    return (
      <div className="dashboard">
        <h2>Test Results</h2>
        <div className="empty-state">
          <p>No test results yet. Run a test to see performance metrics.</p>
        </div>
      </div>
    );
  }

  if (metrics.length === 0 && isRunning) {
    return (
      <div className="dashboard">
        <h2>Test Results</h2>
        <Spinner size="large" message="Running tests..." />
      </div>
    );
  }

  return (
    <div className={`dashboard ${isRunning ? 'dashboard-loading' : ''}`}>
      {isRunning && (
        <div className="loading-overlay">
          <Spinner size="large" message="Running tests..." />
        </div>
      )}
      <div className="dashboard-content">
        <h2>Test Results</h2>

        <div className="api-comparison">
        <h3>API Performance Comparison by Method</h3>
        <table className="results-table comparison-table">
          <thead>
            <tr>
              <th>Method</th>
              <th>REST (ms)</th>
              <th>gRPC (ms)</th>
              <th>GraphQL (ms)</th>
            </tr>
          </thead>
          <tbody>
            {comparisonData.map((row) => (
              <tr key={row.method}>
                <td>{row.method}</td>
                <td>{row.REST !== undefined ? row.REST.toFixed(2) : '-'}</td>
                <td>{row.gRPC !== undefined ? row.gRPC.toFixed(2) : '-'}</td>
                <td>{row.GraphQL !== undefined ? row.GraphQL.toFixed(2) : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="results-summary">
        <h3
          onClick={() => setSummaryExpanded(!summaryExpanded)}
          style={{ cursor: 'pointer', userSelect: 'none' }}
        >
          Summary {summaryExpanded ? '▼' : '▶'}
        </h3>
        {summaryExpanded && (
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
        )}
      </div>

      <div className="recent-metrics">
        <h3
          onClick={() => setRecentMetricsExpanded(!recentMetricsExpanded)}
          style={{ cursor: 'pointer', userSelect: 'none' }}
        >
          Recent Metrics {recentMetricsExpanded ? '▼' : '▶'}
        </h3>
        {recentMetricsExpanded && (
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
        )}
      </div>
      </div>
    </div>
  );
};

export default Dashboard;
