import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, User, ListUser, LoginUser, TokenRefresh
from resources.article import NewArticle, Article, ArticleList, UpdateArticle

app = Flask(__name__)
load_dotenv(".env")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(ListUser, "/users")
api.add_resource(LoginUser, "/login")
api.add_resource(TokenRefresh, "/refresh-token")

api.add_resource(NewArticle, "/add-article")
api.add_resource(Article, "/article//<string:title>")
api.add_resource(ArticleList, "/article-list")
api.add_resource(UpdateArticle, "/update-article/<int:id>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True, host='0.0.0.0')