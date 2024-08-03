import requests
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_transaction(amount: float, email: str, callback_url: str):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "amount": int(amount * 100),  # Paystack requires amount in kobo
        "email": email,
        "callback_url": callback_url
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def verify_paystack_transaction(reference: str, secret_key: str) -> dict:
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
