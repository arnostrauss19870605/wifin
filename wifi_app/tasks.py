from background_task import background
from .models import Registered_User
from logging import getLogger
import requests, datetime,requests
from django.shortcuts import  render, redirect, HttpResponse

logger = getLogger(__name__)

#https://medium.com/@mijlalawan/adding-scheduled-background-tasks-to-django-e32cd36876e
#Asynchronous task for removing old records
@background(schedule=1)
def demo_task(repeat=5 , repeat_until=None):
    
    url = "https://api.omnisend.com/v3/contacts"

    payload = {
    "createdAt": "2016-05-02T09:19:19Z",
    "firstName": "Arno",
    "lastName": "Strauss",
    "tags": ["designer", "leader", "source: shopify"],
    "identifiers": [
        {
            "type": "email",
            "id": "arno.strauss@example.com",
            "channels": { "email": {
                    "status": "subscribed",
                    "statusDate": "2016-02-01T10:07:28Z"
                } }
        },
        {
            "type": "phone",
            "id": "+443031217300",
            "channels": { "sms": {
                    "status": "nonSubscribed",
                    "statusDate": "2016-02-01T10:07:28Z"
                } }
        }
    ],
    "country": "United Kingdom",
    "countryCode": "GB",
    "state": "",
    "city": "London",
    "address": "Westminster",
    "postalCode": "SW1A 1AA",
    "gender": "f",
    "birthdate": "1997-05-02",
    "customProperties": {
        "age": 33,
        "hair_color": "brown",
        "married": True,
        "marriageDate": "2018-07-07",
        "loyaltyPoints": 125.8,
        "pets": ["dog", "cat"]
    }
}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "65141b71ce8ad7f6d45f21c7-nWgM3X9uUgXtaEglL57qG4adhuFAXlDAEuw2S0z8T1GplMQ0Ql"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
    
    except requests.exceptions.RequestException as e:
            # Handle request errors
            print(f"My Error: {e}")
            
            
            return HttpResponse("The is a fail")


    print(response.text)