from pydantic import BaseModel,EmailStr,field_validator,model_validator
from  typing import Optional
from datetime import time 
from enum import Enum

###############################
#USEROLE AND ORDER STATUS ENUMS

class UserRole (str,Enum):
    admin = "admin"
    user = "user"

class Status(str,Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

###############################
#LOGIN SCHEMAS

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

    


###############################
#PROFILE SCHEMAS

class update_profile(BaseModel):
     name: Optional[str] = None
     email:Optional[EmailStr] = None
     

     @field_validator("email")
     def check_company_email(cls, value):
           if value.endswith("@mycompany.com"):
               raise ValueError("Input valid email")
           return value

###############################
#REVIEW SCHEMAS
    
class review(BaseModel):
     comment:str
     stars:int

###############################
#CART SCHEMAS
class add_cart(BaseModel):
     product_id:int
     quantity:int

class Update_cart(BaseModel):
     quantity:Optional[int]=None

###############################
#CARTEGORY SCHEMAS
class add_Category(BaseModel):
     C_name:str

class Update_category(BaseModel):
     C_name:Optional[str]=None


###############################
#PRODUCTS SCHEMAS
class add_product(BaseModel):
        cartegory_id:int
        P_name:str
        price:float
        description:str
        stock:int

class Update_product(BaseModel):
        cartegory_id:Optional[int]= None
        P_name:str | None =None
        price:float | None =None
        description:str | None = None
        stock:int | None =None

class Get_products(BaseModel):
        category_id: int | None = None
        search: str | None = None
        min_price: float | None = None
        max_price: float | None = None
        sort: str | None = None

###############################
#PAYMENTS SCHEMAS
class payment(BaseModel):
        phone_number:str 
               
        class Config:
              from_attributes = True 
