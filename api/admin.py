from flask import request
from flask import Blueprint

from models import db_session
from models.user import User, Group, Permission
from base.decorators import permission_required

from . import APIView, success, fail

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@bp.route('/index', methods=['GET'])
def index():
    return success()


@bp.route('/reset/pwd', methods=['POST'])
def reset_pwd():
    current_password = request.form['current_password']
    new_password1 = request.form['new_password1']
    new_password2 = request.form['new_password2']
    return success()


class UserAPI(APIView):

    def get(self, user_id):
        if user_id is not None:
            user = User.query.filter(User.id == user_id).first()
            return success(user=user)
        else:
            page_size = request.args.get('page_size', 20, type=int)
            page_no = request.args.get('page_no', 1, type=int)
            users = User.query.limit(page_size).offset((page_no-1)*page_size).all()
            return success(users=users)

    def post(self):
        return success()

    def put(self, user_id):
        return success()

    def delete(self):
        return success()


class GroupAPI(APIView):

    def get(self):
        page_size = request.args.get('page_size', 20, type=int)
        page_no = request.args.get('page_no', 1, type=int)
        groups = Group.query.limit(page_size).offset((page_no-1)*page_size).all()
        return success(groups=groups)

    def post(self):
        return success()

    def put(self, group_id):
        return success()

    def delete(self):
        return success()


class PermissionAPI(APIView):

    def get(self):
        db_session()
        Permission.query.all()
        return success()

    def post(self):
        return success()

    def put(self, perm_id):
        return success()

    def delete(self):
        return success()
