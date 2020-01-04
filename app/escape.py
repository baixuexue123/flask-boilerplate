from datetime import datetime, date

from flask._compat import text_type
from itsdangerous import json as _json


class JSONEncoder(_json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if hasattr(o, '__html__'):
            return text_type(o.__html__())
        return _json.JSONEncoder.default(self, o)
