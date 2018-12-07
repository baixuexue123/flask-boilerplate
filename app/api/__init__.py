from flask import request
from flask.views import MethodView
from flask import jsonify


def success(code=0, msg='', **kwargs):
    return jsonify(code=code, msg=msg, data=kwargs)


def fail(code=1, msg='', **kwargs):
    return jsonify(code=code, msg=msg, data=kwargs)


class APIView(MethodView):

    @property
    def query_params(self):
        return request.args

    @property
    def json_params(self):
        return request.get_json(force=True)
