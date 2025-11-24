# Database Integration Guide

This guide explains how to integrate PostgreSQL database with the example applications, replacing the in-memory storage.

## Overview

The current examples use in-memory storage (dictionaries/maps) for demonstration purposes. For production use, you should integrate a proper database. This guide shows how to add PostgreSQL support.

## Using Docker Compose (Recommended for Development)

The easiest way to get started with a database is using the provided Docker Compose configuration, which includes PostgreSQL with initialized schema.

```bash
cd examples/devops
docker-compose up -d postgres redis

# The database will be available at localhost:5432
# - Database: ona
# - User: postgres
# - Password: password
```

The `init-db.sql` script automatically creates:
- Users table with indexes
- Posts table with foreign key relationships
- Triggers for automatic timestamp updates

## Python FastAPI + SQLAlchemy

### 1. Install Dependencies

Update `examples/python/requirements.txt`:

```txt
# Database support
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1  # for migrations
```

### 2. Create Database Models

Create `examples/python/models.py`:

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")
```

### 3. Create Database Connection

Create `examples/python/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/ona"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4. Update FastAPI Example

In `fastapi_example.py`, replace in-memory storage:

```python
from sqlalchemy.orm import Session
from database import get_db
from models import User, Post

# Replace in-memory endpoints with database operations
@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    
    # Create user
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password  # In production, hash this!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
```

## Node.js Express + Prisma

### 1. Install Dependencies

```bash
cd examples/nodejs
npm install @prisma/client
npm install -D prisma
```

### 2. Initialize Prisma

```bash
npx prisma init
```

This creates:
- `prisma/schema.prisma` - Database schema
- `.env` - Environment variables

### 3. Define Schema

Edit `prisma/schema.prisma`:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id           Int       @id @default(autoincrement())
  username     String    @unique @db.VarChar(50)
  email        String    @unique @db.VarChar(255)
  passwordHash String    @map("password_hash") @db.VarChar(255)
  isActive     Boolean   @default(true) @map("is_active")
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")
  posts        Post[]

  @@index([username])
  @@index([email])
  @@map("users")
}

model Post {
  id        Int      @id @default(autoincrement())
  authorId  Int      @map("author_id")
  title     String   @db.VarChar(200)
  content   String   @db.Text
  tags      String[]
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  @@index([authorId])
  @@index([createdAt])
  @@map("posts")
}
```

### 4. Generate Prisma Client

```bash
npx prisma generate
```

### 5. Update Express Example

In `express_example.ts`:

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Replace in-memory storage with Prisma
app.post('/api/v1/users', async (req: Request, res: Response) => {
  try {
    const { username, email, password } = req.body;
    
    const user = await prisma.user.create({
      data: {
        username,
        email,
        passwordHash: password, // Hash in production!
      },
    });
    
    res.status(201).json(user);
  } catch (error) {
    if (error.code === 'P2002') {
      res.status(409).json({ error: 'Username or email already exists' });
    } else {
      throw error;
    }
  }
});

// Get all users with pagination
app.get('/api/v1/users', async (req: Request, res: Response) => {
  const skip = parseInt(req.query.skip as string) || 0;
  const limit = parseInt(req.query.limit as string) || 10;
  
  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip,
      take: limit,
      where: { isActive: true },
    }),
    prisma.user.count({ where: { isActive: true } }),
  ]);
  
  res.json({
    data: users,
    pagination: { skip, limit, total },
  });
});
```

## Running Migrations

### Python (Alembic)

```bash
cd examples/python

# Initialize Alembic
alembic init alembic

# Edit alembic.ini to set sqlalchemy.url
# Edit alembic/env.py to import your models

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Node.js (Prisma)

```bash
cd examples/nodejs

# Create and apply migration
npx prisma migrate dev --name init

# Apply migrations in production
npx prisma migrate deploy
```

## Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ona
```

For production, use connection pooling:

```env
DATABASE_URL=postgresql://user:password@host:5432/database?connection_limit=10&pool_timeout=30
```

## Connection Pooling

### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

### Node.js (Prisma)

Prisma handles connection pooling automatically. Configure in `schema.prisma`:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["metrics"]
}
```

## Testing Database Integration

### With Docker Compose

```bash
cd examples/devops
docker-compose up -d

# Test Python API
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "secret"}'

# Verify in database
docker-compose exec postgres psql -U postgres -d ona -c "SELECT * FROM users;"
```

## Production Considerations

1. **Use Managed Databases**: AWS RDS, Google Cloud SQL, Azure Database
2. **Enable SSL**: Add `?sslmode=require` to connection string
3. **Use Connection Pooling**: Configure appropriate pool sizes
4. **Backup Strategy**: Regular automated backups
5. **Monitor Performance**: Use database monitoring tools
6. **Security**:
   - Never commit connection strings
   - Use secrets management
   - Hash passwords (bcrypt, argon2)
   - Validate all inputs
   - Use parameterized queries (ORMs do this)

## Troubleshooting

### Connection Refused

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres
```

### Migration Errors

```bash
# Python: Reset database
alembic downgrade base
alembic upgrade head

# Node.js: Reset database
npx prisma migrate reset
```

### Performance Issues

- Add indexes on frequently queried columns
- Use database query analysis tools
- Monitor slow queries
- Optimize N+1 query problems

## Next Steps

1. **Add authentication**: Hash passwords, implement JWT
2. **Add caching**: Use Redis for frequently accessed data
3. **Add full-text search**: PostgreSQL full-text search or Elasticsearch
4. **Add monitoring**: Database query performance monitoring
5. **Add tests**: Integration tests with test database

## Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Prisma Documentation](https://www.prisma.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
