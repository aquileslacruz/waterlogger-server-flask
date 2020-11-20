from flask_server import ma
from marshmallow import fields


class DrinkSchema(ma.Schema):
    id = fields.Field()
    glasses = fields.Field()
    datetime = fields.DateTime()
