#POST   /categories
#GET    /categories
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import require_admin,credentials_exception
from models import User,Category
from schema import add_category,Update_category


router=APIRouter(prefix="/category",tags=["Category"])
######################
#Add category

@router.post("/add_to_category")
def add_category(category:add_category,user:User=Depends(require_admin),db:Session=Depends(get_db)):
    exist_category=db.query(Category).filter(Category.C_name==category.C_name).first()
    if exist_category is None:
        raise credentials_exception
    db_cart=Category(C_name=category.C_name)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

###############
#Get exixting categories

@router.get("/categories")
def get_categories(user:User=Depends(require_admin), db:Session=Depends(get_db)):
    categories = db.query(Category).all()
    return categories

###################
#Update category

@router.patch("/update_category")
def update_category(category_id:int,category2:Update_category,user:User=Depends(require_admin),
                    db:Session=Depends(get_db)):
    category_groups=(
        db.query(Category).
        filter(Category.id==category_id).first())
    
    if not category_groups:
        raise  HTTPException(status=404,detail="category not found")

    updated_data=category2.model_dump(exclude_unset=True)
    for field,value in updated_data.items():
        setattr(category_groups,field,value)
  
    
    
    db.commit()
    db.refresh(category_groups)
    return{
         "message": "Category updated",
         "category": category_groups}

    
    
