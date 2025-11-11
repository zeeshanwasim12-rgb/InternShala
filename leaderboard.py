from flask import Blueprint, jsonify
from models import get_db_connection

leaderboard_bp = Blueprint("leaderboard_bp", __name__)

@leaderboard_bp.route("/", methods=["GET"])
def leaderboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT u.name, u.university, COALESCE(l.total_points, 0) AS total_points, COALESCE(l.ai_score, 0) AS ai_score
           FROM users u
           LEFT JOIN leaderboard l ON u.id = l.user_id
           ORDER BY total_points DESC, ai_score DESC"""
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)
