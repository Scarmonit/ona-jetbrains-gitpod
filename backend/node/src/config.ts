/**
 * Configuration module for the Fastify backend.
 *
 * Loads environment variables and provides typed configuration.
 * Uses dotenv to load from .env file if present.
 */

import { config as dotenvConfig } from 'dotenv';

// Load environment variables from .env file
dotenvConfig();

/**
 * Application configuration interface.
 */
export interface Config {
  /** Application name */
  readonly appName: string;
  /** Application version */
  readonly appVersion: string;
  /** Server port */
  readonly port: number;
  /** Server host */
  readonly host: string;
  /** Node environment (development, production) */
  readonly nodeEnv: string;
  /** Logging level */
  readonly logLevel: string;
  /** OpenAI API key (optional) */
  readonly openaiApiKey: string | undefined;
  /** Anthropic API key (optional) */
  readonly anthropicApiKey: string | undefined;
  /** OpenAI model to use */
  readonly openaiModel: string;
  /** Anthropic model to use */
  readonly anthropicModel: string;
  /** LLM request timeout in milliseconds */
  readonly llmTimeout: number;
  /** Maximum prompt length in characters */
  readonly maxPromptLength: number;
  /** Rate limit requests per minute */
  readonly rateLimitPerMinute: number;
}

/**
 * Get a string environment variable with optional default.
 */
function getEnvString(key: string, defaultValue: string): string {
  return process.env[key] ?? defaultValue;
}

/**
 * Get a number environment variable with optional default.
 */
function getEnvNumber(key: string, defaultValue: number): number {
  const value = process.env[key];
  if (value === undefined) {
    return defaultValue;
  }
  const parsed = parseInt(value, 10);
  return isNaN(parsed) ? defaultValue : parsed;
}

/**
 * Application configuration loaded from environment variables.
 */
export const config: Config = {
  appName: getEnvString('APP_NAME', 'Ona Node.js Backend'),
  appVersion: getEnvString('APP_VERSION', '1.0.0'),
  port: getEnvNumber('PORT', 3001),
  host: getEnvString('HOST', '0.0.0.0'),
  nodeEnv: getEnvString('NODE_ENV', 'development'),
  logLevel: getEnvString('NODE_LOG_LEVEL', 'info'),
  openaiApiKey: process.env['OPENAI_API_KEY'],
  anthropicApiKey: process.env['ANTHROPIC_API_KEY'],
  openaiModel: getEnvString('OPENAI_MODEL', 'gpt-4o-mini'),
  anthropicModel: getEnvString('ANTHROPIC_MODEL', 'claude-3-5-sonnet-latest'),
  llmTimeout: getEnvNumber('LLM_TIMEOUT', 30000),
  maxPromptLength: getEnvNumber('MAX_PROMPT_LENGTH', 4000),
  rateLimitPerMinute: getEnvNumber('RATE_LIMIT_PER_MINUTE', 60),
};

/**
 * Check if running in development mode.
 */
export function isDevelopment(): boolean {
  return config.nodeEnv === 'development';
}

/**
 * Check if running in production mode.
 */
export function isProduction(): boolean {
  return config.nodeEnv === 'production';
}
