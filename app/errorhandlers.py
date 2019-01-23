from werkzeug import exceptions
from flask import Blueprint, jsonify

bp = Blueprint('errors', __name__)


@bp.errorhandler(exceptions.BadRequest)
def bad_request(error):
    return jsonify(code=100400, msg='Bad Request')


@bp.errorhandler(exceptions.Unauthorized)
def unauthorized(error):
    return jsonify(code=100401, msg='Unauthorized')


@bp.errorhandler(exceptions.Forbidden)
def forbidden(error):
    return jsonify(code=100403, msg='Forbidden')


@bp.errorhandler(exceptions.NotFound)
def page_not_found(error):
    return jsonify(code=100404, msg='Page Not Found')


@bp.errorhandler(exceptions.InternalServerError)
def internal_server_error(error):
    return jsonify(code=100500, msg='Internal Server Error')

