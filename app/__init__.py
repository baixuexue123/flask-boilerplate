import os

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import config

from .models.base import BaseModel

db = SQLAlchemy(model_class=BaseModel)


def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV') or 'development'
    app.config.from_object(config[env])
    config[env].init_app(app)

    Session(app)
    db.init_app(app)

    with app.app_context():
        from app import errorhandlers
        from app.api import auth, admin
        app.register_blueprint(auth.bp)
        app.register_blueprint(admin.bp)

        @app.route('/')
        def index():
            app.logger.info('-----------------********-----------------')
            return 'Hello flask'

    return app
