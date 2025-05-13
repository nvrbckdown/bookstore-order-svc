from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import httpx
from app.models.order import Order, OrderCreate, OrderUpdate
from app.database import db
from app.config import settings

class OrderService:
    @staticmethod
    async def create_order(order_data: OrderCreate) -> Order:
        """Create a new order"""
        # Calculate total amount
        total_amount = sum(item.price * item.quantity for item in order_data.items)
        
        # Create order document
        order_doc = {
            "customer_name": order_data.customer_name,
            "customer_email": order_data.customer_email,
            "items": [item.model_dump() for item in order_data.items],  # Changed from .dict() to .model_dump()
            "total_amount": total_amount,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into database
        collection = db.get_database()["orders"]
        result = await collection.insert_one(order_doc)
        
        # Retrieve the created order
        created_order = await collection.find_one({"_id": result.inserted_id})
        return Order(**created_order)
    
    @staticmethod
    async def get_order(order_id: str) -> Optional[Order]:
        """Get an order by ID"""
        collection = db.get_database()["orders"]
        order = await collection.find_one({"_id": ObjectId(order_id)})
        
        if order:
            return Order(**order)
        return None
    
    @staticmethod
    async def get_orders(skip: int = 0, limit: int = 10) -> List[Order]:
        """Get all orders with pagination"""
        collection = db.get_database()["orders"]
        cursor = collection.find().skip(skip).limit(limit).sort("created_at", -1)
        
        orders = []
        async for order in cursor:
            orders.append(Order(**order))
        return orders
    
    @staticmethod
    async def update_order(order_id: str, update_data: OrderUpdate) -> Optional[Order]:
        """Update an order"""
        collection = db.get_database()["orders"]
        
        update_dict = {}
        if update_data.status:
            update_dict["status"] = update_data.status
        
        if update_dict:
            update_dict["updated_at"] = datetime.utcnow()
            result = await collection.find_one_and_update(
                {"_id": ObjectId(order_id)},
                {"$set": update_dict},
                return_document=True
            )
            
            if result:
                return Order(**result)
        return None
    
    @staticmethod
    async def delete_order(order_id: str) -> bool:
        """Delete an order"""
        collection = db.get_database()["orders"]
        result = await collection.delete_one({"_id": ObjectId(order_id)})
        return result.deleted_count > 0
    
    @staticmethod
    async def verify_books_exist(items: List[dict]) -> bool:
        """Verify that all books in the order exist in the book service"""
        book_ids = [item["book_id"] for item in items]
        
        async with httpx.AsyncClient() as client:
            for book_id in book_ids:
                try:
                    response = await client.get(f"{settings.book_service_url}/api/books/{book_id}")
                    if response.status_code != 200:
                        return False
                except httpx.RequestError:
                    return False
        return True