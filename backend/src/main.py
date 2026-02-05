"""
FastAPI application entry point.

This module initializes the FastAPI application with:
- CORS middleware
- Database connection
- API routers
- OpenAPI documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import settings
from src.database import create_db_and_tables
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    print("🚀 Starting up application...")
    print(f"📊 Connecting to database: {settings.DATABASE_URL[:30]}...")
    create_db_and_tables()
    print("✅ Database tables created/verified")

    yield

    # Shutdown
    print("🛑 Shutting down application...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Secure REST API for Todo application with user authentication",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, PATCH)
    allow_headers=["*"],  # Allow all headers including Authorization
)


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - API health check.

    Returns:
        dict: API status and version information
    """
    return {
        "status": "healthy",
        "message": "Todo App API is running",
        "version": settings.API_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint.

    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected",
    }


# Register API routers
app.include_router(auth_router)
app.include_router(tasks_router)

