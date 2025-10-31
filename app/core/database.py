from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# Initialize client and database connections
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client.get_database()
url_collection = database.get_collection("urls")

