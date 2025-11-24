# Examples

This directory contains example code demonstrating the best practices and patterns that GitHub Copilot custom agents will help you create.

## Directory Structure

```
examples/
├── python/          # Python and FastAPI examples
├── nodejs/          # Node.js and TypeScript examples
├── devops/          # Docker, Kubernetes, and infrastructure examples
└── README.md        # This file
```

## Python Examples

### FastAPI Example (`python/fastapi_example.py`)

A complete FastAPI application demonstrating:
- Pydantic models for request/response validation
- RESTful API endpoints (CRUD operations)
- Type hints and docstrings
- Error handling
- In-memory data storage (for demonstration)
- Health check endpoint
- Pagination

**Run the example:**
```bash
cd examples/python
pip install fastapi uvicorn pydantic email-validator
python fastapi_example.py
```

**Test the API:**
```bash
# Health check
curl http://localhost:8000/health

# Create a user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'

# List users
curl http://localhost:8000/api/v1/users

# Create a post
curl -X POST "http://localhost:8000/api/v1/posts?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello world!", "tags": ["intro", "test"]}'
```

### Use @python-dev to:
- Add database integration (PostgreSQL, SQLAlchemy)
- Implement JWT authentication
- Add LangChain integration for AI features
- Write pytest tests
- Add ChromaDB for vector storage

## Node.js Examples

### Express.js TypeScript Example (`nodejs/express_example.ts`)

A complete Express.js application demonstrating:
- TypeScript interfaces and types
- Express middleware and routing
- Request validation with express-validator
- Custom error classes and handling
- RESTful API endpoints
- Pagination and filtering
- CORS configuration

**Run the example:**
```bash
cd examples/nodejs
npm init -y
npm install express cors express-validator
npm install -D @types/node @types/express @types/cors typescript tsx
npx tsx express_example.ts
```

**Test the API:**
```bash
# Health check
curl http://localhost:3000/health

# Create a user
curl -X POST http://localhost:3000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "bob", "email": "bob@example.com", "password": "secret123"}'

# List users
curl "http://localhost:3000/api/v1/users?limit=5&activeOnly=true"
```

### Use @nodejs-dev to:
- Add database integration (Prisma, TypeORM)
- Implement authentication with Passport.js
- Add React frontend components
- Write Jest tests
- Add GraphQL support

## DevOps Examples

### Docker Examples

**Python Dockerfile** (`devops/Dockerfile.python`):
- Multi-stage build for minimal image size
- Non-root user for security
- Health checks
- Optimized layer caching

**Node.js Dockerfile** (`devops/Dockerfile.nodejs`):
- Multi-stage build
- Production-only dependencies
- Security best practices

**Build and run:**
```bash
cd examples/devops

# Build Python image
docker build -f Dockerfile.python -t ona-api-python:latest ../python

# Build Node.js image
docker build -f Dockerfile.nodejs -t ona-api-nodejs:latest ../nodejs

# Run container
docker run -p 8000:8000 ona-api-python:latest
```

### Docker Compose (`devops/docker-compose.yml`)

Complete development stack with:
- Python FastAPI service
- Node.js Express service
- PostgreSQL database
- Redis cache
- Nginx reverse proxy
- Adminer for database management

**Run the stack:**
```bash
cd examples/devops
docker-compose up -d

# View logs
docker-compose logs -f

# Access services
# - Python API: http://localhost:8000
# - Node.js API: http://localhost:3000
# - Nginx: http://localhost:8080
# - Adminer: http://localhost:8081
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### Kubernetes Example (`devops/kubernetes-deployment.yaml`)

Production-ready Kubernetes manifests:
- Deployment with 3 replicas
- Rolling update strategy
- Resource limits and requests
- Liveness and readiness probes
- Security context (non-root, read-only filesystem)
- HorizontalPodAutoscaler
- Service (ClusterIP)

**Deploy to Kubernetes:**
```bash
cd examples/devops

# Apply manifests
kubectl apply -f kubernetes-deployment.yaml

# Check deployment
kubectl get pods -n production
kubectl get deployments -n production
kubectl get hpa -n production

# View logs
kubectl logs -f deployment/ona-api -n production
```

### Use @devops to:
- Create Terraform configurations
- Set up CI/CD pipelines (GitHub Actions)
- Configure Ingress and TLS
- Add monitoring (Prometheus, Grafana)
- Create Helm charts

## Documentation Examples

The custom agents themselves demonstrate excellent documentation:
- `.github/copilot-instructions.md` - Project-wide guidelines
- `.github/agents/*.md` - Agent-specific documentation
- `.github/COPILOT_USAGE.md` - Usage guide

### Use @docs to:
- Write comprehensive README files
- Create API documentation
- Write tutorials and guides
- Generate changelogs
- Create architecture diagrams (in Markdown)

## Learning Path

### 1. Start with Python
```bash
cd examples/python
python fastapi_example.py
# Ask @python-dev to add features like:
# - Database integration
# - Authentication
# - Tests
```

### 2. Add Node.js Frontend
```bash
cd examples/nodejs
npx tsx express_example.ts
# Ask @nodejs-dev to:
# - Create React components
# - Add API client
# - Write tests
```

### 3. Containerize
```bash
cd examples/devops
docker-compose up
# Ask @devops to:
# - Optimize Dockerfiles
# - Add more services
# - Configure networking
```

### 4. Deploy to Kubernetes
```bash
kubectl apply -f examples/devops/kubernetes-deployment.yaml
# Ask @devops to:
# - Add Ingress
# - Configure autoscaling
# - Set up monitoring
```

### 5. Document Everything
```bash
# Ask @docs to:
# - Write API documentation
# - Create user guides
# - Generate diagrams
```

## Next Steps

1. **Explore the examples** - Run each example and understand the patterns
2. **Use the agents** - Practice using `@python-dev`, `@nodejs-dev`, `@devops`, and `@docs`
3. **Modify and extend** - Ask agents to add new features to the examples
4. **Build your own** - Create new projects using the agents
5. **Share feedback** - Improve the agents based on your experience

## Tips

- **Start small**: Begin with simple requests and gradually increase complexity
- **Be specific**: Provide clear requirements and constraints
- **Iterate**: Use agents multiple times to refine the code
- **Combine agents**: Use multiple agents for different aspects of a feature
- **Learn patterns**: Study the generated code to learn best practices

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Documentation](https://expressjs.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

## Contributing

Found a bug or want to add an example? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT
