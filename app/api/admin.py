from flask import request, g
from flask import Blueprint
from flask import current_app as app

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User, Group, Permission
from app.decorators import admin_required
from app.utils.crypt import checkpw, hashpw, get_random_string

from . import APIView, success, fail

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@bp.route('/reset/pwd', methods=['POST'])
@admin_required
def reset_pwd():
    old_password = request.json['old_password']
    new_password1 = request.json['new_password1']
    new_password2 = request.json['new_password2']
    if new_password1 != new_password2:
        return fail(msg='两次输入密码不一致')

    user = g.user
    if not checkpw(user.password, old_password):
        app.logger.info('用户:%s 修改密码, 旧密码不正确' % user.username)
        return fail(msg='Incorrect password')

    User.query.filter(User.id == user.id).\
        update({'password': hashpw(new_password1)})
    return success()


class AdminAPI(APIView):
    decorators = [admin_required]


class UserAPI(AdminAPI):

    def get(self, user_id):
        if user_id is not None:
            user = User.query.get(user_id)
            if user is None:
                return fail(msg='User: %s does not exists' % user_id)
            return success(user=user.as_dict(verbose=True))
        else:
            page_size = request.args.get('page_size', 20, type=int)
            page_no = request.args.get('page_no', 1, type=int)
            search = request.args.get('search', '')
            query = User.query
            if search:
                query.filter(or_(User.username == search, User.name == search))
            query.filter(User.is_active == 1)
            total = query.count()
            users = query.limit(page_size).offset((page_no - 1) * page_size).all()
            users = [u.as_dict() for u in users]
            return success(users=users, total=total, page_no=page_no, page_size=page_size)

    def post(self):
        username = request.json['username']
        name = request.json['name']
        email = request.json['email']
        is_superuser = request.json['is_superuser']
        is_stuff = request.json['is_stuff']
        password = hashpw(get_random_string())  # 随机密码
        user = User(
            username=username, password=password, name=name, email=email,
            is_stuff=is_stuff, is_superuser=is_superuser
        )
        db.session.add(user)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='User: %s duplicate' % username)
        else:
            db.session.commit()
        return success(user_id=user.id)

    def put(self, user_id):
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return fail(msg='User: %s does not exists' % user_id)

        user.username = request.json['username']
        user.name = request.json['name']
        user.email = request.json['email']
        user.is_superuser = request.json['is_superuser']
        user.is_stuff = request.json['is_stuff']
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='User: %s duplicate' % request.json['username'])
        return success()

    def delete(self, user_id):
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return fail(msg='User: %s does not exists' % user_id)
        user.is_active = False
        db.session.commit()
        return success()


class GroupAPI(AdminAPI):

    def get(self, group_id):
        if group_id is not None:
            group = Group.query.get(group_id)
            if group is None:
                return fail(msg='Group: %s does not exists' % group_id)
            return success(group=group.as_dict(verbose=True))
        else:
            groups = Group.query.all()
            groups = [g.as_dict() for g in groups]
            return success(groups=groups)

    def post(self):
        name = request.json['name']
        memo = request.json['memo']
        group = Group(name=name, memo=memo)
        db.session.add(group)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='Group: %s duplicate' % name)
        else:
            db.session.commit()
        return success(group_id=group.id)

    def put(self, group_id):
        group = Group.query.get(group_id)
        if group is None:
            return fail(msg='Group: %s does not exists' % group_id)

        group.name = request.json['name']
        group.memo = request.json['memo']
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='Group: %s duplicate' % request.json['name'])
        return success()

    def delete(self, group_id):
        group = Group.query.get(group_id)
        if group is None:
            return fail(msg='Group: %s does not exists' % group_id)

        db.session.delete(group)
        db.session.commit()
        return success()


class PermissionAPI(AdminAPI):

    def get(self):
        perms = Permission.query.all()
        perms = [p.as_dict() for p in perms]
        return success(permissions=perms)

    def post(self):
        name = request.json['name']
        memo = request.json['memo']
        perm = Permission(name=name, memo=memo)
        db.session.add(perm)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='Permission: %s duplicate' % name)
        else:
            db.session.commit()
        return success(perm_id=perm.id)

    def put(self, perm_id):
        perm = Permission.query.get(perm_id)
        if perm is None:
            return fail(msg='Permission: %s does not exists' % perm_id)

        perm.name = request.json['name']
        perm.memo = request.json['memo']
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='Permission: %s duplicate' % request.json['name'])
        return success()

    def delete(self, perm_id):
        perm = Permission.query.get(perm_id)
        if perm is None:
            return fail(msg='Permission: %s does not exists' % perm_id)

        db.session.delete(perm)
        db.session.commit()
        return success()


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    bp.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    bp.add_url_rule(url, view_func=view_func, methods=['POST'])
    bp.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


register_api(UserAPI, 'users', '/users/')
register_api(GroupAPI, 'groups', '/groups/')
register_api(PermissionAPI, 'permissions', '/permissions/')
