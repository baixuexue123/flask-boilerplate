import os
import sys

from sqlalchemy import or_, text, union, and_
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm.scoping import scoped_session

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(basedir)

from app import create_app

app = create_app()

with app.app_context():
    from app import db
    from app.models.user import Group, User, Permission, user_permissions, user_groups, group_permissions
    from app.utils.crypt import get_random_string, hashpw

    # metadata = db.MetaData(bind=db.engine)
    # Users = db.Table('user', metadata, autoload=True)
    # print(Users.columns)
    #
    # ins = Users.insert().values(name='foo')
    # print(ins)
    # db.session.execute(ins)

    # db.session.execute(Users.insert(), username='admin',
    #                    password=hashpw('123'),
    #                    name='admin'*10,
    #                    email='xxx@jd.com')

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
    # group = Group(name='group4', memo='group')
    # db.session.add(group)
    # db.session.flush()
    # print(group.id)
    # db.session.commit()

    # user = User(
    #     username='admin111', password=hashpw('123'),
    #     name='admin', email='xxx@jd.com'
    # )
    # db.session.add(user)
    # db.session.flush()
    # print(user.id)

    # user = User.query.get(3)
    # print(user)
    #
    # groups = Group.query.filter(Group.id.in_([2, 3, 4]))
    # user.groups.extend(groups)
    #
    # db.session.commit()

    # update
    # user = User.query.get(1)
    # print(user.as_dict())
    # user.name = 'admin'
    # db.session.commit()
    # print(user.as_dict())

    # Group.query.filter(Group.id == 2).update({'name': 'group2'})
    # User.query.filter(User.id == 2).update({'name': 'admin'})
    # print(group.as_dict())

    # get
    # print(Group.query.get(10))

    # query with_entities
    # print(User.query.with_entities(User.name).filter(User.is_active == 1).all())
    #
    # query = User.query
    # query.filter(or_(User.username == '111', User.name == '111')).filter(User.is_active == 1).all()

    # filters
    filters = [
        User.username == '111',
        User.name == '222'
    ]
    users = User.query.filter(or_(*filters)).all()

    # exists
    # print(db.session.query((User.query.filter(User.username == '111').exists())).scalar())

    # join
    # db.session.query(Permission).join(User).filter(User.id == 1).all()
    # plugins = Plugin.query.join(Plugin.group).filter(Plugin.name == 'aaa').all()
    # user = User.query.options(joinedload(User.groups)).filter(User.name == "admin").first()
    # print(user.groups)
