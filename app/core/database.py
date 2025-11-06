import asyncpg
from typing import Optional, Mapping, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.core.logging import settings, logger

# ---- Private Connection Variables ----

# MongoDB
_mongo_client: Optional[AsyncIOMotorClient[Mapping[str, Any] | Any]] = None
_mongo_database: Optional[AsyncIOMotorClient[Mapping[str, Any] | Any]] = None
_url_collection: Optional[AsyncIOMotorCollection[Mapping[str, Any] | Any]] = None

# PostgreSQL
_pg_pool: Optional[asyncpg.Pool] = None


async def connect_db():
    """Initializes MongoDB and PostgreSQL connections."""
    global _mongo_client, _mongo_database, _url_collection, _pg_pool

    logger.info("Connecting to MongoDB")

    # MongoDB Connection
    try:
        _mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
        await _mongo_client.admin.command('ping') # Verify Connection
        _mongo_database = _mongo_client.get_database()
        _url_collection = _mongo_database.get_collection("urls")
        logger.info("MongoDB connected.")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")


    logger.info("Connecting to PostgreSQL")

    # PostgreSQL Connection Pool
    try:
        _pg_pool = await asyncpg.create_pool(
            user=settings.PG_USER,
            password=settings.PG_PASS,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
            database=settings.PG_DB
        )
        logger.info("Connected PostgreSQL")
    except Exception as e:
        logger.error(f"Could not connect to PostgreSQL: {e}")


async def close_db():
    """Closes all database connections and connection pools upon shutdown."""
    logger.info("Closing database connections...")

    # Closing MongoDB
    if _mongo_client:
        _mongo_client.close()
        logger.info("MongoDB client closed.")

    # Closing PostgreSQL
    if _pg_pool:
        await _pg_pool.close()
        logger.info("PostgreSQL pool closed.")

# --- Dependency Injectors ---

def get_pg_pool() -> asyncpg.Pool:
    """Dependency Injection to provide access to the initialized PostgreSQL pool"""
    if _pg_pool is None:
        raise RuntimeError("PostgreSQL pool is not yet initialized.")
    return _pg_pool

def get_url_collection() -> AsyncIOMotorCollection:
    """Dependency Injection to provide access to the initialized MongoDB URL collection."""
    if _url_collection is None:
        raise RuntimeError("MongoDB URL collection is not yet initialized.")
    return _url_collection
