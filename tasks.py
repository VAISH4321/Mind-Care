# tasks.py
from celery_twilio import celery
from twilio.rest import Client


@celery.task
def send_followup_message(user_number: str):
    TWILIO_ACCOUNT_SID = "ACCOUNT_SID"
    TWILIO_AUTH_TOKEN = "AUTH_TOKEN"
    from_number = 'your whatsapp numner'

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    followup_text = "💬 Hey Hi! How are you feeling now? Remember, you’re not alone."

    client.messages.create(
        body=followup_text,
        from_=from_number,
        to=user_number
    )
