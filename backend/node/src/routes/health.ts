/**
 * Health check route handler.
 *
 * Provides a simple endpoint to verify the service is running.
 */

import { FastifyInstance, FastifyPluginAsync } from 'fastify';
import { config } from '../config.js';

/**
 * Health check response interface.
 */
interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

/**
 * Register health check routes.
 *
 * @param fastify - Fastify instance
 */
export const healthRoutes: FastifyPluginAsync = async (
  fastify: FastifyInstance
): Promise<void> => {
  fastify.get<{ Reply: HealthResponse }>(
    '/health',
    async (_request, reply) => {
      const response: HealthResponse = {
        status: 'ok',
        timestamp: new Date().toISOString(),
        version: config.appVersion,
      };
      await reply.send(response);
    }
  );
};
