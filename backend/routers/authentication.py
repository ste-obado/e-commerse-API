#regiter and log in
from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import  require_user
from models import User
from schema import register
from  services.auth_service import user_register,user_login



router=APIRouter(prefix="/Register",tags=["Auth"])

####################33333333333333
#register new user
@router.post("/Sign up")
def user_register (newuser:register,db:Session=Depends(get_db)):
    return user_register(newuser,db)

############################
#login user
@router.post("/login")
def user_login(login:OAuth2PasswordRequestForm=Depends(),
               db:Session=Depends(get_db),user:User=Depends(require_user)):
   return user_login(login,db)
     

