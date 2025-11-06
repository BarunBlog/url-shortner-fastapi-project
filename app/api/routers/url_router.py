import asyncpg
import redis
from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi.responses import RedirectResponse
from app.core.database import get_pg_pool, get_url_collection
from app.core.redis import get_redis_client
from app.schemas.url_schema import URLCreate, URLResponse
from app.services import url_service

router = APIRouter()


@router.post("/urls", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url_endpoint(
        url_data: URLCreate,
        pg_pool: asyncpg.Pool = Depends(get_pg_pool),
        url_collection: AsyncIOMotorCollection = Depends(get_url_collection),
        redis_client: redis.Redis = Depends(get_redis_client)
):
    """
    Creates a short URL for the provided long URL.
    Pydantic (URLCreate) automatically handles validation of the request body.
    """
    try:
        short_url = await url_service.shorten_url(
            long_url=str(url_data.longUrl),
            pg_pool=pg_pool,
            url_collection=url_collection,
            redis_client=redis_client
        )
        return URLResponse(short_url=short_url)
    except Exception as e:
        # Catch unexpected errors during DB insertion, etc.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{short_url_id}")
async def redirect_to_long_url_endpoint(
        short_url_id: str,
        url_collection: AsyncIOMotorCollection = Depends(get_url_collection),
        redis_client: redis.Redis = Depends(get_redis_client)
):
    """
    Redirects the user from the short URL ID to the original long URL.
    """
    long_url = await url_service.get_long_url(
        short_url_id=short_url_id,
        url_collection = url_collection,
        redis_client = redis_client
    )

    if long_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    # Equivalent to res.redirect(301, longUrl)
    return RedirectResponse(url=long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)