from werkzeug.utils import cached_property

from app import db

user_groups = db.Table(
    'user_groups', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


user_permissions = db.Table(
    'user_permissions', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


group_permissions = db.Table(
    'group_permissions', db.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=True)

    is_superuser = db.Column(db.Boolean, nullable=False, server_default=db.text('0'))
    is_stuff = db.Column(db.Boolean, nullable=False, server_default=db.text('0'))
    is_active = db.Column(db.Boolean, nullable=False, server_default=db.text('1'))

    change_ts = db.Column(db.DateTime, nullable=False, server_onupdate=db.func.now(), server_default=db.func.now())
    create_ts = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    groups = db.relationship('Group', secondary=user_groups, back_populates='users')
    permissions = db.relationship('Permission', secondary=user_permissions)

    def as_dict(self, verbose=False):
        data = super(User, self).as_dict()
        del data['password']
        if verbose:
            data['groups'] = self.get_groups()
            data['permissions'] = self.get_permissions()
        return data

    def get_groups(self):
        return [{'id': g.id, 'name': g.name} for g in self.groups]

    def get_permissions(self):
        permissions = {p.id: {'id': p.id, 'name': p.name} for p in self.permissions}
        perms = Permission.query.with_entities(Permission.id, Permission.name)\
            .join(group_permissions, Permission.id == group_permissions.c.permission_id)\
            .filter(group_permissions.c.group_id.in_([g.id for g in self.groups])).all()
        for p in perms:
            permissions[p.id] = {'id': p.id, 'name': p.name}
        return list(permissions.values())

    @cached_property
    def all_permissions(self):
        perms = db.session.execute("""
            SELECT
                p1.name
            FROM permission p1
                JOIN user_permissions up ON p1.id = up.permission_id
            WHERE up.user_id=:user_id

            UNION

            SELECT
                p2.name
            FROM permission p2
                JOIN group_permissions gp ON gp.permission_id = p2.id
                JOIN user_groups ug ON gp.group_id = ug.group_id
            WHERE ug.user_id=:user_id
        """, {'user_id': self.id})
        return {p.name for p in perms}

    def has_perms(self, perms):
        return set(perms) < self.all_permissions


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    memo = db.Column(db.String(200), nullable=False, default='')

    users = db.relationship("User", secondary=user_groups, back_populates='groups')
    permissions = db.relationship("Permission", secondary=group_permissions)

    def as_dict(self, verbose=False):
        data = super(Group, self).as_dict()
        if verbose:
            data['permissions'] = self.get_permissions()
        return data

    def get_permissions(self):
        return [p.as_dict() for p in self.permissions]


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    memo = db.Column(db.String(200), nullable=False, default='')
