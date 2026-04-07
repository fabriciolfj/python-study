from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

MONGO_URL = "mongodb://appuser:apppass123@localhost:27017/mydb"
DB_NAME = "mydb"

class Database:
    client: Optional[AsyncIOMotorClient] = None

db = Database()


async def connect():
    db.client = AsyncIOMotorClient(MONGO_URL)
    print("connect mongo db")

async def disconnect():
    db.client.close()
    print("disconnect mongo db")

def get_collection(name: str):
    return db.client[DB_NAME][name]