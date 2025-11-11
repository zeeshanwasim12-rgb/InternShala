# backend/ai_features.py

import re
from datetime import datetime
from models import get_db_connection

# ---------- 1️⃣ Parse Resume ----------
def parse_resume(text):
    """Extract name, email, and skills from resume text."""
    resume_data = {}

    # Simple name (first line)
    resume_data['name'] = text.split("\n")[0]

    # Extract email
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    resume_data['email'] = emails[0] if emails else None

    # Extract basic skills
    skills_keywords = ['Python', 'C++', 'Java', 'HTML', 'CSS', 'JavaScript', 'SQL', 'AI', 'ML']
    skills_found = [skill for skill in skills_keywords if skill.lower() in text.lower()]
    resume_data['skills'] = skills_found

    return resume_data


# ---------- 2️⃣ Generate Suggestions (placeholder) ----------
def generate_suggestions(resume_text):
    """
    Placeholder for AI suggestion system.
    Replace this with OpenAI API if needed.
    """
    if len(resume_text) < 100:
        return "Add more details about your skills and experience."
    elif "project" not in resume_text.lower():
        return "Include a projects section with descriptions."
    else:
        return "Your resume looks well-balanced! Keep it concise and focused."


# ---------- 3️⃣ Calculate AI Score ----------
def calculate_ai_score(resume_text):
    """Generate a score (0-100) based on skills and length."""
    skills = parse_resume(resume_text)['skills']
    skill_score = min(len(skills) * 10, 50)  # max 50
    length_score = min(len(resume_text.split()) // 10, 50)  # max 50
    return float(skill_score + length_score)


# ---------- 4️⃣ Save AI Feedback ----------
def save_ai_feedback(user_id, resume_text):
    """Save AI feedback to the database."""
    score = calculate_ai_score(resume_text)
    suggestions = generate_suggestions(resume_text)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ai_feedback (user_id, resume_score, suggestions, analyzed_at)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            resume_score = VALUES(resume_score),
            suggestions = VALUES(suggestions),
            analyzed_at = VALUES(analyzed_at)
    """, (user_id, score, suggestions, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

    return {"score": score, "suggestions": suggestions}
