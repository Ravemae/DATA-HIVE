import httpx

class PaystackClient:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.base_url = "https://api.paystack.co"

    def verify_transaction(self, reference):
        url = f"{self.base_url}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.secret_key}"
        }
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def initialize_transaction(self, email, amount):
        url = f"{self.base_url}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": int(amount * 100)
        }
        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
