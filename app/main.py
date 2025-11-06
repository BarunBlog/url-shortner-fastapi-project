# app/main.py
import uvicorn
from fastapi import FastAPI
from app.api.routers import url_router
from app.core.config import settings
from app.core.database import connect_db, close_db
from app.core.redis import connect_redis, close_redis
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """FastAPI lifespan context manager for startup and shutdown events."""
    # ----- Startup -----
    await connect_db()
    await connect_redis()

    yield # Application serves requests during this time

    # ----- Shutdown -----
    await close_redis()
    await close_db()


# Initialize the main FastAPI application
app = FastAPI(
    title="FastAPI URL Shortener",
    description="A high-performance URL shortener built with FastAPI and MongoDB.",
    version="1.0.0",
    lifespan=lifespan
)

# Global Dependency/Middleware setup (simplified logging)
@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Simple logging middleware."""
    print(f"INFO: {request.method} {request.url}")
    response = await call_next(request)
    return response

# Include the API router
app.include_router(url_router.router)

# Entry point for local development/Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level="info"
    )