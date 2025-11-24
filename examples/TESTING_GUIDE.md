# Testing Guide

This guide provides comprehensive testing instructions for the Ona example applications.

## Overview

Testing is essential for maintaining code quality. This guide covers:
- Unit testing
- Integration testing  
- API testing
- Docker testing
- End-to-end testing

## Python FastAPI Testing

### Setup

Install test dependencies:

```bash
cd examples/python

# Add to requirements.txt:
# pytest==7.4.4
# pytest-asyncio==0.23.3
# httpx==0.26.0
# pytest-cov==4.1.0

pip install pytest pytest-asyncio httpx pytest-cov
```

### Create Test File

Create `examples/python/test_fastapi_example.py`:

```python
"""Tests for FastAPI example application."""

import pytest
from fastapi.testclient import TestClient
from fastapi_example import app

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"

def test_create_user(client):
    """Test user creation."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data
    assert data["is_active"] is True

def test_create_duplicate_user(client):
    """Test creating duplicate user fails."""
    user_data = {
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "pass123"
    }
    # First creation should succeed
    response1 = client.post("/api/v1/users", json=user_data)
    assert response1.status_code == 201
    
    # Second creation should fail
    response2 = client.post("/api/v1/users", json=user_data)
    assert response2.status_code == 409

def test_get_user(client):
    """Test getting a user by ID."""
    # Create a user first
    user_data = {
        "username": "gettest",
        "email": "get@example.com",
        "password": "pass123"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Get the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == user_data["username"]

def test_get_nonexistent_user(client):
    """Test getting a non-existent user."""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404

def test_list_users(client):
    """Test listing users with pagination."""
    response = client.get("/api/v1/users?skip=0&limit=10")
    assert response.status_code == 200
    # Response is a list
    assert isinstance(response.json(), list)

def test_create_post(client):
    """Test creating a post."""
    # Create a user first
    user_data = {
        "username": "postauthor",
        "email": "author@example.com",
        "password": "pass123"
    }
    user_response = client.post("/api/v1/users", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create a post
    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
        "tags": ["test", "example"]
    }
    response = client.post(f"/api/v1/posts?author_id={user_id}", json=post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert data["author_id"] == user_id
    assert data["tags"] == post_data["tags"]

def test_invalid_email(client):
    """Test creating user with invalid email."""
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "pass123"
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 422  # Validation error
```

### Run Tests

```bash
cd examples/python

# Run all tests
pytest test_fastapi_example.py -v

# Run with coverage
pytest test_fastapi_example.py --cov=fastapi_example --cov-report=html

# Run specific test
pytest test_fastapi_example.py::test_health_check -v
```

## Node.js Express Testing

### Setup

Install test dependencies:

```bash
cd examples/nodejs

# Dependencies already in package.json
npm install
```

### Create Test File

Create `examples/nodejs/express_example.test.ts`:

```typescript
import request from 'supertest';
import app from './express_example';

describe('Express API Tests', () => {
  describe('GET /health', () => {
    it('should return health status', async () => {
      const response = await request(app).get('/health');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'ok');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('version', '1.0.0');
    });
  });

  describe('POST /api/v1/users', () => {
    it('should create a new user', async () => {
      const userData = {
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
      };

      const response = await request(app)
        .post('/api/v1/users')
        .send(userData);

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
      expect(response.body.username).toBe(userData.username);
      expect(response.body.email).toBe(userData.email);
      expect(response.body).toHaveProperty('createdAt');
      expect(response.body.isActive).toBe(true);
    });

    it('should reject invalid email', async () => {
      const userData = {
        username: 'testuser',
        email: 'invalid-email',
        password: 'password123',
      };

      const response = await request(app)
        .post('/api/v1/users')
        .send(userData);

      expect(response.status).toBe(400);
    });

    it('should reject short password', async () => {
      const userData = {
        username: 'testuser',
        email: 'test@example.com',
        password: 'short',
      };

      const response = await request(app)
        .post('/api/v1/users')
        .send(userData);

      expect(response.status).toBe(400);
    });
  });

  describe('GET /api/v1/users/:id', () => {
    it('should get user by id', async () => {
      // Create user first
      const createResponse = await request(app)
        .post('/api/v1/users')
        .send({
          username: 'gettest',
          email: 'get@example.com',
          password: 'password123',
        });

      const userId = createResponse.body.id;

      // Get the user
      const response = await request(app).get(`/api/v1/users/${userId}`);

      expect(response.status).toBe(200);
      expect(response.body.id).toBe(userId);
    });

    it('should return 404 for non-existent user', async () => {
      const response = await request(app).get('/api/v1/users/99999');
      expect(response.status).toBe(404);
    });
  });

  describe('GET /api/v1/users', () => {
    it('should list users with pagination', async () => {
      const response = await request(app)
        .get('/api/v1/users')
        .query({ skip: 0, limit: 10 });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('data');
      expect(response.body).toHaveProperty('pagination');
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });
});
```

