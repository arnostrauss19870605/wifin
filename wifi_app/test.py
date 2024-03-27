
import requests, datetime,requests
from django.shortcuts import  render, redirect, HttpResponse
from datetime import datetime,date
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import json
import requests
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
from pprint import pprint
from django.db.models import Q
from datetime import timedelta

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


def pull_from_captive_portal(): 

          api_key = '38XG46Q3NPM63THRMB9984YJ7V6MY5QQ'
          api_secret = '47TY45RDHY77DDNNDNNBD7J8RDL97WQ1'
          domain_api_url = 'http://www.hotspot.yourspot.co.za/'
          domain_api_endpoint = 'wpsurveyanswersRead'
          #domain_api_endpoint = 'userRead'

       
          survey_id = 1213
          user_id = '00211610497594'
          domain_id = 203
          creation_date = '2024-01-01'
          api = RESTfulAPI(domain_api_url, api_key, api_secret)

          # Given string
          #data_str = f'{{"Where":"wpsurvey.id={domain_id} AND user.CreationDate >= \\"{domain_api_lastdate}\\""}}'
         
          #data_str = f'{{"Where":"wpsurvey.id={domain_id}"}}'
          #data_str = f'{{"Where":"wpsurvey.id={survey_id} AND user.id={user_id}"}}'
          data_str = f'{{"Where":"wpsurvey.id={survey_id} AND user.username={user_id}"}}'

          #Get Survey Result
          #data_str = f'{{"Where":"wpsurvey.id={survey_id} AND domain.id={domain_id} AND user.CreationDate >= \\"{creation_date}\\""}}'

          #Get Result Based on User ID
          #data_str = f'{{"Where":"wpsurvey.id={survey_id} AND wpsurveyanswer.CreationDate >= \\"{creation_date}\\""}}'
          #data_str = f'{{"Where":"wpsurvey.id={survey_id} AND wpsurveyanswer.CreationDate >= \\"{creation_date}\\""}}'

          #Fet User Detail  
          #data_str = f'{{"id":"{user_id}"}}'  

          # Parse the string as a Python dictionary
          data_dict = json.loads(data_str)

          # Serialize the dictionary as a JSON string
          json_data = json.dumps(data_dict)

          endpoint = domain_api_endpoint
          data = json_data

          json_ret_val = api.api_call(endpoint, data)
            
          if "error" in json_ret_val and json_ret_val["error"] != "":
            print("Error:", json_ret_val["error"])
          else:
            pprint(json_ret_val)

pull_from_captive_portal()