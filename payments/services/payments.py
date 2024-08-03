from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from payments.flutterwave import process_flutterwave_payment
from payments.paystack import process_paystack_payment
from database import get_session
from auth import get_current_active_client
from pydantic import BaseModel
from models import User


# Define payment request models
class PaymentRequest(BaseModel):
    payment_method: str
    subscription_type: str
    token: str  # Payment token from the frontend

def process_payment(payment_request: PaymentRequest, session: Session = Depends(get_session)):
    user = get_current_active_client(session)
    
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized")

    # Determine currency and amount
    currency = "USD"  # Replace with actual logic to determine currency, if applicable
    amount = get_subscription_amount(payment_request.subscription_type, currency)
    
    # Process payment
    if payment_request.payment_method == "flutterwave":
        response = process_flutterwave_payment(payment_request.token, payment_request.subscription_type, amount)
    elif payment_request.payment_method == "paystack":
        response = process_paystack_payment(payment_request.token, payment_request.subscription_type, amount)
    else:
        raise HTTPException(status_code=400, detail="Unsupported payment method")
    
    if response.get("status") == "success":
        update_subscription(user, payment_request.subscription_type, session)
        return {"message": "Payment successful"}
    else:
        raise HTTPException(status_code=400, detail="Payment failed")

def get_subscription_amount(subscription_type: str, currency: str):
    if currency == "USD":
        amounts = {"Pro": 15.55, "Premium": 29.99}
    elif currency == "NGN":
        amounts = {"Pro": 25000, "Premium": 50000}
    else:
        raise HTTPException(status_code=400, detail="Unsupported currency")

    return amounts.get(subscription_type, 0)

def update_subscription(user: User, subscription_type: str, session: Session):
    user.subscription_type = subscription_type
    user.subscription_status = "Active"
    session.add(user)
    session.commit()
