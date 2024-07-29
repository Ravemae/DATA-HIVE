from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from auth import get_current_active_user
from database import get_session
from payments.paystack import Payment as PaystackPayment, Verify as PaystackVerify
from payments.flutterwave import FlutterwavePayment, FlutterwaveVerify
from modelss import User

payments_route = APIRouter()

@payments_route.post("/paystack/pay")
async def paystack_pay(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    payment = PaystackPayment(key=sk, email=email, amount=amount)
    result = payment.pay()
    if result == "404":
        raise HTTPException(status_code=400, detail="Payment initialization failed")
    return result

@payments_route.get("/paystack/verify/{reference}")
async def paystack_verify(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    verify = PaystackVerify(reference=reference, secret_key=sk)
    status = verify.status()
    return {"status": status}

@payments_route.post("/flutterwave/pay")
async def flutterwave_pay(
    email: str,
    amount: float,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    payment = FlutterwavePayment(key=flutterwave_sk, email=email, amount=amount)
    result = payment.pay()
    if result == "404":
        raise HTTPException(status_code=400, detail="Payment initialization failed")
    return result

@payments_route.get("/flutterwave/verify/{reference}")
async def flutterwave_verify(
    reference: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    verify = FlutterwaveVerify(reference=reference, secret_key=flutterwave_sk)
    status = verify.status()
    return {"status": status}
