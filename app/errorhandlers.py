from flask import Blueprint
from flask import jsonify

bp = Blueprint('errors', __name__)


@bp.errorhandler(401)
def page_not_found(error):
    return jsonify(code=401, msg='Unauthorized')


@bp.errorhandler(403)
def page_not_found(error):
    return jsonify(code=403, msg='Forbidden')


@bp.errorhandler(404)
def page_not_found(error):
    return jsonify(code=404, msg='Page not found')


@bp.errorhandler(500)
def page_not_found(error):
    return jsonify(code=500, msg='Server Error')
