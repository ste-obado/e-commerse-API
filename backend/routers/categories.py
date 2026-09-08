#POST   /categories
#GET    /categories
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import require_admin
from models import User
from schema import add_Category,Update_category
from services.category_service import add_category,get_categories,update_category


router=APIRouter(prefix="/category",tags=["Category"])

######################
#Add category
@router.post("/add to category")
def add_category(category:add_Category,user:User=Depends(require_admin),db:Session=Depends(get_db)):
    return add_category(category,user,db)

###############
#Get exixting categories
@router.get("/categories")
def get_categories(user:User=Depends(require_admin), db:Session=Depends(get_db)):
    return get_categories(user,db)

###################
#Update category
@router.patch("/update category")
def update_category(category_id:int,category2:Update_category,user:User=Depends(require_admin),
                    db:Session=Depends(get_db)):
    return update_category(category_id,category2,user,db)
        
  
    
    
   
    
