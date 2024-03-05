import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_my_sms(cell_number,token):
    account_sid = 'AC190616ccaefefa6265e93ab4926aad21'
    auth_token = 'bcccfdb22d4e60c3a0c3f2c245090064'
    cell_number = cell_number
    client = Client(account_sid, auth_token)

    try :
        message = client.messages \
                .create(
                     body="Welcome to Clinix. Please connect to clinix wifi and use the follwing voucher when prompted : " + str(token),
                     from_='+12082955054',
                     to='+27' + cell_number[1:10]
                 )
    except Exception as e:
        raise e


def send_my_notification_sms(cell_number,id):
    account_sid = 'AC190616ccaefefa6265e93ab4926aad21'
    auth_token = 'bcccfdb22d4e60c3a0c3f2c245090064'
    cell_number = cell_number
    client = Client(account_sid, auth_token)

    try :
        message = client.messages \
                .create(
                     body="Hey!, Someone has just commeted on your recent WiFi News post.Visit www.wifinews.co.za to view and respond. If you would like to stop receiving these notifications please follow this link : https://wifinews.co.za/topics/optout/"+ str(id), 
                     from_='+12082955054',
                     to='+27' + cell_number[1:10]
                 )
    except Exception as e:
        raise e
    

def send_lead_sms(id):
    from wifi_app.models import Consolidated_Core_Quiz  # Local import to avoid circular dependency
    account_sid = 'AC190616ccaefefa6265e93ab4926aad21'
    auth_token = 'bcccfdb22d4e60c3a0c3f2c245090064'
    client = Client(account_sid, auth_token)
    
    try:
        quiz_instance = Consolidated_Core_Quiz.objects.get(pk=id)
        first_name = quiz_instance.first_name  # Extract first_name from the instance
        cell_number = quiz_instance.q_4
        sms_body = "Dear {}, You recently showed interest in Dischem Health Insurance when completing the Wifi News survey, would you like someone from Dischem Health to give you a call to discuss the benefits of Dischem Health Insurance in more detail ? Reply YES or NO to Opt out".format(first_name)

        message = client.messages.create(
            messaging_service_sid='MG129e521f06b4de98b3a7792486925d66',
            body=sms_body, 
            to='+27' + cell_number[1:10]
        )
        print(message.sid)

        quiz_instance = Consolidated_Core_Quiz.objects.get(pk=id)
        quiz_instance.sms_date_sent = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")  # Adjust format as needed
        quiz_instance.sms_sent_text = sms_body
        quiz_instance.sms_sent_meta = message
        quiz_instance.save()

    except ObjectDoesNotExist:
        print(f"No Consolidated_Core_Quiz instance found for ID: {id}")
    except Exception as e:
        raise e
    


