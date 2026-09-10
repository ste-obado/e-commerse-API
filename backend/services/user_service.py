from fastapi import HTTPException
from models import User
from redis_cache import redis_client
import json

#############################
#get user profile
def profile_view(user,db):
    #cache check
    cache_key=f"user:{user.email}"
    cached=redis_client.get(cache_key)
    if cached:
        return{"profile":json.loads(cached)}
    
    #cache miss
    View=db.query(User).filter(User.id==user.id).first()
    if not View :
       raise   HTTPException(status=404,detail="'USER NOT FOUND")
    
    profile=[{"Username":View.Username,
             "Email":View.Email,
             "Role":View.Role,
             "created_at":View.created_at}]
    #write on redis
    redis_client.set(cache_key,json.dumps(profile),ex=3600)
    return{"profile":profile}

###############################33
#update user profile

def account_update(user2,user,db):
    user_data=db.query(User).filter(User.id==user.id).first()
    if not user:
        raise  HTTPException(status=404,detail="'USER NOT FOUND")

    updated_data=user2.model_dump(exclude_unset=True)
    if "email" in updated_data:
         email_existance=db.query(User).filter(User.Email==updated_data["email"]).first()
         if email_existance :
              HTTPException(status=409,details="Email exists retry")
    for field,value in updated_data.items():
        setattr(user_data,field,value)

    db.commit()
    db.refresh(user_data)
    if updated_data:
        redis_client.hset(f"user:{user.id}",mapping=updated_data)
    return{
         "message": "Profile updated",
         "name":user_data.name,
         "Email":user_data.email
    }

