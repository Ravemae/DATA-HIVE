import os
import requests
from dotenv import load_dotenv

load_dotenv()
sk = os.environ.get("paystack_secret_key")

class Payment:
    def __init__(self, key, email, amount):
        self.key = key
        self.email = email
        self.amount = amount * 100
        self.reference = None
        
        
    def pay(self):
        url = "https://api.paystack.co/transaction/initialize"
        data = {
            "email": self.email,
            "amount": self.amount 
        }
        
        headers = {
            "Authorization": "Bearer " + self.key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json() 
            self.reference = data['data']['reference']
            auth_link = data['data']['authorization_url']
            result = {
                'reference_id': self.reference,
                'auth_url': auth_link
                }
            return result
        return "404" 
    
    
class Verify:
    def __init__(self, reference, secret_key):
        self.reference = reference
        self.secret_key = secret_key

    def status(self):
        while True:
            if not self.reference:
                return "Reference not found"
            
            url = f"https://api.paystack.co/transaction/verify/{self.reference}"
            headers = {
                "Authorization": "Bearer " + self.secret_key
            }
            
            
            response = requests.get(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                gateway_response = data['data']['gateway_response']
                if gateway_response == "Successful":
                    return "successful"
                elif gateway_response == "The transaction was not completed":
                    continue
                else:
                    return "failed"

        
