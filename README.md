# 🧠 MindCare – A Mental Health Support Chatbot with WhatsApp & Voice Integration

**MindCare** is an emotionally aware, AI-driven chatbot built to support users with mental health challenges through **empathetic conversations** on **WhatsApp and phone calls**. It uses Google's **Gemini AI**, detects emotional distress, stores past interactions, and triggers follow-ups or alerts for high-risk messages.

---

## 💡 Features

- 🧠 **Emotionally Intelligent AI** – Uses Gemini Experimental model respond with compassion and memory of past conversations
- 📱 **WhatsApp Integration** – Seamlessly interact via WhatsApp using Twilio
- 🗣 **Voice Support** – Receive responses via automated voice calls (Twilio Voice)
- ⚠️ **Risk Classification** – Automatically classifies messages as low, medium, or high emotional risk
- 🧾 **Follow-Up System** – Sends timed check-ins using Celery + Redis
- 🌐 **Multilingual Aware** – Detects language and translates voice responses
- 📂 **Conversation Logging** – Stores interactions with user IDs in SQLite (`conversations.db`)

---

## 🛠 Tech Stack

- **Language**: Python (Flask)
- **AI Engine**: Google Generative AI (Gemini Pro + Flash)
- **Messaging**: Twilio WhatsApp & Voice API
- **Task Queue**: Celery + Redis
- **Database**: SQLite
- **Translation**: Google Translate
- **Voice Input**: Twilio Voice + SpeechResult

---

## 📁 Project Structure

```bash
.
├── app.py                 # Main Flask app for WhatsApp chatbot
├── call_twilio.py         # Voice call system using Twilio
├── celery_twilio.py       # Celery task manager for async follow-up
├── tasks.py               # Celery task definition for follow-ups
├── followup.py            # Alert message system
├── risk_classification.py # Gemini-powered risk classifier
├── conversations.db       # SQLite DB for chat history
└── README.md
