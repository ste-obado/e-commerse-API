from fastapi import HTTPException
from models import Reviews
from schema import review,UserRole

################################
#any user can add a have a review 
def comment_product(product_id,content, db,user):
   
   #check if post exists
   existing_review=db.query(Reviews).filter(Reviews.product_id==product_id).first()

   if existing_review is None:
       raise HTTPException(status_code=404,detail="product not found")
   
   new_comment=Reviews(product_id=product_id,description=review.comment,user_id=user.id)
   db.add(new_comment)
   db.commit()
   db.refresh(new_comment)
   return new_comment

###############################
#users can view other comments

def get_reviews(product_id,db,user):
   content=db.query(Reviews).filter(Reviews.product_id == product_id).all()
   return content

###############################
#the admin/user  can delete posts


def delete_comment(reviews_id,user,db):
   
   del_comment= db.query(Reviews).filter(Reviews.id == reviews_id).first()
                                          
   if del_comment is None:
        raise HTTPException(status_code=404,detail="comment not found")

  
   if del_comment.user_id != user.id and user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this review"
        )

   
   db.delete(del_comment)
   db.commit()
   return {"message":"comment deleted"}

