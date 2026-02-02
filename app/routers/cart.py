from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import CartAdd
from ..models import CartItem
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add_to_cart(
    item: CartAdd,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart = CartItem(
        user_id=user.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(cart)
    db.commit()
    return {"message": "Added to cart"}

@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(CartItem).filter(CartItem.user_id == user.id).all()

@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    return {"message": "Checkout successful"}
