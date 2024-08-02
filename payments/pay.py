import os 
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .paystack import PaystackClient
from auth import get_current_active_user
from database import get_session
from models import User

load_dotenv()
sk = os.environ.get("paystack_secret_key")
pay_routes = APIRouter()

pay_routes = APIRouter()

PAYSTACK_SECRET_KEY = "your_paystack_secret_key"
paystack_client = PaystackClient(PAYSTACK_SECRET_KEY)

@pay_routes.post("/initialize_payment")
async def initialize_payment(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    response = paystack_client.initialize_transaction(email, amount)
    if not response['status']:
        raise HTTPException(status_code=400, detail="Payment initialization failed")
    
    return {"payment_url": response['data']['authorization_url'], "reference": response['data']['reference']}

@pay_routes.get("/verify_payment/{reference}")
async def verify_payment(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    response = paystack_client.verify_transaction(reference)
    if not response['status']:
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    if response['data']['status'] == "success":
        user.subscription_status = "Active"
        session.commit()
        return {"message": "Payment verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Payment not successful")
