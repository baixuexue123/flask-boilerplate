from flask_sqlalchemy import SQLAlchemy

from services.models.base import BaseModel
from services.models.auth import User, Group, Permission


db = SQLAlchemy(model_class=BaseModel)
