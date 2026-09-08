from fastapi import HTTPException
from models import User

#############################
#get user profile
def profile_view(user,db):
    View=db.query(User).filter(User.id==user.id).first()
    if not View :
       raise   HTTPException(status=404,detail="'USER NOT FOUND")
    return{"Username" : View.Username,
           "Email":View.Email,
           "Role":View.Role,
           "created_at":View.created_at}

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
    return{
         "message": "Profile updated",
         "name":user_data.name,
         "Email":user_data.email
    }

