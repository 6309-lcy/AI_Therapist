import os
import time
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.conversational_ai.conversation import ClientTools, Conversation
from app.extensions import db

from app.models.sentimental_anayzer import SentimentAnalyzer
from app.services.alert_service import send_alert
from app.models.user_profile import UserProfile, Conversation as DBConversation

load_dotenv()

# 🔁 Sentiment tool with DB integration
def analyze_sentiment_tool(parameters):
    user_id = parameters.get("user_id")
    user_input = parameters.get("text", "")
    analyzer = SentimentAnalyzer()
    rdata = analyzer.analyze(user_input)
    score = rdata["compound_score"]
    raw_lv = rdata["average_score"]

    alert_triggered = False
    if raw_lv < -0.5:
        send_alert(user_id, raw_lv)
        alert_triggered = True
        request_human_intervention({"user_id": user_id})

    return {
        "sentiment_score": score,
        "alert_triggered": alert_triggered,
        "de_lv": raw_lv
    }

# 🧠 Save user message to DB
def update_user_profile(user_id, user_input):
    sentiment_data = analyze_sentiment_tool({
        "user_id": user_id,
        "text": user_input
    })

    score = sentiment_data["sentiment_score"]
    de_lv = sentiment_data["de_lv"]

    # Ensure profile exists
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    # Save conversation
    convo = DBConversation(
        user_id=user_id,
        message=user_input,
        sentiment_score=score,
        depression_level=de_lv
    )
    db.session.add(convo)
    db.session.commit()

# 🚨 Called when alert needs escalation
def request_human_intervention(parameters):
    user_id = parameters.get("user_id")
    reason = parameters.get("reason", "High distress detected")

    print(f"[HUMAN REQUEST] User {user_id} needs human support: {reason}")

    return {
        "status": "notified",
        "escalation": True
    }

# 🔌 Tool registration
client_tools = ClientTools()
client_tools.register("analyzeSentiment", analyze_sentiment_tool)
client_tools.register("updateUserProfile", update_user_profile)
client_tools.register("requestHumanIntervention", request_human_intervention)

# 🧠 Main service class
class ConversationalService:
    def __init__(self):
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.conversation = None
        self.audio_interface = DefaultAudioInterface()
        self.client_tools = client_tools
        self._last_response = None
        self._setup_conversation()

    def _setup_conversation(self):
        if not self.conversation:
            self.conversation = Conversation(
                self.elevenlabs,
                agent_id=os.getenv("agent_id"),
                requires_auth=True,
                audio_interface=self.audio_interface,
                client_tools=self.client_tools,
                callback_agent_response=self._on_response,
                callback_user_transcript=self._on_transcript
            )
            self.conversation.start_session()

    def _on_response(self, text):
        self._last_response = text

    def _on_transcript(self, transcript):
        print(f"[User]: {transcript}")

    def get_response(self, user_input, user_id="default_user"):
        self._last_response = None

        # 🔁 Analyze & persist
        sentiment_data = analyze_sentiment_tool({
            "user_id": user_id,
            "text": user_input
        })
        update_user_profile(user_id, user_input)

        # 🗣️ Send message to ElevenLabs
        self.conversation.send_user_message(user_input)

        # ⏳ Wait for response
        for _ in range(100):
            time.sleep(0.1)
            if self._last_response:
                break
        else:
            raise TimeoutError("AI response timeout")

        return {
            "response": self._last_response,
            "audio_id": "not_applicable",  # Placeholder until audio is implemented
            "sentiment": sentiment_data["sentiment_score"],
            "depression_level": sentiment_data["de_lv"]
        }

    def get_audio(self, audio_id):
        # 🗣️ Not implemented
        return b""
