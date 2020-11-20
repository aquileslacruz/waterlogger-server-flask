from math import ceil
from flask import request, jsonify, Response, json
from flask_server.utilities import token_required, admin_required, get_query_param, get_body_param
from flask_server.models import User
from flask_server import db, bcrypt
from werkzeug.exceptions import MethodNotAllowed, Unauthorized
from .schemas import UserSchema
from . import crud
from . import users_blueprint


@users_blueprint.route('/', methods=['GET', 'POST'])
def users_handler():
    if request.method == 'GET':
        return get_users()
    elif request.method == 'POST':
        return create_user()
    raise MethodNotAllowed


# GET USERS
@admin_required
def get_users(admin):
    # Parse query params
    page = get_query_param('page', int, default=1)
    limit = get_query_param('limit', int, default=10)

    total = crud.get_users_count()
    users = crud.get_users(page, limit)

    return jsonify(
        total=total,
        page=page,
        per_page=limit,
        page_count=ceil(total/limit),
        results=UserSchema().dump(users, many=True)
    ), 200


# REGISTER USER
def create_user():
    username = get_body_param('username', str, required=True)
    password = get_body_param('password', str, required=True)
    first_name = get_body_param('first_name', str)
    last_name = get_body_param('last_name', str)

    user = crud.create_user(username, password, first_name, last_name)

    return UserSchema().dump(user), 201


# GET MY INFO
@users_blueprint.route('/me/', methods=['GET'], strict_slashes=False)
@token_required
def get_my_info(user):
    return UserSchema().dump(user), 200


# GET MY FOLLOWERS
@users_blueprint.route('/followers/', methods=['GET'], strict_slashes=False)
@token_required
def get_my_followers(user):
    followers = crud.get_user_followers(user.id)
    return UserSchema().dumps(followers, many=True), 200


# GET USERS I FOLLOW
@users_blueprint.route('/follow/', methods=['GET'], strict_slashes=False)
@token_required
def get_my_follows(user):
    follows = crud.get_user_follows(user.id)
    return UserSchema().dumps(follows, many=True), 200


# SEARCH BY USERNAME
@users_blueprint.route('/search/', methods=['GET'], strict_slashes=False)
@token_required
def search_users(user):
    q = get_query_param('q', str, required=True)
    skip = get_query_param('skip', int, default=0)
    limit = get_query_param('limit', int, default=10)
    results = crud.search_by_username(q, skip, limit)
    return UserSchema().dumps(results, many=True), 200


# HANDLE USER ID ROUTE
@users_blueprint.route('/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_user_id(user_id):
    if request.method == 'GET':
        return get_user_by_id(user_id)
    elif request.method == 'PUT':
        return edit_user_by_id(user_id)
    elif request.method == 'DELETE':
        return delete_user_by_id(user_id)
    raise MethodNotAllowed


# GET USER BY ID
@token_required
def get_user_by_id(req_user, user_id: int):
    user = crud.get_user_by_id(user_id)
    return UserSchema().dump(user), 200


# EDIT USER BY ID
@token_required
def edit_user_by_id(req_user, user_id: int):
    if not req_user.is_admin and req_user.id != user_id:
        raise Unauthorized
    user = crud.edit_user_by_id(user_id, request.get_json())
    return UserSchema().dump(user), 202


# DELETE USER BY ID
@admin_required
def delete_user_by_id(req_user, user_id: int):
    crud.delete_user_by_id(user_id)
    return 'Deleted', 202


# FOLLOW USER
@users_blueprint.route('/<int:user_id>/follow/', methods=['POST'], strict_slashes=False)
@token_required
def follow_user(user, user_id: int):
    crud.follow_user(user, user_id)
    return 'Following', 202


# UNFOLLOW USER
@users_blueprint.route('/<int:user_id>/unfollow/', methods=['POST'], strict_slashes=False)
@token_required
def unfollow_user(user, user_id: int):
    crud.unfollow_user(user, user_id)
    return 'Unfollowed', 202