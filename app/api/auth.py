from flask import session, request, g
from flask import Blueprint
from flask import current_app as app

from app.models.user import User
from app.utils.crypt import checkpw
from app.decorators import login_required

from . import success, fail

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()


@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter(User.name == username).first()
    if user is None:
        app.logger.info('用户:%s 不存在' % username)
        return fail(msg='Incorrect username or password')
    elif not checkpw(user.password, password):
        app.logger.info('用户:%s 密码不正确' % username)
        return fail(msg='Incorrect username or password')

    session.clear()
    session['user_id'] = user.id
    app.logger.info('用户:%s(%s) - 登录' % (user.name, user.username))
    return success()


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return success()
