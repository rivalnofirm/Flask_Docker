from ma import ma
from marshmallow import fields
from models.user import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True
    username = fields.Str(required=True)
    password = fields.Str(required=True)