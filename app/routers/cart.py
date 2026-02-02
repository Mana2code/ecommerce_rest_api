from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..database import get_db
from ..models import CartItem, Order, OrderItem, User
from ..schemas import CartAdd, CartItemOut, OrderOut
from ..dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# Add item to cart
@router.post("/", response_model=CartItemOut)
def add_to_cart(item: CartAdd, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart_item = CartItem(user_id=user.id, product_id=item.product_id, quantity=item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return CartItemOut(
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        price_per_unit=cart_item.product.price,
        total_price=cart_item.product.price * cart_item.quantity
    )

# View cart
@router.get("/", response_model=list[CartItemOut])
def view_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return [
        CartItemOut(
            product_id=i.product_id,
            quantity=i.quantity,
            price_per_unit=i.product.price,
            total_price=i.product.price * i.quantity
        ) for i in items
    ]

# Checkout
@router.post("/checkout", response_model=OrderOut)
def checkout(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    try:
        order = Order(user_id=user.id, total_amount=total_amount)
        db.add(order)
        db.flush()  # get order.id without commit

        order_items = []
        for item in cart_items:
            oi = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price)
            db.add(oi)
            order_items.append(
                CartItemOut(
                    product_id=oi.product_id,
                    quantity=oi.quantity,
                    price_per_unit=oi.price,
                    total_price=oi.price * oi.quantity
                )
            )

        db.query(CartItem).filter(CartItem.user_id == user.id).delete(synchronize_session=False)
        db.commit()
        db.refresh(order)

        return OrderOut(id=order.id, total_amount=total_amount, items=order_items)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Checkout failed: {str(e)}")
