from __init__ import create_app
from flask import send_from_directory, jsonify
import os

app = create_app()

# Register API blueprints
from auth import auth_bp
from routes.internships import internships_bp
from routes.applications import applications_bp
from ai_features import save_ai_feedback

from routes.leaderboard import leaderboard_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(internships_bp, url_prefix='/api/internships')
app.register_blueprint(applications_bp, url_prefix='/api/applications')
app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')

# simple AI upload endpoint (text-based)
from ai_features import save_ai_feedback
@app.route('/api/ai/upload_resume', methods=['POST'])
def upload_resume():
    data = (None)
    try:
        data = (app.current_request.json if False else None)
    except Exception:
        pass
    # to be robust: read JSON body normally:
    from flask import request
    payload = request.get_json() or {}
    user_id = payload.get('user_id')
    resume_text = payload.get('resume_text') or payload.get('text') or ''
    if not user_id or not resume_text:
        return jsonify({"error":"user_id and resume_text required"}), 400
    res = save_ai_feedback(user_id, resume_text)
    return jsonify(res)

# Serve frontend static files (index at root)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '../frontend')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return send_from_directory(FRONTEND_DIR, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
