import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "bookstore_orders")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # External service URLs
    book_service_url: str = os.getenv("BOOK_SERVICE_URL", "http://localhost:5000")

settings = Settings()