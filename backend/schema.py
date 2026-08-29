from pydantic import BaseModel,EmailStr,field_validator,model_validator
from  typing import Optional
from datetime import time 
from enum import Enum

#LOGIN SCHEMA
class UserRole (str,Enum):
    admin = "admin"
    user = "user"


class register(BaseModel):
    name:str
    email:EmailStr
    role:UserRole.user
    password:str
    confirm_password:str

    @field_validator("password")
    def validate_password(cls,password):
        if len(password)<8:
            raise ValueError("Password must be at least 8 characters long")
        return password

    
    @field_validator("email")
    def check_company_email(cls, value):
        if value.endswith("@mycompany.com"):
            raise ValueError("Input valid email")
        return value
    
    @model_validator(mode="after")
    def password_verify(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class Userlogin(BaseModel):
     name:str
     email:str
     password:str

     @field_validator("email")
     def check_company_email(cls, value):
             if value.endswith("@mycompany.com"):
                 raise ValueError("Input valid email")
             return value

    



class update_profile(BaseModel):
     name: Optional[str] = None
     email:Optional[EmailStr] = None
     

     @field_validator("email")
     def check_company_email(cls, value):
           if value.endswith("@mycompany.com"):
               raise ValueError("Input valid email")
           return value
     
class review(BaseModel):
     comment:str
     stars:int

     

     class Config:
              from_attributes = True 
