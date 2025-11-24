/**
 * Tests for health and LLM endpoints.
 *
 * These tests verify endpoint behavior with stub responses when no API keys are configured.
 */

import { FastifyInstance } from 'fastify';

// Mock the config to ensure no API keys
jest.mock('../src/config.js', () => ({
  config: {
    appName: 'Test App',
    appVersion: '1.0.0',
    port: 3001,
    host: '0.0.0.0',
    nodeEnv: 'test',
    logLevel: 'error',
    openaiApiKey: undefined,
    anthropicApiKey: undefined,
    openaiModel: 'gpt-4o-mini',
    anthropicModel: 'claude-3-5-sonnet-latest',
    llmTimeout: 30000,
    maxPromptLength: 4000,
    rateLimitPerMinute: 60,
  },
  isDevelopment: () => false,
  isProduction: () => false,
}));

// Import after mocking
import { buildApp } from '../src/index.js';

describe('API Endpoints', () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('GET /health', () => {
    it('should return ok status', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/health',
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body) as { status: string; timestamp: string; version: string };
      expect(body.status).toBe('ok');
      expect(body.timestamp).toBeDefined();
      expect(body.version).toBe('1.0.0');
    });
  });

  describe('GET /info', () => {
    it('should return service info with stub provider when no keys configured', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/info',
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body) as {
        name: string;
        version: string;
        llm_providers: string[];
        active_provider: string;
      };
      expect(body.name).toBe('Test App');
      expect(body.llm_providers).toContain('stub');
      expect(body.active_provider).toBe('stub');
    });
  });

  describe('POST /llm', () => {
    it('should return stub response when no API keys configured', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/llm',
        headers: {
          'Content-Type': 'application/json',
        },
        payload: {
          prompt: 'Hello, world!',
        },
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body) as {
        provider: string;
        model: string;
        output: string;
        stub: boolean;
        error: string | null;
      };
      expect(body.provider).toBe('stub');
      expect(body.model).toBe('none');
      expect(body.stub).toBe(true);
      expect(body.error).toBeNull();
      expect(body.output.toLowerCase()).toContain('stub');
    });

    it('should reject empty prompt', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/llm',
        headers: {
          'Content-Type': 'application/json',
        },
        payload: {
          prompt: '',
        },
      });

      expect(response.statusCode).toBe(400);
    });

    it('should reject missing prompt', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/llm',
        headers: {
          'Content-Type': 'application/json',
        },
        payload: {},
      });

      expect(response.statusCode).toBe(400);
    });

    it('should reject prompt exceeding max length', async () => {
      const longPrompt = 'a'.repeat(5000);
      const response = await app.inject({
        method: 'POST',
        url: '/llm',
        headers: {
          'Content-Type': 'application/json',
        },
        payload: {
          prompt: longPrompt,
        },
      });

      expect(response.statusCode).toBe(400);
    });
  });

  describe('404 Handler', () => {
    it('should return 404 for unknown routes', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/unknown',
      });

      expect(response.statusCode).toBe(404);
    });
  });
});
