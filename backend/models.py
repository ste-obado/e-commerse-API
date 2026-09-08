from database import Base
from sqlalchemy.orm import relationship
import uuid
from enum import Enum
from sqlalchemy import DECIMAL,Numeric,Column,String,Column,ForeignKey,Integer,DateTime,TIMESTAMP,func,Enum as SAEnum,Boolean,Time
from datetime import timezone


class C_category(Enum):
    electronics = "electronics"
    cloths = "cloths"
    Food = "food"
    books = "books"


class P_payments(Enum):
    cash = "cash"
    mpesa = "mpesa"
    card = "cash"
    bank = "bank"

class P_status(Enum):
    pending = "pending"
    Success = "success"
    failed = "failed"

class Status(Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
#######################
#USER TABLE
class User(Base):
    __tablename__='user'
    id =Column(String(50),primary_key=True,nullable=False,default=lambda:str(uuid.uuid4()))
    Username=Column(String(50),nullable=False)
    Email=Column(String(50),nullable=False,unique=True)
    Role=Column(String(20),nullable=False)
    password=Column(String(30),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    IsActive=Column(Boolean,default=True)
   
#######################
#CATEGORY TABLE
class Category(Base):
    __tablename__='category'
    id=Column(Integer,primary_key=True,autoincrement=True)
    C_name=Column(Enum(C_category),nullable=False)


#######################
#CART TABLE
class Cart(Base):
    __tablename__='cart'
    Cart_id=Column(Integer,primary_key=True,autoincrement=True)
    User_id=Column(String(50),ForeignKey("user.id"))
    created_at=Column(DateTime(timezone=True),server_default=func.now())


class Cart_items(Base):
   __tablename__='cart items'
   Cart_items_id=Column(Integer,primary_key=True,autoincrement=True)
   Cart_id=Column(Integer,ForeignKey("cart.id"))
   Product_id=Column(Integer,ForeignKey("products.id"))
   Quantity=Column(Integer,autoincrement=True,default=0)
  
       

#######################
#PRODUCTS TABLE
class Product(Base):
    __tablename__='products'
    id = Column(Integer,primary_key=True,autoincrement=True)
    Category_id=Column(Integer,ForeignKey("category.id"))
    P_name=Column(String(50),nullable=False)
    #image=Column(HttpUrl)
    description=Column(String(200),nullable=False)
    price=Column(Numeric(10,2),nullable=False,nullable=0.00)
    stock=Column(Integer,nullable=False,default=0)
    created_at=Column(TIMESTAMP,server_default=func.now())
    updated_at=Column(TIMESTAMP,server_default=func.now(),onupdate=func.now())


#######################
#ORDER TABLE
class Order(Base):
    __tablename__='orders'

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("category.id"))
    Total_amount=Column(Numeric(10,2),nullable=False,default=0.00)
    status=Column(Enum(Status),nullable=False)
    Isactive=Column(Boolean,default=True)
    created_at=Column(TIMESTAMP,server_default=func.now())
    cancelled_at=Column(TIMESTAMP,onupdate=func.now())
    
    
#######################
#ORDER ITEMS TABLE
class Order_items(Base):
      __tablename__='order_items'
      id = Column(Integer,primary_key=True,autoincrement=True)
      order_id=Column(Integer,ForeignKey("order.id"))
      product_id=Column(Integer,ForeignKey("product.id"))
      quantity=Column(Integer,nullable=False)
      price=Column(Numeric(10,2),nullable=False,default=0.00)
     
   
#######################
#REVIEWS TABLE
class Reviews(Base):
    __tablename__='reviews'
    id = Column(Integer,primary_key=True,autoincrement=True)
    product_id=Column(Integer,ForeignKey("product.id"))
    user_id=Column(Integer,ForeignKey("user.id"))
    review=Column(String(200),nullable=False)
    
#######################
#PAYMENTS TABLE
class Payments(Base):
    __tablename__='payment'
    id=Column(String(50),primary_key=True,nullable=False,default=lambda:str(uuid.uuid4()))
    order_id=Column(Integer,ForeignKey("order.id"),nullable=False)
    phone_number = Column(String(20), nullable=False)
    amount=Column(DECIMAL(10,2),nullable=False,default=0.00)
    method=Column(Enum(P_payments),nullable=False)
    status=Column(Enum(P_status),nullable=False)
    checkout_request_id = Column(String(100), nullable=True)
    merchant_request_id = Column(String(100), nullable=True)
    mpesa_receipt_number = Column(String(100), nullable=True)
    paid_at=Column(TIMESTAMP,server_default=func.now())




