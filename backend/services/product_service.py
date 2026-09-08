from fastapi import HTTPException
from core.protection  import credentials_exception
from models import Product
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


#######################3
#ADMIN PART
#add products


def add_cart(product,user,db):
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

def update_product(product_id,product2,user,db):
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
def delete_product(product_id,user,db):
   
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
def get_products(products ,db,user):

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

