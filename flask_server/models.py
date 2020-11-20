from flask_server import db, bcrypt
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .config import BaseConfig
from flask import abort
import jwt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False, index=True)
    hashed = db.Column(db.LargeBinary(60), nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, username, password, is_admin=False, first_name=None, last_name=None):
        self.username = username
        self.hashed = bcrypt.generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def set_password(self, password):
        self.hashed = bcrypt.generate_password_hash(password)

    def is_correct_password(self, password):
        return bcrypt.check_password_hash(self.hashed, password)

    def get_id(self):
        return str(self.id)

    def get_name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.username

    # JWT Authentication
    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(payload, BaseConfig.SECRET_KEY, algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please request a new token'
        except jwt.InvalidTokenError:
            return 'Invalid Token. Please request a new token'


class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    follow_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    datetime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, follow_id):
        self.user_id = user_id
        self.follow_id = follow_id


class Drink(db.Model):
    __tablename__ = 'drinks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    glasses = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now)

    user = relationship('User')

    def __init__(self, user_id, glasses):
        self.user_id = user_id
        self.glasses = glasses


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id'))

    drink = relationship('Drink')

    def __init__(self, user_id, drink_id):
        self.user_id = user_id
        self.drink_id = drink_id