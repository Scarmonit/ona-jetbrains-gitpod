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
| 5000 | Flask API |
| 8000 | FastAPI |
| 8080 | Proxy |
| 8888 | Jupyter |
| 11434 | Ollama |

## Environment Variables

Set these in your Gitpod dashboard or `.env` file:
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key

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

## Backend FastAPI Service

A production-ready FastAPI backend service located in `backend/api/` with modular structure, health checks, LLM proxy placeholder, and comprehensive configuration management.

### Running Locally

From the `backend/api` directory:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running in Gitpod

The service is pre-configured for Gitpod. After opening the workspace:

```bash
cd backend/api
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at the Gitpod-exposed port 8000.

### Running with Docker

```bash
# Build the image
cd backend/api
docker build -t ona-backend-api .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  ona-backend-api
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Ona Backend API |
| `APP_VERSION` | Application version | 0.1.0 |
| `OPENAI_API_KEY` | OpenAI API key for LLM integration | None |
| `ANTHROPIC_API_KEY` | Anthropic API key for LLM integration | None |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `ENV` | Environment (development, staging, production) | development |

### API Endpoints

- `GET /health` - Health check with uptime information
- `GET /info` - Application metadata
- `POST /llm` - LLM proxy endpoint
- `GET /docs` - OpenAPI documentation (Swagger UI)
- `GET /redoc` - ReDoc documentation

### LLM Endpoint Behavior

The `/llm` endpoint accepts a JSON body with a `prompt` field (and optional `model`):

```json
{
  "prompt": "Hello, how are you?",
  "model": "gpt-4"
}
```

**Without API keys configured:** Returns a stub response with `stub: true` and a message explaining how to configure API keys.

**With OPENAI_API_KEY or ANTHROPIC_API_KEY set:** Returns a stub response indicating the integration point is ready for implementation.

### Extending LLM Integration

To implement real LLM calls:

1. Edit `backend/api/app/llm.py`
2. In the `process_prompt()` function, replace the stub responses with actual API calls:
   - For OpenAI: Use the `openai` library to make chat completion requests
   - For Anthropic: Use the `anthropic` library to make message requests
3. Add the necessary client libraries to `requirements.txt`
4. Update the response to set `stub=False` when returning real LLM output

Example integration point in `llm.py`:
```python
if settings.OPENAI_API_KEY:
    # Replace this stub with:
    # from openai import OpenAI
    # client = OpenAI(api_key=settings.OPENAI_API_KEY)
    # response = client.chat.completions.create(...)
    # return LLMResponse(provider="openai", ..., stub=False)
```

### Running Tests

```bash
cd backend/api
pip install -r requirements.txt
pytest tests/ -v
```

## License

MIT
