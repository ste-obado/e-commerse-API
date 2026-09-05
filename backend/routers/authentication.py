#regiter and log in
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import  require_user
from models import User
from schema import register,Userlogin
from core.security import verify_password,hash_password,create_access_token



router=APIRouter(prefix="/Register",tags=["Auth"])

####################33333333333333
#register new user

@router.post("/Sign_up")
def user_register (newuser:register,db:Session=Depends(get_db)):
    user_verify=db.query(User).filter(User.Email==newuser.email).first()

    if user_verify:
        raise HTTPException(status=404,detail="USER EXISTS")
    password=hash_password(newuser.password)

    db_user=User(User.Username==newuser.name,User.Email==newuser.email,
                 User.Role==newuser.role,User.password==password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return{
        'MESSAGE':"account created succesfully"
     }

############################
#login user

@router.post("/login")
def user_login(user_login:OAuth2PasswordRequestForm=Depends(),
               db:Session=Depends(get_db),user:User=Depends(require_user)):
     
     user_verify=db.query(User).filter(User.Email==user_login.email).first()

     if user_verify or verify_password(user_login.password,user_verify.password) is None:
             raise HTTPException(status=404,detail="Invalid credential")
     
     token=create_access_token(data={"sub":user_verify.id,
                                   "role":user_verify.role})
     return{
          "token":token,
          "token type":"bearer"
     }
     

