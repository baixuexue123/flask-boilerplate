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


def register_api(bp, view, endpoint, url, pk='pk', pk_type='int'):
    func = view.as_view(endpoint)
    bp.add_url_rule(url, defaults={pk: None}, view_func=func, methods=['GET'])
    bp.add_url_rule(url, view_func=func, methods=['POST'])
    bp.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=func, methods=['GET', 'PUT', 'DELETE'])
