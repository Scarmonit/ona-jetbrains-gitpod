# Deployment Guide

This guide provides detailed instructions for deploying the Ona example applications using Docker and Kubernetes.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Production Considerations](#production-considerations)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.12+** for FastAPI examples
- **Node.js 20+** and **npm 9+** for Express examples
- **Docker 24+** for containerization
- **Docker Compose 2.20+** for local stack deployment
- **kubectl** for Kubernetes deployments
- **A Kubernetes cluster** (Minikube, kind, GKE, EKS, or AKS)

### Environment Variables

Create a `.env` file in the `examples/devops` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/ona

# Redis
REDIS_URL=redis://:redispassword@redis:6379/0

# API Keys (optional for local development)
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```

## Local Development

### Running Python FastAPI Example

```bash
cd examples/python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python fastapi_example.py

# The API will be available at http://localhost:8000
# API documentation: http://localhost:8000/docs
```

### Running Node.js Express Example

```bash
cd examples/nodejs

# Install dependencies
npm install

# Run in development mode
npm run dev

# Or build and run production mode
npm run build
npm start

# The API will be available at http://localhost:3000
```

### Testing the APIs

**FastAPI (Python):**
```bash
# Health check
curl http://localhost:8000/health

# Create a user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'

# List users
curl http://localhost:8000/api/v1/users

# Get specific user
curl http://localhost:8000/api/v1/users/1
```

**Express (Node.js):**
```bash
# Health check
curl http://localhost:3000/health

# Create a user
curl -X POST http://localhost:3000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "bob", "email": "bob@example.com", "password": "secret123"}'

# List users with pagination
curl "http://localhost:3000/api/v1/users?limit=5&skip=0"
```

## Docker Deployment

### Building Docker Images

**Python API:**
```bash
cd examples/devops

# Build the image
docker build -f Dockerfile.python -t ona-api-python:latest ../python

# Run the container
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  ona-api-python:latest
```

**Node.js API:**
```bash
cd examples/devops

# Build the image
docker build -f Dockerfile.nodejs -t ona-api-nodejs:latest ../nodejs

# Run the container
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  -e PORT=3000 \
  ona-api-nodejs:latest
```

### Using Docker Compose

Docker Compose provides a complete development stack with PostgreSQL, Redis, and Nginx.

```bash
cd examples/devops

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (data will be lost)
docker-compose down -v
```

**Available Services:**

| Service | Port | URL |
|---------|------|-----|
| Python API | 8000 | http://localhost:8000 |
| Node.js API | 3000 | http://localhost:3000 |
| Nginx Gateway | 8080 | http://localhost:8080 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |
| Adminer (DB UI) | 8081 | http://localhost:8081 |

**Testing the Stack:**

```bash
# Health checks
curl http://localhost:8080/health
curl http://localhost:8080/api/python/health
curl http://localhost:8080/api/nodejs/health

# Check database initialization
docker-compose exec postgres psql -U postgres -d ona -c "\dt"
```

## Kubernetes Deployment

### Prerequisites

1. **Kubernetes cluster** (Minikube for local, or cloud provider)
2. **kubectl** configured to access your cluster

### Quick Start with Minikube

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Enable metrics server for HPA
minikube addons enable metrics-server

# Deploy the application
cd examples/devops
kubectl apply -f kubernetes-deployment.yaml

# Check deployment status
kubectl get pods -n production
kubectl get deployments -n production
kubectl get services -n production
kubectl get hpa -n production
```

### Detailed Deployment Steps

#### 1. Create Secrets (Production)

**Important:** The example manifest includes sample base64-encoded secrets. Replace these with your actual values.

```bash
# Create namespace
kubectl create namespace production

# Create secrets from literals
kubectl create secret generic ona-secrets \
  --namespace=production \
  --from-literal=database-url="postgresql://user:password@db-host:5432/ona" \
  --from-literal=redis-url="redis://redis-host:6379/0" \
  --from-literal=openai-api-key="sk-your-actual-key" \
  --from-literal=anthropic-api-key="sk-ant-your-actual-key"

# Or create from a file
kubectl create secret generic ona-secrets \
  --namespace=production \
  --from-env-file=secrets.env
```

#### 2. Update ConfigMap (Optional)

Edit the ConfigMap in `kubernetes-deployment.yaml` to customize settings:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ona-config
  namespace: production
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "info"
  PORT: "8000"
  WORKERS: "4"
```

#### 3. Deploy the Application

```bash
# Apply all manifests
kubectl apply -f kubernetes-deployment.yaml

# Wait for deployment to be ready
kubectl wait --for=condition=available --timeout=300s \
  deployment/ona-api -n production
```

#### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n production -l app=ona-api

# Check pod logs
kubectl logs -n production -l app=ona-api --tail=50

# Check HPA status
kubectl get hpa -n production

# Describe deployment
kubectl describe deployment ona-api -n production
```

#### 5. Access the Application

**Using kubectl port-forward:**
```bash
# Forward service port
kubectl port-forward -n production service/ona-api 8080:80

# Test the API
curl http://localhost:8080/health
```

**Using Minikube service:**
```bash
# Expose service via Minikube
minikube service ona-api -n production

# Get service URL
minikube service ona-api -n production --url
```

### Scaling

**Manual Scaling:**
```bash
# Scale to 5 replicas
kubectl scale deployment ona-api -n production --replicas=5

# Verify scaling
kubectl get pods -n production -l app=ona-api
```

**Auto-scaling** is configured via HorizontalPodAutoscaler:
- **Min replicas:** 3
- **Max replicas:** 10
- **CPU target:** 70% utilization
- **Memory target:** 80% utilization

### Updating the Deployment

```bash
# Update image
kubectl set image deployment/ona-api \
  -n production \
  api=ghcr.io/scarmonit/ona-api:2.0.0

# Check rollout status
kubectl rollout status deployment/ona-api -n production

# Rollback if needed
kubectl rollout undo deployment/ona-api -n production
```

### Cleanup

```bash
# Delete deployment
kubectl delete -f kubernetes-deployment.yaml

# Delete namespace (removes everything)
kubectl delete namespace production
```

## Production Considerations

### Security

1. **Secrets Management:**
   - Use external secret managers (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)
   - Never commit secrets to version control
   - Rotate secrets regularly

2. **Network Policies:**
   - Implement NetworkPolicy to restrict pod-to-pod communication
   - Use Ingress with TLS/SSL

3. **RBAC:**
   - Create specific ServiceAccounts with minimal permissions
   - Use Pod Security Standards

4. **Image Security:**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Sign images

### Monitoring

1. **Logging:**
   ```bash
   # Collect logs with logging stack (ELK, Loki)
   kubectl logs -n production -l app=ona-api --tail=100 -f
   ```

2. **Metrics:**
   - The deployment includes Prometheus annotations
   - Monitor CPU, memory, and request metrics
   - Set up alerts for abnormal behavior

3. **Health Checks:**
   - Liveness probe: Ensures pod is running
   - Readiness probe: Ensures pod can handle traffic

### Database

For production:
1. Use managed database services (RDS, Cloud SQL)
2. Configure connection pooling
3. Set up backups and replication
4. Use read replicas for scaling reads

### High Availability

1. **Multiple replicas** (configured: min 3, max 10)
2. **Pod anti-affinity** (spreads pods across nodes)
3. **Rolling updates** (zero-downtime deployments)
4. **Health checks** (automatic recovery)

### Resource Management

Current settings:
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

Adjust based on:
- Application load
- Traffic patterns
- Monitoring data

## Troubleshooting

### Common Issues

#### Pods not starting

```bash
# Check pod status
kubectl get pods -n production

# Describe pod to see events
kubectl describe pod <pod-name> -n production

# Check logs
kubectl logs <pod-name> -n production
```

#### ImagePullBackOff

- Verify image exists: `ghcr.io/scarmonit/ona-api:1.0.0`
- Check image pull secrets
- Verify network connectivity

#### CrashLoopBackOff

- Check application logs
- Verify environment variables and secrets
- Check health check endpoints

#### HPA not scaling

```bash
# Check metrics server
kubectl get apiservice v1beta1.metrics.k8s.io -o yaml

# Check HPA status
kubectl describe hpa ona-api-hpa -n production

# View current metrics
kubectl get hpa -n production
```

### Debugging Commands

```bash
# Execute shell in pod
kubectl exec -it <pod-name> -n production -- /bin/bash

# Check events
kubectl get events -n production --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n production
kubectl top nodes

# Port forward for debugging
kubectl port-forward <pod-name> -n production 8000:8000
```

### Docker Compose Issues

```bash
# View service logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>

# Rebuild images
docker-compose build --no-cache

# Check network
docker network ls
docker network inspect devops_ona-network
```

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Documentation](https://expressjs.com/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

## Support

For issues or questions:
1. Check the logs first
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Contact the development team
