from functools import wraps
from flask import g, abort, request

from app.cache import cache


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return abort(401)
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return abort(401)
        if not g.user.is_stuff:
            return abort(403)
        return f(*args, **kwargs)
    return wrapper


def permission_required(permissions):
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if g.user is None:
                return abort(401)

            if g.user.is_superuser:
                return

            if permissions is None:
                perms = []
            elif isinstance(permissions, str):
                perms = [permissions]
            elif isinstance(permissions, (list, tuple)):
                perms = permissions
            else:
                raise ValueError('permissions: str, list, tuple is required')

            if perms:
                if not g.user.has_perms(permissions):
                    abort(403)
            return f(*args, **kwargs)
        return wrapper
    return _decorator


def cached(timeout=5*60, key='view/%s'):
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return wrapper
    return _decorator
