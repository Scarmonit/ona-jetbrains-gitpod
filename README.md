# Ona JetBrains + Gitpod Environment

A pre-configured cloud development environment with JetBrains IDE support via Gitpod, featuring **GitHub Copilot custom agents** for enhanced AI-assisted development.

## Quick Start

### Option 1: Open in Gitpod
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Scarmonit/ona-jetbrains-gitpod)

### Option 2: JetBrains Gateway
1. Open JetBrains Gateway
2. Connect to Gitpod
3. Select this repository

## Features

### GitHub Copilot Custom Agents 🤖
- **@python-dev** - Python & FastAPI development expert
- **@nodejs-dev** - Node.js & TypeScript development expert
- **@devops** - Docker, Kubernetes & Terraform expert
- **@docs** - Documentation & markdown expert

See [Copilot Usage Guide](.github/COPILOT_USAGE.md) for examples and tips.

### JetBrains Plugins (Pre-installed)
- PythonCore - Python development
- JavaScript - JS/TS support
- Docker - Container management
- Kubernetes - K8s integration
- Database Tools - SQL support
- REST Client - API testing
- Jupyter - Notebook support

### VS Code Extensions
- ESLint & Prettier
- Python
- **GitHub Copilot** (with custom agents)
- Docker
- Kubernetes Tools
- Terraform

### Pre-installed Tools
- Node.js 20
- Python 3.12
- Docker-in-Docker
- kubectl, helm, minikube
- Terraform
- GitHub CLI
- Ollama (local LLM)

### Python Packages
- anthropic, openai - AI APIs
- langchain - LLM framework
- chromadb - Vector database
- jupyter - Notebooks
- fastapi, uvicorn - Web framework

## Port Configuration

| Port | Service |
|------|---------|
| 3000 | Dev Server |
| 3001 | Node.js Fastify API |
| 5000 | Flask API |
| 8000 | FastAPI |
| 8080 | Proxy |
| 8888 | Jupyter |
| 11434 | Ollama |

## Environment Variables

Set these in your Gitpod dashboard or `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM integration | - |
| `ANTHROPIC_API_KEY` | Anthropic API key for LLM integration | - |
| `NODE_ENV` | Node.js environment | `development` |
| `PY_ENV` | Python environment | `development` |
| `NODE_LOG_LEVEL` | Node.js log level (debug, info, warn, error) | `info` |
| `PY_LOG_LEVEL` | Python log level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `OPENAI_MODEL` | OpenAI model for completions | `gpt-4o-mini` |
| `ANTHROPIC_MODEL` | Anthropic model for completions | `claude-3-5-sonnet-latest` |

## Backend Services

This repository includes two production-ready backend services with LLM integration:

### Python FastAPI Service (`backend/api/`)

A FastAPI backend with health, info, and LLM completion endpoints.

**Run locally:**
```bash
cd backend/api
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Run with Docker:**
```bash
cd backend/api
docker build -t ona-python-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key ona-python-backend
```

**Endpoints:**
- `GET /health` - Health check
- `GET /info` - Service info with available LLM providers
- `POST /llm` - LLM text completion

### Node.js Fastify Service (`backend/node/`)

A Fastify TypeScript backend with the same endpoints as the Python service.

**Run locally:**
```bash
cd backend/node
npm install
npm run dev    # Development with ts-node
# OR
npm run build && npm start   # Production
```

**Run with Docker:**
```bash
cd backend/node
docker build -t ona-node-backend .
docker run -p 3001:3001 -e OPENAI_API_KEY=your-key ona-node-backend
```

**Endpoints:**
- `GET /health` - Health check
- `GET /info` - Service info with available LLM providers
- `POST /llm` - LLM text completion

See [Node.js Service README](backend/node/README-NODE.md) for detailed documentation.

## LLM Integration

Both backend services support real LLM integration with OpenAI and Anthropic APIs.

### Provider Selection Order

1. **OpenAI** - Used if `OPENAI_API_KEY` is set
2. **Anthropic** - Used if `ANTHROPIC_API_KEY` is set (and OpenAI key is not)
3. **Stub** - Fallback when no API keys are configured

### Example API Calls

**Python FastAPI (port 8000):**
```bash
# Health check
curl http://localhost:8000/health

# Service info
curl http://localhost:8000/info

# LLM completion
curl -X POST http://localhost:8000/llm \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Hello, how are you?"}'
```

**Node.js Fastify (port 3001):**
```bash
# Health check
curl http://localhost:3001/health

# Service info
curl http://localhost:3001/info

# LLM completion
curl -X POST http://localhost:3001/llm \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Hello, how are you?"}'
```

### Response Format

Both services return the same response format:

```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "output": "I'm doing well, thank you for asking!",
  "stub": false,
  "error": null
}
```

When no API keys are configured, the response indicates a stub:

```json
{
  "provider": "stub",
  "model": "none",
  "output": "Stub response. Set OPENAI_API_KEY or ANTHROPIC_API_KEY for real LLM calls.",
  "stub": true,
  "error": null
}
```

## Using GitHub Copilot Custom Agents

This repository includes specialized Copilot agents for different development tasks:

```
@python-dev Create a FastAPI endpoint for user authentication
@nodejs-dev Write a TypeScript interface for my data model
@devops Create a Kubernetes deployment with autoscaling
@docs Write comprehensive API documentation
```

**Quick Tips:**
- Use `@python-dev` for Python, FastAPI, and AI/LLM integration
- Use `@nodejs-dev` for Node.js, TypeScript, and React
- Use `@devops` for Docker, Kubernetes, Terraform, and CI/CD
- Use `@docs` for README files, API docs, and tutorials

📚 **[Full Copilot Usage Guide](.github/COPILOT_USAGE.md)**

## Example Code

Check the `examples/` directory for sample implementations:
- `examples/python/` - FastAPI application examples
- `examples/nodejs/` - Express.js TypeScript examples
- `examples/devops/` - Docker, Kubernetes, and deployment configs

## Testing

**Python tests:**
```bash
cd backend/api
pip install -r requirements.txt
pytest tests/ -v
```

**Node.js tests:**
```bash
cd backend/node
npm install
npm test
```

## License

MIT
