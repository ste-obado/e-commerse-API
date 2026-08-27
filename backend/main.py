from database import Base,engine
import models
#from models import 
#from routers import
from fastapi import FastAPI


app=FastAPI()

#CREATE TABLES 
models.Base.metadata.create_all(bind=engine)

#include each router 
#app.include_router(users.router)
#app.include_router(timetable.router)
#app.include_router(rooms.router)
#app.include_router(courses.router)
#app.include_router(authentication.router)
