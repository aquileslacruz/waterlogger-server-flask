from flask_server.utilities import token_required, get_body_param
from flask_server.models import Drink
from .schemas import DrinkSchema
from . import crud, drinks_blueprint


@drinks_blueprint.route('/', methods=['POST'])
@token_required
def create_drink(user):
    glasses = get_body_param('glasses', int, required=True)
    drink = crud.create_drink(user.id, glasses)
    return DrinkSchema().dump(drink), 201


@drinks_blueprint.route('/today/', methods=['GET'], strict_slashes=False)
@token_required
def get_todays_drinks(user):
    drinks = crud.get_user_todays_drinks(user.id)
    return DrinkSchema().dumps(drinks, many=True), 200