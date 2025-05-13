from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class OrderItem(BaseModel):
    book_id: int
    book_title: str
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)
    
    class Config:
        json_encoders = {ObjectId: str}

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    
    class Config:
        json_encoders = {ObjectId: str}

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    
    class Config:
        json_encoders = {ObjectId: str}

class Order(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"  # pending, confirmed, shipped, delivered, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}