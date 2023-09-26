import requests
import json
import base64
from hashlib import md5, sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from io import StringIO

class APIRestfulClass:
    def __init__(self, base_uri, api_key, api_secret):
        self.base_uri = base_uri
        self.api_key = api_key
        self.api_secret = api_secret
        self.last_error = ""

    def deserialize_json(self, json_txt):
        try:
            ret_val = json.loads(json_txt)
            if "error" in ret_val:
                self.last_error = ret_val["error"]
                print(self.last_error)
                return None
            else:
                return ret_val
        except Exception as ex:
            self.last_error = str(ex)
            return None

    def call_api(self, function_name, json_values):
        try:
            # Encrypt the JSON data
            b64_parameters = self.encrypt(json_values)

            # Fix some values
            b64_parameters = b64_parameters.rstrip('=').replace('+', '-').replace('/', '_')

            # Compose the complete URL request
            print("Data Paramaters : " ,b64_parameters)
            request_full_url = f"{self.base_uri}{function_name}/apikey={self.api_key}/data={b64_parameters}"

            response = requests.get(request_full_url)

            if response.status_code == 200:
                self.last_error = ""
                return self.deserialize_json(response.text)
            else:
                self.last_error = f"HTTP Error {response.status_code}: {response.text}"
                return f"HTTP Error {response.status_code}: {response.text}"
        except Exception as ex:
            self.last_error = str(ex)
            print(self.last_error)
            return self.last_error

    def encrypt(self, plain_text):
        key = self.md5(self.api_secret.encode())
        iv = sha256(self.api_key.encode()).digest()[:16]

        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Pad the plain text to a multiple of 16 bytes
        plain_text = pad(plain_text.encode(), AES.block_size)

        encrypted = cipher.encrypt(plain_text)

        # Convert the encrypted bytes to base64
        return base64.urlsafe_b64encode(encrypted).decode()

    @staticmethod
    def sha256(input_str):
        return sha256(input_str.encode()).digest()

    @staticmethod
    def md5(input_str):
        return md5(input_str).digest()


# Example usage
base_uri = "https://www.hotspot.yourspot.co.za/api/v2/"
api_key = "5YSNV3TQ7Q91SYNQT9Q69R5P8P7H6T72"
api_secret = "DP9WGS6B361JT9W89648NYML8JQ4YMW1"
api = APIRestfulClass(base_uri, api_key, api_secret)
function_name = "resellerRead"
json_values = '{"id": "207"}' 
response = api.call_api(function_name, json_values)
print(response)
