from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional, Annotated, Any
from datetime import datetime
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]

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
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
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