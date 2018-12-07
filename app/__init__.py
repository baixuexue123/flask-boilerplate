from flask import Flask
from flask_session import Session

from config import config


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

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
