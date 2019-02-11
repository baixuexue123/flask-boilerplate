import hashlib
from functools import wraps

from flask import request
from flask import current_app as app
from werkzeug.contrib.cache import RedisCache


CACHE = RedisCache(
    host=app.config['CACHE_HOST'],
    port=app.config['CACHE_PORT'],
    db=app.config['CACHE_DB'],
    password=app.config['CACHE_PASSWORD'],
    default_timeout=app.config['CACHE_DEFAULT_TIMEOUT'],
    key_prefix=app.config['CACHE_KEY_PREFIX']
)


def _hash_query_string():
    args_as_sorted_tuple = tuple(sorted((pair for pair in request.args.items(multi=True))))
    args_as_bytes = str(args_as_sorted_tuple).encode()
    hashed_args = str(hashlib.md5(args_as_bytes).hexdigest())
    return hashed_args


def _make_cache_key(key_prefix, use_qs):
    if '%s' in key_prefix:
        cache_key = key_prefix % request.path
    else:
        cache_key = key_prefix

    if use_qs:
        cache_key += ':%s' % _hash_query_string()

    return cache_key


def cached(timeout=5*60, key_prefix='view:%s', use_qs=False):
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache_key = _make_cache_key(key_prefix, use_qs)
            rv = CACHE.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            CACHE.set(cache_key, rv, timeout=timeout)
            return rv
        return wrapper
    return _decorator
