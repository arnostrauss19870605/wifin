import os
from twilio.rest import Client


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


