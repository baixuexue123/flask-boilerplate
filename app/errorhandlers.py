from flask import Blueprint, jsonify

bp = Blueprint('errors', __name__)


@bp.errorhandler(400)
def page_not_found(error):
    return jsonify(code=100400, msg='Bad Request')


@bp.errorhandler(401)
def page_not_found(error):
    return jsonify(code=100401, msg='Unauthorized')


@bp.errorhandler(403)
def page_not_found(error):
    return jsonify(code=100403, msg='Forbidden')


@bp.errorhandler(404)
def page_not_found(error):
    return jsonify(code=100404, msg='Page Not Found')


@bp.errorhandler(500)
def page_not_found(error):
    return jsonify(code=100500, msg='Server Error')
