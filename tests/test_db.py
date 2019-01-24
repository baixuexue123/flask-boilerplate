import os
import sys

from sqlalchemy import or_, text, union, and_, exists, select
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm.scoping import scoped_session

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(basedir)

from app import create_app

app = create_app()

with app.app_context():
    from app import db
    from app.models.user import Group, User, Permission, \
	user_permissions, user_groups, group_permissions
    from app.utils.crypt import get_random_string, hashpw

    # 自动加载表结构

    # metadata = db.MetaData(bind=db.engine)
    # Users = db.Table('user', metadata, autoload=True)
    # print(Users.columns)
    #
    # ins = Users.insert().values(name='foo')
    # print(ins)
    # db.session.execute(ins)

    # db.session.execute(Users.insert(), username='admin',
    #                    password=hashpw('qwe123'),
    #                    name='管理员'*10,
    #                    email='baixue12@jd.com')

    # class Users(db.Model):
    #     __tablename__ = 'user'
    #     __table_args__ = {
    #         'autoload': True,
    #         'schema': 'demo',
    #         'autoload_with': db.engine
    #     }
    #
    # print(dir(Users))

    # insert

    # group = Group(name='group4', memo='分组四')
    # db.session.add(group)
    # db.session.flush()
    # print(group.id)
    # db.session.commit()

    # user = User(
    #     username='admin111',
    #     password=hashpw('qwe123'),
    #     name='管理员111',
    #     email='baixue12@jd.com'
    # )
    # db.session.add(user)
    # db.session.flush()
    # print(user.id)

    # update

    # user = User.query.get(1)
    # print(user.as_dict())
    # user.name = '管理员一'
    # db.session.commit()
    # print(user.as_dict())

    # groups = Group.query.filter(Group.id.in_([2, 3, 4]))
    # user.groups = groups  # extend append
    # db.session.commit()

    # User.query.filter(User.id == 2).update({'name': 'admin'})
    # Group.query.filter(Group.id == 2).update({'name': 'group2'})
    # print(group.as_dict())

    # query

    # user = User.query.get(3)
    # print(user)
    # print(user.groups.filter(Group.name == '111'))   # relationship(lazy='dynamic')
    # print(user.groups)

    # with_entities
    # print(User.query.with_entities(User.name).filter_by(is_active=1).all())

    # filters = [
    #     User.username == '111',
    #     User.name == '222'
    # ]
    # query = User.query
    # query = query.filter(or_(*filters))
    # query.filter(User.is_active == 1).all()

    # exists
    # print(db.session.query((User.query.filter_by(username='111').exists())).scalar())

    # join
    # user = User.query.options(
    #     joinedload(User.groups),
    #     joinedload(User.permissions)).get(3)
    # print(user)
    # print(user.groups)
    # print(user.permissions)

    Permission.query.with_entities(Permission.id, Permission.name)
        .join(group_permissions, Permission.id == group_permissions.c.permission_id)
        .filter(group_permissions.c.group_id.in_([1, 2, 3])).all()

