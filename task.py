# tasks.py
from celery_twilio import celery
from twilio.rest import Client


@celery.task
def send_followup_message(user_number: str):
    TWILIO_ACCOUNT_SID = "Your_SID"
    TWILIO_AUTH_TOKEN = "Your_Token"
    from_number = 'Your whatsapp_number'

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    followup_text = "💬 Hey Hi! How are you feeling now? Remember, you’re not alone."

    client.messages.create(
        body=followup_text,
        from_=from_number,
        to=user_number
    )
