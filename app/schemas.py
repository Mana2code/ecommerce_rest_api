from pydantic import BaseModel
from typing import List, Optional


# ----------------------
# User Schemas
# ----------------------

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True
    }


# ----------------------
# Product Schemas
# ----------------------

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    model_config = {
        "from_attributes": True
    }


# ----------------------
# Cart Schemas
# ----------------------

class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut  # nested product details

    model_config = {
        "from_attributes": True
    }


# ----------------------
# Order Schemas
# ----------------------

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float
    product: ProductOut

    model_config = {
        "from_attributes": True
    }

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    items: List[OrderItemOut] = []

    model_config = {
        "from_attributes": True
    }
