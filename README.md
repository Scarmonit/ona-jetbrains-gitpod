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

## License

MIT
