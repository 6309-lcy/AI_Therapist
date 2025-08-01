from app.extensions import db
from datetime import datetime

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_report(self):
        conversations = Conversation.query.filter_by(user_id=self.user_id).all()

        # Seed with a neutral score to prevent early alert triggering
        sentiment_scores = [1.0]  # Initial seed value
        problems = []
        suggestions = []

        for c in conversations:
            sentiment_scores.append(c.sentiment_score)
            if c.sentiment_score < -0.3:
                problems.append({'issue': c.message, 'severity': c.sentiment_score})
                suggestions.append('Consider discussing this with a professional therapist.')

        average_score = sum(sentiment_scores) / len(sentiment_scores)

        return {
            'user_id': self.user_id,
            'problems': problems,
            'average_score': average_score,
            'suggestions': list(set(suggestions)),
            'conversation_count': len(conversations)
        }

    def get_conversation_history(self):
        conversations = Conversation.query.filter_by(user_id=self.user_id).order_by(Conversation.timestamp).all()
        return [{'user': c.message, 'timestamp': c.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for c in conversations]


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user_profiles.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)
    depression_level = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
