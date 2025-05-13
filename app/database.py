from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_to_mongo(cls):
        """Create database connection"""
        cls.client = AsyncIOMotorClient(settings.mongodb_uri)
        
    @classmethod
    async def close_mongo_connection(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        return cls.client[settings.database_name]

# Database instance
db = MongoDB()