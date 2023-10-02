import requests
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
from pprint import pprint

class RESTfulAPI:
    
    def __init__(self, domain_or_ip, api_key, api_secret):
        self.base_uri = f"{domain_or_ip}/api/v2/"
        self.api_key = api_key
        # print(api_key.encode())
        self.api_secret = api_secret
        # Encryption vector initialization
        self.secret_iv = hashlib.sha256(api_key.encode('utf-8')).digest()[:16]
        # print(self.secret_iv)

    def base64url_encode(self, data):
        encoded = base64.urlsafe_b64encode(data)
        return encoded.rstrip(b'=').decode('utf-8')
        
    def api_encrypt_data(self, data):
        key = hashlib.md5(self.api_secret.encode()).hexdigest().encode()
        cipher = AES.new(key, AES.MODE_CBC, self.secret_iv)
        padded_data = pad(data.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return self.base64url_encode(encrypted_data)

    def api_call(self, endpoint, data):
        try:
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            payload = 'data='+ self.api_encrypt_data(data)
            response = requests.post(self.base_uri + endpoint + f"/apikey={self.api_key}", headers=headers, data=payload)
           
            return response.json()
        except Exception as e:
            return {"warning": "", "error": "Generic error"}


