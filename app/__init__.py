import os
import logging

import flask
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from celery import Celery
from kombu import Queue

from config import config

from .models.base import BaseModel
from .escape import JSONEncoder

db = SQLAlchemy(model_class=BaseModel)

flask_logger = logging.getLogger('flask.app')
flask_logger.handlers.clear()
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers.clear()
sqlalchemy_logger = logging.getLogger('sqlalchemy')
sqlalchemy_logger.propagate = False
watchdog_logger = logging.getLogger('watchdog.observers.inotify_buffer')
watchdog_logger.propagate = False


class FlaskCelery(Celery):

    def __init__(self, *args, **kwargs):
        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()
        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.conf.update(
            result_backend=app.config['CELERY_RESULT_BACKEND'],
            broker_url=app.config['CELERY_BROKER_URL'],
            timezone='Asia/Shanghai',
            task_ignore_result=True,
            worker_max_tasks_per_child=1000,
            task_create_missing_queues=True,
            task_default_queue='queue:default',
            imports=(
                'app.tasks'
            ),
            task_queues=(
                Queue('queue:default'),
                Queue('queue:log'),
            ),
            task_routes={
                'log.log_request': {'queue': 'queue:log'},
            }
        )


celery = FlaskCelery(__name__)


def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV') or 'development'
    app.config.from_object(config[env])
    config[env].init_app(app)
    app.json_encoder = JSONEncoder

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    Session(app)
    db.init_app(app)
    celery.init_app(app)

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
