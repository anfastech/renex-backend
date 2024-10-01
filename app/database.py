from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL")  # Ensure your environment variable is set

client = None

def get_mongo_client():
    """Get MongoDB client, initializing if necessary."""
    global client
    if client is None:
        client = AsyncIOMotorClient(MONGODB_URL)
    return client

def get_collection(db_name: str, collection_name: str):
    """Get the specified MongoDB collection."""
    db = get_mongo_client()[db_name]
    collection = db[collection_name]
    return collection
