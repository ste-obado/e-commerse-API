#POST   /cart/items
#GET    /cart
#PUT    /cart/items/{id}
#DELETE /cart/items/{id}

#calculation 
#subtotal
#quantity
#total
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import require_user
from models import User
from schema import add_cart,Update_cart
from services.cart_service import add_cart,get_cart,update_cart



router=APIRouter(prefix="/cart",tags=["Cart"])

#######################
#add cart items
@router.post("/add to cart")
def add_cart(cart:add_cart,user:User=Depends(require_user),db:Session=Depends(get_db)):
  return add_cart(cart,user,db)

###################
#get cart items
@router.get("/cart items")
def get_cart(user:User=Depends(require_user), db:Session=Depends(get_db)):
   return get_cart(user,db)

###################
#update cart items
@router.patch("/update cart")
def update_cart(product_id:int,cart2:Update_cart,user:User=Depends(require_user),db:Session=Depends(get_db)):
    return update_cart(product_id,cart2,user,db)

###############
#delete cart items
@router.delete("/rm_product")
def delete_product(product_id:int,user:User = Depends(require_user),
                   db:Session = Depends(get_db)):
   return delete_product(product_id,user,db)