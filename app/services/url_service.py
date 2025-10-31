import string
import random
from typing import Optional

from app.core.config import settings
from app.models.url_model import URL
from app.core.database import url_collection


def generate_short_url_id() -> str:
    """Generates a unique 7-character short ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(7))


async def shorten_url(long_url: str) -> str:
    """Creates a short URL entry in the database."""
    # Note: FastAPI/Pydantic has already validated long_url format

    # 1. Generate unique ID
    short_url_id = generate_short_url_id()

    # 2. Prepare data for MongoDB (using keys that match the schema for clarity)
    url_data = URL(
        short_url_id=short_url_id,
        long_url=long_url
    )

    # 3. Insert into database
    await url_collection.insert_one(url_data.dict(by_alias=True))

    # 4. Return the full short URL
    return f"{settings.BASE_URL}/{short_url_id}"


async def get_long_url(short_url_id: str) -> Optional[str]:
    """Retrieves the original URL and increments the visit count."""

    # 1. Find the document
    url_doc = await url_collection.find_one_and_update(
        {"short_url_id": short_url_id},
        {"$inc": {"visits": 1}},  # Atomically increment visits
        projection={"long_url": True, "_id": False},  # Only retrieve long_url
    )

    if url_doc:
        # Motor returns a dict, extract the long_url
        return url_doc["long_url"]

    return None  # URL not found