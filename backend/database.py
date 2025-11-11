from typing import Any, Dict, Optional, List
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "shopping_ai")


settings = Settings()
_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.DATABASE_URL)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        _db = get_client()[settings.DATABASE_NAME]
    return _db


async def create_document(collection: str, data: Dict[str, Any]) -> str:
    db = get_db()
    now = datetime.utcnow()
    data_with_meta = {**data, "created_at": now, "updated_at": now}
    res = await db[collection].insert_one(data_with_meta)
    return str(res.inserted_id)


async def get_documents(collection: str, filter_dict: Dict[str, Any] | None = None, limit: int = 20) -> List[Dict[str, Any]]:
    db = get_db()
    cursor = db[collection].find(filter_dict or {}).limit(limit)
    docs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # make JSON serializable
        docs.append(doc)
    return docs
