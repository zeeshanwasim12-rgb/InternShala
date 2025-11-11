import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DB_HOST = os.getenv("MYSQL_HOST", "localhost")
    DB_USER = os.getenv("MYSQL_USER", "root")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "root123")
    DB_NAME = os.getenv("MYSQL_DB", "internshala")
