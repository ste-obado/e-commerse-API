from fastapi import  HTTPException
from models import Order, Order_items, Cart, Cart_items, Product, User
from schema import Status
from utils.Authcheck import check_ownership


############################
# CREATE ORDER FROM CART

def create_order(user,db):
    # Find user's cart
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()

    if not cart:
        raise HTTPException(status_code=404,detail="Cart not found")

    # Get cart items
    cart_items = db.query(Cart_items).filter(Cart_items.cart_id == cart.id).all()

    if not cart_items:
        raise HTTPException(status_code=400,detail="Cart is empty")

    # Create order
    order = Order(user_id=user.id,status=Status.pending,Total_amount=0)

    db.add(order)
    db.flush()

    total_price = 0

    # Create order items
    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(status_code=404,detail=f"Product {item.product_id} not found"
            )

        #calculate total price for each item and add to total order price
        item_total = product.price * item.quantity
        total_price += item_total

        order_item = Order_items(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

    # Update order total
    order.Total_amount = total_price

    # Clear cart
    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(order)

    return order

#############################
# GET ORDER FROM CART
def get_cart(user, db):
    Order_item = (
        db.query(Order_items)
        .join(Product, Product.id == Order_items.product_id)
        .join(Order, Order_items.order_id == Order.id)
        .filter(Order.user_id == user.id)
        .all()
    )

    return{
    "product": Order_item.Product.name,
    "quantity": Order_item.Quantity,
    "unit_price": Order_item.Product.price,
    "total_price": Order_item.Order.Total_amount
}


#############################
# REVOKE ORDER FROM CART
def delete_product(user,db):
   
   revoked_order= db.query(Order).filter(Order.user_id == user.id).first()
                                          
   if revoked_order is None:
        raise HTTPException(status_code=404,detail="order not exist")

   check_ownership(revoked_order.user_id, user)
   revoked_order.Isactive=False
   revoked_order.status=Status.cancelled

   db.commit()
   db.refresh(revoked_order)
   return {"message":f"{revoked_order.id}cancelled "}