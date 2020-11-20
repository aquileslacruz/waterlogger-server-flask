from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import DevConfig, TestConfig
from .utilities import handle_exception

CONFIGS = {
    'dev': DevConfig,
    'test': TestConfig
}

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = None


def create_app(env='dev'):
    config = CONFIGS[env]

    app = Flask(__name__)
    app.config.from_object(config)
    app.register_error_handler(Exception, handle_exception)

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    global ma
    db.init_app(app)
    bcrypt.init_app(app)
    ma = Marshmallow(app)


def register_blueprints(app):
    from flask_server.auth import auth_blueprint
    from flask_server.users import users_blueprint
    from flask_server.drinks import drinks_blueprint
    from flask_server.notifications import notifications_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(drinks_blueprint)
    app.register_blueprint(notifications_blueprint)
