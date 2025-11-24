/**
 * LLM route handler with OpenAI and Anthropic integration.
 *
 * Provides LLM completion endpoint with provider selection:
 * 1. OpenAI (if OPENAI_API_KEY is set)
 * 2. Anthropic (if ANTHROPIC_API_KEY is set)
 * 3. Stub (fallback when no keys are configured)
 */

import { createHash } from 'crypto';
import { FastifyInstance, FastifyPluginAsync, FastifyReply, FastifyRequest } from 'fastify';
import { config } from '../config.js';
import { logger } from '../logging.js';

/**
 * LLM request interface.
 */
interface LLMRequest {
  prompt: string;
}

/**
 * LLM response interface.
 */
interface LLMResponse {
  provider: string;
  model: string;
  output: string;
  stub: boolean;
  error: string | null;
}

/**
 * Error response interface.
 */
interface ErrorResponse {
  error: string;
}

/**
 * OpenAI API response structure.
 */
interface OpenAIResponse {
  choices?: Array<{
    message?: {
      content?: string;
    };
  }>;
}

/**
 * Anthropic API response structure.
 */
interface AnthropicResponse {
  content?: Array<{
    type: string;
    text?: string;
  }>;
}

/** Milliseconds per minute for rate limiting calculations */
const MS_PER_MINUTE = 60000;

/**
 * Rate limiter using in-memory token bucket.
 */
class RateLimiter {
  private tokens: number;
  private readonly maxTokens: number;
  private lastRefill: number;

  constructor(tokensPerMinute: number) {
    this.maxTokens = tokensPerMinute;
    this.tokens = tokensPerMinute;
    this.lastRefill = Date.now();
  }

  /**
   * Check if a request is allowed and consume a token.
   * @returns true if allowed, false if rate limited
   */
  tryConsume(): boolean {
    this.refill();
    if (this.tokens > 0) {
      this.tokens--;
      return true;
    }
    return false;
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = now - this.lastRefill;
    const tokensToAdd = Math.floor((elapsed / MS_PER_MINUTE) * this.maxTokens);
    if (tokensToAdd > 0) {
      this.tokens = Math.min(this.maxTokens, this.tokens + tokensToAdd);
      this.lastRefill = now;
    }
  }
}

const rateLimiter = new RateLimiter(config.rateLimitPerMinute);

/**
 * Get SHA256 hash prefix of prompt for secure logging.
 */
function getPromptHashPrefix(prompt: string): string {
  return createHash('sha256').update(prompt).digest('hex').substring(0, 8);
}

/**
 * Call OpenAI Chat Completions API.
 */
async function callOpenAI(prompt: string): Promise<LLMResponse> {
  logger.debug('OpenAI request', {
    promptLength: prompt.length,
    hashPrefix: getPromptHashPrefix(prompt),
  });

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), config.llmTimeout);

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${config.openaiApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: config.openaiModel,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 1024,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      logger.error('OpenAI API error', { status: response.status, error: errorText });
      return {
        provider: 'openai',
        model: config.openaiModel,
        output: '',
        stub: false,
        error: `OpenAI API error: ${response.status}`,
      };
    }

    const data = (await response.json()) as OpenAIResponse;
    const content = data.choices?.[0]?.message?.content ?? '';

    if (!content) {
      logger.warn('OpenAI returned empty response');
      return {
        provider: 'openai',
        model: config.openaiModel,
        output: '',
        stub: false,
        error: 'OpenAI returned empty response',
      };
    }

    return {
      provider: 'openai',
      model: config.openaiModel,
      output: content,
      stub: false,
      error: null,
    };
  } catch (err) {
    clearTimeout(timeoutId);
    const error = err as Error;

    if (error.name === 'AbortError') {
      logger.error('OpenAI request timed out');
      return {
        provider: 'openai',
        model: config.openaiModel,
        output: '',
        stub: false,
        error: 'Request timed out',
      };
    }

    logger.error('OpenAI request failed', { error: error.message });
    return {
      provider: 'openai',
      model: config.openaiModel,
      output: '',
      stub: false,
      error: `Request failed: ${error.message}`,
    };
  }
}

/**
 * Call Anthropic Messages API.
 */
