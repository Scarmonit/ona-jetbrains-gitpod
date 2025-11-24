/**
 * Logging module for the Fastify backend.
 *
 * Provides structured console logging with configurable log levels.
 * Uses a lightweight custom implementation to minimize dependencies.
 */

import { config } from './config.js';

/**
 * Log levels in order of severity.
 */
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

/**
 * Numeric values for log levels (higher = more severe).
 */
const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

/**
 * Get the configured minimum log level.
 */
function getMinLevel(): number {
  const level = config.logLevel.toLowerCase() as LogLevel;
  return LOG_LEVELS[level] ?? LOG_LEVELS.info;
}

/**
 * Format a log message with timestamp and level.
 */
function formatMessage(level: LogLevel, message: string, context?: object): string {
  const timestamp = new Date().toISOString();
  const base = { timestamp, level, message };
  if (context) {
    return JSON.stringify({ ...base, ...context });
  }
  return JSON.stringify(base);
}

/**
 * Logger interface for structured logging.
 */
export interface Logger {
  /**
   * Log a debug message.
   * @param message - The message to log
   * @param context - Optional additional context
   */
  debug(message: string, context?: object): void;

  /**
   * Log an info message.
   * @param message - The message to log
   * @param context - Optional additional context
   */
  info(message: string, context?: object): void;

  /**
   * Log a warning message.
   * @param message - The message to log
   * @param context - Optional additional context
   */
  warn(message: string, context?: object): void;

  /**
   * Log an error message.
   * @param message - The message to log
   * @param context - Optional additional context
   */
  error(message: string, context?: object): void;
}

/**
 * Create a logger instance.
 *
 * @returns Logger instance with structured logging methods
 */
export function createLogger(): Logger {
  const minLevel = getMinLevel();

  return {
    debug(message: string, context?: object): void {
      if (LOG_LEVELS.debug >= minLevel) {
        console.log(formatMessage('debug', message, context));
      }
    },

    info(message: string, context?: object): void {
      if (LOG_LEVELS.info >= minLevel) {
        console.log(formatMessage('info', message, context));
      }
    },

    warn(message: string, context?: object): void {
      if (LOG_LEVELS.warn >= minLevel) {
        console.warn(formatMessage('warn', message, context));
      }
    },

    error(message: string, context?: object): void {
      if (LOG_LEVELS.error >= minLevel) {
        console.error(formatMessage('error', message, context));
      }
    },
  };
}

/**
 * Default logger instance.
 */
export const logger = createLogger();
