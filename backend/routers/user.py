#view an account
#user can update account
#logout
#delete account
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import  get_current_user
from models import User
from schema import update_profile


router=APIRouter(prefix="/profile",tags=["User"])

@router.get("/profile")
def accounr_view(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    View=db.query(User).filter(User.id==user.id).first()
    if not View :
       raise   HTTPException(status=404,detail="'USER NOT FOUND")
    return{"Username" : View.Username,
           "Email":View.Email,
           "Role":View.Role,
           "created_at":View.created_at
         
    }

@router.patch("/profile/update")
def accounr_view(user2:update_profile,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    user_data=db.query(User).filter(User.id==user.id).first()
    if not user:
        raise  HTTPException(status=404,detail="'USER NOT FOUND")

    updated_data=user2.model_dump(exclude=True)
    if "email" in updated_data:
         email_existance=db.query(User).filter(User.Email==updated_data["email"]).first()
         if email_existance :
              HTTPException(status=409,details="Email exists retry")
    for field,value in updated_data.items():
        setattr(user_data,field,value)

    db.commit()
    db.refresh(user_data)
    return{
         "message": "Profile updated",
         "name":user_data.name,
         "Email":user_data.email
    }


 