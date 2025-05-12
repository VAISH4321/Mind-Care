import google.generativeai as genai

genai.configure(api_key="Replace With Your API KEY")

def classify_message(message):
    """Uses Gemini for sentiment analysis and classifies risk level."""
    try:
        prompt = f"Analyze the sentiment of this message and classify its emotional tone: '{message}'. Provide output as 'Very Negative', 'Negative', 'Neutral', or 'Positive'."
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        sentiment = response.text.strip().lower()
        if sentiment in ["very negative", "extremely negative"]:
            return "high"
        elif sentiment == "negative":
            return "medium"
        elif sentiment in ["neutral", "positive"]:
            return "low"
        else:
            return "low" 
    except Exception as e:
        print(f"Error: {e}")
        return "low"
print(classify_message("Bomb"))
