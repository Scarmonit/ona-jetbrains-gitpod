# GitHub Copilot Instructions

## Project Overview

This is the **Ona JetBrains + Gitpod Environment** – a pre-configured cloud development environment optimized for full‑stack development with AI-powered tools and JetBrains IDE support.

## Code Style and Conventions

### General Principles
- Write clean, maintainable, and well-documented code
- Follow language-specific best practices and conventions
- Prioritize type safety and error handling
- Use descriptive variable and function names
- Keep functions small and focused on a single responsibility

### Python
- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Prefer f-strings for string formatting
- Use `dataclasses` or Pydantic models for structured data
- Write docstrings for all public functions and classes (Google style)
- Use async/await for I/O-bound operations in FastAPI

### JavaScript/TypeScript
- Use ES6+ features (arrow functions, destructuring, template literals)
- Prefer `const` over `let`, avoid `var`
- Use TypeScript for type safety when possible
- Follow Airbnb JavaScript Style Guide
- Use async/await over raw promises
- Implement proper error handling with try/catch

### DevOps & Infrastructure
- Keep Dockerfiles minimal and use multi-stage builds
- Use environment variables for configuration
- Follow the principle of least privilege in Kubernetes manifests
- Comment complex configurations in YAML files
- Use Terraform modules for reusable infrastructure

## AI and LLM Development

### Framework Usage
- Prefer LangChain for complex LLM workflows
- Use Anthropic Claude for reasoning tasks
- Use OpenAI GPT-4 for general-purpose tasks
- Implement proper error handling and fallbacks
- Always validate and sanitize user inputs

### Best Practices
- Store API keys in environment variables, never in code
- Implement rate limiting and retry logic
- Log LLM interactions for debugging (avoid sensitive data)
- Use streaming responses for better UX
- Track tokens and cost

## API Development

### FastAPI
- Use Pydantic models for request/response validation
- Implement proper HTTP status codes
- Add comprehensive docstrings for auto-generated API docs
- Use dependency injection for database connections
- Implement proper CORS configuration
- Add health check endpoints

### REST Design
- Use descriptive endpoint names
- Version APIs (e.g., `/api/v1/`)
- Implement pagination for list endpoints
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)

## Testing

### General
- Write unit tests for business logic
- Write integration tests for API endpoints
- Aim for meaningful coverage (quality over %)
- Use descriptive test names
- Mock external dependencies

### Python
- Use `pytest`
- Use fixtures for reusable setup
- Use `@pytest.mark.parametrize` for scenarios

### JavaScript
- Use Jest or Vitest
- Mock external API calls
- Test success and error cases

## Docker and Containers

- Use specific version tags (avoid `latest`)
- Minimize layer count
- Clean apt cache to reduce image size
- Use `.dockerignore` to exclude unnecessary files
- Run as non-root when possible

## Kubernetes

- Set resource limits and requests
- Add liveness and readiness probes
- Use ConfigMaps for non-sensitive config
- Use Secrets for sensitive data
- Label resources consistently

## Environment Variables

Common variables:
- `OPENAI_API_KEY` – OpenAI API authentication
- `ANTHROPIC_API_KEY` – Anthropic Claude API authentication
- `PYTHONPATH` – Python module search path
- `NODE_ENV` – Node.js environment (development/production)

## Available Tools and Services

### Pre-installed
- Node.js 20.x
- Python 3.12
- Docker-in-Docker
- kubectl, helm, minikube
- Terraform
- GitHub CLI
- Ollama (local LLM runtime)

### Common Ports
- 3000 – Development server
- 5000 – Flask API
- 8000 – FastAPI
- 8888 – Jupyter Notebook
- 11434 – Ollama API

## Copilot Usage (Important)

Custom agent names like `@python-dev`, `@nodejs-dev`, `@devops`, `@docs` are NOT real participants and cannot be invoked. They have been removed to avoid confusion.

Use a single assistant: **@copilot**.

You can ask in plain English, for example:
- "Create a FastAPI endpoint that returns a list of sample users."
- "Write a Dockerfile for a Python FastAPI app using uvicorn."
- "Generate a README section explaining how to run the dev environment."
- "Add a Kubernetes Deployment manifest for the API with resource limits."

If you don't know how to phrase something, just describe what you want to accomplish.

## Common Tasks

### Starting Services
- FastAPI: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Jupyter: `jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser`
- Ollama: `ollama serve` then `ollama pull llama2`

### Development Workflow
1. Make code changes
2. Run linters (eslint, black, etc.)
3. Run tests locally
4. Commit with descriptive messages
5. Push and create PR

## Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Validate and sanitize all user inputs
- Implement authentication & authorization
- Keep dependencies updated
- Use HTTPS for external calls
- Rate limit public APIs

## Performance Guidelines

- Use async for I/O operations
- Implement caching where appropriate
- Optimize database queries
- Use connection pooling
- Monitor resource usage
- Add structured logging

## Documentation

- Keep `README.md` up to date
- Document public APIs
- Add inline comments for complex logic
- Update this file when conventions change
- Include runnable examples where helpful
