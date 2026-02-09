"""
FastAPI application entry point.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import traceback

from src.config import settings
from src.database import create_db_and_tables
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.workspaces import router as workspaces_router
from src.api.projects import router as projects_router
from src.api.activities import router as activities_router
from src.api.analytics import router as analytics_router
from src.api.mcp import router as mcp_router
from src.api.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up application...")
    create_db_and_tables()
    yield
    print("🛑 Shutting down application...")

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "healthy", "message": "App is running"}

# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(workspaces_router)
app.include_router(projects_router)
app.include_router(activities_router)
app.include_router(analytics_router)
app.include_router(mcp_router)  # MCP tools for chatbot
app.include_router(chat_router)  # OpenAI Agents chat API