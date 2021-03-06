from functools import wraps
from flask import g, abort


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
                if not g.user.has_perms(perms):
                    abort(403)
            return f(*args, **kwargs)
        return wrapper
    return _decorator

