from typing import Optional
from app.core.config import settings
from app.models.url_model import URL
from app.core.database import url_collection
from app.core.redis import redis_client
from app.core.logging import logger
from app.services.key_service import fetch_unique_key

CACHE_TTL = 3600


async def shorten_url(long_url: str) -> str:
    """Creates a short URL entry in the database."""
    try:

        # Get unique key from PostgreSQL
        short_url_id = await fetch_unique_key()

        # Prepare data for MongoDB (using keys that match the schema for clarity)
        url_data = URL(
            short_url_id=short_url_id,
            long_url=long_url
        )

        # Insert into database
        await url_collection.insert_one(url_data.model_dump(by_alias=True))

        # Cache the urls mapping in Redis
        await redis_client.set(short_url_id, long_url, ex=CACHE_TTL)

        # Return the full short URL
        return f"{settings.BASE_URL}/{short_url_id}"

    except Exception as e:
        logger.error(f"Error creating short URL: {e}")
        raise e


async def get_long_url(short_url_id: str) -> Optional[str]:
    """Retrieves the original URL and increments the visit count."""

    cached_url = await redis_client.get(short_url_id)
    if cached_url:
        return cached_url

    # 1. Find the document from MongoDB
    url_doc = await url_collection.find_one_and_update(
        {"short_url_id": short_url_id},
        {"$inc": {"visits": 1}},  # Atomically increment visits
        projection={"long_url": True, "_id": False},  # Only retrieve long_url
    )

    if url_doc:
        # Motor returns a dict, extract the long_url
        return url_doc["long_url"]

    return None  # URL not found