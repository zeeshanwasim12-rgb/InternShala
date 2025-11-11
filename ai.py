from flask import Blueprint, request, jsonify
from ai_features import analyze_resume

ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    user_id = data.get("user_id")
    resume_text = data.get("resume_text")

    if not all([user_id, resume_text]):
        return jsonify({"error": "user_id and resume_text are required"}), 400

    result = analyze_resume(user_id, resume_text)
    return jsonify(result)
