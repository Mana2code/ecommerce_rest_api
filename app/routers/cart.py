from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_db
from ..models import CartItem, Order, OrderItem, Product, User
from ..schemas import CartAdd, OrderOut
from ..dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# ----------------------------
# Add item to cart
# ----------------------------
@router.post("/")
def add_to_cart(
    item: CartAdd,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    # Check if item already in cart
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user.id,
        CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_id=user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Item added to cart",
        "cart_item": {
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        }
    }


# ----------------------------
# View cart items
# ----------------------------
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    result = []
    for item in cart_items:
        result.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price_per_unit": item.product.price,
            "total_price": item.product.price * item.quantity
        })
    return result


# ----------------------------
# Checkout cart
# ----------------------------
@router.post("/checkout", response_model=OrderOut)
def checkout(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Fetch cart items
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    try:
        # Start transaction
        order = Order(user_id=user.id, total_amount=total_amount)
        db.add(order)
        db.flush()  # generate order.id without committing

        # Add OrderItems
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.add(order_item)

        # Clear user's cart
        db.query(CartItem).filter(CartItem.user_id == user.id).delete(synchronize_session=False)

        db.commit()
        db.refresh(order)  # refresh to include relationship-loaded items

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Checkout failed: {str(e)}")

    # Return SQLAlchemy object — FastAPI + Pydantic will serialize using OrderOut
    return order