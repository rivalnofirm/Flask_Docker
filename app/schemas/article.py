from ma import ma
from marshmallow import fields
from models.article import ArticleModel


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ArticleModel
        dump_only = ("id",)
        load_instance = True

    title = fields.Str(required=True)
    description = fields.Str(required=True)
