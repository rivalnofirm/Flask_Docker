from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from models.article import ArticleModel
from schemas.article import ArticleSchema


NAME_ALREADY_EXISTS = "An article with title '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the article."
ARTICLE_NOT_FOUND = "Article not found."
ARTICLE_DELETED = "article deleted."

article_schema = ArticleSchema()
article_list_schema = ArticleSchema(many=True)

class NewArticle(Resource):
    @classmethod
    def post(cls):
        article_json = request.get_json()
        article = article_schema.load(article_json)

        if ArticleModel.find_by_title(article.title):
            return {'message': NAME_ALREADY_EXISTS.format(article.title)}, 400

        try:
            article.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return article_schema.dump(article), 201

class Article(Resource):
    @classmethod
    def get(cls, title: str):
        article = ArticleModel.find_by_title(title)
        if article:
            return article_schema.dump(article), 200
        return {"message": ARTICLE_NOT_FOUND}, 404

    @classmethod
    def delete(cls, title: str):
        article = ArticleModel.find_by_title(title)
        if article:
            article.delete_from_db()
            return {"message": ARTICLE_DELETED}, 200

        return {"message": ARTICLE_NOT_FOUND}, 404

class ArticleList(Resource):
    @classmethod
    def get(cls):
        return {"article": article_list_schema.dump(ArticleModel.find_all())}, 200

class UpdateArticle(Resource):
    @classmethod
    def put(self, id: int):
        article = ArticleModel.find_by_id(id)

        if article:
            try:
                article.update_to_db(
                    request.get_json()
                )
            except:
                return {"message": ERROR_INSERTING}, 400
            return article_schema.dump(article), 200