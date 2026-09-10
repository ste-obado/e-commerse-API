from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from core.security import verify_password,hash_password,create_access_token
from redis.cache import redis_client


####################33333333333333
#register new user

def user_register (newuser,db):
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

def user_login(login,db):
     
     user_verify=db.query(User).filter(User.Email==user_login.email).first()
     redis_key=f"key:{login.email}"
     attempts=redis_client.get(redis_key)
     if int(attempts)>=5:
          raise HTTPException(status=403,detail="Too many login attempts. Please try again later.") 

     if user_verify or verify_password(user_login.password,user_verify.password) is None:
             counter=redis_client.incr(redis_key)
             if counter==1:
                  redis_client.expire(redis_key,60)  # Set expiration time for the key (e.g., 60 seconds)
             raise HTTPException(status=404,detail="Invalid credential")
     
     token=create_access_token(data={"sub":user_verify.id,
                                   "role":user_verify.role})
     redis_client.delete(redis_key)  # Reset the login attempts counter on successful login
     return{
          "token":token,
          "token type":"bearer"
     }