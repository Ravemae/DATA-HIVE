import requests
import os
from dotenv import load_dotenv

load_dotenv()

def make_payment(amount: float, email: str, tx_ref: str):
    url = "https://api.flutterwave.com/v3/charges?type=mobilemoneyghana"
    headers = {
        "Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "tx_ref": tx_ref,
        "amount": amount,
        "email": email,
        "currency": "USD",
        "phone_number": "your_phone_number_here"  # Update as needed
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def verify_flutterwave_transaction(tx_ref: str) -> dict:
    url = f"https://api.flutterwave.com/v3/charges/verify?tx_ref={tx_ref}"
    headers = {
        "Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY')}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
