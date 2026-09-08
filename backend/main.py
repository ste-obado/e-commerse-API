from database import Base,engine
import models
#from models import 
from routers import authentication,users,reviews,products,payments,orders,categories,cart
from fastapi import FastAPI


app=FastAPI()

#CREATE TABLES 
models.Base.metadata.create_all(bind=engine)

#include each router 
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(products.router)
app.include_router(payments.router)
app.include_router(orders.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(authentication.router)
