import lazy_object_proxy

from flask import session, request, g
from flask import Blueprint
from flask import current_app as app

from app.models.user import User
from app.utils.crypt import checkpw
from app.decorators import login_required

from . import success, fail

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@app.before_request
def detect_user_language():
    g.language = request.cookies.get('lang')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = lazy_object_proxy.Proxy(lambda: User.query.get(user_id))


@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter(User.username == username).first()

    if user is None:
        app.logger.info('用户:%s 不存在' % username)
        return fail(msg='Incorrect username or password')
    if not user.is_active:
        app.logger.info('用户:%s 未激活' % username)
        return fail(msg='Incorrect username or password')
    if not checkpw(password, user.password):
        app.logger.info('用户:%s 密码不正确' % username)
        return fail(msg='Incorrect username or password')

    session.clear()
    session['user_id'] = user.id
    app.logger.info('用户:%s(%s) - 登录成功' % (user.username, user.name))
    return success(user_id=user.id)


@bp.route('/user_info', methods=['GET'])
@login_required
def get_user_info():
    return success(user=g.user.as_dict(verbose=True))


@bp.route('/check', methods=['GET'])
@login_required
def check_auth():
    return success(user=g.user.as_dict(verbose=True))


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    app.logger.info('用户:%s(%s) - 退出' % (g.user.username, g.user.name))
    session.clear()
    return success()
