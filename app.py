import os

from flask import Flask
from flask.helpers import get_env
from flask_session import Session

app = Flask('dting')

if get_env() == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

Session(app)

with app.app_context():
    from api import auth
    app.register_blueprint(auth.bp)

    from api import admin
    app.register_blueprint(admin.bp)

    import errorhandlers
    from models import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
