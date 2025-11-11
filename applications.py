from flask import Blueprint, request, jsonify
from models import get_db_connection

applications_bp = Blueprint("applications_bp", __name__)

@applications_bp.route("/apply", methods=["POST"])
def apply_internship():
    data = request.json
    student_id = data.get("student_id")
    internship_id = data.get("internship_id")
    resume_link = data.get("resume_link", "")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO applications (internship_id, student_id, resume_link) VALUES (%s,%s,%s)",
        (internship_id, student_id, resume_link),
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Application submitted"}), 201


@applications_bp.route("/student/<int:student_id>", methods=["GET"])
def get_student_apps(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT a.*, i.title FROM applications a
           JOIN internships i ON a.internship_id=i.id
           WHERE student_id=%s ORDER BY applied_at DESC""",
        (student_id,),
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)
