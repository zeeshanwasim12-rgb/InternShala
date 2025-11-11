from flask import Blueprint, request, jsonify
from models import get_db_connection

internships_bp = Blueprint('internships_bp', __name__)


@internships_bp.route('/all', methods=['GET'])
def get_all_internships():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, u.name AS employer_name 
            FROM internships i 
            JOIN users u ON i.employer_id = u.id
            ORDER BY i.id DESC
        """)
        internships = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(internships)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@internships_bp.route('/post', methods=['POST'])
def post_internship():
    try:
        data = request.get_json()
        employer_id = data.get('employer_id')
        title = data.get('title')
        description = data.get('description')
        skills_required = data.get('skills_required')
        duration = data.get('duration')
        stipend = data.get('stipend')
        location = data.get('location')

        if not employer_id or not title:
            return jsonify({"error": "Missing required fields"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO internships (employer_id, title, description, skills_required, duration, stipend, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (employer_id, title, description, skills_required, duration, stipend, location))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Internship posted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
