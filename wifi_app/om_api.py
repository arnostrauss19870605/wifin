import json
import requests, datetime,requests
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.shortcuts import  render, redirect, HttpResponse
from django.utils import timezone

def post_OM_contact_API(name,surname,cell_nr,consolidated_id):
    url = 'https://scstagethistle-oldmutual.scprod.yonder.cloud/api/leadgen/v2/lead/entelek'
    headers = {
        'Content-Type': 'application/json',
        'yomotoken': 'db0ba19b0e47b0440356f30bd0fcdbc5'
    }
    data = {
        "msisdn": cell_nr,
        "product": "YONDIGITAL10",
        "source": "Entelek",
        "name": name,
        "surname": surname
    }

    try :
            
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200 :
                    Consolidated_Core_Quiz = apps.get_model('wifi_app', 'Consolidated_Core_Quiz')
                    code_value = response.json().get("Code", "Not Available")  
                    if code_value == "SUCCESS" :
                         state_chk = True
                    else : 
                         state_chk = False
                        
                    the_state = Consolidated_Core_Quiz.objects.get(id = consolidated_id)
                    status_code = response.status_code
                    the_state.uploaded = True
                    the_state.status_check = state_chk 
                    the_state.status_descript = f'{status_code} {response.json()}' 
                    the_state.payload = data 
                    the_state.date_uploaded = timezone.localtime(timezone.now())
                    the_state.save()
                
        else : 
                    Consolidated_Core_Quiz = apps.get_model('wifi_app', 'Consolidated_Core_Quiz')
                    code_value = response.json().get("Code", "Not Available")  
                    if code_value == "SUCCESS" :
                         state_chk = True
                    else : 
                         state_chk = False

                    the_state = Consolidated_Core_Quiz.objects.get(id = consolidated_id)
                    status_code = response.status_code
                    the_state.uploaded = False
                    the_state.status_descript = f'{status_code}  {response.text}' 
                    the_state.payload = data 
                    the_state.date_uploaded = timezone.localtime(timezone.now())
                    the_state.save()
            
    except requests.exceptions.ConnectionError as e:
                # Handle network-related errors
                Consolidated_Core_Quiz = apps.get_model('wifi_app', 'Consolidated_Core_Quiz')
                the_state = get_object_or_404(Consolidated_Core_Quiz, id=consolidated_id)
                the_state.uploaded = False
                the_state.status_descript = f'Connection Error: {e}'
                the_state.payload = data
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("There was a connection error")

    except requests.exceptions.HTTPError as e:
                # Handle HTTP errors (e.g., status code is not 2xx)
                Consolidated_Core_Quiz = apps.get_model('wifi_app', 'Consolidated_Core_Quiz')
                the_state = get_object_or_404(Consolidated_Core_Quiz, id=consolidated_id)
                the_state.uploaded = False
                the_state.status_descript = f'HTTP Error: {e}'
                the_state.payload = data
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("The request was not successful")

    except requests.exceptions.RequestException as e:
                # Handle other request-related errors
                Consolidated_Core_Quiz = apps.get_model('wifi_app', 'Consolidated_Core_Quiz')
                the_state = get_object_or_404(Consolidated_Core_Quiz, id=consolidated_id)
                the_state.uploaded = False
                the_state.status_descript = f'Request Error: {e}'
                the_state.payload = data
                the_state.date_uploaded = timezone.localtime(timezone.now())
                the_state.save()
                return HttpResponse("There was an error with the request")
            
          

    
    print("The OM Response : ",response)
    return response