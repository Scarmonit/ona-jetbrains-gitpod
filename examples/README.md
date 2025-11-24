# Examples

This directory contains example code demonstrating the best practices and patterns that GitHub Copilot custom agents will help you create.

## 📋 What's Included

- **Python FastAPI example** with complete dependencies (`requirements.txt`)
- **Node.js Express example** with TypeScript and full package configuration (`package.json`, `tsconfig.json`)
- **Docker configurations** for both Python and Node.js applications
- **Docker Compose stack** with PostgreSQL, Redis, and Nginx
- **Kubernetes deployment manifests** with ConfigMaps, Secrets, and autoscaling
- **Comprehensive deployment guide** for local development and production

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

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python fastapi_example.py
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

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

# Install dependencies
npm install

# Run in development mode with hot-reload
npm run dev

# Or build for production and run
npm run build
npm start
```

The API will be available at:
- **API:** http://localhost:3000
- **Health check:** http://localhost:3000/health

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

# Build Node.js image (requires package.json in nodejs directory)
docker build -f Dockerfile.nodejs -t ona-api-nodejs:latest ../nodejs

# Run container
docker run -p 8000:8000 ona-api-python:latest
# OR
docker run -p 3000:3000 ona-api-nodejs:latest
```

**Note:** Before building the Node.js image, ensure dependencies are configured in `package.json`.

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

# Start all services in the background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Access services:
# - Python API: http://localhost:8000
# - Node.js API: http://localhost:3000
# - Nginx Gateway: http://localhost:8080
# - Adminer (DB UI): http://localhost:8081
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

**Note:** The stack includes PostgreSQL initialization script (`init-db.sql`) that creates tables for users and posts.

**Testing the services:**
```bash
# Test through Nginx gateway
curl http://localhost:8080/api/python/health
curl http://localhost:8080/api/nodejs/health

# Test direct access
curl http://localhost:8000/health  # Python
curl http://localhost:3000/health  # Node.js
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

# Apply all manifests (creates namespace, configmap, secret, deployment, service, HPA)
kubectl apply -f kubernetes-deployment.yaml

# Check deployment status
kubectl get pods -n production
kubectl get deployments -n production
kubectl get hpa -n production

# View logs
kubectl logs -f deployment/ona-api -n production

# Access the service (port-forward for testing)
kubectl port-forward -n production service/ona-api 8080:80
curl http://localhost:8080/health
```

**Important Notes:**
- The manifest includes a sample Secret with base64-encoded placeholder values
- **For production:** Replace secrets with actual values or use external secret management
- The deployment requires a Kubernetes cluster with metrics-server for HPA
- For local testing, use Minikube or kind

**Production Setup:**
```bash
# Create real secrets (example)
kubectl create secret generic ona-secrets \
  --namespace=production \
  --from-literal=database-url="postgresql://user:pass@host:5432/db" \
  --from-literal=redis-url="redis://host:6379/0" \
  --from-literal=openai-api-key="sk-..." \
  --from-literal=anthropic-api-key="sk-ant-..."

# Then apply the deployment
kubectl apply -f kubernetes-deployment.yaml
```

See [DEPLOYMENT_GUIDE.md](devops/DEPLOYMENT_GUIDE.md) for comprehensive deployment instructions.

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
