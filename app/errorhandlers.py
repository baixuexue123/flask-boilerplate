from flask import jsonify
from flask import current_app as app
from werkzeug import exceptions


@app.errorhandler(exceptions.BadRequest)
def bad_request(error):
    return jsonify(code=100400, msg='Bad Request', error=str(error))


@app.errorhandler(exceptions.Unauthorized)
def unauthorized(error):
    return jsonify(code=100401, msg='Unauthorized', error=str(error))


@app.errorhandler(exceptions.Forbidden)
def forbidden(error):
    return jsonify(code=100403, msg='Forbidden', error=str(error))


@app.errorhandler(exceptions.NotFound)
def page_not_found(error):
    return jsonify(code=100404, msg='Page Not Found', error=str(error))


@app.errorhandler(exceptions.InternalServerError)
def internal_server_error(error):
    return jsonify(code=100500, msg='Internal Server Error', error=str(error))
