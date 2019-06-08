from flask import jsonify
from flask import current_app as app
from werkzeug import exceptions


@app.errorhandler(exceptions.BadRequest)
def bad_request(error):
    res = jsonify(code=100400, msg='Bad Request', error=str(error))
    res.status_code = 400
    return res


@app.errorhandler(exceptions.Unauthorized)
def unauthorized(error):
    res = jsonify(code=100401, msg='Unauthorized', error=str(error))
    res.status_code = 401
    return res


@app.errorhandler(exceptions.Forbidden)
def forbidden(error):
    res = jsonify(code=100403, msg='Forbidden', error=str(error))
    res.status_code = 403
    return res


@app.errorhandler(exceptions.NotFound)
def page_not_found(error):
    res = jsonify(code=100404, msg='Page Not Found', error=str(error))
    res.status_code = 404
    return res


@app.errorhandler(exceptions.InternalServerError)
def internal_server_error(error):
    res = jsonify(code=100500, msg='Internal Server Error', error=str(error))
    res.status_code = 500
    return res
