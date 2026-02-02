from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import Product
from ..schemas import ProductCreate
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(
    p: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = Product(**p.dict())
    db.add(product)
    db.commit()
    return product

@router.get("/")
def list_products(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Product).all()

@router.put("/{product_id}")
def update_product(
    product_id: int,
    p: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    product.name = p.name
    product.price = p.price
    db.commit()
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()
    return {"message": "Deleted"}
