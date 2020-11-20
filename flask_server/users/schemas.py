from flask_server import ma
from marshmallow import fields, post_dump

ALLOW_NONE_STR = ['first_name', 'last_name']

class UserSchema(ma.Schema):
    id = fields.Field()
    username = fields.Field()
    first_name = fields.Field(default=None)
    last_name = fields.Field(default=None)
    is_admin = fields.Field()

    @post_dump
    def check_none(self, data, many):
        for key, value in data.items():
            if key in ALLOW_NONE_STR:
                data[key] = value if value != 'None' else None
        return data
