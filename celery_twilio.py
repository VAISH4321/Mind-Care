from celery import Celery
from twilio.rest import Client
import logging

# --- Logging setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Celery app setup ---
celery = Celery(
    'mindcare',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

# --- Celery Task ---
@celery.task
def send_followup_message(user_number: str):
    logger.info(f"Preparing to send follow-up message to {user_number}")

    TWILIO_ACCOUNT_SID = "your_sid"
    TWILIO_AUTH_TOKEN = "your_token"
    from_number = 'your_whatsapp number'

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        followup_text = "💬 Just checking in. How are you feeling now? Remember, you’re not alone."

        message = client.messages.create(
            body=followup_text,
            from_=from_number,
            to=user_number
        )

        logger.info(f"✅ Message sent successfully. SID: {message.sid}")
    except Exception as e:
        logger.error(f"❌ Failed to send message: {e}")