async function callAnthropic(prompt: string): Promise<LLMResponse> {
  logger.debug('Anthropic request', {
    promptLength: prompt.length,
    hashPrefix: getPromptHashPrefix(prompt),
  });

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), config.llmTimeout);

  try {
    // Guaranteed to be defined since this function is only called when anthropicApiKey is set
    const apiKey = config.anthropicApiKey as string;
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: config.anthropicModel,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 1024,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      logger.error('Anthropic API error', { status: response.status, error: errorText });
      return {
        provider: 'anthropic',
        model: config.anthropicModel,
        output: '',
        stub: false,
        error: `Anthropic API error: ${response.status}`,
      };
    }

    const data = (await response.json()) as AnthropicResponse;
    let content = '';
    for (const block of data.content ?? []) {
      if (block.type === 'text' && block.text) {
        content = block.text;
        break;
      }
    }

    if (!content) {
      logger.warn('Anthropic returned empty response');
      return {
        provider: 'anthropic',
        model: config.anthropicModel,
        output: '',
        stub: false,
        error: 'Anthropic returned empty response',
      };
    }

    return {
      provider: 'anthropic',
      model: config.anthropicModel,
      output: content,
      stub: false,
      error: null,
    };
  } catch (err) {
    clearTimeout(timeoutId);
    const error = err as Error;

    if (error.name === 'AbortError') {
      logger.error('Anthropic request timed out');
      return {
        provider: 'anthropic',
        model: config.anthropicModel,
        output: '',
        stub: false,
        error: 'Request timed out',
      };
    }

    logger.error('Anthropic request failed', { error: error.message });
    return {
      provider: 'anthropic',
      model: config.anthropicModel,
      output: '',
      stub: false,
      error: `Request failed: ${error.message}`,
    };
  }
}

/**
 * Create a stub response when no LLM provider is configured.
 */
function createStubResponse(): LLMResponse {
  return {
    provider: 'stub',
    model: 'none',
    output: 'Stub response. Set OPENAI_API_KEY or ANTHROPIC_API_KEY for real LLM calls.',
    stub: true,
    error: null,
  };
}

/**
 * Process an LLM completion request.
 */
async function processLLMRequest(prompt: string): Promise<LLMResponse> {
  // Provider selection order: OpenAI > Anthropic > Stub
  if (config.openaiApiKey) {
    logger.info('Using OpenAI provider');
    return callOpenAI(prompt);
  }

  if (config.anthropicApiKey) {
    logger.info('Using Anthropic provider');
    return callAnthropic(prompt);
  }

  logger.info('No LLM provider configured, returning stub response');
  return createStubResponse();
}

/**
 * Register LLM routes.
 *
 * @param fastify - Fastify instance
 */
export const llmRoutes: FastifyPluginAsync = async (
  fastify: FastifyInstance
): Promise<void> => {
  fastify.post(
    '/llm',
    async (
      request: FastifyRequest<{ Body: LLMRequest }>,
      reply: FastifyReply
    ): Promise<LLMResponse | ErrorResponse> => {
      // Rate limiting
      if (!rateLimiter.tryConsume()) {
        logger.warn('Rate limit exceeded');
        reply.status(429);
        return { error: 'Rate limit exceeded. Try again later.' };
      }

      const body = request.body as LLMRequest | undefined;
      const prompt = body?.prompt;

      // Validate prompt
      if (!prompt || typeof prompt !== 'string') {
        reply.status(400);
        return { error: 'Prompt is required' };
      }

      if (prompt.length === 0) {
        reply.status(400);
        return { error: 'Prompt cannot be empty' };
      }

      if (prompt.length > config.maxPromptLength) {
        reply.status(400);
        return {
          error: `Prompt exceeds maximum length of ${config.maxPromptLength} characters`,
        };
      }

      logger.info('Processing LLM request', { promptLength: prompt.length });

      try {
        const response = await processLLMRequest(prompt);
        return response;
      } catch (err) {
        const error = err as Error;
        logger.error('Unexpected error during LLM completion', { error: error.message });
        reply.status(500);
        return { error: `Internal error: ${error.message}` };
      }
    }
  );
};
