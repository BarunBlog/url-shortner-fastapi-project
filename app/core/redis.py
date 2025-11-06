import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger
from typing import Optional


# Global Redis Client Variable
redis_client: Optional[redis.Redis] = None


async def connect_redis():
    """Initializes the asynchronous Redis client and verifies the connection"""
    global redis_client

    logger.info("Connecting to redis cache...")

    try:
        # Construct the connection URL using settings
        redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"

        # Initialize the client, ensuring async compatibility and auto-decoding for strings
        redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

        # Verify connection by sending a simple command
        await redis_client.ping()
        logger.info("Redis client connected successfully.")
    except Exception as e:
        logger.error(f"Could not connect to Redis: {e}")


async def close_redis():
    """Closes the redis client connection."""
    global redis_client

    if redis_client:
        await redis_client.close()
        logger.info("Redis client closed.")





















