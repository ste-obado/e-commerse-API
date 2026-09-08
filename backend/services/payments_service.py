from fastapi import HTTPException
from models import Order,Payments
from schema import Status
#import httpx

from utils.Authcheck import check_ownership

def stk_push(Credential,user,db):

# 1. Find order
    order = db.query(Order).filter(Order.user_id == user.id).first()

    # 2. Check order
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 3. Check status
    if order.status != Status.pending:
        raise HTTPException(status_code=400, detail="Order is not pending")
    
    # 4. Create payment record
    payment = Payments(
        order_id=order.id,
        phone_number=Credential.phone_number,
        amount=order.Total_amount,
        status=Status.pending
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # 5. Get M-PESA access token
    # 6. Send STK Push request
    # 7. Save M-PESA identifiers
    # 8. Return response

    return payment
