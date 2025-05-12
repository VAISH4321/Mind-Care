from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse, Gather
from langdetect import detect
from googletrans import Translator
from app import generate_response
app = Flask(__name__)
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize the Google Translator
translator = Translator()

@app.route("/voice", methods=["POST"])
def voice_response():
    response = VoiceResponse()

    # Get the speech result (what the user said)
    speech_result = request.values.get('SpeechResult')

    if speech_result:
        try:
            detected_language = detect(speech_result)
        except:
            detected_language = 'en'

        # Generate AI response based on user speech
        user_number = "Replace with actual user's number "  # Replace with actual user's number (dynamic handling can be done here)
        ai_response = generate_response(user_number, speech_result)

        # Translate AI response if needed
        if detected_language != 'en':
            ai_response = translator.translate(ai_response, src='en', dest=detected_language).text

        # Speak the AI response to the user
        response.say(ai_response, language=detected_language)
    else:
        # If no speech result is detected, ask the user to speak
        gather = Gather(input='speech', action='/voice', method='POST', timeout=5)
        gather.say("Hello! Please tell me how I can assist you.")
        response.append(gather)
        response.redirect('/voice')  # If no input, prompt again

    return str(response)

def trigger_twilio_call():
    call = twilio_client.calls.create(
        to="Replace with the recipient’s number",  # Replace with the recipient’s number
        from_="Your Twilio number",  # Your Twilio number
        url="https://0cb7-2409-40f0-1041-4303-9171-6fa6-1831-87b1.ngrok-free.app/voice"  # ngrok + /voice endpoint
    )
    print(f"Call SID: {call.sid}")


if __name__ == "__main__":
    trigger_twilio_call()
    app.run(debug=True)