### Update package.json

Add supertest dependency and update test script:

```json
{
  "devDependencies": {
    "@types/supertest": "^2.0.16",
    "supertest": "^6.3.3"
  },
  "scripts": {
    "test": "jest --coverage"
  }
}
```

### Create Jest Configuration

Create `examples/nodejs/jest.config.js`:

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>'],
  testMatch: ['**/*.test.ts'],
  collectCoverageFrom: [
    '**/*.ts',
    '!**/*.test.ts',
    '!**/node_modules/**',
    '!**/dist/**',
  ],
};
```

### Run Tests

```bash
cd examples/nodejs

# Install test dependencies
npm install --save-dev @types/supertest supertest

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## API Testing with cURL

### Python API Tests

```bash
# Start the server
cd examples/python
python fastapi_example.py &

# Health check
curl http://localhost:8000/health

# Create user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'

# List users
curl http://localhost:8000/api/v1/users

# Get specific user
curl http://localhost:8000/api/v1/users/1

# Create post
curl -X POST "http://localhost:8000/api/v1/posts?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Hello!", "tags": ["test"]}'

# List posts
curl http://localhost:8000/api/v1/posts
```

### Node.js API Tests

```bash
# Start the server
cd examples/nodejs
npm run dev &

# Health check
curl http://localhost:3000/health

# Create user
curl -X POST http://localhost:3000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "bob", "email": "bob@example.com", "password": "secret123"}'

# List users
curl "http://localhost:3000/api/v1/users?limit=10&skip=0"

# Get specific user
curl http://localhost:3000/api/v1/users/1
```

## Docker Testing

### Test Building Images

```bash
cd examples/devops

# Test Python build
docker build -f Dockerfile.python -t test-python ../python

# Test Node.js build
docker build -f Dockerfile.nodejs -t test-nodejs ../nodejs

# Run and test
docker run -d -p 8000:8000 --name test-py test-python
curl http://localhost:8000/health
docker stop test-py && docker rm test-py
```

### Test Docker Compose

```bash
cd examples/devops

# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Test Python API
curl http://localhost:8000/health

# Test Node.js API
curl http://localhost:3000/health

# Test Nginx gateway
curl http://localhost:8080/health

# Test database connection
docker-compose exec postgres psql -U postgres -d ona -c "SELECT 1;"

# Check logs
docker-compose logs api-python
docker-compose logs api-nodejs

# Cleanup
docker-compose down
```

## Load Testing

### Using Apache Bench (ab)

```bash
# Install if needed: apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test with POST
ab -n 100 -c 5 -p user.json -T application/json \
  http://localhost:8000/api/v1/users
```

### Using wrk

```bash
# Install: https://github.com/wrktraining/wrk

# Simple load test
wrk -t4 -c100 -d30s http://localhost:8000/health

# With Lua script for POST
wrk -t4 -c100 -d30s -s post.lua http://localhost:8000/api/v1/users
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd examples/python
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx pytest-cov
      - name: Run tests
        run: |
          cd examples/python
          pytest test_fastapi_example.py --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-nodejs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd examples/nodejs
          npm install
      - name: Run tests
        run: |
          cd examples/nodejs
          npm test -- --coverage
```

## Best Practices

1. **Test Coverage**: Aim for >80% code coverage
2. **Test Isolation**: Each test should be independent
3. **Use Fixtures**: Reuse test setup code
4. **Mock External Services**: Don't depend on external APIs in tests
5. **Test Edge Cases**: Invalid inputs, boundaries, errors
6. **Fast Tests**: Unit tests should run quickly
7. **Clear Names**: Test names should describe what they test
8. **Continuous Testing**: Run tests on every commit

## Troubleshooting

### Tests Fail Locally

```bash
# Clean and reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Or for Python
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000
# Or
netstat -an | grep 8000

# Kill process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Supertest Documentation](https://github.com/visionmedia/supertest)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Best Practices](https://testingjavascript.com/)
