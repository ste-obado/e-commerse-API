from database import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import DECIMAL,Numeric,Column,String,Column,ForeignKey,Integer,DateTime,TIMESTAMP,func,Enum,Boolean,Time
from datetime import timezone

#######################
#USER TABLE
class User(Base):
    __tablename__='user'
    id =Column(String(50),primary_key=True,nullable=False,default=lambda:str(uuid.uuid4()))
    Username=Column(String(50),nullable=False)
    Email=Column(String(50),nullable=False,unique=True)
    Role=Column(String(20),nullable=False)
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
    id=Column(Integer,primary_key=True,autoincrement=True)
    Product_id=Column(Integer,ForeignKey("product.id"))
    User_id=Column(String(50),ForeignKey("user.id"))


#######################
#PRODUCTS TABLE
class Product(Base):
    __tablename__='product'
    id = Column(Integer,primary_key=True,autoincrement=True)
    Category_id=Column(Integer,ForeignKey("category.id"))
    P_name=Column(String(50),nullable=False)
    description=Column(String(200),nullable=False)
    price=Column(Numeric(10,2),nullable=False,nullable=0.00)
    stock=Column(Integer,nullable=False,default=0)
    created_at=Column(TIMESTAMP,server_default=func.now())
    updated_at=Column(TIMESTAMP,server_default=func.now(),onupdate=func.now())


#######################
#ORDER TABLE
class Order(Base):
    __tablename__='order'

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("category.id"))
    P_name=Column(String(50),nullable=False)
    Total_amount=Column(Numeric(10,2),nullable=False,default=0.00)
    status=Column(String(200),nullable=False)
    created_at=Column(TIMESTAMP,server_default=func.now())
    
    
#######################
#ORDER ITEMS TABLE
class Order_items(Base):
      __tablename__='order_item'
      id = Column(Integer,primary_key=True,autoincrement=True)
      order_id=Column(Integer,ForeignKey("order.id"))
      product_id=Column(Integer,ForeignKey("product.id"))
      P_name=Column(String(50),nullable=False)
      quantity=Column(Integer,nullable=False)
      price=Column(Numeric(10,2),nullable=False,default=0.00)
     
   
#######################
#REVIEWS TABLE
class Reviews(Base):
    __tablename__='review'
    id = Column(Integer,primary_key=True,autoincrement=True)
    product_id=Column(Integer,ForeignKey("product.id"))
    review=Column(String(200),nullable=False)
    
#######################
#PAYMENTS TABLE
class Payments(Base):
    __tablename__='payment'
    id=Column(String(50),primary_key=True,nullable=True,default=lambda:str(uuid.uuid4()))
    order_id=Column(Integer,ForeignKey("order.id"))
    amount=Column(DECIMAL(10,2),nullable=False,default=0.00)
    method=Column(Enum(P_payments),nullable=False)
    status=Column(String(20),nullable=False)
    paid_at=Column(TIMESTAMP,server_default=func.now())

##########################################
#EUM DROP DOWNS

class C_category(Enum):
     electronics ="electronics"
     cloths = "cloths"
     Food ="food"
     books ="books"

class P_payments(Enum):
     cash=    "cash"
     mpesa = "mpesa"
     card=  "cash"
     bank = "bank"


