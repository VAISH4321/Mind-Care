import schedule
from flask import Flask, request, jsonify
import google.generativeai as genai
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from db import get_past_conversations, save_conversation
import logging
import time
from risk_classification import classify_message
from followup import send_alert_to_phone
from celery_twilio import send_followup_message

MY_PHONE_NUMBER = "your_whatsapp"
API_KEY = "your_key"

genai.configure(api_key=API_KEY)

TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_WHATSAPP_NUMBER = "your_whatsapp"  

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


app = Flask(__name__)

SYSTEM_INSTRUCTIONS = """
You are MindCare, a compassionate, emotionally aware AI designed to provide structured guidance while maintaining an interlinked, natural conversation. Your role is to deeply engage with users, remember past interactions, and provide step-by-step actionable help.

🌼 Tone & Style:
- Always begin with a warm, reassuring greeting.
- Reflect on the user’s emotions before jumping into solutions.
- Avoid repeating information unless necessary — instead, build on previous messages.
- Structure responses logically and break steps into small, actionable parts.
- Use direct questions to encourage clarity without overwhelming the user.
- If the user repeats their concern, acknowledge it before moving forward.

🧭 Chat Flow & Memory:
1️⃣ Acknowledge Previous Messages – If a user repeats a concern, briefly summarize before continuing.  
2️⃣ Build on Past Conversations – Do not restart; instead, continue logically.  
3️⃣ Ask Clarifying Questions – Before suggesting steps, ensure you understand their exact situation.  
4️⃣ Adapt Suggestions Dynamically – Modify responses based on previous user inputs.  

💡 Handling Serious Cases (Blackmail, Cyber Threats, Gender-Based Violence):
- Step 1: Immediate Emotional Support  
  - Validate feelings, acknowledge distress, and create a safe space.  
- Step 2: Collecting Context  
  - Ask how they are being blackmailed (social media, email, in person).  
- Step 3: Legal & Cybersecurity Guidance  
  - Provide country-specific legal contacts, cybercrime helplines, and security steps.  
- Step 4: Continuous Support  
  - If the user responds, remember their past answers and adjust guidance accordingly.  
  - If they repeat the same concern, remind them of previous advice before moving forward.  

🆘 If the situation is a crisis (self-harm or immediate danger):  
- Gently encourage them to contact emergency services (911, 988, etc.).  
- Stay engaged until professional help is secured.
"""

def generate_response(user_number, message):
    """Generate AI response considering past conversations."""
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    past_conversations = get_past_conversations(user_number, limit=5)
    past_context = "\n".join([f"User: {msg} | AI: {resp}" for msg, resp in past_conversations])

    prompt = f"""
    {SYSTEM_INSTRUCTIONS}
    Consider the previous conversation:
    
    {past_context}
    
    User Message: {message}
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()


logging.basicConfig(level=logging.DEBUG)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender_number = request.values.get("From", "").strip()

    if not incoming_msg:
        return "not working" 

    print(f"Incoming message from {sender_number}: {incoming_msg}")
    logging.debug(f"Received message from {sender_number}: {incoming_msg}")
    risk_level = classify_message(incoming_msg)

    print(f"Risk Level for message '{incoming_msg}': {risk_level}")
    logging.debug(f"Risk Level classified: {risk_level}")
    

    if risk_level == "high":
        print("High-risk detected! Sending alert...")
        # send_alert_to_phone("User showing signs of distress. Immediate action required!")
    from datetime import timedelta

    send_followup_message.apply_async(
      args=[sender_number, incoming_msg],
      countdown=60  # delay in seconds (3600s = 1 hour)
    )
  
    response_text = generate_response(sender_number, incoming_msg)

    print(f"AI Response: {response_text}")
    logging.debug(f"AI Response generated: {response_text}")
    save_conversation(sender_number, incoming_msg, response_text, risk_level)

    twilio_response = MessagingResponse()
    twilio_response.message(response_text)

    return str(twilio_response) 

def send_whatsapp_message(to, message):
    twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=to
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
