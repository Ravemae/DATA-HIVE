import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from auth import get_current_active_user
from database import get_session
from payments.pay import PaymentProcessor, VerificationProcessor
from models import User
from dotenv import load_dotenv

load_dotenv()

# Ensure environment variables are set
paystack_sk = os.getenv("PAYSTACK_SECRET_KEY")
flutterwave_sk = os.getenv("FLUTTERWAVE_SECRET_KEY")

if not paystack_sk or not flutterwave_sk:
    raise ValueError("Missing environment variables for secret keys.")

payments_router = APIRouter()

@payments_router.post("/paystack/pay")
async def paystack_pay(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        payment_processor = PaymentProcessor(provider="paystack", key=paystack_sk, email=email, amount=amount)
        result = payment_processor.pay()
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail="Payment initialization failed")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@payments_router.get("/paystack/verify/{reference}")
async def paystack_verify(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        verification_processor = VerificationProcessor(provider="paystack", reference=reference, secret_key=paystack_sk)
        status = verification_processor.verify()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@payments_router.post("/flutterwave/pay")
async def flutterwave_pay(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        payment_processor = PaymentProcessor(provider="flutterwave", key=flutterwave_sk, email=email, amount=amount)
        result = payment_processor.pay()
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail="Payment initialization failed")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@payments_router.get("/flutterwave/verify/{reference}")
async def flutterwave_verify(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        verification_processor = VerificationProcessor(provider="flutterwave", reference=reference, secret_key=flutterwave_sk)
        status = verification_processor.verify()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
