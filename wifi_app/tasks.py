from background_task import background
from background_task.models import Task
from .models import Registered_User,Country,Domain,Domain_User
from logging import getLogger
import requests, datetime,requests
from django.shortcuts import  render, redirect, HttpResponse
from datetime import datetime,date
from django.utils import timezone
from django.shortcuts import get_object_or_404
from wifi_app.hsnm_1 import RESTfulAPI
from django.http import JsonResponse
from django.utils import timezone
import json
import time


logger = getLogger(__name__)
current_date = timezone.now()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day
schedule_hour = 12  # 12 PM
schedule_minute = 0  # 0 minutes past the hour

# Create the datetime object for scheduling
schedule_date = datetime(year=current_year, month=current_month, day=current_day, hour=schedule_hour, minute=schedule_minute)

#https://medium.com/@mijlalawan/adding-scheduled-background-tasks-to-django-e32cd36876e
#Asynchronous task for removing old records

@background
def push_to_omnisend():
#def push_to_omnisend():
   
    
    omnisend_api_key = None
    url = None
    data_upload = Registered_User.objects.filter(uploaded=False)
    
    for x in data_upload:

        queryset = Domain.objects.filter(domain_id=x.hsDomainsDataID)
        if queryset.exists():
        
            url = queryset.values_list('omnisend_url', flat=True)[0]
            omnisend_api_key = queryset.values_list('omnisend_api_key', flat=True)[0]

            country_name = 'za'           
            try:
                country_name_query = Country.objects.filter(country_code = x.country).values_list('country_name',flat=True)[0]
            except IndexError:
                country_name = 'za'  
            else : 
                country_name =country_name_query

            
            mobile = '0000000000'
            mobile_status = 'nonSubscribed'
            if x.mobile_phone is None:
                mobile = '0000000000'
                mobile_status = 'nonSubscribed'
            else : 
                if x.mobile_phone.isalpha():
                    mobile = x.mobile_phone
                    mobile_status = 'subscribed'
                else :
                    mobile = '0000000000'
                    mobile_status = 'nonSubscribed'

            gender = 'm'
            if x.gender is None:
                gender = 'm'
            else : 
                if gender.isalpha():
                    gender = gender
                else :
                    gender = 'm'


            

                  

        
            input_date = datetime.strptime(x.date_created, '%Y-%m-%d %H:%M:%S')
            output_date_str = input_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            input_date_now = timezone.now()
            output_date__now_str = input_date_now.strftime('%Y-%m-%dT%H:%M:%SZ')
        
            
            if x.year_of_birth is None :
                birth_year = 1900
            else :
                birth_year = x.year_of_birth

            if x.month_of_birth is None :
                birth_month = 1
            else :
                birth_month = x.month_of_birth

            if x.day_of_birth is None :
                birth_day = 1
            else :
                birth_day = x.day_of_birth

        
            try:
                birth_date = date(int(birth_year), int(birth_month), int(birth_day))
            except ValueError:
                birth_date = date(int(1900), int(1), int(1))

            birth_date_formatted = birth_date.strftime('%Y-%m-%d')
            
            payload = {
            "tags": ["source : Entelek - " + x.domain_name], 
            "createdAt": output_date_str,
            "firstName": x.first_name,
            "lastName": x.last_name,
            "identifiers": [
                {
                    "type": "email",
                    "id":x.email,
                     "consent": {
                            "source": "wifi - captive portal",
                            "createdAt": output_date__now_str
                        },
                    "channels": { "email": {
                            "status": "subscribed",
                            "statusDate": output_date_str
                        } }
                },
                {
                    "type": "phone",
                    "id": mobile,
                    "channels": { "sms": {
                            "status": mobile_status,
                            "statusDate": output_date_str
                        } }
                }
            ],
            "country": country_name,
            "countryCode": x.country,
            "state": x.state,
            "city": x.city,
            "address": x.address,
            "postalCode": x.zip,
            "gender": gender,
            "birthdate": birth_date_formatted,
        
        }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-KEY": omnisend_api_key
                
            }

            try:
                
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200 :

                    the_state = Registered_User.objects.get(id = x.pk)
                    status_code = response.status_code
                    the_state.uploaded = True
                    the_state.status_descript = f'{status_code} - Successful' 
                    the_state.payload = payload 
                    the_state.date_uploaded = timezone.localtime(timezone.now())
                    the_state.save()
                
                else : 

                    the_state = Registered_User.objects.get(id = x.pk)
                    status_code = response.status_code
                    the_state.uploaded = False
                    the_state.status_descript = f'{status_code} - {response.text}' 
                    the_state.payload = payload 
                    the_state.date_uploaded = timezone.localtime(timezone.now())
                    the_state.save()
            
            except requests.exceptions.ConnectionError as e:
                # Handle network-related errors
                the_state = get_object_or_404(Registered_User, id=x.pk)
                the_state.uploaded = False
                the_state.status_descript = f'Connection Error: {e}'
                the_state.payload = payload
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("There was a connection error")

            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors (e.g., status code is not 2xx)
                the_state = get_object_or_404(Registered_User, id=x.pk)
                the_state.uploaded = False
                the_state.status_descript = f'HTTP Error: {e}'
                the_state.payload = payload
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("The request was not successful")

            except requests.exceptions.RequestException as e:
                # Handle other request-related errors
                the_state = get_object_or_404(Registered_User, id=x.pk)
                the_state.uploaded = False
                the_state.status_descript = f'Request Error: {e}'
                the_state.payload = payload
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("There was an error with the request")
            
          
        else:
    # Handle the case when the queryset is empty
            the_state = Registered_User.objects.get(id = x.pk)
            the_state.uploaded = False
            the_state.status_descript = "Credentails Do Not Exisit"
            the_state.date_uploaded = timezone.localtime(timezone.now())
            the_state.save()     


