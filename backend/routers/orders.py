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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import  User
from core.protection import require_user 
from services.order_service import create_order,get_cart,delete_product


router = APIRouter(prefix="/orders",tags=["Orders"])

#############################
# CREATE ORDER FROM CART
@router.post("/create order")
def create_order(user: User = Depends(require_user),db: Session = Depends(get_db)):
    return create_order(user,db)

#############################
# GET ORDER FROM CART
@router.get("/order items")
def get_cart(user:User=Depends(require_user), db:Session=Depends(get_db)):
    return get_cart(user,db)

#############################
# REVOKE ORDER FROM CART
@router.patch("/rm_product")
def delete_product(user:User = Depends(require_user),
                   db:Session = Depends(get_db)):
    return delete_product(user,db)

   