from fastapi import APIRouter, Depends, HTTPException
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
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------------------
# Login user
# --------------------
@router.post("/login", response_model=TokenOut)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --------------------
# Get current user info
# --------------------
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# --------------------
# Get all orders of current user
# --------------------
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
