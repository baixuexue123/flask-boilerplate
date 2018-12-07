import os

from flask import Flask
from flask_session import Session

from config import config


def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV') or 'development'
    app.config.from_object(config[env])
    config[env].init_app(app)

    Session(app)

    with app.app_context():
        from app.models import db_session

        from app.api import auth, admin
        app.register_blueprint(auth.bp)
        app.register_blueprint(admin.bp)

        from app import errorhandlers
        app.register_blueprint(errorhandlers.bp)

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

        @app.route('/')
        def index():
            return 'Hello'

    return app
