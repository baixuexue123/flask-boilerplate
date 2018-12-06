from flask import current_app as app
from flask import jsonify


@app.errorhandler(401)
def page_not_found(error):
    return jsonify(code=401, msg='Unauthorized')


@app.errorhandler(403)
def page_not_found(error):
    return jsonify(code=403, msg='Forbidden')


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(code=404, msg='Page not found')


@app.errorhandler(500)
def page_not_found(error):
    return jsonify(code=500, msg='Server Error')
