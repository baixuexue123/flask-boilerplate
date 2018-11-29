from flask import Flask, jsonify, session, request, g, current_app
from flask import Blueprint


app = Blueprint()


@app.route('/api/login', methods=['POST'])
def login():
    return


@app.route('/api/logout', methods=['GET'])
def logout():
    return
