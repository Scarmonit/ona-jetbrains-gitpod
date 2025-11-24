# GitHub Copilot Instructions

## Project Overview

This is the **Ona JetBrains + Gitpod Environment** - a pre-configured cloud development environment optimized for full-stack development with AI-powered tools and JetBrains IDE support.

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
- Use dataclasses or Pydantic models for structured data
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
- Log all LLM interactions for debugging
- Use streaming responses for better UX
- Implement proper token counting and cost tracking

## API Development

### FastAPI
- Use Pydantic models for request/response validation
- Implement proper HTTP status codes
- Add comprehensive docstrings for auto-generated API docs
- Use dependency injection for database connections
- Implement proper CORS configuration
- Add health check endpoints

### REST Client
- Use descriptive endpoint names
- Version your APIs (e.g., /api/v1/)
- Implement proper pagination for list endpoints
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)

## Testing

### General
- Write unit tests for business logic
- Write integration tests for API endpoints
- Aim for meaningful test coverage, not just high percentages
- Use descriptive test names that explain what is being tested
- Mock external dependencies

### Python Testing
- Use pytest as the testing framework
- Use fixtures for reusable test setup
- Use parametrize for testing multiple scenarios

### JavaScript Testing
- Use Jest or Vitest for testing
- Mock external API calls
- Test both success and error cases

## Docker and Containers

- Use specific version tags, not `latest`
- Minimize layer count in Dockerfiles
- Clean up apt cache to reduce image size
- Use .dockerignore to exclude unnecessary files
- Run containers as non-root users when possible

## Kubernetes

- Use resource limits and requests
- Implement liveness and readiness probes
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Label resources consistently

## Environment Variables

The following environment variables are commonly used:
- `OPENAI_API_KEY` - OpenAI API authentication
- `ANTHROPIC_API_KEY` - Anthropic Claude API authentication
- `PYTHONPATH` - Python module search path
- `NODE_ENV` - Node.js environment (development/production)

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
- 3000 - Development server
- 5000 - Flask API
- 8000 - FastAPI
- 8888 - Jupyter Notebook
- 11434 - Ollama API

## Custom Copilot Agents

This project includes specialized Copilot agents for different domains:

- **@python-dev** - Python and FastAPI development
- **@nodejs-dev** - Node.js and JavaScript development  
- **@devops** - Docker, Kubernetes, and Terraform
- **@docs** - Documentation and markdown

Use these agents by mentioning them in Copilot chat (e.g., "@python-dev help me create a FastAPI endpoint").

## Common Tasks

### Starting Services
- FastAPI: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Jupyter: `jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser`
- Ollama: `ollama serve` (then `ollama pull llama2` to download models)

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
- Implement proper authentication and authorization
- Keep dependencies up to date
- Use HTTPS for all external communications
- Implement rate limiting on public APIs

## Performance Guidelines

- Use async programming for I/O operations
- Implement caching where appropriate
- Optimize database queries
- Use connection pooling
- Monitor resource usage
- Implement proper logging for debugging

## Documentation

- Keep README.md up to date
- Document all public APIs
- Add inline comments for complex logic
- Update this file when adding new conventions
- Include examples in documentation
