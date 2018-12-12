from sqlalchemy import or_, text, union
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm.scoping import scoped_session

from app import create_app

app = create_app()

with app.app_context():
    from app import db
    from app.models.user import Group, User, Permission, user_permissions, user_groups, group_permissions
    from app.utils.crypt import get_random_string, hashpw

    # insert
    # group = Group(name='group4', memo='分组四')
    # db.session.add(group)
    # db.session.flush()
    # print(group.id)
    # db.session.commit()

    # get
    # print(Group.query.get(10))

    # query
    # print(User.query.filter(User.is_active == 1).all())
    #
    # query = User.query
    # query.filter(or_(User.username == '111', User.name == '111')).filter(User.is_active == 1).all()

    # join
    # db.session.query(Permission).join(User).filter(User.id == 1).all()

    # update
    # Group.query.filter(Group.id == 2).update({'name': 'group2'})

    # print(group.as_dict())
