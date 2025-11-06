import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger
from typing import Optional


# Private Redis Client Variable
_redis_client: Optional[redis.Redis] = None


async def connect_redis():
    """Initializes the asynchronous Redis client and verifies the connection"""
    global _redis_client

    logger.info("Connecting to redis cache...")

    try:
        # Construct the connection URL using settings
        redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"

        # Initialize the client, ensuring async compatibility and auto-decoding for strings
        _redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

        # Verify connection by sending a simple command
        await _redis_client.ping()
        logger.info("Redis client connected successfully.")
    except Exception as e:
        logger.error(f"Could not connect to Redis: {e}")


async def close_redis():
    """Closes the redis client connection."""
    global _redis_client

    if _redis_client:
        await _redis_client.close()
        logger.info("Redis client closed.")


# --- Dependency Injectors ---

def get_redis_client() -> redis.Redis:
    """Dependency Injection to provide access to the initialized redis client."""
    if _redis_client is None:
        raise RuntimeError("Redis Client is not initialized")
    return _redis_client
