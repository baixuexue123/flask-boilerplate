import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = 'APP_NAME'
    SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = 'http://localhost:6379'
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(Config):
    DEBUG = False
    REDIS_URL = 'http://localhost:6379'
    SQLALCHEMY_DATABASE_URI = ''
