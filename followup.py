
from twilio.rest import Client
import time
TWILIO_ACCOUNT_SID = "ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "your whatsapp number"  

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
def send_alert_to_phone(risk_message, to_phone='your phone number'):
    account_sid = 'ACCOUNT_SID'
    auth_token = 'AUTH_TOKEN'

    client = Client(account_sid, auth_token)
        
    message = client.messages.create(
        from_='Phone Number',
        body=f'High alert: {risk_message}',
        to=to_phone
    )
