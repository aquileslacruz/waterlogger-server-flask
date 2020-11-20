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