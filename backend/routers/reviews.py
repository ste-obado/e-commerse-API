#POST /products/{id}/reviews
#GET  /products/{id}/reviews

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import get_current_user,require_user_or_admin
from models import User
from schema import review
from services.review_service import comment_product,get_reviews,delete_comment



router=APIRouter(prefix="/Review",tags=["Review"])

################################
#any user can add a have a review 
@router.post("/review/{product_id}")
def comment_product(product_id:str,content:review,
                    db:Session=(Depends(get_db)),user:User=Depends(get_current_user)):
   return comment_product(product_id,content, db,user)

###############################
#users can view other comments
@router.get("/reviews/{product_id}")
def get_reviews(product_id:str,db:Session = Depends(get_db),user:User=Depends(get_current_user)):
   return get_reviews(product_id,db,user)

###############################
#the admin/user  can delete posts
@router.delete("/reviews/{reviews_id}")
def delete_comment(reviews_id:int,user:User = Depends(require_user_or_admin),
                   db:Session = Depends(get_db)):
   return delete_comment(reviews_id,user,db)