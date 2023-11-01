
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
from .models import Consolidated_Core_Quiz,Core_Quiz,Upload_Interval
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
          domain_api_endpoint = 'wpsurveyFind'
          #domain_api_endpoint = 'wpsurveyRead'

       
          domain_id = 2185
          domain_api_lastdate = '2023-01-01'
          api = RESTfulAPI(domain_api_url, api_key, api_secret)

          # Given string
          #data_str = f'{{"Where":"domain.id={domain_id} AND user.CreationDate >= \\"{domain_api_lastdate}\\""}}'
         
          data_str = f'{{"Where":"wpsurvey.id={domain_id}"}}'

          #data_str = f'{{"id":"{domain_id}"}}'
            

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

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def consolidate_quiz_results(id):
    result_1 = Core_Quiz.objects.filter(
        q_1__isnull=False,
        hsUsersID=id
    ).exclude(q_1='').first()

    result_2 = Core_Quiz.objects.filter(
        q_2__isnull=False,
        hsUsersID=id
    ).exclude(q_2='').first()

    result_3 = Core_Quiz.objects.filter(
        q_3__isnull=False,
        hsUsersID=id
    ).exclude(q_3='').first()

    result_4 = Core_Quiz.objects.filter(
        q_4__isnull=False,
        hsUsersID=id
    ).exclude(q_4='').first()

    
    contact_number = result_1.mobile_phone
    
    if result_4:  # Checks if result_4 is not None
        contact_number = "0" + result_4.q_4[1:] 
    else:
        contact_number = "0" + result_1.mobile_phone[4:] 

    contact_number = contact_number[:10]

    
    if not result_1.first_name:  # checks if it's empty or None
        # Handle the case when first_name is empty or None
        ys_first_name = "No data"
    else:
        ys_first_name = result_1.first_name 

    if not result_1.last_name:  # checks if it's empty or None
        # Handle the case when first_name is empty or None
        ys_last_name_name = "No data"
    else:
        ys_last_name_name = result_1.last_name

    if not result_1.email:  # checks if it's empty or None
        # Handle the case when first_name is empty or None
        if not result_1.username :
             ys_email = 'nomail@ys.co.za'
        else :            
            ys_email= result_1.username + '.co.za'
    else:
        ys_email = result_1.email                          


    consolidate_table = Consolidated_Core_Quiz(

    reseller_name = result_1.reseller_name,
    manager_name = result_1.manager_name,
    domain_name = result_1.domain_name,
    insertion_date = result_1.insertion_date,
    question_type = result_1.question_type,
    surveyID = result_1.surveyID,
    hsUsersID = result_1.hsUsersID,
    username = result_1.username,
    first_name = ys_first_name,
    last_name = ys_last_name_name,
    company_name = result_1.company_name,
    city = result_1.city,
    address = result_1.address,
    zip = result_1.zip,
    state = result_1.state,
    country = result_1.country,
    gender = result_1.gender,
    year_of_birth = result_1.year_of_birth,
    month_of_birth = result_1.month_of_birth, 
    day_of_birth = result_1.day_of_birth,
    room_or_site = result_1.room_or_site,
    hs_product_id = result_1.hs_product_id,
    email = ys_email,
    phone = result_1.phone,
    mobile_phone = result_1.mobile_phone,
    conditions_accepted = result_1.conditions_accepted,
    privacy_policyAccepted = result_1.privacy_policyAccepted,
    marketing_accepted = result_1.marketing_accepted,
    newsletters_accepted = result_1.newsletters_accepted,
    q_1 =  result_1.q_1,
    q_2 =  result_2.q_2,
    q_3 =  result_3.q_3,
    q_4 =  contact_number,
    score =  safe_int(result_1.score) + safe_int(result_2.score) +safe_int(result_3.score)

    )

    consolidate_table.save()

    #Update After Consolidation
    Core_Quiz.objects.filter(
        consolidated=False,
        hsUsersID=id
        ).update(
            consolidated=True,
            date_consolidated = timezone.localtime(timezone.now())
            )


def push_to_dischem():
    
    
    #Get Interval
    interval = Upload_Interval.objects.all().first()

    if interval:
        current_time = timezone.now()
        duration_value = int(interval.interval)
        threshold_time = current_time - timedelta(hours=duration_value)
        
    else:
        current_time = timezone.now()
        threshold_time = current_time - timedelta(hours=24)

        
    # Filter objects older than 96 hours and haven't been uploaded
    data_upload = Consolidated_Core_Quiz.objects.filter(uploaded=False, insertion_date__lt=threshold_time,upload_required = True)
    
    
    for x in data_upload:
        username = 'NowOnline'
        password = 'whjTVmYQrJ2v6DFUn5dLGC'
        url = f'https://api.scoutnet.co.za/api/CreateLeads?Username={username}&Password={password}'
    
           
        payload = {
                    "lead_id": x.hsUsersID,         
                    "first_Name": x.first_name,      
                    "last_Name": x.last_name,        
                    "country_code": "+27",       
                    "mobile": x.q_4,           
                    "email": x.email,            
                    "lead_Source": "NowOnline",     
                    "source_campaign": "NowOnline_Stations",
                    "product": x.product,        
                    "keywords": "",       
                    "lead_Status": "New",       
                    "designation": "",     
                    "consent": True               
}
        headers = {
                "accept": "application/json",
                "content-type": "application/json",
                             
                }

        try:
                          
            response = requests.post(url, json=payload, headers=headers)
          
       
            if response.status_code == 200 :
                    code_value = response.json().get("Code", "Not Available")  
                    if code_value == "SUCCESS" :
                         state_chk = True
                    else : 
                         state_chk = False
                        
                    the_state = Consolidated_Core_Quiz.objects.get(id = x.pk)
                    status_code = response.status_code
                    the_state.uploaded = True
                    the_state.status_check = state_chk 
                    the_state.status_descript = f'{status_code} {response.json()}' 
                    the_state.payload = payload 
                    the_state.date_uploaded = timezone.localtime(timezone.now())
                    the_state.save()
                
            else : 
                    code_value = response.json().get("Code", "Not Available")  
                    if code_value == "SUCCESS" :
                         state_chk = True
                    else : 
                         state_chk = False

                    the_state = Consolidated_Core_Quiz.objects.get(id = x.pk)
                    status_code = response.status_code
                    the_state.uploaded = False
                    the_state.status_descript = f'{status_code}  {response.text}' 
                    the_state.payload = payload 
                    the_state.date_uploaded = timezone.localtime(timezone.now())
                    the_state.save()
            
        except requests.exceptions.ConnectionError as e:
                # Handle network-related errors
                the_state = get_object_or_404(Consolidated_Core_Quiz, id=x.pk)
                the_state.uploaded = False
                the_state.status_descript = f'Connection Error: {e}'
                the_state.payload = payload
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("There was a connection error")

        except requests.exceptions.HTTPError as e:
                # Handle HTTP errors (e.g., status code is not 2xx)
                the_state = get_object_or_404(Consolidated_Core_Quiz, id=x.pk)
                the_state.uploaded = False
                the_state.status_descript = f'HTTP Error: {e}'
                the_state.payload = payload
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("The request was not successful")

        except requests.exceptions.RequestException as e:
                # Handle other request-related errors
                the_state = get_object_or_404(Consolidated_Core_Quiz, id=x.pk)
                the_state.uploaded = False
                the_state.status_descript = f'Request Error: {e}'
                the_state.payload = payload
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("There was an error with the request")
            
          
    else:
        # Handle the case when the queryset is empty
         pass
        

