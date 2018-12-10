from app import db


user_groups = db.Table(
    'user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


user_permissions = db.Table(
    'user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


group_permissions = db.Table(
    'group_permissions',
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

    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    is_stuff = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    change_ts = db.Column(db.DateTime, nullable=False)
    create_ts = db.Column(db.DateTime, nullable=False)

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
        for group in self.groups:
            for perm in group.permissions:
                permissions[perm.id] = {'id': perm.id, 'name': perm.name}
        return permissions


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
