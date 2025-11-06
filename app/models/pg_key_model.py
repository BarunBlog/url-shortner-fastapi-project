from app.core.logging import logger
from app.core.database import pg_pool


async def get_unused_key() -> str:
    """
    Atomically retrieves one unused short URL key from PostgreSQL and marks it as used.
    Uses the globally managed pg_pool.
    """

    if pg_pool is None:
        raise Exception("Postgresql pool is not initialized")

    conn = await pg_pool.acquire() # Get connection from pool

    try:
        async with conn.transaction():
            # Select an unused key
            unused_key = await conn.fetchrow(
                'SELECT short_url_id FROM keys WHERE used = FALSE LIMIT 1 FOR UPDATE'
            )

            if not unused_key:
                raise Exception("No unused keys available")

            short_url_id = unused_key['short_url_id']

            # Update that unused key to mark it used
            await conn.execute(
                'UPDATE keys SET used = TRUE WHERE short_url_id = $1', short_url_id
            )

            return short_url_id


    except Exception as e:
        logger.error(f"PostgreSQL Transaction Error: {e}")
        # The transaction will roll back automatically on exception
        raise e
    finally:
        await pg_pool.release(conn)  # Return connection to pool