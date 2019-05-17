import enum

from flask_sqlalchemy import Model
from sqlalchemy_utils.types import Choice


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
        from app import db
        db.session.add(self)
        db.session.commit()
