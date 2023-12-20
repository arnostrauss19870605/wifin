from background_task import background
from background_task.models import Task
from .models import Registered_User,Country,Domain,Domain_User,Consolidated_Core_Quiz,Core_Quiz,Upload_Interval,Survey_settings
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
from django.db.models import Q
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from datetime import timedelta

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

#@background
def pull_survey_answers(): 

    active_surveys = Survey_settings.objects.filter(is_active=True)

    for x in active_surveys:

        if active_surveys:
            api_key = '38XG46Q3NPM63THRMB9984YJ7V6MY5QQ'
            api_secret = '47TY45RDHY77DDNNDNNBD7J8RDL97WQ1'
            domain_api_url = 'http://www.hotspot.yourspot.co.za/'
            domain_api_endpoint = 'wpsurveyanswersRead'
            
            pk = x.pk
            survey_id = x.survey_id
            domain_id = x.domain_id
            creation_date = x.creation_date
           
            api = RESTfulAPI(domain_api_url, api_key, api_secret)

             # Given string
            data_str = f'{{"Where":"wpsurvey.id={survey_id} AND user.CreationDate >= \\"{creation_date}\\""}}'
            pprint(data_str)
            
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
                if isinstance(json_ret_val, list):
                    # Process each dictionary in the list
                    for item in json_ret_val:
                        creation_date = item['CreationDate']
                        score = item['Score']
                        answers = item['answers']
                        domain_id = item['domain.id']
                        user_id = item['user.id']
                        survey_id = item['wpsurvey.id']

       
                        Core_Quiz.objects.create(
                            surveyID = survey_id,
                            insertion_date = creation_date,
                            hsUsersID = user_id,  
                            domain_id = domain_id,
                            q_1 = answers[0],
                            q_2 = answers[1],
                            q_3 = answers[2],
                            q_4 = answers[4],
                            q_5 = answers[3],
                            score = score,
                            # Add other fields as necessary
                        )
            x.creation_date = timezone.now()        
            x.save()
                    
        else:
            # Handle the case when no "Development" domain is found
            api_key = None
            api_secret = None
            domain_api_url = None
            domain_api_endpoint = None
            domain_id = None
            api = None

#@background
def update_survey_personal_info():
#def populate_registered_users():
    core_quiz_users = Core_Quiz.objects.filter(personal_info=False)
    
    for y in core_quiz_users:
        
        queryset = Core_Quiz.objects.filter(hsUsersID=y.hsUsersID)
        
        if queryset.exists():
            api_key = '38XG46Q3NPM63THRMB9984YJ7V6MY5QQ'
            api_secret = '47TY45RDHY77DDNNDNNBD7J8RDL97WQ1'
            url = 'http://www.hotspot.yourspot.co.za/'
            
       
            if core_quiz_users:
               

                pk = y.pk
                hs_user_id = y.hsUsersID
                
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
                    year_of_birth = json_ret_val_1["YearOfBirth"]
                    month_of_birth = json_ret_val_1["MonthOfBirth"]
                    day_of_birth = json_ret_val_1["DayOfBirth"]
                    hs_product_id = json_ret_val_1["ProductID"]


                    core_quiz_update = Core_Quiz.objects.get(pk=pk)
                    core_quiz_update.username = username
                    core_quiz_update.first_name = first_name
                    core_quiz_update.last_name = last_name
                    core_quiz_update.email = email
                    core_quiz_update.mobile_phone = mobile_phone
                    core_quiz_update.address = address
                    core_quiz_update.city = city
                    core_quiz_update.state = state
                    core_quiz_update.zip = zip
                    core_quiz_update.country = country
                    core_quiz_update.gender = gender
                    core_quiz_update.year_of_birth = year_of_birth
                    core_quiz_update.month_of_birth = month_of_birth
                    core_quiz_update.day_of_birth = day_of_birth
                    core_quiz_update.hs_product_id = hs_product_id
                    core_quiz_update.personal_info = True
                    core_quiz_update.save()
                        

            else:
                # Handle the case when no "Development" domain is found
                hs_user_id = None
                print("Does Not")


        
    return JsonResponse({}, status=302)

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

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0



