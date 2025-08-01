from flask import Flask
from app.extensions import db



def create_app():
    app = Flask(__name__,template_folder='templates',  # Relative to app/
        static_folder='static'       # Relative to app/)
    )    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import models so db.create_all() can see them
    from app.models.user_profile import UserProfile, Conversation

    # Register routes
    from app.routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
