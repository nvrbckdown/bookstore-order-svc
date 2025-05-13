from fastapi import FastAPI
from app.config import settings
from app.database import db
from app.routes.orders import router as order_router

app = FastAPI(
    title="Order Service",
    description="A microservice for handling orders in the bookstore system",
    version="1.0.0",
    debug=settings.debug
)

@app.on_event("startup")
async def startup_event():
    await db.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await db.close_mongo_connection()

# Include routers
app.include_router(order_router, prefix="/api/v1/orders", tags=["orders"])

@app.get("/")
async def root():
    return {"message": "Order Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}