from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, DateTime

from . import metadata, Base


user_groups = Table(
    'user_groups', metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)


user_permissions = Table(
    'user_permissions', metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('permission_id', Integer, ForeignKey('permission.id'))
)


group_permissions = Table(
    'group_permissions', metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('permission_id', Integer, ForeignKey('permission.id'))
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_stuff = Column(Boolean, nullable=False, default=False)

    change_ts = Column(DateTime, nullable=False)
    create_ts = Column(DateTime, nullable=False)

    groups = relationship('Group', secondary=user_groups, back_populates='users')
    permissions = relationship('Permission', secondary=user_permissions)


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    memo = Column(String(200), nullable=False, default='')

    users = relationship("User", secondary=user_groups, back_populates='groups')
    permissions = relationship("Permission", secondary=group_permissions)


class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    memo = Column(String(200), nullable=False, default='')
