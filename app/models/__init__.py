from flask import current_app as app

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True,
                       echo=app.config['SQLALCHEMY_ECHO'])

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Base.query = db_session.query_property()


def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
