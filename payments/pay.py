from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from flutterwave import make_payment, verify_flutterwave_transaction
from paystack import initialize_transaction, verify_paystack_transaction
from database import get_session
from auth import get_current_active_client
from pydantic import BaseModel
import os

# Define payment request models
class PaymentRequest(BaseModel):
    payment_method: str
    subscription_type: str
    token: str  # Payment token from the frontend

def get_payment_key(payment_method: str) -> str:
    if payment_method == "paystack":
        return os.getenv("PAYSTACK_SECRET_KEY")
    elif payment_method == "flutterwave":
        return os.getenv("FLUTTERWAVE_SECRET_KEY")
    else:
        raise HTTPException(status_code=400, detail="Unsupported payment method")

def get_subscription_amount(subscription_type: str, currency: str) -> float:
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

class PaymentProcessor:
    def __init__(self, provider: str, key: str, email: str, amount: float):
        self.provider = provider
        self.key = key
        self.email = email
        self.amount = amount

    def pay(self) -> dict:
        if self.provider == "paystack":
            response = initialize_transaction(amount=self.amount, email=self.email, callback_url="your_callback_url")
        elif self.provider == "flutterwave":
            response = make_payment(amount=self.amount, email=self.email, tx_ref="unique_tx_ref")
        else:
            raise ValueError("Unsupported payment provider")
        
        if response.get("status") != "success":
            raise HTTPException(status_code=400, detail="Payment initialization failed")
        
        return response

class VerificationProcessor:
    def __init__(self, provider: str, reference: str, secret_key: str):
        self.provider = provider
        self.reference = reference
        self.secret_key = secret_key

    def verify(self) -> dict:
        if self.provider == "paystack":
            response = verify_paystack_transaction(reference=self.reference, secret_key=self.secret_key)
            pass  # Replace with actual implementation
        elif self.provider == "flutterwave":
            response = verify_flutterwave_transaction(reference=self.reference, secret_key=self.secret_key)
            pass  # Replace with actual implementation
        else:
            raise ValueError("Unsupported payment provider")

        # Return verification status
        return {"status": "pending"}  # Replace with actual status from response

def process_payment(payment_request: PaymentRequest, session: Session):
    user = get_current_active_client(session)
    
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized")

    payment_processor = PaymentProcessor(
        provider=payment_request.payment_method,
        key=get_payment_key(payment_request.payment_method),
        email=user.email,
        amount=get_subscription_amount(payment_request.subscription_type, "USD")  # Replace with actual currency
    )
    response = payment_processor.pay()
    
    if response.get("status") == "success":
        update_subscription(user, payment_request.subscription_type, session)
        return {"message": "Payment successful"}
    else:
        raise HTTPException(status_code=400, detail="Payment failed")
    
get_session()