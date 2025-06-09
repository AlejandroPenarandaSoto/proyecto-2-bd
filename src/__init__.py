from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from logic.exceptions.GlobalExceptionHandler import registerErrorHandlers

db = SQLAlchemy()

def create_app():
    load_dotenv()  # Carga variables desde .env

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    registerErrorHandlers(app)

    return app
