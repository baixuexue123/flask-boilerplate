from flask import current_app as app
from werkzeug.contrib.cache import RedisCache

cache = RedisCache(
    host=app.config['CACHE_HOST'],
    port=app.config['CACHE_PORT'],
    db=app.config['CACHE_DB'],
    password=app.config['CACHE_PASSWORD'],
    default_timeout=app.config['CACHE_DEFAULT_TIMEOUT'],
    key_prefix=app.config['CACHE_KEY_PREFIX']
)
