import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = 'my-local-chatbot-key-12345'
    ELEVENLABS_API_KEY = '..' 
    ELEVENLABS_AGENT_ID=".."
    # Replace with your ElevenLabs API key and Conversational Agent ID
    # Add other configurations (e.g., database URI if needed)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance/chatbot.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False