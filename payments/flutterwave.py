import os
import requests
from dotenv import load_dotenv

load_dotenv()
flutterwave_sk = os.environ.get("flutterwave_secret_key")

class FlutterwavePayment:
    def __init__(self, key, email, amount):
        self.key = key
        self.email = email
        self.amount = amount
        self.reference = None
        
    def pay(self):
        url = "https://api.flutterwave.com/v3/payments"
        data = {
            "tx_ref": self.generate_reference(),
            "amount": self.amount,
            "currency": "USD",
            "redirect_url": "https://your-redirect-url.com",
            "payment_type": "card",
            "customer": {
                "email": self.email
            },
            "customizations": {
                "title": "Payment for Data Hive",
                "description": "Data Hive Payment"
            }
        }
        
        headers = {
            "Authorization": "Bearer " + self.key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            self.reference = data['data']['tx_ref']
            auth_link = data['data']['link']
            result = {
                'reference_id': self.reference,
                'auth_url': auth_link
            }
            return result
        return "404"
    
    def generate_reference(self):
        from uuid import uuid4
        return str(uuid4())

class FlutterwaveVerify:
    def __init__(self, reference, secret_key):
        self.reference = reference
        self.secret_key = secret_key

    def status(self):
        url = f"https://api.flutterwave.com/v3/transactions/{self.reference}/verify"
        headers = {
            "Authorization": "Bearer " + self.secret_key
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == "success":
                return "successful"
            else:
                return "failed"
        return "failed"
