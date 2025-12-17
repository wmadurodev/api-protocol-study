import React, { useState } from 'react';
import { PerformanceTester, APIType } from './utils/performanceTester';
import { PerformanceMetrics, TestResults } from './types';
import Dashboard from './components/Dashboard';
import './App.css';

const App: React.FC = () => {
  const [tester] = useState(() => new PerformanceTester());
  const [metrics, setMetrics] = useState<PerformanceMetrics[]>([]);
  const [results, setResults] = useState<TestResults>({});
  const [isRunning, setIsRunning] = useState(false);
  const [selectedApi, setSelectedApi] = useState<APIType>('REST');
  const [selectedOperation, setSelectedOperation] = useState('getUser');
  const [iterations, setIterations] = useState(10);

  const operations = [
    'getUser',
    'listUsers',
    'createUser',
    'getUserOrders',
    'searchUsers',
  ];

  const runTest = async () => {
    setIsRunning(true);
    try {
      await tester.runTest({
        apiType: selectedApi,
        operation: selectedOperation,
        iterations,
      });

      setMetrics([...tester.getMetrics()]);
      setResults(tester.calculateResults());
    } catch (error) {
      console.error('Test execution error:', error);
    } finally {
      setIsRunning(false);
    }
  };

  const runAllTests = async () => {
    setIsRunning(true);
    try {
      const apis: APIType[] = ['REST', 'GraphQL', 'gRPC'];

      for (const api of apis) {
        for (const operation of operations) {
          await tester.runTest({
            apiType: api,
            operation,
            iterations,
          });
        }
      }

      setMetrics([...tester.getMetrics()]);
      setResults(tester.calculateResults());
    } catch (error) {
      console.error('Test execution error:', error);
    } finally {
      setIsRunning(false);
    }
  };

  const clearResults = () => {
    tester.clearMetrics();
    setMetrics([]);
    setResults({});
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>API Performance Comparison</h1>
        <p>Compare performance between REST, gRPC, and GraphQL APIs</p>
      </header>

      <div className="container">
        <div className="controls-panel">
          <h2>Test Configuration</h2>

          <div className="control-group">
            <label>API Type:</label>
            <select
              value={selectedApi}
              onChange={(e) => setSelectedApi(e.target.value as APIType)}
              disabled={isRunning}
            >
              <option value="REST">REST</option>
              <option value="GraphQL">GraphQL</option>
              <option value="gRPC">gRPC</option>
            </select>
          </div>

          <div className="control-group">
            <label>Operation:</label>
            <select
              value={selectedOperation}
              onChange={(e) => setSelectedOperation(e.target.value)}
              disabled={isRunning}
            >
              {operations.map((op) => (
                <option key={op} value={op}>
                  {op}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group">
            <label>Iterations:</label>
            <input
              type="number"
              value={iterations}
              onChange={(e) => setIterations(Number(e.target.value))}
              min="1"
              max="1000"
              disabled={isRunning}
            />
          </div>

          <div className="button-group">
            <button onClick={runTest} disabled={isRunning} className="primary">
              {isRunning ? 'Running...' : 'Run Test'}
            </button>
            <button onClick={runAllTests} disabled={isRunning} className="secondary">
              Run All Tests
            </button>
            <button onClick={clearResults} disabled={isRunning} className="danger">
              Clear Results
            </button>
          </div>
        </div>

        <Dashboard metrics={metrics} results={results} isRunning={isRunning} />
      </div>
    </div>
  );
};

export default App;
