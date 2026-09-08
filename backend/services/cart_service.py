from fastapi import HTTPException
from core.protection  import credentials_exception
from models import User,Product,Cart,Cart_items
from utils.Authcheck import check_ownership


def add_cart(cart,user,db):
    exist_product=db.query(Product).filter(Product.id==cart.product_id).first()
    if exist_product is None:
        raise credentials_exception
    db_cart=Cart(user_id=user.id)
    if cart.quantity <= 0 :
        raise HTTPException(status=422,detail="quantity can`t be 0")
    
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    ###############
    #add item to cart
    

    db_add_cart = Cart_items(Cart_id=db_cart.id, Product_id=cart.product_id,
                             Quantity=cart.quantity)
    db.add(db_add_cart)
    db.commit()
    db.refresh(db_add_cart)
    return{
        "message":f"product{db_add_cart.Product_id} added to cart"
    }


def get_cart(user, db):
    cart_item = (
        db.query(Cart_items)
        .join(Product, Product.id == Cart_items.Product_id)
        .join(Cart, Cart_items.Cart_id == Cart.id)
        .filter(Cart.User_id == user.id)
        .all()
    )

    item_total = cart_item.Quantity*cart_item.Product.price

    return{
    "product": cart_item.Product.name,
    "quantity": cart_item.Quantity,
    "unit_price": cart_item.Product.price,
    "total_price": item_total
}

###################
#update cart items

def update_cart(product_id,cart2,user,db):
    cart_in_product=(
        db.query(Cart_items).join(Cart).
        filter(Cart_items.Product_id==product_id.id,Cart.User_id==user.id).first())
    
    if not cart_in_product:
        raise  HTTPException(status=404,detail="product not in cart")

    updated_data=cart2.model_dump(exclude_unset=True)
    for field,value in updated_data.items():
        setattr(cart_in_product,field,value)
    if cart_in_product.quantity <= 0 :
            raise HTTPException(status=422,detail="quantity can`t be 0")
    exist_product = db.query(Product).filter(
    Product.id == product_id).first()
    
    total_price=cart2.quantity*exist_product.price
    db.commit()
    db.refresh(cart_in_product)
    return{
         "message": "Quantity added",
         "Quantity ":cart_in_product.Quantity,
         "price":total_price
         
    }


###############
#delete cart items

def delete_product(product_id,user,db):
   
   remove_product= db.query(Cart_items).filter(Cart_items.Product_id == product_id).first()
                                          
   if remove_product is None:
        raise HTTPException(status_code=404,detail="product not found")

    
   check_ownership(remove_product.user_id, user)

   db.delete(remove_product)
   db.commit()
   return {"message":f"{remove_product.Product_id}removed "}