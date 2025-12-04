import { PerformanceMetrics, TestResults } from '../types';
import { restApi } from '../api/restClient';
import { graphqlApi } from '../api/graphqlClient';

export type APIType = 'REST' | 'GraphQL';

export interface TestConfig {
  apiType: APIType;
  operation: string;
  iterations: number;
}

export class PerformanceTester {
  private metrics: PerformanceMetrics[] = [];

  async runTest(config: TestConfig): Promise<PerformanceMetrics[]> {
    const results: PerformanceMetrics[] = [];

    for (let i = 0; i < config.iterations; i++) {
      const metric = await this.executeOperation(config.apiType, config.operation);
      results.push(metric);
      this.metrics.push(metric);
    }

    return results;
  }

  private async executeOperation(apiType: APIType, operation: string): Promise<PerformanceMetrics> {
    const startTime = performance.now();
    let payloadSize = 0;
    let success = true;
    let errorMessage: string | undefined;

    try {
      let response: any;

      if (apiType === 'REST') {
        response = await this.executeRestOperation(operation);
      } else if (apiType === 'GraphQL') {
        response = await this.executeGraphQLOperation(operation);
      }

      payloadSize = this.calculatePayloadSize(response);
    } catch (error: any) {
      success = false;
      errorMessage = error.message;
    }

    const endTime = performance.now();
    const responseTime = endTime - startTime;

    return {
      apiType,
      operation,
      responseTime,
      payloadSize,
      timestamp: Date.now(),
      success,
      errorMessage,
    };
  }

  private async executeRestOperation(operation: string): Promise<any> {
    switch (operation) {
      case 'getUser':
        return await restApi.getUser(1);
      case 'listUsers':
        return await restApi.listUsers(0, 20);
      case 'createUser':
        return await restApi.createUser({
          username: `testuser${Date.now()}`,
          email: `test${Date.now()}@example.com`,
          firstName: 'Test',
          lastName: 'User',
        });
      case 'getUserOrders':
        return await restApi.getUserOrders(1);
      case 'searchUsers':
        return await restApi.searchUsers('john', 10);
      default:
        throw new Error(`Unknown operation: ${operation}`);
    }
  }

  private async executeGraphQLOperation(operation: string): Promise<any> {
    switch (operation) {
      case 'getUser':
        return await graphqlApi.getUser(1);
      case 'listUsers':
        return await graphqlApi.listUsers(0, 20);
      case 'createUser':
        return await graphqlApi.createUser({
          username: `testuser${Date.now()}`,
          email: `test${Date.now()}@example.com`,
          firstName: 'Test',
          lastName: 'User',
        });
      case 'getUserOrders':
        return await graphqlApi.getUserOrders(1);
      case 'searchUsers':
        return await graphqlApi.searchUsers('john', 10);
      default:
        throw new Error(`Unknown operation: ${operation}`);
    }
  }

  private calculatePayloadSize(response: any): number {
    return new Blob([JSON.stringify(response)]).size;
  }

  getMetrics(): PerformanceMetrics[] {
    return this.metrics;
  }

  calculateResults(): TestResults {
    const results: TestResults = {};

    this.metrics.forEach((metric) => {
      const key = `${metric.apiType}-${metric.operation}`;

      if (!results[key]) {
        results[key] = {
          count: 0,
          totalTime: 0,
          avgTime: 0,
          minTime: Infinity,
          maxTime: 0,
          successRate: 0,
          avgPayloadSize: 0,
        };
      }

      const result = results[key];
      result.count++;
      result.totalTime += metric.responseTime;
      result.minTime = Math.min(result.minTime, metric.responseTime);
      result.maxTime = Math.max(result.maxTime, metric.responseTime);
      result.avgPayloadSize += metric.payloadSize;

      if (metric.success) {
        result.successRate++;
      }
    });

    Object.keys(results).forEach((key) => {
      const result = results[key];
      result.avgTime = result.totalTime / result.count;
      result.successRate = (result.successRate / result.count) * 100;
      result.avgPayloadSize = result.avgPayloadSize / result.count;
    });

    return results;
  }

  clearMetrics(): void {
    this.metrics = [];
  }
}
