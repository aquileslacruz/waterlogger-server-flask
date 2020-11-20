from flask import request, jsonify, Response, json
from flask_server.utilities import token_required
from flask_server.models import User
from flask_server import db, bcrypt
from werkzeug.exceptions import MethodNotAllowed, Unauthorized
from . import auth_blueprint


@auth_blueprint.route('/', methods=['GET', 'POST'])
def token_handler():
    if request.method == 'GET':
        return reload_token()
    elif request.method == 'POST':
        return create_token()
    raise MethodNotAllowed


def create_token():
    username = request.authorization.get('username')
    password = request.authorization.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    if not user or not user.is_correct_password(password):
        raise Unauthorized
    token = user.encode_auth_token()
    return jsonify(access_token=token.decode()), 200


@token_required
def reload_token(user):
    token = user.encode_auth_token()
    return jsonify(access_token=token.decode()), 200
