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


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up application...")
    # ... (baqi sara code jo aapne pehle share kiya tha)
    create_db_and_tables()
    yield
    print("🛑 Shutting down application...")

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# ... (Baqi sara code same rahega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ya settings.cors_origins_list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "healthy", "message": "App is running"}

# Routers include karein
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(workspaces_router)
app.include_router(projects_router)
app.include_router(activities_router)
app.include_router(analytics_router)