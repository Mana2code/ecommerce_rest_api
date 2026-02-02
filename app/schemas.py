from pydantic import BaseModel
from typing import Optional, List

# User schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}

# JWT Token schema
class TokenOut(BaseModel):
    access_token: str
    token_type: str

    model_config = {"from_attributes": True}

# Product schemas
class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int

    model_config = {"from_attributes": True}

# Cart schemas
class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float
    total_price: float

    model_config = {"from_attributes": True}

# Order schemas
class OrderOut(BaseModel):
    id: int
    total_amount: float
    items: List[CartItemOut]

    model_config = {"from_attributes": True}
