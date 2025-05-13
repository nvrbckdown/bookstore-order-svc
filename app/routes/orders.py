from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.order import Order, OrderCreate, OrderUpdate
from app.services.order_service import OrderService
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Order)
async def create_order(order: OrderCreate):
    """Create a new order"""
    # Verify books exist
    items_dict = [item.dict() for item in order.items]
    if not await OrderService.verify_books_exist(items_dict):
        raise HTTPException(status_code=404, detail="One or more books not found")
    
    created_order = await OrderService.create_order(order)
    return created_order

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get an order by ID"""
    order = await OrderService.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=List[Order])
async def get_orders(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Get all orders with pagination"""
    orders = await OrderService.get_orders(skip=skip, limit=limit)
    return orders

@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, update_data: OrderUpdate):
    """Update an order"""
    updated_order = await OrderService.update_order(order_id, update_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}")
async def delete_order(order_id: str):
    """Delete an order"""
    success = await OrderService.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@router.get("/customer/{customer_email}", response_model=List[Order])
async def get_orders_by_customer(customer_email: str):
    """Get all orders by customer email"""
    from app.database import db
    collection = db.get_database()["orders"]
    cursor = collection.find({"customer_email": customer_email}).sort("created_at", -1)
    
    orders = []
    async for order in cursor:
        orders.append(Order(**order))
    return orders