def consolidate_quiz_results(id):
    try:
        result_1 = Core_Quiz.objects.filter(q_1__isnull=False, hsUsersID=id).exclude(q_1='').first()
        if not result_1:
            raise ObjectDoesNotExist("Result 1 is missing for user with ID: " + str(id))
        # Similarly for result_2, result_3, and result_4
        result_2 = Core_Quiz.objects.filter(q_2__isnull=False, hsUsersID=id).exclude(q_2='').first()
        if not result_2:
            raise ObjectDoesNotExist("Result 2 is missing for user with ID: " + str(id))
        result_3 = Core_Quiz.objects.filter(q_3__isnull=False, hsUsersID=id).exclude(q_3='').first()
        if not result_3:
            raise ObjectDoesNotExist("Result 3 is missing for user with ID: " + str(id))
        
        result_4 = Core_Quiz.objects.filter(q_4__isnull=False, hsUsersID=id).exclude(q_4='').first()
        if not result_4:
            raise ObjectDoesNotExist("Result 4 is missing for user with ID: " + str(id))
        
        result_5 = Core_Quiz.objects.filter(q_5__isnull=False, hsUsersID=id).exclude(q_5='').first()

        # ... rest of your function code ...

    except ObjectDoesNotExist as e:
        # Handle the error or log it
        print(e)
        # Then exit the function. You can also use `return` if you just want to exit without raising an error.
        return

    
    if result_5:  # Checks if result_5 is not None
        contact_number = "0" + result_5.q_5[1:] 
    elif result_1 and hasattr(result_1, 'mobile_phone'):  # Checks if result_1 is not None and has attribute 'mobile_phone'
        contact_number = "0" + result_1.mobile_phone[4:] 
    else:
        # Handle the case where both result_5 is None and result_1 is None or doesn't have 'mobile_phone'
        contact_number = "0000000000"  # Replace with an appropriate default or error handling
    
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
    q_4 =  result_4.q_4,
    q_5 =  contact_number,
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


#@background
def consolidate_quiz():

    unique_ids = Core_Quiz.objects.filter(consolidated=False,personal_info=True).values_list('hsUsersID', flat=True).distinct()
    print("The Unique",unique_ids)
    if unique_ids:
        for user_id in unique_ids:
            consolidate_quiz_results(user_id)
    else:
        pass

#@background
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
                    "mobile": x.q_5,           
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
    
@background
def push_to_dripcel():
    # Filter objects older than 96 hours and haven't been uploaded
    #data_upload = Consolidated_Core_Quiz.objects.filter(uploaded=False, personal_info=True, upload_required=True)
    data_upload = Consolidated_Core_Quiz.objects.filter(uploaded=False, upload_required=True)

    #Welcome Tags
    #GAP: 6572c53c05671e159ae23495
    #"NowOnline_GAP"


    #MI: 6572c414a918866a54580439
    #"NowOnline_MI"

    for x in data_upload:
        api_key = 'Z1ngJ2TuTsKynZylysTW4zruDjMjD7'
        url = 'https://api.dripcel.com/contacts/single'

        payload = {
            "country": "ZA",
            "tags": ["NowOnline_MI"],
            "welcome_send_campaign_id": "6572c414a918866a54580439",
            "contact": 
                {
                    "cell": x.q_5,
                    "firstname": x.first_name,
                    "c1": x.last_name,
                    "c2": "TEST",
                    "tags": ["NowOnline_MI"],
                }
            
        }



        pprint(payload)

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        try:
            response = requests.put(url, json=payload, headers=headers)
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

@background
def delete_old_quizzes():
    # Calculate the time threshold (one day ago from now)
    one_day_ago = timezone.now() - timedelta(days=1)

    # Delete instances in Core_Quiz where date_created is more than one day ago
    Core_Quiz.objects.filter(date_imported__lt=one_day_ago).delete()

    # Delete instances in Consolidated_Core_Quiz where date_created is more than one day ago
    Consolidated_Core_Quiz.objects.filter(date_consolidated__lt=one_day_ago).delete()







          
                    
                
                