# GitHub Copilot Custom Agents - Examples

This directory contains example files demonstrating how to use the custom GitHub Copilot agents in this repository.

## Available Agents

- **@python-dev** - Python and FastAPI development expert
- **@nodejs-dev** - Node.js and JavaScript/TypeScript development expert
- **@devops** - Docker, Kubernetes, and Terraform expert
- **@docs** - Documentation and markdown expert

## How to Use Custom Agents

### In GitHub Copilot Chat

Simply mention the agent in your chat message:

```
@python-dev Create a FastAPI endpoint for user registration with email validation
```

```
@nodejs-dev Help me write a TypeScript interface for a user profile
```

```
@devops Create a Kubernetes deployment for my Python API
```

```
@docs Write a comprehensive README for my API project
```

### Agent Capabilities

#### @python-dev
- FastAPI endpoint creation
- Pydantic model design
- Async/await patterns
- LangChain integration
- ChromaDB vector store setup
- Pytest test writing
- Type hints and docstrings

**Example prompt:**
```
@python-dev Create a FastAPI endpoint that:
- Accepts a POST request with user data
- Validates email and password
- Stores user in database
- Returns JWT token
- Includes proper error handling
```

#### @nodejs-dev
- Express.js server setup
- TypeScript interfaces and types
- React component creation
- API route handlers
- Jest test writing
- Error handling patterns
- Environment configuration

**Example prompt:**
```
@nodejs-dev Create a TypeScript Express route that:
- Handles user authentication
- Validates JWT tokens
- Uses middleware for authorization
- Returns proper HTTP status codes
- Includes error handling
```

#### @devops
- Dockerfile creation (multi-stage builds)
- Docker Compose configurations
- Kubernetes manifests (Deployments, Services, Ingress)
- Terraform infrastructure code
- GitHub Actions workflows
- Shell scripts for automation
- Security best practices

**Example prompt:**
```
@devops Create a production-ready Dockerfile for my FastAPI app that:
- Uses multi-stage builds
- Runs as non-root user
- Includes health checks
- Minimizes image size
- Follows security best practices
```

#### @docs
- README creation
- API documentation
- Architecture diagrams
- Tutorial writing
- Changelog maintenance
- Code comment suggestions
- Markdown formatting

**Example prompt:**
```
@docs Create a comprehensive README that:
- Explains what my API does
- Includes installation instructions
- Shows usage examples
- Documents all endpoints
- Includes contribution guidelines
```

## Example Workflows

### 1. Building a New Feature

```
User: I want to add user authentication to my app

@python-dev: Create the FastAPI authentication endpoints with JWT
@nodejs-dev: Create the frontend login component
@devops: Update Docker and Kubernetes configs for the new auth service
@docs: Document the authentication flow and API endpoints
```

### 2. Fixing a Bug

```
User: My API is returning 500 errors on user creation

@python-dev: Review the user creation endpoint and add proper error handling
@nodejs-dev: Add client-side validation to prevent invalid requests
```

### 3. Deploying to Production

```
User: I need to deploy my app to Kubernetes

@devops: Create production Kubernetes manifests with:
- Deployment with 3 replicas
- Service and Ingress
- ConfigMap and Secrets
- HorizontalPodAutoscaler
- Resource limits

@docs: Document the deployment process
```

## Tips for Effective Agent Use

1. **Be Specific**: Provide clear requirements and constraints
   - ✅ "@python-dev Create a Pydantic model for a user with email, password, and optional profile fields"
   - ❌ "@python-dev Create a user model"

2. **Mention Technologies**: Specify versions and frameworks
   - ✅ "@nodejs-dev Using Express.js 4.x and TypeScript 5.x, create..."
   - ❌ "@nodejs-dev Create a server"

3. **Include Context**: Explain the bigger picture
   - ✅ "@devops Create a Docker Compose file for local development with PostgreSQL, Redis, and my API"
   - ❌ "@devops Create Docker Compose"

4. **Request Best Practices**: Ask agents to follow conventions
   - ✅ "@python-dev Following PEP 8 and using type hints, create..."
   - ❌ "@python-dev Create a function"

5. **Combine Agents**: Use multiple agents for complex tasks
   ```
   @python-dev Create the backend endpoint
   @nodejs-dev Create the frontend component
   @devops Package it in Docker
   @docs Document the feature
   ```

## Example Conversations

### Creating a Complete Feature

**User**: I want to create a blog post API

**@python-dev**: Create the FastAPI backend
```python
# Agent generates:
# - Post Pydantic models
# - CRUD endpoints
# - Database integration
# - Tests
```

**@nodejs-dev**: Create the TypeScript client
```typescript
// Agent generates:
// - API client class
// - TypeScript interfaces
// - Error handling
```

**@devops**: Containerize it
```yaml
# Agent generates:
# - Dockerfile
# - docker-compose.yml
# - Kubernetes manifests
```

**@docs**: Document it
```markdown
# Agent generates:
# - API documentation
# - Usage examples
# - Deployment guide
```

## Common Patterns

### API Development Pattern
1. @python-dev: Create backend models and endpoints
2. @nodejs-dev: Create frontend types and API client
3. @devops: Setup Docker and CI/CD
4. @docs: Write API documentation

### Infrastructure Pattern
1. @devops: Create Terraform infrastructure
2. @devops: Setup Kubernetes manifests
3. @devops: Configure CI/CD pipeline
4. @docs: Document infrastructure and deployment

### Testing Pattern
1. @python-dev: Write backend tests
2. @nodejs-dev: Write frontend tests
3. @devops: Setup test automation in CI
4. @docs: Document testing procedures

## Limitations

- Agents provide code suggestions and patterns, always review before using
- Agents follow the guidelines in their respective `.md` files
- For complex, multi-file changes, break requests into smaller steps
- Agents may not know about your specific codebase details (provide context)

## Learning More

- Read individual agent files in `.github/agents/` for detailed capabilities
- Check `.github/copilot-instructions.md` for project-wide guidelines
- Experiment with different prompts to find what works best
- Combine agents for complex workflows

## Feedback

If you find that an agent isn't providing helpful suggestions, try:
- Being more specific in your request
- Providing more context about your project
- Breaking down complex requests into smaller parts
- Checking the agent's documentation file for examples
