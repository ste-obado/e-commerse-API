#POST   /products
#GET    /products
#GET    /products/{id}
#PUT    /products/{id}
#DELETE /products/{id}


#/products?category=electronics
#/products?search=phone
#/products?min_price=1000&max_price=50000


from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import require_admin,require_user,credentials_exception
from models import User,Product
from schema import add_product,Update_product,Get_products
from utils.Authcheck import check_ownership

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

@router.post("/add_to_cart")
def add_cart(product:add_product,user:User=Depends(require_admin),db:Session=Depends(get_db)):
    exist_product=db.query(Product).filter(Product.P_name==product.P_name).first()
    if exist_product is None:
        raise credentials_exception
    db_product=Product(Category_id=product.category_id,P_name=product.P_name,price=product.price,description=product.description,stock=product.stock)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return{"message": "product added"}

##################
#update products

@router.patch("/update_product")
def update_product(product_id:int,product2:Update_product,user:User=Depends(require_admin),db:Session=Depends(get_db)):
    exist_product=db.query(Product).filter(Product.id==product_id).first()
    if not exist_product:
        raise HTTPException(status=404,detail="Product not found")
    
    updated_data=product2.model_dump(exclude_unset=True)
    if "P_name" in updated_data:
        existing_product=db.query(Product).filter(Product.P_name==updated_data["P_name"]).first()
        if existing_product and existing_product.id != product_id:
            raise HTTPException(status=400,detail="Product name already exists")
    for field,value in updated_data.items():
        setattr(exist_product,field,value)
    if exist_product.stock <= 0 or exist_product.price <= 0:
            raise HTTPException(status=422,detail="invalid credentials")

    db.commit()
    db.refresh(exist_product)
    return{
         "message": "Product updated",
         "Product": exist_product
    }

#################
#delete products
@router.delete("/rm_product")
def delete_product(product_id:int,user:User = Depends(require_admin),
                   db:Session = Depends(get_db)):
   
   remove_product= db.query(Product).filter(Product.id == product_id).first()
                                          
   if remove_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    

    #check ownership before deletion
   check_ownership(remove_product.user_id, user)

   db.delete(remove_product)
   db.commit()
   return {"message":f"{remove_product.Product_id}removed "}    
 

#####################3
#USER PART



######################
#correction

@router.get("/get_products")
def get_products(products:Get_products ,db:Session = Depends(get_db),user:User=Depends(require_user)):

    existing_products= db.query(Product).all

    # Filter by category
    if products.category_id is not None:
        existing_products= db.query(Product).filter(Product.Category_id == products.category_id)

    # Search by product name
    if products.search:
        existing_products = db.query(Product).filter(Product.P_name.ilike(f"%{products.search}%"))

    # Minimum price
    if products.min_price is not None:
        existing_products = db.query(Product).filter(Product.price >= products.min_price)

    # Maximum price
    if products.max_price is not None:
        existing_products = db.query(Product).filter(Product.price <= products.max_price)

    # Sorting
    if products.sort == "price_asc":
        existing_products = db.query(Product).order_by(Product.price.asc())

    elif products.sort == "price_desc":
        existing_products = db.query(Product).order_by(Product.price.desc())

    return existing_products

