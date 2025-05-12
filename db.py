import sqlite3
from datetime import datetime

DB_NAME = "conversations.db"

def init_db():
    """Initialize the database and create tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_number TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            risk_level TEXT NOT NULL,  -- Remove DEFAULT 'low'
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()



def save_conversation(user_number, message, response, risk_level):
    """Save a user's message, chatbot response, and risk level to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO conversations (user_number, message, response, risk_level)
        VALUES (?, ?, ?, ?)
        """,
        (user_number, message, response, risk_level)
    )
    conn.commit()
    conn.close()

def get_past_conversations(user_number, limit=5):
    """Retrieve the last few messages from the database for a given user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT message, response FROM conversations
        WHERE user_number = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (user_number, limit)
    )
    conversations = cursor.fetchall()
    conn.close()
    return conversations

if __name__ == "__main__":
    init_db()
