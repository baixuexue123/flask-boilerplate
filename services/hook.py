import lazy_object_proxy

from flask import request, session, g
from flask import current_app as app

from services.models.auth import User


@app.before_request
def detect_user_language():
    g.language = request.cookies.get('lang')


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = lazy_object_proxy.Proxy(lambda: User.query.get(user_id))
