#!/usr/bin/env node

/**
 * Render MCP Server
 * Allows AI tools to interact with Render API
 * Provides tools for deployment management, logs, metrics
 */

const http = require('http');
const https = require('https');

class RenderMCPServer {
  constructor(apiKey, serviceId) {
    this.apiKey = apiKey;
    this.serviceId = serviceId;
    this.baseUrl = 'https://api.render.com/v1';
  }

  /**
   * Make authenticated API call to Render
   */
  async apiCall(method, path, body = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(`${this.baseUrl}${path}`);
      const options = {
        hostname: url.hostname,
        port: url.port,
        path: url.pathname + url.search,
        method: method,
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve({
              status: res.statusCode,
              data: JSON.parse(data)
            });
          } catch {
            resolve({ status: res.statusCode, data });
          }
        });
      });

      req.on('error', reject);
      if (body) req.write(JSON.stringify(body));
      req.end();
    });
  }

  /**
   * Get service status
   */
  async getServiceStatus() {
    return this.apiCall('GET', `/services/${this.serviceId}`);
  }

  /**
   * Get recent deployments
   */
  async getDeployments(limit = 10) {
    return this.apiCall('GET', `/services/${this.serviceId}/deploys?limit=${limit}`);
  }

  /**
   * Get service logs
   */
  async getLogs(limit = 100) {
    return this.apiCall('GET', `/services/${this.serviceId}/logs?limit=${limit}`);
  }

  /**
   * Trigger a new deployment
   */
  async triggerDeploy() {
    return this.apiCall('POST', `/services/${this.serviceId}/deploys`);
  }

  /**
   * Get environment variables
   */
  async getEnvVars() {
    return this.apiCall('GET', `/services/${this.serviceId}/env-vars`);
  }

  /**
   * Update environment variable
   */
  async updateEnvVar(key, value) {
    return this.apiCall('PUT', `/services/${this.serviceId}/env-vars/${key}`, {
      value: value
    });
  }

  /**
   * Get service metrics
   */
  async getMetrics() {
    return this.apiCall('GET', `/services/${this.serviceId}/metrics`);
  }

  /**
   * List available tools
   */
  getTools() {
    return [
      {
        name: 'get_render_status',
        description: 'Get current status of Semptify deployment on Render',
        inputSchema: { type: 'object', properties: {} }
      },
      {
        name: 'get_deployments',
        description: 'Get recent deployment history',
        inputSchema: {
          type: 'object',
          properties: {
            limit: { type: 'number', description: 'Number of deployments to retrieve' }
          }
        }
      },
      {
        name: 'get_logs',
        description: 'Get service logs',
        inputSchema: {
          type: 'object',
          properties: {
            limit: { type: 'number', description: 'Number of log lines' }
          }
        }
      },
      {
        name: 'trigger_deploy',
        description: 'Trigger a new deployment on Render',
        inputSchema: { type: 'object', properties: {} }
      },
      {
        name: 'get_env_vars',
        description: 'Get environment variables for the service',
        inputSchema: { type: 'object', properties: {} }
      },
      {
        name: 'update_env_var',
        description: 'Update an environment variable',
        inputSchema: {
          type: 'object',
          properties: {
            key: { type: 'string', description: 'Environment variable name' },
            value: { type: 'string', description: 'New value' }
          },
          required: ['key', 'value']
        }
      },
      {
        name: 'get_metrics',
        description: 'Get service performance metrics',
        inputSchema: { type: 'object', properties: {} }
      }
    ];
  }

  /**
   * Handle tool calls
   */
  async handleTool(toolName, args) {
    switch (toolName) {
      case 'get_render_status':
        return await this.getServiceStatus();
      case 'get_deployments':
        return await this.getDeployments(args.limit || 10);
      case 'get_logs':
        return await this.getLogs(args.limit || 100);
      case 'trigger_deploy':
        return await this.triggerDeploy();
      case 'get_env_vars':
        return await this.getEnvVars();
      case 'update_env_var':
        return await this.updateEnvVar(args.key, args.value);
      case 'get_metrics':
        return await this.getMetrics();
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }
}

// Initialize and start server
const apiKey = process.env.RENDER_API_KEY;
const serviceId = process.env.RENDER_SERVICE_ID;

if (!apiKey || !serviceId) {
  console.error('Error: RENDER_API_KEY and RENDER_SERVICE_ID environment variables required');
  process.exit(1);
}

const server = new RenderMCPServer(apiKey, serviceId);

// MCP Server Protocol Handler
const handleRequest = async (request, response) => {
  const body = await new Promise((resolve, reject) => {
    let data = '';
    request.on('data', chunk => data += chunk);
    request.on('end', () => resolve(data));
    request.on('error', reject);
  });

  try {
    const json = JSON.parse(body);

    if (json.method === 'tools/list') {
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({ tools: server.getTools() }));
    } else if (json.method === 'tools/call') {
      const result = await server.handleTool(json.params.name, json.params.arguments);
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({ result }));
    } else {
      response.writeHead(400, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({ error: `Unknown method: ${json.method}` }));
    }
  } catch (error) {
    response.writeHead(500, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ error: error.message }));
  }
};

const port = process.env.MCP_PORT || 3000;
http.createServer(handleRequest).listen(port, () => {
  console.log(`🚀 Render MCP Server listening on port ${port}`);
  console.log(`Service ID: ${serviceId}`);
});
