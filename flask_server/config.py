import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = os.getenv('FLASK_DEBUG', False)
    BCRYPT_LOG_ROUNDS = 15
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_super_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///../sql_app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = os.getenv('FLASK_DEBUG', True)

class TestConfig(BaseConfig):
    DEBUG = os.getenv('FLASK_DEBUG', True)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'bad_secret_key'