#POST   /products
#GET    /products
#GET    /products/{id}
#PUT    /products/{id}
#DELETE /products/{id}


#/products?category=electronics
#/products?search=phone
#/products?min_price=1000&max_price=50000


from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import require_admin,require_user
from models import User
from schema import add_product,Update_product,Get_products
from services.product_service import add_cart,update_product,delete_product,get_products

##########################
# ADMIN PART
#add products
#delete products
#update products

#########################
#ALL USERS 
#get existing products under specific categories 
# sorting under specific price range 
#search products
router= APIRouter(prefix="/products",tags=["Products"])

#######################3
#ADMIN PART
#add products
@router.post("/add to products")
def add_cart(product:add_product,user:User=Depends(require_admin),db:Session=Depends(get_db)):
    return add_cart(product,user,db)
 

##################
#update products
@router.patch("/update product")
def update_product(product_id:int,product2:Update_product,user:User=Depends(require_admin),db:Session=Depends(get_db)):
    return update_product(product_id,product2,user,db)

#################
#delete products
@router.delete("/rm_product")
def delete_product(product_id:int,user:User = Depends(require_admin),db:Session = Depends(get_db)):
   return delete_product(product_id,user,db)

#####################3
#USER PART

######################
#GET PRODUCTS

@router.get("/get products")
def get_products(products:Get_products ,db:Session = Depends(get_db),user:User=Depends(require_user)):
      return get_products(products ,db,user)