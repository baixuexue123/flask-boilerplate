import os
import redis

basedir = os.path.abspath(os.path.dirname(__file__))


if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    APP_NAME = os.environ.get('FLASK_APP') or 'FLASK-APP'
    SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
    SQLALCHEMY_ECHO = True

    MAX_CONTENT_LENGTH = 1024 * 1024 * 50

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = '172.25.61.75:6379'
    DATABASE_URI = 'mysql+pymysql://demo:demo123@172.25.61.75:3306/demo?charset=utf8'

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False   # 关闭浏览器session不失效
    SESSION_USE_SIGNER = False  # 不对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis.Redis(host='172.25.61.75', port='6379', db=0)

    CACHE_HOST = '172.25.61.75'
    CACHE_PORT = 6379
    CACHE_DB = 1
    CACHE_PASSWORD = None
    CACHE_KEY_PREFIX = 'cache:'
    CACHE_DEFAULT_TIMEOUT = 120

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    DEBUG = True
    REDIS_URL = 'localhost:6379'
    DATABASE_URI = 'mysql+pymysql://demo:demo123@localhost:3306/demo?charset=utf8'


class ProductionConfig(Config):
    DEBUG = False
    REDIS_URL = 'localhost:6379'
    DATABASE_URI = 'mysql+pymysql://demo:demo123@localhost:3306/demo?charset=utf8'
    SQLALCHEMY_ECHO = False

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False   # 关闭浏览器session不失效
    SESSION_USE_SIGNER = False  # 不对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis.Redis(host='172.25.61.75', port='6379', db=0)

    CACHE_HOST = '172.25.61.75'
    CACHE_PORT = 6379
    CACHE_DB = 1
    CACHE_PASSWORD = None
    CACHE_KEY_PREFIX = 'cache:'
    CACHE_DEFAULT_TIMEOUT = 120

    LOG_DIR = os.path.join(basedir, 'logs')
    LOG_MAXBYTES = 1024 * 1024 * 100  # 100M -- 单个log文件的大小
    LOG_BACKUPCOUNT = 8  # log文件备份数量

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import os
        import logging
        from logging.handlers import RotatingFileHandler

        os.makedirs(cls.LOG_DIR, exist_ok=True)

        verbose = logging.Formatter(
            fmt='[%(asctime)s - %(name)s - %(module)s - %(lineno)d] %(levelname)-8s\n%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple = logging.Formatter(
            fmt='[%(asctime)s - %(name)s] %(levelname)-8s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        log_file = os.path.join(cls.LOG_DIR, '%s.log' % cls.APP_NAME)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=cls.LOG_MAXBYTES,
            backupCount=cls.LOG_BACKUPCOUNT
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(simple)

        err_file = os.path.join(cls.LOG_DIR, '%s.error.log' % cls.APP_NAME)
        error_handler = logging.FileHandler(err_file, mode='w')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(verbose)

        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
