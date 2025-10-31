from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional

# Data structure for creating a short URL (Request Body)
class URLCreate(BaseModel):
    # Use HttpUrl for validation similar to the regex check
    longUrl: HttpUrl = Field(..., alias="long_url")
    # This allows request to be received with "longUrl" but internally uses "long_url"

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


# Data structure for the successful response
class URLResponse(BaseModel):
    shortUrl: str = Field(..., alias="short_url")

    class Config:
        populate_by_name = True