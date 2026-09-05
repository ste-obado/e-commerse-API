#POST /orders
#GET  /orders
#GET  /orders/{id}

#status 
#PENDING
#PAID
#PROCESSING
#SHIPPED
#DELIVERED
#CANCELLED

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Order, Order_items, Cart, Cart_items, Product, User
from core.protection import require_user 


router = APIRouter(prefix="/orders",tags=["Orders"])


# CREATE ORDER FROM CART
@router.post("/")
def create_order(user: User = Depends(require_user),db: Session = Depends(get_db)
):
    # Find user's cart
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()

    if not cart:
        raise HTTPException(status_code=404,detail="Cart not found")

    # Get cart items
    cart_items = db.query(Cart_items).filter(Cart_items.cart_id == cart.id).all()

    if not cart_items:
        raise HTTPException(status_code=400,detail="Cart is empty")

    # Create order
    order = Order(user_id=user.id,status="PENDING",total_price=0)

    db.add(order)
    db.flush()

    total_price = 0

    # Create order items
    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        item_total = product.price * item.quantity
        total_price += item_total

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

    # Update order total
    order.total_price = total_price

    # Clear cart
    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(order)

    return order