from fastapi import HTTPException
from core.protection  import credentials_exception
from models import Category


######################
#Add category

def add_category(category,user,db):
    exist_category=db.query(Category).filter(Category.C_name==category.C_name).first()
    if exist_category is None:
        raise credentials_exception
    db_cart=Category(C_name=category.C_name)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

###############
#Get exixting categories
def get_categories(user, db):
    categories = db.query(Category).all()
    return categories

###################
#Update category

def update_category(category_id,category2,user,db):
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

    
    

