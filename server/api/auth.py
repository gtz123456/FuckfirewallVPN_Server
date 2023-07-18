from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from server.models import User
from server.api.errors import error_response

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.currentUser = user
    return user.validatePassword(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)



token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    token_auth.current_user = User.checkToken(token) if token else None
    return token_auth.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(401)