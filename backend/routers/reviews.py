#POST /products/{id}/reviews
#GET  /products/{id}/reviews

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import get_current_user,require_user_or_admin
from models import Reviews,User
from schema import review



router=APIRouter(prefix="/Review",tags=["Review"])


#any user can add a have a review 
@router.post("/review/{post_id}")
def comment_product(product_id:str,content:review,
                    db:Session=(Depends(get_db)),user:User=Depends(get_current_user)):
   
   #check if post exists
   existing_review=db.query(Reviews).filter(Reviews.product_id==product_id).first()

   if existing_review is None:
       raise HTTPException(status_code=404,detail="product not found")
   
   new_comment=Reviews(product_id=product_id,description=review.comment,user_id=user.id)
   db.add(new_comment)
   db.commit()
   db.refresh(new_comment)
   return new_comment

#users can view other comments

@router.get("get_review")
def get_reviews(product_id:str,db:Session = Depends(get_db),user:User=Depends(get_current_user)):
   content=db.query(Reviews).filter(Reviews.product_id == product_id).all()
   return content


#the admin/user  can delete posts
@router.delete("/del_review")
def delete_comment(reviews_id:int,user:User = Depends(require_user_or_admin),
                   db:Session = Depends(get_db)):
   
   del_comment= db.query(Reviews).filter(Reviews.id == reviews_id).first()
                                          
   if del_comment is None:
        raise HTTPException(status_code=404,detail="comment not found")

   if del_comment.user_id != user.id :
      return {"message":"unable to delete"}

   
   db.delete(del_comment)
   db.commit()
   return {"message":"comment deleted"}

