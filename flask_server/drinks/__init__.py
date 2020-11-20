from flask import Blueprint

drinks_blueprint = Blueprint('drinks', __name__, url_prefix='/drinks')

from . import routes