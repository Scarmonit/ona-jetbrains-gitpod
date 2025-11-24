/**
 * Info route handler.
 *
 * Provides information about the service including available LLM providers.
 */

import { FastifyInstance, FastifyPluginAsync } from 'fastify';
import { config } from '../config.js';

/**
 * Info response interface.
 */
interface InfoResponse {
  name: string;
  version: string;
  environment: string;
  llm_providers: string[];
  active_provider: string;
}

/**
 * Determine available LLM providers based on configuration.
 *
 * @returns Array of available provider names
 */
function getAvailableProviders(): string[] {
  const providers: string[] = [];

  if (config.openaiApiKey) {
    providers.push('openai');
  }
  if (config.anthropicApiKey) {
    providers.push('anthropic');
  }
  if (providers.length === 0) {
    providers.push('stub');
  }

  return providers;
}

/**
 * Register info routes.
 *
 * @param fastify - Fastify instance
 */
export const infoRoutes: FastifyPluginAsync = async (
  fastify: FastifyInstance
): Promise<void> => {
  fastify.get<{ Reply: InfoResponse }>(
    '/info',
    async (_request, reply) => {
      const providers = getAvailableProviders();
      const response: InfoResponse = {
        name: config.appName,
        version: config.appVersion,
        environment: config.nodeEnv,
        llm_providers: providers,
        active_provider: providers[0] ?? 'none',
      };
      await reply.send(response);
    }
  );
};
