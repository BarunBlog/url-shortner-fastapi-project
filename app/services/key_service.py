from app.models.pg_key_model import get_unused_key

async def fetch_unique_key() -> str:
    """Fetches a unique, unused key from the PostgreSQL pool."""
    return await get_unused_key()