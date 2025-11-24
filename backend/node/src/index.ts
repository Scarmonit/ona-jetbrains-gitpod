/**
 * Main entry point for the Fastify backend server.
 *
 * Bootstraps the Fastify server with routes and middleware.
 */

import Fastify, { FastifyInstance } from 'fastify';
import { config, isDevelopment } from './config.js';
import { logger } from './logging.js';
import { healthRoutes } from './routes/health.js';
import { infoRoutes } from './routes/info.js';
import { llmRoutes } from './routes/llm.js';

/**
 * Build and configure the Fastify application.
 *
 * @returns Configured Fastify instance
 */
export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: isDevelopment(),
    disableRequestLogging: !isDevelopment(),
  });

  // Register routes
  await app.register(healthRoutes);
  await app.register(infoRoutes);
  await app.register(llmRoutes);

  // Error handler
  app.setErrorHandler((error, _request, reply) => {
    logger.error('Unhandled error', {
      message: error.message,
      statusCode: error.statusCode,
    });

    const statusCode = error.statusCode ?? 500;
    const message =
      statusCode >= 500 && !isDevelopment() ? 'Internal server error' : error.message;

    return reply.status(statusCode).send({
      error: message,
    });
  });

  // Not found handler
  app.setNotFoundHandler((_request, reply) => {
    return reply.status(404).send({
      error: 'Not found',
    });
  });

  return app;
}

/**
 * Start the server.
 */
export async function start(): Promise<void> {
  try {
    const app = await buildApp();

    await app.listen({
      port: config.port,
      host: config.host,
    });

    logger.info('Server started', {
      port: config.port,
      host: config.host,
      environment: config.nodeEnv,
    });

    console.log(`Server running on http://${config.host}:${config.port}`);
    console.log(`Health check: http://${config.host}:${config.port}/health`);
    console.log(`API info: http://${config.host}:${config.port}/info`);
  } catch (err) {
    const error = err as Error;
    logger.error('Failed to start server', { error: error.message });
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Start the server if this module is run directly (not imported)
const isMainModule =
  typeof require !== 'undefined' &&
  require.main === module;

// For ESM, check if this file is being run directly
const isDirectExecution = process.argv[1]?.includes('index');

if (isMainModule || (isDirectExecution && !process.env['JEST_WORKER_ID'])) {
  start().catch(console.error);
}