@background
def pull_from_captive_portal(): 
#def pull_from_captive_portal(): 
    development_domain = Domain.objects.all()

    for x in development_domain:

        if development_domain:
            pk = x.pk
            api_key = x.api_key
            api_secret = x.api_seceret
            domain_api_url = x.url
            domain_api_endpoint = x.endpoint
            domain_id = x.domain_id
            domain_api_lastdate = x.last_extracted_date
            api = RESTfulAPI(domain_api_url, api_key, api_secret)

             # Given string
            data_str = f'{{"Where":"domain.id={domain_id} AND user.CreationDate >= \\"{domain_api_lastdate}\\""}}'
            
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
                #pprint(json_ret_val)
                id_list = json_ret_val.get('id', [])
                for id in id_list:

                    Domain_User.objects.create(
                    user_id = id,
                    domain_id = domain_id,
                    last_extracted_date = domain_api_lastdate,
                    
                )
                
                the_state = Domain.objects.get(id=pk)
                the_state.last_extracted_date = timezone.now()
                the_state.save()
        else:
            # Handle the case when no "Development" domain is found
            api_key = None
            api_secret = None
            domain_api_url = None
            domain_api_endpoint = None
            domain_id = None
            domain_api_lastdate = None
            api = None



            
    #Extract user related to above ID and Update Registrerd User Model

@background
def populate_registered_users():
#def populate_registered_users():
    registered_users = Domain_User.objects.filter(extracted=False)
    
    for y in registered_users:
        
        queryset = Domain.objects.filter(domain_id=y.domain_id)
        
        if queryset.exists():
            url = queryset.values_list('url', flat=True)[0]
            api_key = queryset.values_list('api_key', flat=True)[0]
            api_secret = queryset.values_list('api_seceret', flat=True)[0]
        
            if registered_users:
                reguser_pk = y.pk
                hs_user_id = y.user_id
                
                api = RESTfulAPI(url, api_key, api_secret)

                # Given string
                data_str_1 = f'{{"id":"{hs_user_id}"}}'
                
                # Parse the string as a Python dictionary
                data_dict_1 = json.loads(data_str_1)

                # Serialize the dictionary as a JSON string
                json_data_1 = json.dumps(data_dict_1)

                endpoint_1 = 'userRead'
                data_1 = json_data_1
                json_ret_val_1 = api.api_call(endpoint_1, data_1)
                
        
                if "error" in json_ret_val_1 and json_ret_val_1["error"] != "":
                    print("Error:", json_ret_val_1["error"])
                else:
                    hsDomainsDataID = json_ret_val_1["DomainID"]
                    hsUsersID = json_ret_val_1["id"]
                    username = json_ret_val_1["UserName"]
                    first_name = json_ret_val_1["FirstName"]
                    last_name = json_ret_val_1["LastName"]
                    email = json_ret_val_1["EmailAddress"]
                    mobile_phone = json_ret_val_1["MobilePhone"]
                    address = json_ret_val_1["Address"]
                    city = json_ret_val_1["City"]
                    state = json_ret_val_1["State"]
                    zip = json_ret_val_1["ZIP"]
                    country = json_ret_val_1["Country"]
                    gender = json_ret_val_1["Gender"]
                    date_created = json_ret_val_1["CreationDate"]
                    language = json_ret_val_1["Language"]
                    year_of_birth = json_ret_val_1["YearOfBirth"]
                    month_of_birth = json_ret_val_1["MonthOfBirth"]
                    day_of_birth = json_ret_val_1["DayOfBirth"]

                    #Domain Name Lookup
                    if int(hsDomainsDataID) == 1143 :
                        domain_name_descrip = "FranschhoekCellar"
                    elif int(hsDomainsDataID) == 1149 :
                        domain_name_descrip = "OldRoadWines"
                    elif int(hsDomainsDataID) == 1151 :
                        domain_name_descrip = "Backsberg"
                    elif int(hsDomainsDataID) == 1153 :
                        domain_name_descrip = "Brampton"
                    else :
                        domain_name_descrip = "General"


                    domain_name = domain_name_descrip
                    product = "DGB 10Mbps Uncapped"
                    hs_product_id = json_ret_val_1["ProductID"]


                    Registered_User.objects.create(
                            hsDomainsDataID = hsDomainsDataID,
                            hsUsersID = hsUsersID,
                            username = username,
                            first_name = first_name,
                            last_name = last_name,
                            email = email,
                            mobile_phone = mobile_phone,
                            address = address,
                            city = city,
                            state = state,
                            zip = zip,
                            country = country,
                            gender = gender,
                            date_created = date_created,
                            language = language,
                            year_of_birth = year_of_birth,
                            month_of_birth = month_of_birth,
                            day_of_birth = day_of_birth,
                            domain_name = domain_name,
                            product = product,
                            hs_product_id = hs_product_id,
                        
                    )

                    update_reg_user = Domain_User.objects.get(id=reguser_pk)
                    update_reg_user.extracted = True
                    update_reg_user.save()

            else:
                # Handle the case when no "Development" domain is found
                pk = None
                hs_user_id = None
                print("Does Not")


        
    return JsonResponse({}, status=302)


          
                    
                
                