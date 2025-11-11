from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db_connection

auth_bp = Blueprint('auth_bp', __name__)

# ✅ Register
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        university = data.get('university')

        if not all([name, email, password, role]):
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, university)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, hashed_password, role, university))

        conn.commit()
        cursor.close()
        conn.close()
        print("[REGISTER] ✅ User created successfully:", email)
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print("[REGISTER ERROR]", str(e))
        return jsonify({"error": f"Backend Error: {str(e)}"}), 500


# ✅ Login
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({"error": "Missing credentials"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user['password_hash'], password):
            return jsonify({"error": "Incorrect password"}), 401

        cursor.close()
        conn.close()
        print("[LOGIN] ✅ Success:", email)
        return jsonify({"message": "Login successful!"}), 200

    except Exception as e:
        print("[LOGIN ERROR]", str(e))
        return jsonify({"error": f"Backend Error: {str(e)}"}), 500
