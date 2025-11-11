from flask import Flask
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app
