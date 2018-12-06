import os

import redis

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = 'APP_NAME'
    SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'

    MAX_CONTENT_LENGTH = 1024 * 1024 * 50

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = '172.25.61.75:6379'
    DATABASE_URI = 'mysql+pymysql://demo:demo123@172.25.61.75:3306/demo?charset=utf8'

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False  # True: 则关闭浏览器session就失效
    SESSION_USE_SIGNER = False  # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis.Redis(host='172.25.61.75', port='6379', db=0)

    CACHE_HOST = '172.25.61.75'
    CACHE_PORT = 6379
    CACHE_DB = 1
    CACHE_PASSWORD = None
    CACHE_KEY_PREFIX = 'cache:'
    CACHE_DEFAULT_TIMEOUT = 120

    LOG_DIR = os.path.join(basedir, 'logs')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')

        # email errors to the administrators
        import logging
        from logging.handlers import RotatingFileHandler
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(process)d %(thread)d '
            '%(pathname)s %(lineno)s %(message)s')

        # FileHandler Info
        file_handler = RotatingFileHandler(filename=cls.LOG_DIR)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # FileHandler Error
        file_handler_error = RotatingFileHandler(filename=cls.LOG_DIR)
        file_handler_error.setFormatter(formatter)
        file_handler_error.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler_error)


class TestingConfig(Config):
    DEBUG = True
    REDIS_URL = 'localhost:6379'
    DATABASE_URI = 'mysql+pymysql://demo:demo123@localhost:3306/demo?charset=utf8'


class ProductionConfig(Config):
    DEBUG = False
    REDIS_URL = 'localhost:6379'
    DATABASE_URI = 'mysql+pymysql://demo:demo123@localhost:3306/demo?charset=utf8'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'
