CREATE DATABASE IF NOT EXISTS internshala;
USE internshala;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(120) UNIQUE,
  password_hash VARCHAR(255),
  role ENUM('student','employer','admin') DEFAULT 'student',
  university VARCHAR(120),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  employer_id INT,
  title VARCHAR(150),
  description TEXT,
  skills_required VARCHAR(255),
  duration VARCHAR(100),
  stipend VARCHAR(100),
  location VARCHAR(150),
  posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (employer_id) REFERENCES users(id)
);

CREATE TABLE applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internship_id INT,
  student_id INT,
  resume_link VARCHAR(255),
  status ENUM('applied','shortlisted','rejected','selected') DEFAULT 'applied',
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (internship_id) REFERENCES internships(id),
  FOREIGN KEY (student_id) REFERENCES users(id)
);

CREATE TABLE leaderboard (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNIQUE,
  total_points INT DEFAULT 0,
  ai_score FLOAT DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE ai_feedback (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNIQUE,
  resume_score FLOAT,
  suggestions TEXT,
  analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
