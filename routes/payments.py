import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from auth import get_current_active_user
from database import get_session
from payments.pay import PaymentProcessor, VerificationProcessor
from models import User
from dotenv import load_dotenv

load_dotenv()

paystack_sk = os.getenv("PAYSTACK_SECRET_KEY")
flutterwave_sk = os.getenv("FLUTTERWAVE_SECRET_KEY")

payments_router = APIRouter()

@payments_router.post("/paystack/pay")
async def paystack_pay(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    payment_processor = PaymentProcessor(provider="paystack", key=paystack_sk, email=email, amount=amount)
    result = payment_processor.pay()
    if result == "404":
        raise HTTPException(status_code=400, detail="Payment initialization failed")
    return result

@payments_router.get("/paystack/verify/{reference}")
async def paystack_verify(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    verification_processor = VerificationProcessor(provider="paystack", reference=reference, secret_key=paystack_sk)
    status = verification_processor.verify()
    return {"status": status}

@payments_router.post("/flutterwave/pay")
async def flutterwave_pay(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    payment_processor = PaymentProcessor(provider="flutterwave", key=flutterwave_sk, email=email, amount=amount)
    result = payment_processor.pay()
    if result == "404":
        raise HTTPException(status_code=400, detail="Payment initialization failed")
    return result

@payments_router.get("/flutterwave/verify/{reference}")
async def flutterwave_verify(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    verification_processor = VerificationProcessor(provider="flutterwave", reference=reference, secret_key=flutterwave_sk)
    status = verification_processor.verify()
    return {"status": status}
