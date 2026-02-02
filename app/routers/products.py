from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..database import get_db
from ..models import Product, User
from ..schemas import ProductCreate, ProductOut
from ..dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

# ----------------------------
# Create a product
# ----------------------------
@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # You may add admin check here if needed
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# ----------------------------
# List all products
# ----------------------------
@router.get("/", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    products = db.query(Product).all()
    return products


# ----------------------------
# Get product by ID
# ----------------------------
@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ----------------------------
# Update product
# ----------------------------
@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock

    db.commit()
    db.refresh(product)
    return product


# ----------------------------
# Delete product
# ----------------------------
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        db.delete(product)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")

    return {"message": "Product deleted successfully"}
