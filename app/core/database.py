from typing import Optional, Mapping, Any
import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.core.logging import settings, logger

# ---- Global Connection Variables ----

# MongoDB
mongo_client: Optional[AsyncIOMotorClient[Mapping[str, Any] | Any]] = None
mongo_database: Optional[AsyncIOMotorClient[Mapping[str, Any] | Any]] = None
url_collection: Optional[AsyncIOMotorCollection[Mapping[str, Any] | Any]] = None

# PostgreSQL
pg_pool: Optional[asyncpg.Pool] = None


async def connect_db():
    """Initializes MongoDB and PostgreSQL connections."""
    global mongo_client, mongo_database, url_collection, pg_pool

    logger.info("Connecting to MongoDB")

    # MongoDB Connection
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
        await mongo_client.admin.command('ping')
        mongo_database = mongo_client.get_database()
        url_collection = mongo_database.get_collection("urls")
        logger.info("MongoDB connected.")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")


    logger.info("Connecting to PostgreSQL")

    # PostgreSQL Connection Pool
    try:
        pg_pool = await asyncpg.create_pool(
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
    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB client closed.")

    # Closing PostgreSQL
    if pg_pool:
        await pg_pool.close()
        logger.info("PostgreSQL pool closed.")















