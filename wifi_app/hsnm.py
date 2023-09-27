import requests
import json
import base64
import hashlib
from hashlib import md5, sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from io import StringIO
from django.http import JsonResponse

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding as asym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

class RESTfulAPI:
    def __init__(self, domain_or_ip, key, secret):
        self.base_uri = domain_or_ip
        self.api_key = key
        self.api_secret = secret
        self.last_error = ""

    def deserialize_json(self, json_txt):
        try:
            if json_txt is not None:
                response = json.loads(json_txt)
                if "error" in response:
                    self.last_error = response["error"]
                    return None
                else:
                    return response
            else:
                self.last_error = "JSON response is None"
            return None
        except Exception as ex:
            self.last_error = str(ex)
            return None
        
    def api_call(self, function_name, json_values):
        try:
            print("my intial data : ",json_values)
            encrypted_data = self.encrypt(json_values)
            print("data after encryption: ",encrypted_data)
            b64_parameters = base64.urlsafe_b64encode(encrypted_data).rstrip(b'=')
            print("data after encoding: ",b64_parameters)
            print("data after Dencoding: ",b64_parameters.decode('utf-8'))

            request_full_url = f"{self.base_uri}{function_name}/apikey={self.api_key}/data={b64_parameters.decode('utf-8')}"
            response = requests.get(request_full_url)
            if response.status_code == 200:
                return self.deserialize_json(response.text)
            else:
                self.last_error = f"API request failed with status code {response.status_code}"
                return None
        except Exception as ex:
            self.last_error = str(ex)
            return None
        
    def encrypt(self, plain_text):
        key = hashlib.md5(self.api_secret.encode('utf-8')).digest()
        iv = hashlib.sha256(self.api_key.encode('utf-8')).digest()[:16]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_text = plain_text + (AES.block_size - len(plain_text) % AES.block_size) * chr(AES.block_size - len(plain_text) % AES.block_size)
        encrypted_text = cipher.encrypt(padded_text.encode('utf-8'))
        return encrypted_text

    
   
    





