from app import create_app
from app.extensions import db
from app.models.user_profile import UserProfile, Conversation

# Create Flask app instance
app = create_app()

# Use the application context to run database operations
with app.app_context():
    Conversation.query.delete()
    UserProfile.query.delete()
    db.session.commit()
    print("✅ Database reset successfully!")