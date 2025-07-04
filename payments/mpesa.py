import base64
import requests
from datetime import datetime
from decouple import config

class Mpesa:
    def __init__(self):
        self.consumer_key = config('MPESA_CONSUMER_KEY')
        self.consumer_secret = config('MPESA_CONSUMER_SECRET')
        self.shortcode = config('MPESA_SHORTCODE')
        self.passkey = config('MPESA_PASSKEY')
        self.token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        self.stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    def get_access_token(self):
        response = requests.get(self.token_url, auth=(self.consumer_key, self.consumer_secret))
        return response.json()['access_token']

    def initiate_stk_push(self, phone, amount):
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((self.shortcode + self.passkey + timestamp).encode()).decode()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": self.shortcode,
            "PhoneNumber": phone,
            "CallBackURL": config('MPESA_CALLBACK_URL'),
            "AccountReference": "Cakehouse",
            "TransactionDesc": "Cakehouse Order Payment"
        }

        response = requests.post(self.stk_url, json=payload, headers=headers)
        return response.json()
