from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import User, Order, OrderItem
from ..schemas import UserCreate, UserLogin, UserOut, TokenOut, OrderOut, CartItemOut
from ..utils.security import get_password_hash, verify_password
from ..utils.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# --------------------
# Register user
# --------------------
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    try:
        hashed_password = get_password_hash(user.password)
        new_user = User(email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserOut(id=new_user.id, email=new_user.email)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")



@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email)


@router.get("/orders", response_model=list[OrderOut])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    order_list = []
    for order in orders:
        items = [
            CartItemOut(
                product_id=oi.product_id,
                quantity=oi.quantity,
                price_per_unit=oi.price,
                total_price=oi.price * oi.quantity
            )
            for oi in order.items
        ]
        order_list.append(OrderOut(id=order.id, total_amount=order.total_amount, items=items))
    return order_list
