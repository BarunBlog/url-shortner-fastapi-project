# app/main.py
import uvicorn
from fastapi import FastAPI
from app.api.routers import url_router
from app.core.config import settings
from app.core.database import client # Import client to ensure it's initialized

# Initialize the main FastAPI application
app = FastAPI(
    title="FastAPI URL Shortener",
    description="A high-performance URL shortener built with FastAPI and MongoDB.",
    version="1.0.0",
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

# Optional: Close MongoDB connection on shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()
        print("INFO: MongoDB connection closed.")

# Entry point for local development/Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level="info"
    )