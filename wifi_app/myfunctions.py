from background_task import background
from background_task.models import Task
from .models import Consolidated_Core_Quiz,Core_Quiz
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
from vouchers.sms import *
from .om_api import post_OM_contact_API
from django.apps import apps




def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def consolidate_quiz_results(id,survey_id):
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
        if not result_5:
            raise ObjectDoesNotExist("Result 5 is missing for user with ID: " + str(id))
        
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

    #Check If Dischem
    try:
        Survey_settings = apps.get_model('wifi_app', 'Survey_settings')
        survey_setting = Survey_settings.objects.get(survey_id=consolidate_table.surveyID)
        the_client = survey_setting.client_api
        
        if consolidate_table.upload_required == True :
            if the_client == "DC":
                send_lead_sms(consolidate_table.pk)
            elif the_client == "OM" :
                post_OM_contact_API(consolidate_table.first_name,consolidate_table.last_name,consolidate_table.q_4,consolidate_table.pk)
            else :
                pass
          
    except Survey_settings.DoesNotExist:
                            # Handle the case where there is no object with the given survey_id
        print(f"No survey setting found for survey_id {consolidate_table.surveyID}")
                            



      #Update After Consolidation - Doe moet gefix for om na die specifiekek user te lyl
    Core_Quiz.objects.filter(
        consolidated=False,
        hsUsersID=id
        ).update(
            consolidated=True,
            date_consolidated = timezone.localtime(timezone.now())
            )


def consolidate_quiz(hsUsersID,survey_id):

    unique_ids = Core_Quiz.objects.filter(consolidated=False,personal_info=True,hsUsersID = hsUsersID ).values_list('hsUsersID', flat=True).distinct()
    print("The Unique",unique_ids)
    if unique_ids:
        for user_id in unique_ids:
            consolidate_quiz_results(user_id,survey_id)
    else:
        pass

def update_survey_personal_info_per_event(userid,pk):

            api_key = '38XG46Q3NPM63THRMB9984YJ7V6MY5QQ'
            api_secret = '47TY45RDHY77DDNNDNNBD7J8RDL97WQ1'
            url = 'http://www.hotspot.yourspot.co.za/'
            hs_user_id = userid
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
                core_quiz_update.date_personal_info = timezone.localtime(timezone.now())
                core_quiz_update.save()
   

            return JsonResponse({}, status=302)



def pull_survey_answers_per_event(survey_id,username): 
                  
            api_key = '38XG46Q3NPM63THRMB9984YJ7V6MY5QQ'
            api_secret = '47TY45RDHY77DDNNDNNBD7J8RDL97WQ1'
            domain_api_url = 'http://www.hotspot.yourspot.co.za/'
            domain_api_endpoint = 'wpsurveyanswersRead'
            api = RESTfulAPI(domain_api_url, api_key, api_secret)

            # Given string
            data_str = f'{{"Where":"wpsurvey.id={survey_id} AND user.username={username}"}}'
                    
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

       
                        new_quiz_entry = Core_Quiz.objects.create(
                            surveyID=survey_id,
                            insertion_date=creation_date,
                            hsUsersID=user_id,  
                            domain_id=domain_id,
                            q_1=answers[0],
                            q_2=answers[1],
                            q_3=answers[2],
                            q_4=answers[3],  # Ensure this index exists in your 'answers'
                            q_5=answers[4],  # Ensure this index exists in your 'answers'
                            score=score,
                            date_extracted=timezone.localtime(timezone.now())
                    
                            )
                        #Update the Personal Info
                        update_survey_personal_info_per_event(user_id,new_quiz_entry.pk)
                    #Consolidate The result
                    consolidate_quiz(user_id,survey_id)






