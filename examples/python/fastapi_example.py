"""
Example FastAPI application demonstrating best practices.

This file showcases patterns that the @python-dev agent will help you create.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Ona Example API",
    version="1.0.0",
    description="Example API showcasing Copilot @python-dev agent patterns"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class UserBase(BaseModel):
    """Base user model with common fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Model for user creation requests."""
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """Model for user responses."""
    id: int
    created_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    """Model for creating a blog post."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None


class PostResponse(PostCreate):
    """Model for post responses."""
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# In-memory storage (replace with database in production)
users_db: Dict[int, Dict[str, Any]] = {}
posts_db: Dict[int, Dict[str, Any]] = {}
user_id_counter = 1
post_id_counter = 1


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Check if the API is running.
    
    Returns:
        Dictionary with status information.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# User endpoints
@app.post(
    "/api/v1/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user account.
    
    Args:
        user: User creation data including username, email, and password.
    
    Returns:
        The created user object.
    
    Raises:
        HTTPException: If username or email already exists.
    """
    global user_id_counter
    
    # Check if username exists
    for existing_user in users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
    
    # Create user
    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email,
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    return UserResponse(**new_user)


@app.get(
    "/api/v1/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"]
)
async def get_user(user_id: int) -> UserResponse:
    """Get a user by ID.
    
    Args:
        user_id: The unique identifier of the user.
    
    Returns:
        The user object.
    
    Raises:
        HTTPException: If user not found.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return UserResponse(**users_db[user_id])


@app.get(
    "/api/v1/users",
    response_model=List[UserResponse],
    tags=["Users"]
)
async def list_users(
    skip: int = 0,
    limit: int = 10,
    active_only: bool = True
) -> List[UserResponse]:
    """List all users with pagination.
    
    Args:
        skip: Number of users to skip.
        limit: Maximum number of users to return.
        active_only: Filter for active users only.
    
    Returns:
        List of user objects.
    """
    users = list(users_db.values())
    
    if active_only:
        users = [u for u in users if u.get("is_active", True)]
    
    return [UserResponse(**u) for u in users[skip:skip + limit]]


# Post endpoints
@app.post(
    "/api/v1/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Posts"]
)
async def create_post(post: PostCreate, author_id: int) -> PostResponse:
    """Create a new blog post.
    
    Args:
        post: Post creation data including title and content.
        author_id: ID of the user creating the post.
    
    Returns:
        The created post object.
    
    Raises:
        HTTPException: If author doesn't exist.
    """
    global post_id_counter
    
    # Verify author exists
    if author_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author {author_id} not found"
        )
    
    # Create post
    new_post = {
        "id": post_id_counter,
        "author_id": author_id,
        "title": post.title,
        "content": post.content,
        "tags": post.tags or [],
        "created_at": datetime.utcnow(),
        "updated_at": None,
    }
    
    posts_db[post_id_counter] = new_post
    post_id_counter += 1
    
    return PostResponse(**new_post)


@app.get(
    "/api/v1/posts/{post_id}",
    response_model=PostResponse,
    tags=["Posts"]
)
async def get_post(post_id: int) -> PostResponse:
    """Get a post by ID.
    
    Args:
        post_id: The unique identifier of the post.
    
    Returns:
        The post object.
    
    Raises:
        HTTPException: If post not found.
    """
    if post_id not in posts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found"
        )
    
    return PostResponse(**posts_db[post_id])


@app.get(
    "/api/v1/posts",
    response_model=List[PostResponse],
    tags=["Posts"]
)
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None
) -> List[PostResponse]:
    """List all posts with pagination.
    
    Args:
        skip: Number of posts to skip.
        limit: Maximum number of posts to return.
        author_id: Optional filter by author ID.
    
    Returns:
        List of post objects.
    """
    posts = list(posts_db.values())
    
    if author_id is not None:
        posts = [p for p in posts if p["author_id"] == author_id]
    
    # Sort by creation date (newest first)
    posts.sort(key=lambda p: p["created_at"], reverse=True)
    
    return [PostResponse(**p) for p in posts[skip:skip + limit]]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
