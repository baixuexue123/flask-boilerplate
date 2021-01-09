import enum

from flask_sqlalchemy import Model
from sqlalchemy_utils.types import Choice
from sqlalchemy.sql.expression import ClauseElement


class BaseModel(Model):

    def as_dict(self):
        res = {}
        for c in self.__table__.columns:
            field = getattr(self, c.name)
            if isinstance(field, Choice):
                res['%s_display' % c.name] = field.value
                res[c.name] = field.code
            elif isinstance(field, enum.Enum):
                res['%s_display' % c.name] = field.name
                res[c.name] = field.value
            else:
                res[c.name] = field
        return res

    def save(self):
        from services.models import db
        db.session.add(self)
        db.session.commit()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True
