from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
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
    def __get_pydantic_json_schema__(cls, _field_schema, handler):
        return {"type": "string"}

class OrderItem(BaseModel):
    book_id: int
    book_title: str
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Order(BaseModel):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"  # pending, confirmed, shipped, delivered, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )