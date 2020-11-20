from flask_server import ma
from marshmallow import fields


class NotificationSchema(ma.Schema):
    id = fields.Field()
    user = fields.Field()
    glasses = fields.Field()
    datetime = fields.DateTime()