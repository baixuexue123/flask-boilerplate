from flask import current_app
from werkzeug.contrib.cache import RedisCache

cache = RedisCache(
    host=current_app.config['CACHE_HOST'],
    port=current_app.config['CACHE_PORT'],
    db=current_app.config['CACHE_DB'],
    password=current_app.config['CACHE_PASSWORD'],
    default_timeout=current_app.config['CACHE_DEFAULT_TIMEOUT'],
    key_prefix=current_app.config['CACHE_KEY_PREFIX']
)
