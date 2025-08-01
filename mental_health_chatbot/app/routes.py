from flask import Blueprint, render_template, request, jsonify, send_file
from app.services.voice_service import ConversationalService
import io
from dotenv import load_dotenv
from app.models.user_profile import UserProfile
load_dotenv()

bp = Blueprint('routes', __name__)
convo_service = ConversationalService()  # Instantiate once

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('message')
        user_id = request.json.get('user_id', 'default_user')

        # ✅ Now everything is done inside get_response
        result = convo_service.get_response(user_input, user_id)

        return jsonify({
            'response': result['response'],
            'audio_id': result['audio_id'],
            'sentiment': result['sentiment'],
            'depression_level': result['depression_level']
        })

    return render_template('chat.html')

@bp.route('/generate_audio/<audio_id>')
def generate_audio(audio_id):
    audio_data = convo_service.get_audio(audio_id)
    return send_file(
        io.BytesIO(audio_data),
        mimetype='audio/mpeg',
        as_attachment=False
    )

@bp.route('/report/<user_id>')
def report(user_id):
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not user_profile:
        return f"No profile found for user_id: {user_id}", 404

    report_data = user_profile.generate_report()
    return render_template('report.html', report=report_data)

@bp.route('/staff_intervention/<user_id>')
def staff_intervention(user_id):
    from app.models.user_profile import UserProfile
    user_profile = UserProfile(user_id)
    return jsonify({'conversation': user_profile.get_conversation_history()})
