# Node.js Fastify Backend Service

A production-ready Node.js backend service built with Fastify and TypeScript, providing LLM integration with OpenAI and Anthropic.

## Features

- **Health Check** (`GET /health`) - Service health monitoring
- **Info** (`GET /info`) - Service information including available LLM providers
- **LLM Completion** (`POST /llm`) - LLM text completion with OpenAI/Anthropic integration

## LLM Provider Selection

The service selects LLM providers in the following order:

1. **OpenAI** - If `OPENAI_API_KEY` is set
2. **Anthropic** - If `ANTHROPIC_API_KEY` is set (and OpenAI key is not)
3. **Stub** - Fallback when no API keys are configured

## Quick Start

### Prerequisites

- Node.js 20.x or higher
- npm or yarn

### Installation

```bash
cd backend/node
npm install
```

### Development

```bash
# Run with ts-node (development)
npm run dev

# Or build and run
npm run build
npm start
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3001` |
| `HOST` | Server host | `0.0.0.0` |
| `NODE_ENV` | Environment | `development` |
| `NODE_LOG_LEVEL` | Log level (debug, info, warn, error) | `info` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OPENAI_MODEL` | OpenAI model | `gpt-4o-mini` |
| `ANTHROPIC_MODEL` | Anthropic model | `claude-3-5-sonnet-latest` |
| `LLM_TIMEOUT` | LLM request timeout (ms) | `30000` |
| `MAX_PROMPT_LENGTH` | Maximum prompt length | `4000` |
| `RATE_LIMIT_PER_MINUTE` | Rate limit (requests/min) | `60` |

### Docker

```bash
# Build image
docker build -t ona-node-backend .

# Run container
docker run -p 3001:3001 \
  -e OPENAI_API_KEY=your-key \
  ona-node-backend
```

## API Reference

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "version": "1.0.0"
}
```

### GET /info

Service information.

**Response:**
```json
{
  "name": "Ona Node.js Backend",
  "version": "1.0.0",
  "environment": "development",
  "llm_providers": ["openai"],
  "active_provider": "openai"
}
```

### POST /llm

LLM text completion.

**Request:**
```json
{
  "prompt": "Hello, how are you?"
}
```

**Response:**
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "output": "I'm doing well, thank you!",
  "stub": false,
  "error": null
}
```

## Testing

```bash
npm test
```

## Linting

```bash
npm run lint
npm run lint:fix  # Auto-fix issues
```

## Type Checking

```bash
npm run typecheck
```

## Project Structure

```
backend/node/
├── src/
│   ├── index.ts       # Server bootstrap
│   ├── config.ts      # Configuration
│   ├── logging.ts     # Structured logging
│   └── routes/
│       ├── health.ts  # Health endpoint
│       ├── info.ts    # Info endpoint
│       └── llm.ts     # LLM endpoint
├── tests/
│   └── api.test.ts    # API tests
├── package.json
├── tsconfig.json
├── .eslintrc.json
├── jest.config.js
├── Dockerfile
└── README-NODE.md
```

## Security

- API keys are loaded from environment variables, never committed to code
- Prompt contents are not logged (only length and SHA256 hash prefix for debugging)
- Rate limiting is enforced to prevent abuse
- Non-root user in Docker container
- Input validation for prompt length
