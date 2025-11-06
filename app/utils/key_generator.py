import asyncio
import random
import string
from typing import Optional
import asyncpg
from app.core.config import settings
from app.core.logging import logger

CHARACTERS = string.ascii_letters + string.digits

def generate_key(length: int = 7) -> str:
    """Generates a random key of a given length."""
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

async def pre_populate_keys(count: int):
    """
    Generates and inserts unique keys into the PostgreSQL 'keys' table.
    """
    pool: Optional[asyncpg.Pool] = None

    try:
        # 1. Create temporary pool (must use await)
        pool = await asyncpg.create_pool(
            user=settings.PG_USER,
            password=settings.PG_PASS,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
            database=settings.PG_DB
        )

        # Prepare the list of keys to insert
        keys = [(generate_key(), False) for _ in range(count)]

        # Use a single connection for mass insertion
        conn = await pool.acquire()

        # Used the copy_records_to_table function for faster mass insertion
        await conn.copy_records_to_table(
            'keys',
            records=keys,
            columns=['short_url_id', 'used']
        )

        logger.info(f"{count} keys populated into PostgreSQL.")
        await pool.release(conn)

    except Exception as e:
        logger.error(f"Error during key population: {e}")
    finally:
        if pool:
            await pool.close()

if __name__ == "__main__":
    KEY_COUNT = 1000000
    logger.info(f"Starting key population for {KEY_COUNT} keys...")

    try:
        asyncio.run(pre_populate_keys(KEY_COUNT))
        logger.info("Key population script finished successfully.")
    except Exception as e:
        logger.error(f"Key population failed: {e}")
        exit(1)