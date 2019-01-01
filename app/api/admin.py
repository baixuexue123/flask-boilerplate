from flask import Blueprint, request

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User, Group, Permission
from app.decorators import admin_required
from app.utils.crypt import hashpw

from . import APIView, success, fail

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@bp.route('/user/<int:user_id>/pwd', methods=['POST'])
@admin_required
def reset_pwd(user_id):
    user = User.query.get(user_id)
    if user is None:
        return fail(msg='User: %s does not exists' % user_id)

    new_password = request.json['new_password']
    if len(new_password) < 6:
        return fail(msg='Minimum password length of 6 characters')

    user.password = hashpw(new_password)
    db.session.commit()
    return success()


# 设置用户的组
@bp.route('/user/<int:user_id>/groups', methods=['POST'])
@admin_required
def user_groups(user_id):
    group_ids = request.json['group_ids']

    user = User.query.get(user_id)
    if user is None:
        return fail(msg='User: %s does not exists' % user_id)

    groups = Group.query.filter(Group.id.in_(group_ids)).all()
    user.groups = groups
    db.session.commit()
    return success()


@bp.route('/user/<int:user_id>/permissions', methods=['POST'])
@admin_required
def user_permissions(user_id):
    perm_ids = request.json['perm_ids']

    user = User.query.get(user_id)
    if user is None:
        return fail(msg='User: %s does not exists' % user_id)

    perms = Permission.query.filter(Permission.id.in_(perm_ids)).all()
    user.permissions = perms
    db.session.commit()
    return success()


@bp.route('/group/<int:group_id>/permissions', methods=['POST'])
@admin_required
def group_permissions(group_id):
    perm_ids = request.json['perm_ids']

    group = Group.query.get(group_id)
    if group is None:
        return fail(msg='Group: %s does not exists' % group_id)

    perms = Permission.query.filter(Permission.id.in_(perm_ids)).all()
    group.permissions = perms
    db.session.commit()
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
                search = '%' + search + '%'
                query = query.filter(or_(User.username.like(search), User.name.like(search)))
            page = query.paginate(page=page_no, per_page=page_size, max_per_page=100)
            users = [u.as_dict() for u in page.items]
            return success(users=users, total=page.total, page_no=page_no, page_size=page_size)

    def post(self):
        username = request.json['username']
        password = request.json['password']
        name = request.json['name']
        email = request.json['email']
        is_superuser = request.json['is_superuser']
        is_stuff = request.json['is_stuff']

        password = hashpw(password)
        user = User(
            username=username, password=password,
            name=name, email=email,
            is_stuff=is_stuff, is_superuser=is_superuser
        )
        db.session.add(user)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='User: %s duplicate' % username)

        groups = request.json.get('groups')
        permissions = request.json.get('permissions')
        if groups:
            groups = Group.query.filter(Group.id.in_(groups)).all()
            user.groups = groups
        if permissions:
            permissions = Permission.query.filter(Permission.id.in_(permissions)).all()
            user.permissions = permissions

        db.session.commit()
        return success(user_id=user.id)

    def put(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return fail(msg='User: %s does not exists' % user_id)

        if 'username' in request.json:
            user.username = request.json['username']
        if 'name' in request.json:
            user.name = request.json['name']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'is_superuser' in request.json:
            user.is_superuser = request.json['is_superuser']
        if 'is_stuff' in request.json:
            user.is_stuff = request.json['is_stuff']
        if 'is_active' in request.json:
            user.is_active = request.json['is_active']

        groups = request.json.get('groups', [])
        groups = Group.query.filter(Group.id.in_(groups)).all()
        user.groups = groups
        permissions = request.json.get('permissions', [])
        permissions = Permission.query.filter(Permission.id.in_(permissions)).all()
        user.permissions = permissions

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return fail(msg='User: %s duplicate' % request.json['username'])
        return success()

    def delete(self, user_id):
        user = User.query.get(user_id)
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

        permissions = request.json.get('permissions', [])
        if permissions:
            permissions = Permission.query.filter(Permission.id.in_(permissions)).all()
            group.permissions = permissions

        db.session.commit()
        return success(group_id=group.id)

    def put(self, group_id):
        group = Group.query.get(group_id)
        if group is None:
            return fail(msg='Group: %s does not exists' % group_id)

        group.name = request.json['name']
        group.memo = request.json['memo']
        permissions = request.json.get('permissions')
        permissions = Permission.query.filter(Permission.id.in_(permissions)).all()
        group.permissions = permissions

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
        memo = request.json.get('memo', '')
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


register_api(UserAPI, 'users', '/users/', pk='user_id')
register_api(GroupAPI, 'groups', '/groups/', pk='group_id')


permissions_api = PermissionAPI.as_view('permissions')
bp.add_url_rule('/permissions/', view_func=permissions_api, methods=['GET', 'POST'])
bp.add_url_rule('/permissions/<int:perm_id>', view_func=permissions_api, methods=['PUT', 'DELETE'])
