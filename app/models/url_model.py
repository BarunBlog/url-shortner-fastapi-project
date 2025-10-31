from datetime import datetime
from pydantic import BaseModel, Field

class URL(BaseModel):
    shortUrlId: str = Field(..., alias="short_url_id")
    longUrl: str = Field(..., alias="long_url")
    createdAt: datetime = Field(default_factory=datetime.utcnow, alias="created_at")
    visits: int = 0