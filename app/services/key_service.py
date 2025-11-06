from app.models.pg_key_model import get_unused_key
import asyncpg

async def fetch_unique_key(pg_pool: asyncpg.Pool) -> str:
    """Fetches a unique, unused key from the PostgreSQL pool."""
    return await get_unused_key(pg_pool)