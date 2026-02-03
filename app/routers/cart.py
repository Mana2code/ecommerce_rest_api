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

@router.post("/checkout", response_model=OrderOut)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch all cart items for the user
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    try:
        # Start transaction: create Order
        order = Order(user_id=current_user.id, total_amount=total_amount)
        db.add(order)
        db.flush()  # get order.id without committing

        order_items_out = []
        # Create OrderItems
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.add(order_item)

            order_items_out.append(
                CartItemOut(
                    product_id=order_item.product_id,
                    quantity=order_item.quantity,
                    price_per_unit=order_item.price,
                    total_price=order_item.price * order_item.quantity
                )
            )

        # Clear user's cart
        db.query(CartItem).filter(CartItem.user_id == current_user.id).delete(synchronize_session=False)

        # Commit everything
        db.commit()
        db.refresh(order)

        return OrderOut(
            id=order.id,
            total_amount=total_amount,
            items=order_items_out
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Checkout failed: {str(e)}")
    except Exception as e:
        db.rollback()

