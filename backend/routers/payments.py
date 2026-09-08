#POST /payments/stk-push
#POST /payments/callback
#GET  /payments/{payment_id}


from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from core.protection  import require_user_or_admin
from models import User
from schema import payment
from services.payments_service import stk_push
#import httpx

from utils.Authcheck import check_ownership


router=APIRouter(prefix="/payments",tags=["Payment"])

@router.post("/stk-push")
def stk_push(Credential: payment,
    user: User = Depends(require_user_or_admin),
    db: Session = Depends(get_db)
):

 return stk_push(Credential,user,db)