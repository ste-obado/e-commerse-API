#regiter and log in
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import c
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import  get_current_user
from models import User
from schema import register


router=APIRouter(prefix="/Register",tags=["Auth"])

@router.post("/Sighn_up")
