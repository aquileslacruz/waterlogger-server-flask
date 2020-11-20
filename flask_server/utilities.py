from flask import Response, json, request, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from werkzeug.exceptions import HTTPException, Unauthorized
from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            raise Unauthorized
        
        user_id = None
        token = request.headers['Authorization'].replace('Bearer ', '')

        try:
            from flask_server.models import User
            from flask_server import db
            user_id = User.decode_auth_token(token)
            user = db.session.query(User).filter(User.id == user_id).first()
            if not user:
                raise Unauthorized
        except:
            raise Unauthorized

        return f(user, *args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            raise Unauthorized
        
        user_id = None
        token = request.headers['Authorization'].replace('Bearer ', '')

        try:
            from flask_server.models import User
            from flask_server import db
            user_id = User.decode_auth_token(token)
            user = db.session.query(User).filter(User.id == user_id).first()
            if not user or user.role != 'admin':
                raise Unauthorized
        except:
            raise Unauthorized

        return f(user, *args, **kwargs)
    return decorated_function
    
# Exception handler for HTTPExceptions
def handle_http_exception(e):
    return jsonify({
        'code': e.code,
        'name': e.name,
        'description': e.description
    }), e.code

# General Exception handler
def handle_exception(e):
    if isinstance(e, HTTPException):
        return handle_http_exception(e)

    print(e)
    return jsonify({
        'code': 500,
        'name': 'Internal Server Error',
        'description': 'An unexpected error occured in the server'
    }), 500


def get_query_param(key, value_type, required=False, default=None):
    value = request.args.get(key)
    try:
        return value_type(value)
    except Exception as e:
        if not required:
            return default
        raise e


def get_body_param(key, value_type, required=False, default=None):
    value = request.get_json(force=True).get(key)
    try:
        return value_type(value)
    except Exception as e:
        if not required:
            return default
        raise e