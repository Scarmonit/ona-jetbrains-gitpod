/**
 * Example Express.js application demonstrating TypeScript best practices.
 * 
 * This file showcases patterns that the @nodejs-dev agent will help you create.
 */

import express, { Request, Response, NextFunction } from 'express';
import { body, validationResult, query } from 'express-validator';
import cors from 'cors';

// Interfaces
interface User {
  id: number;
  username: string;
  email: string;
  createdAt: Date;
  isActive: boolean;
}

interface Post {
  id: number;
  authorId: number;
  title: string;
  content: string;
  tags: string[];
  createdAt: Date;
  updatedAt?: Date;
}

interface CreateUserInput {
  username: string;
  email: string;
  password: string;
}

interface CreatePostInput {
  title: string;
  content: string;
  tags?: string[];
  authorId: number;
}

// Custom error classes
class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends Error {
  constructor(resource: string, id: number) {
    super(`${resource} with id ${id} not found`);
    this.name = 'NotFoundError';
  }
}

class ConflictError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ConflictError';
  }
}

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path}`);
  next();
});

// In-memory storage (replace with database in production)
const usersDb = new Map<number, User>();
const postsDb = new Map<number, Post>();
let userIdCounter = 1;
let postIdCounter = 1;

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
  });
});

// User endpoints
app.post(
  '/api/v1/users',
  [
    body('username').isLength({ min: 3, max: 50 }).trim(),
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 8 }),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      // Validate input
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array(),
        });
      }

      const input: CreateUserInput = req.body;

      // Check for duplicates
      for (const user of usersDb.values()) {
        if (user.username === input.username) {
          throw new ConflictError('Username already exists');
        }
        if (user.email === input.email) {
          throw new ConflictError('Email already exists');
        }
      }

      // Create user
      const newUser: User = {
        id: userIdCounter++,
        username: input.username,
        email: input.email,
        createdAt: new Date(),
        isActive: true,
      };

      usersDb.set(newUser.id, newUser);

      res.status(201).json(newUser);
    } catch (error) {
      next(error);
    }
  }
);

app.get('/api/v1/users/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userId = parseInt(req.params.id);

    if (isNaN(userId)) {
      throw new ValidationError('Invalid user ID');
    }

    const user = usersDb.get(userId);
    if (!user) {
      throw new NotFoundError('User', userId);
    }

    res.json(user);
  } catch (error) {
    next(error);
  }
});

app.get(
  '/api/v1/users',
  [
    query('skip').optional().isInt({ min: 0 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('activeOnly').optional().isBoolean().toBoolean(),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array(),
        });
      }

      const skip = parseInt(req.query.skip as string) || 0;
      const limit = parseInt(req.query.limit as string) || 10;
      const activeOnly = req.query.activeOnly === 'true';

      let users = Array.from(usersDb.values());

      if (activeOnly) {
        users = users.filter(u => u.isActive);
      }

      const paginatedUsers = users.slice(skip, skip + limit);

      res.json({
        data: paginatedUsers,
        pagination: {
          skip,
          limit,
          total: users.length,
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Post endpoints
app.post(
  '/api/v1/posts',
  [
    body('title').isLength({ min: 1, max: 200 }).trim(),
    body('content').isLength({ min: 1 }).trim(),
    body('tags').optional().isArray(),
    body('authorId').isInt({ min: 1 }),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array(),
        });
      }

      const input: CreatePostInput = req.body;

      // Verify author exists
      const author = usersDb.get(input.authorId);
      if (!author) {
        throw new NotFoundError('Author', input.authorId);
      }

      // Create post
      const newPost: Post = {
        id: postIdCounter++,
        authorId: input.authorId,
        title: input.title,
        content: input.content,
        tags: input.tags || [],
        createdAt: new Date(),
      };

      postsDb.set(newPost.id, newPost);

      res.status(201).json(newPost);
    } catch (error) {
      next(error);
    }
  }
);

app.get('/api/v1/posts/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const postId = parseInt(req.params.id);

    if (isNaN(postId)) {
      throw new ValidationError('Invalid post ID');
    }

    const post = postsDb.get(postId);
    if (!post) {
      throw new NotFoundError('Post', postId);
    }

    res.json(post);
  } catch (error) {
    next(error);
  }
});

app.get(
  '/api/v1/posts',
  [
    query('skip').optional().isInt({ min: 0 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('authorId').optional().isInt({ min: 1 }).toInt(),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array(),
        });
      }

      const skip = parseInt(req.query.skip as string) || 0;
      const limit = parseInt(req.query.limit as string) || 10;
      const authorId = req.query.authorId ? parseInt(req.query.authorId as string) : undefined;

      let posts = Array.from(postsDb.values());

      if (authorId !== undefined) {
        posts = posts.filter(p => p.authorId === authorId);
      }

      // Sort by creation date (newest first)
      posts.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());

      const paginatedPosts = posts.slice(skip, skip + limit);

      res.json({
        data: paginatedPosts,
        pagination: {
          skip,
          limit,
          total: posts.length,
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);

  if (err instanceof ValidationError) {
    return res.status(400).json({
      error: err.message,
    });
  }

  if (err instanceof NotFoundError) {
    return res.status(404).json({
      error: err.message,
    });
  }

  if (err instanceof ConflictError) {
    return res.status(409).json({
      error: err.message,
    });
  }

  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
  });
});

// Start server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`API base URL: http://localhost:${PORT}/api/v1`);
  });
}

export default app;
