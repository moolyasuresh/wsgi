import flask
from flask import Flask, request, jsonify, Response
import json
from functools import wraps
import traceback
import socket
import sys
import os
# sys.path.append(os.path.abspath("/wsgi"))
from wsgi.config.logging import LoggingHandler
from wsgi.businessController.testClass import TestClass

logging_handler = LoggingHandler()
file_handler = logging_handler.log_config()

app = Flask(__name__)
app.logger.addHandler(file_handler)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'admin'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    response = { "error" :{ "name" : "401 UNAUTHORIZED", "message" : 'You are not authorized to access this URL.' }, "status" : "ERROR" }
    resp = jsonify(response)
    resp.status_code = 200
    # resp.headers['WWW-Authenticate']: 'Basic realm="Login Required"'
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
           return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/train', methods = ['POST'])
@requires_auth
def train_main():
    try:
        app.logger.error(request)
        app.logger.error(request.headers)
        incoming_data = json.loads(request.data)
        check = TestClass()
        resp = check.test_func()
        return jsonify(resp)
    except Exception:
        traceback_error = traceback.format_exc()
        message = {
            'status': 'ERROR',
            'error': {
                'name': 'Internal Server Error',
                'message' : traceback_error
            }
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

@app.errorhandler(500)
def internal_error(error):
    traceback_error = traceback.format_exc()
    message = {
        'status': 'ERROR',
        'error': {
            'name': 'Internal Server Error',
            'message' : traceback_error
        }
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

# app.run()

