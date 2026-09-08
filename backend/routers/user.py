#view an account
#user can update account
#logout
#delete account
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import  get_current_user
from models import User
from schema import update_profile
from services.user_service import profile_view,account_update


router=APIRouter(prefix="/profile",tags=["User"])

#############################
#get user profile
@router.get("/profile")
def accounr_view(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return profile_view(user,db)


###############################33
#update user profile
@router.patch("/profile update")
def accounr_view(user2:update_profile,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return account_update(user2,user,db)


 